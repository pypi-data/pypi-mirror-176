"""Utility functions to create QR Code to join wifi networks"""

import os
import random

import qrcode as qrcode_lib

from simple_wifi_qrcode import wifi


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
        password = _random_hex(12)

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


def _random_hex(len: int) -> str:
    return "".join((random.choice("abcdefABCDEF0123456789") for _ in range(12)))
