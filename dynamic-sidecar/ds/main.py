from .application import create_app


the_app = create_app()

## uvicorn ds.main:the_app --reload --host=0.0.0.0
