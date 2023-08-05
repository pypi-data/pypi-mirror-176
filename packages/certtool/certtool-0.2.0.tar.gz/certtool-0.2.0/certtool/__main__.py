import argparse
import re
import socket
import ssl
from datetime import datetime

import OpenSSL.crypto
import colorama

_store = None


def get_store():
    global _store
    if _store is not None:
        return _store

    defaults = ssl.get_default_verify_paths()
    _store = OpenSSL.crypto.X509Store()
    _store.load_locations(defaults.cafile, defaults.capath)

    return _store


def cn_to_regex(cn):
    result = []
    for part in cn.split('.'):
        result.append(part.replace('*', r'[^\.]+'))
    parts = r'\.'.join(result)
    return f"^{parts}$"


def verify_callback(sock, x509, errnum, errdepth, ok):
    if not ok:
        print(errnum, errdepth)
    return True


def ocsp_callback(sock, ocsp_bytes, user_data):
    print('ocsp', ocsp_bytes)
    return True


def check_ocsp(domain, port, chain):
    # TODO: Actually make this work and include in the cert check
    ctx = OpenSSL.SSL.Context(OpenSSL.SSL.SSLv23_METHOD)
    ctx.set_options(OpenSSL.SSL.OP_NO_SSLv2)
    ctx.set_options(OpenSSL.SSL.OP_NO_SSLv3)
    ctx.set_timeout(10)
    ctx.use_certificate(chain[0])
    defaults = ssl.get_default_verify_paths()
    ctx.load_verify_locations(defaults.cafile, defaults.capath)

    # ctx.set_verify(VERIFY_PEER, callback=verify_callback)
    ctx.set_mode(OpenSSL.SSL.VERIFY_CLIENT_ONCE)
    ctx.set_ocsp_client_callback(callback=ocsp_callback, data=None)
    conn = socket.create_connection((domain, port))
    sock = OpenSSL.SSL.Connection(ctx, conn)
    sock.set_tlsext_host_name(domain.encode())
    sock.request_ocsp()
    sock.set_connect_state()
    try:
        pass
        sock.do_handshake()
    except Exception as e:
        print(e)


def get_tls_certificate(domain, port, timeout=5, starttls=False):
    ctx = OpenSSL.SSL.Context(OpenSSL.SSL.TLSv1_2_METHOD)
    conn = socket.create_connection((domain, port), timeout=timeout)
    if starttls:
        banner = conn.recv(1000)
        conn.send(b'EHLO\nSTARTTLS\n')
        leftover = conn.recv(1000)
    sock = OpenSSL.SSL.Connection(ctx, conn)
    sock.setblocking(True)
    sock.set_connect_state()
    sock.set_tlsext_host_name(domain.encode())
    sock.do_handshake()
    chain = sock.get_peer_cert_chain()
    return chain


def check_generic(domain, port, timeout=5, starttls=False):
    try:
        chain = get_tls_certificate(domain, port, timeout=timeout, starttls=starttls)
    except TimeoutError:
        return False, "Timeout"
    except OpenSSL.SSL.Error as e:
        return False, str(e)
    x509 = chain[0]
    components = x509.get_subject().get_components()
    for component in components:
        if component[0] == b'CN':
            cn = component[1].decode()
            break
    else:
        return False, "Certificate had no common name"

    names = [cn]

    ocsp = False
    for i in range(0, x509.get_extension_count()):
        ext = x509.get_extension(i)
        if ext.get_short_name() == b'subjectAltName':
            san = str(ext)
            sans = san.split(', ')
            for s in sans:
                s_type, s_name = s.split(":", maxsplit=1)
                if s_type == 'DNS':
                    names.append(s_name)
        if ext.get_short_name() == b'authorityInfoAccess':
            info = str(ext)
            for line in info.splitlines():
                if line.startswith('OCSP '):
                    _, ocsp_uri = line.split('URI:')
                    ocsp = True

    for name in names:
        name_regex = cn_to_regex(name)
        if re.match(name_regex, domain):
            break
    else:
        return False, f"Wrong CN, certificate is for {cn}"

    # TODO: If ocsp is True, verify ocsp

    not_before = datetime.strptime(x509.get_notBefore().decode(), '%Y%m%d%H%M%SZ')
    not_after = datetime.strptime(x509.get_notAfter().decode(), '%Y%m%d%H%M%SZ')
    now = datetime.now()
    time_left = not_after - now

    if now < not_before:
        return False, f"Certificate is not yet valid (valid after {not_before})"

    if now > not_after:
        return False, f"Certificate is expired (valid until {not_after})"

    if (not_after - now).days < 20:
        return None, f"Certificate almost expired ({time_left})"

    # Check the chain
    store = get_store()
    store_ctx = OpenSSL.crypto.X509StoreContext(store, x509, chain=chain)
    try:
        store_ctx.get_verified_chain()
    except OpenSSL.crypto.X509StoreContextError as e:
        errnum = e.args[0][0]
        if errnum == 18:
            return False, "Certificate is self-signed"
        elif errnum == 19:
            return False, "Self-signed certificate in the certificate chain"
        return False, str(e)

    return True, f"Ok, {time_left.days} days remaining"


def main():
    parser = argparse.ArgumentParser("Certificate checker")
    parser.add_argument('domain', nargs='+')
    parser.add_argument('--https', action=argparse.BooleanOptionalAction, default=True, help='Check http (443)')
    parser.add_argument('--imaps', action=argparse.BooleanOptionalAction, default=False, help='Check imap (993)')
    parser.add_argument('--pop3s', action=argparse.BooleanOptionalAction, default=False, help='Check pop3s (995)')
    parser.add_argument('--smtps', action=argparse.BooleanOptionalAction, default=False, help='Check smtp (465)')
    parser.add_argument('--submission', action=argparse.BooleanOptionalAction, default=False, help='Check smtp with starttls (587)')
    parser.add_argument('--port', action="append", help="Check a specific port", default=[], type=int)
    parser.add_argument('--timeout', '-t', default=5, help='Set the timeout in seconds for the TCP connection',
                        type=int)
    args = parser.parse_args()

    domain_len = len(max(args.domain, key=len))

    protolist = []
    if args.https:
        protolist.append('https')
    if args.imaps:
        protolist.append('imaps')
    if args.pop3s:
        protolist.append('pop3s')
    if args.smtps:
        protolist.append('smtps')
    if args.submission:
        protolist.append('submission')
    protolist.extend(args.port)

    protocols = {
        'https': 443,
        'imaps': 993,
        'pop3s': 995,
        'smtps': 465,
        'submission': 587,
    }

    proto_len = len(max(protolist, key=lambda l: len(str(l))))

    returncode = 0
    for domain in args.domain:
        print(domain.ljust(domain_len + 2), end='')
        first_proto = True

        for proto in protolist:
            if len(protolist) > 1:
                if not first_proto:
                    print(' ' * (domain_len + 2), end='')
                print(f'{str(proto).ljust(proto_len)} ', end='', flush=True)
            first_proto = False

            if isinstance(proto, str):
                proto = protocols[proto]

            starttls = proto == 587
            result = check_generic(domain, proto, timeout=args.timeout, starttls=starttls)

            if result[0] is True:
                print(colorama.Fore.GREEN, result[1], colorama.Style.RESET_ALL)
            elif result[0] is False:
                print(colorama.Fore.RED, result[1], colorama.Style.RESET_ALL)
                returncode = 1
            else:
                print(colorama.Fore.YELLOW, result[1], colorama.Style.RESET_ALL)

    exit(returncode)


if __name__ == '__main__':
    main()
