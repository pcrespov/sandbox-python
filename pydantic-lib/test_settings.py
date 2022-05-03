from pydantic import BaseSettings, validator, constr


class MySettings(BaseSettings):
    SOME_INT: int
    SOME_LIST: list[int]
    OTHER_LIST: list[
        constr(strip_whitespace=True, regex=r"^[a-zA-Z0-9.]*(!=|==){1}[a-zA-Z0-9.]*$")
    ]

    class Config:
        env_file = "pydantic-lib/.env-settings"  # <<<< Check content of this file
        env_file_encoding = "utf-8"

    @validator("OTHER_LIST", pre=True, always=True)
    @classmethod
    def other_list(cls, v, values):
        return v


def test_it():
    settings = MySettings()
    assert settings.SOME_INT == 42
    assert settings.SOME_LIST == [1, 2, 3, 4, 5]
    assert settings.OTHER_LIST == ["one==yes", "two!=no"]
