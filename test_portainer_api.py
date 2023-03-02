from datetime import datetime

import httpx
from pydantic import BaseSettings, SecretStr


class PortainerSettings(BaseSettings):
    PORTAINER_ADMIN_USER: str
    PORTAINER_ADMIN_PASSWORD: SecretStr
    PORTAINER_HOST: str
    PORTAINER_PORT: int

    @property
    def base_url(self):
        return f"https://{self.PORTAINER_HOST}:{self.PORTAINER_PORT}"


if __name__ == "__main__":
    settings = PortainerSettings()

    response = httpx.post(
        settings.base_url,
        "/api/auth",
        json={
            "username": settings.PORTAINER_ADMIN_USER,
            "password": settings.PORTAINER_ADMIN_PASSWORD,
        },
    )


date_string = "Tue Feb 28 20:34:50 2023 +0100"
date_format = "%a %b %d %H:%M:%S %Y %z"

datetime_object = datetime.strptime(date_string, date_format)

print(datetime_object)
