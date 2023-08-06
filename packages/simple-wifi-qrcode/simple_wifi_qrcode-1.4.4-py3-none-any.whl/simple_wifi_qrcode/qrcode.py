"""Utility functions to create QR Code to join wifi networks"""

import os
from secrets import token_hex

import qrcode as qrcode_lib

from simple_wifi_qrcode import wifi

# pylint: disable-msg=too-many-arguments
def generate_wifi_qrcode(
    ssid: str,
    password: str = None,
    alg: str = "",
    output: str = "output.png",
    random_password: bool = False,
    verbose: bool = False,
) -> None:
    """Generates QR Code to join a wifi network and save it to a PNG file"""

    if random_password:
        password = token_hex(12)
    content: str = wifi.wifi_join_string(ssid, password, alg)
    qrcode_img = qrcode_lib.make(content)
    qrcode_img.save(os.path.join(os.getcwd(), output))

    if verbose:
        print(
            f"""QR Code created successfully.
             \n--------------------------------------
             \n  SSID:    \t{ssid}
             \n  Password:\t{password}
             \n--------------------------------------
             \nScan the QR Code with your camera to join {ssid}network."""
        )
