import os
import sys
import json
import warnings
import configparser

import logging
log = logging.getLogger(__name__)
logging.basicConfig(format='%(levelname)s: [%(filename)s:%(lineno)d] %(message)s', level=logging.INFO)


def _show_only_warning_message(message, category, filename, lineno, file=None, line=None):
    # the default warning behavior shows a superfluous line of code
    # See: https://stackoverflow.com/a/2187390
    return str(message) + '\n'

warnings.showwarning = _show_only_warning_message


class OverwriteWarning(UserWarning):
    "Alert user that a Setting was overwritten."
    pass


class ShadowWarning(UserWarning):
    "Alert user that a Setting key is the same as a Configuration method."
    pass


class Setting:
    """Individual option setting.

    A Configuration is a collection of Settings.  A Setting represents
    some value which the developer wishes to persist beyond the
    immediate run.  Each Setting is identified by a key.  An optional
    default value provides the initial value.  If the Setting
    corresponds to a component, such as a UI element, define optional
    setter and getter functions to interact with the component.

    Parameters
    ----------
    key : str

      Setting identifier.

    default : object, optional

      Initial value.  Default is None.

    setter : callable, optional

      Function which assigns the current Setting.value.  Must take a
      single argument, the value to be set.

    getter : callable, optional

      Function which retrieves a value.  Must have no parameters and
      return a value.

    """

    def __init__(self, key, default=None, setter=None, getter=None):

        self.key     = key
        self.default = default
        self.value   = self.default
        self.setter  = setter
        self.getter  = getter


class SingletonMetaclass(type):
    "Force a single Configuration instance."

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in SingletonMetaclass._instances:
            SingletonMetaclass._instances[cls] = super().__call__(*args, **kwargs)
        return SingletonMetaclass._instances[cls]

    def __reset(cls):
        """Delete the instance.

        Used for testing.

        Call as:

          nostalgic.Configuration._SingletonMetaclass__reset()

        """

        try:
            del SingletonMetaclass._instances[cls]
        except KeyError:
            pass


