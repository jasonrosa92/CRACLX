from fastapi import FastAPI

from craclx.api.error_handlers import register_error_handlers
from craclx.domain.quote_calculator import DomainValidationError


def test_register_error_handlers_adds_domain_validation_handler() -> None:
    app = FastAPI()

    register_error_handlers(app=app)

    assert DomainValidationError in app.exception_handlers
