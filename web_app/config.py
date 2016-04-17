import os


# default config class
class Base(object):
    DEBUG = False
    SECRET_KEY = '$L\x12\xe7\x00\x9c\xfb\xb2\xde\xbb\x1d\x8b\xc5\xc3\xba\x93|}}m\xcb\x83"\xf8\xe9'


class Development(Base):
    DEBUG = True


class Production(Base):
    DEBUG = False


class EnvironmentSettings:
    """Access to environment variables via system os or .env file for different environments (Prod vs Dev)

    """
    def __init__(self, root_folder_path):
        self._root_folder_path = root_folder_path

    def __getitem__(self, key):
        return self._get_env_variable(key)

    def __setitem__(self, key, value):
        raise InvalidOperationException('Environment Settings are read-only')

    def __delitem__(self, key):
        raise InvalidOperationException('Environment Settings are read-only')

    def _get_env_variable(self, var_name, default=False):
        """
        Get the environment variable or return exception
        :param var_name: Environment Variable to lookup
        """
        try:
            return os.environ[var_name]
        except KeyError:
            from io import StringIO
            from configparser import ConfigParser

            env_file = os.environ.get('PROJECT_ENV_FILE', self._root_folder_path + "/.env")
            try:
                config = StringIO()
                config.write("[DATA]\n")
                config.write(open(env_file).read())
                config.seek(0, os.SEEK_SET)
                cp = ConfigParser()
                cp.read_file(config)
                value = dict(cp.items('DATA'))[var_name.lower()]
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                elif value.startswith("'") and value.endswith("'"):
                    value = value[1:-1]
                os.environ.setdefault(var_name, value)
                return value
            except (KeyError, IOError):
                if default is not False:
                    return default
                error_msg = "Either set the env variable '{var}' or place it in your " \
                            "{env_file} file as '{var} = VALUE'"
                raise ConfigurationError(error_msg.format(var=var_name, env_file=env_file))


class ConfigurationError(Exception):
    pass


class InvalidOperationException(Exception):
    pass
