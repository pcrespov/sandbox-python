

# TODO: create dynamically with pydantic class: https://pydantic-docs.helpmanual.io/usage/models/#dynamic-model-creation

class RequestParams(BaseModel, ValidationMixin):
    file_type: str
    file_name: Optional[str] = None
    file_size: Optional[PositiveInt] = Field(
        None, description="Expected file size in bytes"
    )
