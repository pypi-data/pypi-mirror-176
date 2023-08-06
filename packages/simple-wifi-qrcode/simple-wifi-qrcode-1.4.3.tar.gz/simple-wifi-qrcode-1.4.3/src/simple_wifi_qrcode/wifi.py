"""Functions useful for wifi related utilities"""


def wifi_join_string(ssid: str, password: str, alg: str = "") -> str:
    """
    Generate a string for joining a wifi network.

    Parameters
    ----------
    ssid : str
        The SSID (name) of the wifi network to join
    password : str
        The password used to join the wifi network
    alg: str
        The authentication algorithm used to join the wifi network

    Returns
    -------
    str
        A string to be used to in the QR Code to join the wifi network in
        the following format:
          WIFI:S:<SSID>;T:<WEP|WPA|blank>;P:<PASSWORD>;H:<true|false|blank>;;

    """
    return f"WIFI:T:{alg};S:{ssid};P:{password};H:;"
