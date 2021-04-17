from pydantic import BaseSettings


class AppSettings(BaseSettings):
    debug: bool = False

    # etc
    class Config:
        case_sensitive = False
        env_prefix = "DYNAMIC_SIDECAR_"
