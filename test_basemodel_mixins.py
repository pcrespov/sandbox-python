from typing import Any, Optional
from pydantic.fields import FieldInfo,
from pydantic import BaseModel, root_validator

from functools import cached_property
from typing import Sequence, get_args

from pydantic import BaseConfig, BaseSettings, Extra, ValidationError, validator
from pydantic.error_wrappers import ErrorList, ErrorWrapper
from pydantic.fields import ModelField, Undefined


class DefaultFromEnvFactoryError(ValidationError):
    ...


def create_settings_from_env(field: ModelField):
    # NOTE: Cannot pass only field.type_ because @prepare_field (when this function is called)
    #  this value is still not resolved (field.type_ at that moment has a weak_ref).
    #  Therefore we keep the entire 'field' but MUST be treated here as read-only

    def _default_factory():
        """Creates default from sub-settings or None (if nullable)"""
        field_settings_cls = field.type_
        try:
            return field_settings_cls()

        except ValidationError as err:
            if field.allow_none:
                return None

            def _prepend_field_name(ee: ErrorList):
                if isinstance(ee, ErrorWrapper):
                    return ErrorWrapper(ee.exc, (field.name,) + ee.loc_tuple())
                assert isinstance(ee, Sequence)  # nosec
                return [_prepend_field_name(e) for e in ee]

            raise DefaultFromEnvFactoryError(
                errors=_prepend_field_name(err.raw_errors),  # type: ignore
                model=err.model,
                # FIXME: model = shall be the parent settings?? but I dont find how retrieve it from the field
            ) from err

    return _default_factory


class BaseCustomSettings(BaseSettings):
    """
    - Customized configuration for all settings
    - If a field is a BaseCustomSettings subclass, it allows creating a default from env vars setting the Field
      option 'auto_default_from_env=True'.

    SEE tests for details.
    """

    @validator("*", pre=True)
    @classmethod
    def parse_none(cls, v, field: ModelField):
        # WARNING: In nullable fields, envs equal to null or none are parsed as None !!
        if field.allow_none:
            if isinstance(v, str) and v.lower() in ("null", "none"):
                return None
        return v

    class Config(BaseConfig):
        case_sensitive = True  # All must be capitalized
        extra = Extra.forbid
        allow_mutation = False
        frozen = True
        validate_all = True
        keep_untouched = (cached_property,)

        @classmethod
        def prepare_field(cls, field: ModelField) -> None:
            super().prepare_field(field)

            auto_default_from_env = field.field_info.extra.get(
                "auto_default_from_env", False
            )

            field_type = field.type_
            if args := get_args(field_type):
                field_type = next(a for a in args if a != type(None))

            if issubclass(field_type, BaseCustomSettings):

                if auto_default_from_env:

                    assert field.field_info.default is Undefined
                    assert field.field_info.default_factory is None

                    # Transform it into something like `Field(default_factory=create_settings_from_env(field))`
                    field.default_factory = create_settings_from_env(field)
                    field.default = None
                    field.required = False  # has a default now

            elif issubclass(field_type, BaseSettings):
                raise ValueError(
                    f"{cls}.{field.name} of type {field_type} must inherit from BaseCustomSettings"
                )

            elif auto_default_from_env:
                raise ValueError(
                    "auto_default_from_env=True can only be used in BaseCustomSettings subclasses"
                    f"but field {cls}.{field.name} is {field_type} "
                )

    @classmethod
    def create_from_envs(cls, **overrides):
        # Kept for legacy. Identical to the constructor.
        # Optional to use to make the code more readable
        # More explicit and pylance seems to get less confused
        return cls(**overrides)


import secrets
from typing import Any, Callable, Optional

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials


# NOTE: Kept in case we want to re-enable them
_get_basic_credentials = HTTPBasic()


def get_validated_credentials(
    credentials: Optional[HTTPBasicCredentials] = Depends(_get_basic_credentials),
    settings: ApplicationSettings = Depends(get_settings),
) -> Optional[HTTPBasicCredentials]:

    if settings.is_auth_enabled:

        def _is_valid(current: str, expected: str) -> bool:
            return secrets.compare_digest(
                current.encode("utf8"), expected.encode("utf8")
            )

        if (
            not credentials
            or not _is_valid(
                credentials.username,
                expected=settings.INVITATIONS_USERNAME,
            )
            or not _is_valid(
                credentials.password,
                expected=settings.INVITATIONS_PASSWORD.get_secret_value(),
            )
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Basic"},
            )
    else:
        assert not settings.is_auth_enabled  # nosec

        logger.debug("Auth was disabled: %s", f"{settings=}")

    return credentials



class BasicAuthMixin:
    """
    Requires marking


    SEE test_utils_auth.py for example of usage
    """

    @classmethod
    def _get_mark_name(cls: type[BaseModel], value: str):
        field: FieldInfo
        for field in cls.__field__.values():
            if field.extra.get("x_basic_auth_mixin") == value: #<================= A mechanism to mark fields and identify them in mixins
                return field.name
        raise ValueError(f"Undefined mark 'x_basic_auth_mixin=\"{value}\"'")

    def is_auth_enabled(self) -> bool:
        """
        raise: ValueError
        raises: AttributeError
        """
        username = getattr(self._get_mark_name("USERNAME"))
        password = getattr("PASSWORD")

        return username is not None and password is not None

    @staticmethod
    def do_check_complete_auth_state(
        username: Optional[str], password: Optional[str],
    ):
        # either both None or none of them is None
        if (username is None and password is not None) or (
            username is not None and password is None
        ):
            raise ValueError(
                f"To disable auth, set username==password==None. Partial None is not allowed, got {username=}, {password=}"
            )





from pydantic import Field, SecretStr
#from settings_library.utils_auth import BasicAuthMixin
from settings_library.base import BaseCustomSettings

from typing import Optional

class ApplicationSettings(BaseCustomSettings, BasicAuthMixin):
    SOME_USERNAME: Optional[str] = Field(None, x_basic_auth_mixin="USERNAME")
    SOME_PASSWORD: Optional[SecretStr] = Field(None, x_basic_auth_mixin="PASSWORD")
    SOME_VALUE: int = 3

def test_valid_basic_auth_mixin():



def test_invalid_basic_auth_mixin():
    class UnmarkedSettings(BaseCustomSettings, BasicAuthMixin):
        SOME_USERNAME: Optional[str] = Field(None, x_basic_auth_mixin="USERNAME")
        SOME_PASSWORD: Optional[SecretStr] = None