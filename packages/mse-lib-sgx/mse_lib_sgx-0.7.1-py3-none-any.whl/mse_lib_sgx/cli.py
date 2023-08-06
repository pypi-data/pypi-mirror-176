"""mse_lib_sgx.cli module."""

import argparse
import asyncio
import importlib
import os
import logging
import sys
from pathlib import Path
from typing import Union

from cryptography import x509
from cryptography.x509.oid import NameOID
from hypercorn.asyncio import serve
from hypercorn.config import Config

from mse_lib_sgx import globs
from mse_lib_sgx.certificate import SelfSignedCertificate, SGXCertificate
from mse_lib_sgx.http_server import serve as serve_sgx_secrets
from mse_lib_sgx.import_hook import import_set_key


def parse_args() -> argparse.Namespace:
    """Argument parser."""
    parser = argparse.ArgumentParser(description="Start a MSE Enclave server.")
    parser.add_argument(
        "application",
        type=str,
        help="Application to dispatch to as path.to.module:instance.path")
    parser.add_argument("--encrypted-code",
                        action="store_true",
                        default=False,
                        help="Whether the application is encrypted")
    parser.add_argument(
        "--self-signed",
        type=int,
        metavar="EXPIRE_IN",
        required=False,
        help="Generate a self-signed certificate for the app. "
        "Number of days before certificate expired. "
        "If not specified, the public key is supposed "
        "to be in `data-dir/cert.app.pem` and the private key will "
        "be sent using the configuration server")
    parser.add_argument("--host",
                        required=True,
                        type=str,
                        help="Hostname of the server")
    parser.add_argument("--port",
                        required=True,
                        type=int,
                        help="Port of the server")
    parser.add_argument("--app-dir",
                        required=True,
                        type=Path,
                        help="Path the microservice application "
                        "and the cert.app.pem if not --self-signed")
    parser.add_argument(
        "--data-dir",
        required=True,
        type=Path,
        help="Path with data encrypted for a specific MRENCLAVE")
    parser.add_argument("--debug",
                        action="store_true",
                        help="Debug mode without SGX")

    return parser.parse_args()


def run() -> None:
    """Entrypoint of the CLI.

    The program creates a self signed certificate.

    Then starts a configuration server using HTTPS and this previous cert
    in order to allow the user to send some secrets params.

    Once all the secrets has been sent, two options:
    - If the app owner relies on the enclave certificate,
      then start the app server using this same certificate
    - If not, start the app server using the certificate
      provided by the app owner. In that case, the certificate
      is already present in the workspace of the program
      but the private key is sent by the app owner
      when the configuration server is up.
    """
    args: argparse.Namespace = parse_args()
    os.makedirs(args.data_dir, exist_ok=True)

    FORMAT = '[%(asctime)s] [%(levelname)s] %(message)s'
    logging.basicConfig(level=logging.INFO, format=FORMAT)

    expires_in = 10
    force_ssl_certificate = True
    if args.self_signed:
        # The conf server and the app server will use the same self signed cert
        expires_in = args.self_signed
        force_ssl_certificate = False

    logging.info("Generating the self signed certificate...")

    subject: x509.Name = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "FR"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Ile-de-France"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "Paris"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Cosmian Tech"),
        x509.NameAttribute(NameOID.COMMON_NAME, "cosmian.com"),
    ])

    cert: Union[SGXCertificate, SelfSignedCertificate] = (SGXCertificate(
        dns_name=args.host,
        subject=subject,
        root_path=Path(args.data_dir),
        expires_in=expires_in) if not args.debug else SelfSignedCertificate(
            dns_name=args.host,
            subject=subject,
            root_path=Path(args.data_dir),
            expires_in=expires_in))

    if force_ssl_certificate:
        # We should find the certificate in args.app_dir
        cert_path = args.app_dir / "cert.app.pem"
        key_path = args.data_dir / "key.app.pem"
    else:
        cert_path = cert.cert_path
        key_path = cert.key_path

    if args.encrypted_code or force_ssl_certificate:
        logging.info("Starting the configuration server...")

        # The app owner could send (both or a single):
        # - the key to decrypt the code if it's encrypted
        # - the SSL private key if it doesn't want to use our self-signed cert
        serve_sgx_secrets(
            hostname="0.0.0.0",
            port=args.port,
            certificate=cert,
            encrypted_code=args.encrypted_code,
            ssl_private_key_path=key_path if force_ssl_certificate else None)

        if args.encrypted_code and globs.SEALED_KEY:
            import_set_key(globs.SEALED_KEY)

    config = Config.from_mapping({
        "bind": f"0.0.0.0:{args.port}",
        "keyfile": key_path,
        "certfile": cert_path,
        "alpn_protocols": ["h2"],
        "workers": 1,
        "accesslog": "-",
        "errorlog": "-",
        "worker_class": "uvloop",
        "wsgi_max_body_size": 2 * 1024 * 1024 * 1024  # 2 GB
    })

    logging.info("Loading the application...")
    sys.path.append(f"{args.app_dir.resolve()}")
    module, app = args.application.split(":")
    app = getattr(importlib.import_module(module), app)

    logging.info("Starting the application...")
    asyncio.run(serve(app, config))
