
import os

from gi import require_version
require_version("Gtk", "3.0")
require_version("Gdk", "3.0")

from gi.repository import GObject, GLib

from nvidia_fan_control import __author__, __website_url__, __license__

APP_NAME = "nvidia-fan-control"
DATA_DIR = os.path.join(os.path.expanduser("~"), '.config', APP_NAME)
os.makedirs(DATA_DIR, exist_ok=True)
SETTINGS_FILE = "settings.conf"
CONFIG_FILE = os.path.join(DATA_DIR, SETTINGS_FILE)
SETTINGS_GROUP_NAME = "Default"


class SettingStorage(GObject.Object):
    """Stores all settings.

    Settings can be accessed via SettingStorage.get_type("key") and changed by
    calling SettingStorage.set_type("key", value), where type is the type of data(boolean,integer,etc).

    Signals:
        changed: Emitted when a setting was changed.
    """

    def __init__(self):
        super(SettingStorage, self).__init__()
        self._init_from_keyfile()

    @staticmethod
    def _init_from_keyfile():
        """Initialize te key file in DATA_DIR folder with CONFIG_FILE path and create default values for keys
        """
        _keyfile = GLib.KeyFile()
        # check if DATA_DIR exist and eventually create it
        if not os.path.exists(DATA_DIR):
            try:
                os.makedirs(DATA_DIR)
            except OSError as error:
                print(error)
                print("Creation of the directory %s failed" % DATA_DIR)
            else:
                print("Successfully created the directory %s " % DATA_DIR)

        # check if CONFIG_FILE exist and eventually create it
        if os.path.exists(CONFIG_FILE):
            _keyfile.load_from_file(CONFIG_FILE, GLib.KeyFileFlags.KEEP_COMMENTS)
            print("CONFIG_FILE loaded")
        else:
            _keyfile = GLib.KeyFile.new()
            # _keyfile.set_comment(None, None, COPYRIGHT)
            _keyfile.set_comment(None, None, __author__ + "\n" + __website_url__ + "\n" + __license__)
            print("no CONFIG_FILE, new keyfile created")

        # check if SETTINGS_GROUP_NAME settings group exist and eventually create and initialize it
        if not _keyfile.has_group(SETTINGS_GROUP_NAME):
            _keyfile.set_integer_list(SETTINGS_GROUP_NAME, "geometry", [640, 420])
            _keyfile.set_boolean(SETTINGS_GROUP_NAME, "initialized", False)
            print("CONFIG_FILE initialized")
        else:
            _keyfile.set_comment(None, None, __author__ + "\n" + __website_url__ + "\n" + __license__)
            if _keyfile.get_integer_list(SETTINGS_GROUP_NAME, "geometry") == 0:
                _keyfile.set_integer_list(SETTINGS_GROUP_NAME, "geometry", [640, 420])
            if not _keyfile.get_boolean(SETTINGS_GROUP_NAME, "initialized"):
                _keyfile.set_boolean(SETTINGS_GROUP_NAME, "initialized", False)
            print("CONFIG_FILE updated")

        _keyfile.save_to_file(CONFIG_FILE)
        print("CONFIG_FILE saved")

    @staticmethod
    def _get_keyfile():
        """Load keyfile from CONFIG_FILE

        Returns:
            keyfile containing settings
        """
        _keyfile = GLib.KeyFile()
        try:
            _keyfile.load_from_file(CONFIG_FILE, GLib.KeyFileFlags.KEEP_COMMENTS)
        except GLib.Error as error:
            print(error)
        finally:
            return _keyfile

    def get_boolean(self, key) -> bool:
        """Return boolean value of the key setting

        Args:
            key: the name of the setting containing the boolean value to be retrieved

        Returns:
            the value associated with the key as a boolean, or False if the key was not found or could not be parsed.
        """
        keyfile = self._get_keyfile()
        try:
            result = keyfile.get_boolean(SETTINGS_GROUP_NAME, key)
        except GLib.Error as error:
            print(error.message)
            result = False

        return result

    def set_boolean(self, key, value):
        """ Associates a new boolean value with key. If key cannot be found then it is created.

        Args:
            key: key name
            value: True or False

        Return:
            True if value is set, False otherwise
        """
        keyfile = self._get_keyfile()
        result = False
        if isinstance(value, bool):
            try:
                keyfile.set_boolean(SETTINGS_GROUP_NAME, key, value)
                keyfile.save_to_file(CONFIG_FILE)
            except GLib.Error as error:
                print(error.message)
            finally:
                result = True

        return result

    def get_integer(self, key) -> int:
        """Return integer value of the key setting

        Args:
            key: the name of the setting containing the integer value to be retrieved

        Returns:
            the value associated with the key as an integer, or 0 if the key was not found or could not be parsed.
        """
        keyfile = self._get_keyfile()
        try:
            result = keyfile.get_integer(SETTINGS_GROUP_NAME, key)
        except GLib.Error as error:
            print(error.message)
            result = 0

        return result

    def set_integer(self, key, value):
        """ Associates a new integer value with key. If key cannot be found then it is created.

        Args:
            key: key name
            value: an integer value

        Return:
            True if value is set, False otherwise
        """
        keyfile = self._get_keyfile()
        result = False
        if isinstance(value, int):
            try:
                keyfile.set_integer(SETTINGS_GROUP_NAME, key, value)
                keyfile.save_to_file(CONFIG_FILE)
            except GLib.Error as error:
                print(error.message)
            finally:
                result = True

        return result

    def get_integer_list(self, key) -> [int]:
        """Return a list of integer values of the key setting

        Args:
            key: the name of the setting containing the list of integer values to be retrieved

        Returns:
            the values associated with the key as a list of integers, or an empty list [] if the key was not found or
            could not be parsed. The returned list of integers should be freed with GLib.free() when no longer needed.
        """
        keyfile = self._get_keyfile()
        try:
            result = keyfile.get_integer_list(SETTINGS_GROUP_NAME, key)
        except GLib.Error as error:
            print(error.message)
            result = [0]

        return result

    def set_integer_list(self, key, my_list):
        """ Associates a list of integer values with key. If key cannot be found then it is created.

        Args:
            key: key name
            my_list: an array of integer values

        Return:
            True if value is set, False otherwise
        """
        keyfile = self._get_keyfile()
        result = False
        if all(isinstance(item, int) for item in my_list):
            try:
                keyfile.set_integer_list(SETTINGS_GROUP_NAME, key, my_list)
                keyfile.save_to_file(CONFIG_FILE)
            except GLib.Error as error:
                print(error.message)
            finally:
                result = True

        return result


# Initiate signals for the SettingsStorage
GObject.signal_new("changed", SettingStorage, GObject.SIGNAL_RUN_LAST,
                   None, (GObject.TYPE_PYOBJECT,))


# Initialize an actual SettingsStorage object to work with
settings = SettingStorage()
