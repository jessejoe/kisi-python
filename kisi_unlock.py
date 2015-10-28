#!/usr/bin/env python
import logging
import argparse
import getpass

from api import KisiApi


def main():
    parser = argparse.ArgumentParser(
        description='Script to unlock a lock using the Kisi API')
    parser.add_argument('-v',
                        '--verbose',
                        action='store_true',
                        help='verbose logging')
    parser.add_argument('-e',
                        '--email',
                        help='e-mail to login with',
                        required=True)
    parser.add_argument(
        '-p',
        '--password',
        help='password to login with, will prompt if not supplied')
    parser.add_argument('-l',
                        '--lock',
                        help='name of lock to unlock (partial match supported)',
                        required=True)
    args = parser.parse_args()

    password = args.password
    if not password:
        password = getpass.getpass()

    if args.verbose:
        loglevel = logging.INFO
    else:
        loglevel = logging.DEBUG

    logging.basicConfig(level=loglevel,
                        format='%(asctime)s %(name)s %(levelname)s %(message)s')
    # requests default INFO logs are noisy
    logging.getLogger("requests").setLevel(logging.WARNING)

    api = KisiApi(args.email, password)
    api.unlock(args.lock)

if __name__ == "__main__":
    main()