class Configuration(metaclass=SingletonMetaclass):
    """Collection of Settings.

    A Configuration describes the state of an application which the
    developer wishes to persist.  It provides a high-level interface
    to a collection of Setting objects.

    Parameters
    ----------
    name : str

      Name to associate with Configuration settings.  If a valid file,
      then use that to store settings.  Otherwise, use 'name' to define
      a directory where settings are stored.  See 'config_file'.

    Properties
    ----------
    config_file

      Default Setting for Configuration file.  If the 'name' argument
      was a valid file, then 'config_file' is 'name'.  Otherwise,
      where settings are stored depends on the operating system.

      Windows:

        %APPDATA%<name>\\config.ini

      GNU/Linux or MacOS:

        If XDG_CONFIG_HOME defined,

          $XDG_CONFIG_HOME/<name>/config.ini

        Otherwise,

          ~/.config/<name>/config.ini

    """

    def __init__(self, name):
        super().__init__()

        if os.path.isfile(name):
            config_file = os.path.abspath(name)
        else:
            if os.environ.get('APPDATA'):
                parent_dir = os.environ['APPDATA']
            elif os.environ.get('XDG_CONFIG_HOME'):
                parent_dir = os.environ['XDG_CONFIG_HOME']
            else:
                parent_dir = os.path.join(os.environ['HOME'], '.config')

            dir = os.path.join(parent_dir, name)
            config_file = os.path.abspath(os.path.join(dir, "config.ini"))

        # must define this way since we're overriding __setattr__
        self.__dict__['_settings'] = {}

        # Default Settings
        self.add_setting('config_file', config_file)
        log.info(f"Configuration file: '{config_file}'")

    def __setattr__(self, key, value):
        if key in self.__dict__['_settings']:
            self.__dict__['_settings'][key].value = value
        else:
            raise AttributeError(f"'{type(self).__name__}' object has no setting '{key}'")

    def __getitem__(self, key):
        return self.__dict__['_settings'][key]

    def __getattr__(self, name):
        return self.__dict__['_settings'][name].value

    # TODO implement "(python) Emulating container types" methods

    def add_setting(self, key, default=None, setter=None, getter=None):
        """Add a configuration setting.

        Parameters
        ----------
        key : str

          Setting name.  If key already exists, the corresponding
          setting will be replaced according to the latest call.

        default : object, optional

          Default value returned for setting value.  Default is None.

        setter : callable, optional

          Function to apply setting value to an external component on
          read() or set().  Must take a single argument, the value to
          be set.

        getter : callable, optional

          Function to get setting value from an external component on
          write() or get().  Must take zero arguments and return a
          value (e.g. from the external component).  The return value
          must be serializable.

        """

        overwrite = False
        if key in self.__dict__['_settings']:
            overwrite = True

        if key in Configuration.__dict__ and key[:2] != '__':
            warnings.warn(f"[WARNING]: Setting '{key}' shadows a Configuration method of the same name!", ShadowWarning)

        setting = Setting(key, default=default, getter=getter, setter=setter)

        self.__dict__['_settings'][key] = setting

        if overwrite:
            warnings.warn(f"[WARNING]: Setting '{key}' was overwritten", OverwriteWarning)

    def read(self, filename=None, sync=True):
        """Load settings from disk.

        Parameters
        ----------
        filename : path, optional

          Path to configuration file.  Default location is
          Configuration().config_file.

        sync : bool, optional

          Call setters after configuration is read from disk. Default
          is True.

        """

        if not filename:
            filename = self.config_file

        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                text = f.read()

            parser = configparser.ConfigParser()
            parser.read_string(text)

            for key, setting in self.__dict__['_settings'].items():
                if parser.has_option('General', key):
                    raw_value = parser['General'][key]
                    value = json.loads(raw_value)
                    setting.value = value
                    log.debug(f"Reading setting: ('{key}', '{value}')")
                    if sync and setting.setter:
                        setting.setter(value)

            log.debug(f"Read configuration: '{filename}'")

    def write(self, filename=None, sync=True):
        """Save settings to disk.

        Parameters
        ----------
        filename : path, optional

          Path to configuration file.  Default location is
          Configuration().config_file.

        sync : bool, optional

          Call getters before writing Setting values to disk. Default
          is True.

        """

        if not filename:
            filename = self.config_file

        if not os.path.isdir(os.path.dirname(self.config_file)):
            os.makedirs(os.path.dirname(self.config_file))

        parser = configparser.ConfigParser()
        parser.add_section('General')

        for key, setting in self.__dict__['_settings'].items():
            if key != 'config_file':
                if sync and setting.getter:
                    setting.value = setting.getter()
                value = json.dumps(setting.value)
                log.debug(f"Writing setting: ('{key}', '{value}')")
                parser.set('General', key, value)

        with open(self.config_file, 'w+', encoding='utf-8') as f:
            parser.write(f)
            log.debug(f"Wrote configuration: '{filename}'")


    def get(self, keys=None):
        """Update configuration according to getters.

        Parameters
        ----------
        keys : iterable, optional

          List of setting keys whose getters should be called.
          Default is None which calls the getter for all settings with
          getters.

        Returns
        -------

        Dict keyed by which settings were updated and whose values are
        the value *before* the update.

        """

        if not keys:
            keys = self.__dict__['_settings'].keys()

        settings_from = {}
        for key in keys:
            setting = self.__dict__['_settings'][key]
            if setting.getter:
                new_value = setting.getter()
                settings_from[key] = setting.value
                setting.value = new_value

        return settings_from

    def set(self, keys=None, use_defaults=False, sync=False):
        """Apply configuration according to setters.

        Parameters
        ----------
        keys : iterable, optional

          List of setting keys whose setters should be called.
          Default is None which calls the setter for all settings with
          setters.

        use_defaults : bool, optional

          Call setters using default Setting values.  Default is
          False.

        sync : bool, optional

          When used with use_defaults=True, also update Settings with
          default values.  Default is False.

        Returns
        -------

          None

        """

        if not keys:
            keys = self.__dict__['_settings'].keys()

        for key in keys:
            setting = self.__dict__['_settings'][key]
            if setting.setter:
                if use_defaults:
                    setting.setter(setting.default)
                    if sync:
                        setting.value = setting.default
                else:
                    setting.setter(setting.value)
