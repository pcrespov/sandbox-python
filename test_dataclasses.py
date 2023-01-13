import json
from dataclasses import asdict, dataclass

from pydantic import BaseModel


@dataclass
class Login:
    two_factor_enabled: bool = False  # overrides LOGIN_2FA_REQUIRED


class Model(BaseModel):
    login_settings: Login


def test_it():
    m1 = Model(login_settings={"two_factor_enabled": False})
    m2 = Model(login_settings={"two_factor_enabled": 0})

    assert m1 == m2

    assert not m1.login_settings.two_factor_enabled

    assert asdict(Login()) == asdict(m1.login_settings)

    assert json.dumps(asdict(Login()))
