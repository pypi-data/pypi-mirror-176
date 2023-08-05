"""mse_lib_sgx.global module."""

from pathlib import Path
import threading
from typing import Optional, Union

from mse_lib_sgx.certificate import SelfSignedCertificate, SGXCertificate

CERT: Union[SGXCertificate, SelfSignedCertificate, None] = None
SEALED_KEY: Optional[bytes] = None
EXIT_EVENT: threading.Event = threading.Event()
ENCRYPTED_CODE: bool = False
SSL_PRIVATE_KEY_PATH: Optional[Path] = None
