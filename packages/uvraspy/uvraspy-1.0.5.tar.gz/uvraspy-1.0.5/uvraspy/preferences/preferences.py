from datetime import datetime


class Preferences:
    """
    Class used to store user preferences
    .
    Attributes
    ----------
    tolerance : int
        the amount of tolerance the user has to UV Light
    sunscreen : int

    hatName : str
        the name of the hat
    password : str
        the password of the user
    """

    tolerance = 0
    sunscreen = 0
    last_sunscreen_change = 0

    def toBytes():
        """
        convert the preferences to a byte array
        """
        # convert the preferences to a byte array
        # this is used to send the preferences to the piHat
        return bytes([Preferences.tolerance, Preferences.sunscreen])

    def fromBytes(bytes: bytes):
        """
        convert byte array to preferences
        """
        # convert the bytes to the preferences
        # this is used to read the preferences from the piHat
        try:
            Preferences.tolerance = bytes[0]
            Preferences.sunscreen = bytes[1]
            Preferences.last_sunscreen_change = datetime.now().timestamp()
        except Exception as e:
            raise ValueError("Could not convert bytes to preferences", e)


class NoPreferenceException(Exception):
    pass
