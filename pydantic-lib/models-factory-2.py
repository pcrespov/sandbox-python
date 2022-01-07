from pydantic import create_model, ValidationError, validator


def username_alphanumeric(cls, v):
    assert v.isalnum(), "must be alphanumeric"
    return v


validators = {"username_validator": validator("username")(username_alphanumeric)}

UserModel = create_model("UserModel", username=(str, ...), __validators__=validators)

user = UserModel(username="scolvin")
print(user)
# > username='scolvin'

try:
    UserModel(username="scolvi%n")
except ValidationError as e:
    print(e)
    """
    1 validation error for UserModel
    username
      must be alphanumeric (type=assertion_error)
    """
