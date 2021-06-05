from pydantic import BaseSettings

from modules.mod1_settings import MyModuleSettings
from modules.mod2_settings import MyModule2Settings
from modules import _base


# (1) Settings factory.

# This is my preferred way
def create_settings_class():
    # controls when environs for subsettings are captured

    class Settings(BaseSettings):
        """ Main application settings """

        host: str
        port: int

        settings1: MyModuleSettings = MyModuleSettings()
        settings2: MyModule2Settings = MyModule2Settings()

        class Config(_base.CommonConfig):
            pass

    return Settings


# could be implemented as this ... but more verbose!
def create_factory():
    # controls when environs for subsettings are captured

    class Settings(BaseSettings):
        host: str
        port: int

        settings1: MyModuleSettings = MyModuleSettings()
        settings2: MyModule2Settings = MyModule2Settings()

        class Config(_base.CommonConfig):
            pass

    def create(**values):
        return Settings(**values)

    # attach some attributes to the Functor
    create.Settings = Settings
    create.create = create # syntax sweetener
    return create


################################################################################################


# (2) Adding a factory as a class method
#
class Settings2(BaseSettings):
    host: str
    port: int

    settings1: MyModuleSettings
    settings2: MyModule2Settings

    class Config(_base.CommonConfig):
        pass

    @classmethod
    def create_from_environ(cls, **kwargs):
        # WRONG: e.g. if MyModuleSettings fails but "settings1" in kwargs!!
        kwargs.setdefault("settings1", MyModuleSettings())
        kwargs.setdefault("settings2", MyModule2Settings())
        return cls(**kwargs)

    @classmethod
    def create_from_env(cls) -> "Settings":
        # NOTE: having a settings class factory would avoid
        # this function but we found more natural to have direct access
        # to Settings class to use e.g. autocompletion

        defaults = {}
        for name, default_cls in [
            ("postgres", PostgresSettings),
            ("s3", S3Config),
            ("tracing", TracingSettings),
        ]:
            if f"STORAGE_{name.upper()}" not in os.environ:
                defaults[name] = default_cls()
        return cls(**defaults)

################################################################################################

# (3) a global reading from .env or environs
# - my least favorite
#
# - global!
# - fails upon import if validation fails: difficult to debug!
# - difficult to debug: difficult to control creation time
#
# the_settings = Settings2(settings1=MyModuleSettings(), settings2=MyModule2Settings())
