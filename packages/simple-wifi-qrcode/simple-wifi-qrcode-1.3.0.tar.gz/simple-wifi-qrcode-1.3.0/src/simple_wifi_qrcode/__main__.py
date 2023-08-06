""" Call generate_wifi_qrcode on package execution """

import argparse
from simple_wifi_qrcode import qrcode


def main():
    """Retrieve args and call generate_wifi_qrcode"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        action="store",
        default=False,
        required=True,
        help="The PNG file that will store the QR Code",
    )
    parser.add_argument(
        "--ssid",
        action="store",
        default=None,
        required=True,
        help="The SSID of the network",
    )
    parser.add_argument(
        "--password",
        action="store",
        default=None,
        required=True,
        help="The password of the network",
    )
    parser.add_argument(
        "--alg",
        action="store",
        default="WPA",
        required=True,
        help="The authentication algorithm",
        choices=("WEP", "WPA", "nopass"),
    )
    parser.add_argument(
        "--random-password",
        action="store_true",
        default=False,
        required=False,
        help="Generate a random password for the network",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        default=False,
        help="Print verbose information",
    )
    (args, _) = parser.parse_known_args()

    qrcode.generate_wifi_qrcode(
        ssid=args.ssid,
        password=args.password,
        alg=args.alg,
        output=args.output,
        verbose=args.verbose,
        random_password=args.random_password,
    )


if __name__ == "__main__":
    main()
