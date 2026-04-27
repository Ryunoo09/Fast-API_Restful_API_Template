from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError


async def global_exception_handler(request: Request, exc: Exception):
    """Fallback handler untuk error 500 (Internal Server Error) yang tidak terduga."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "message": "Terjadi kesalahan pada sistem, silakan coba beberapa saat lagi.",
            "detail": str(exc)  # Catatan: Di server production sesungguhnya, sembunyikan detail ini.
        },
    )


async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    """Handler khusus untuk error yang berhubungan dengan Database MySQL/SQLAlchemy."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Database Error",
            "message": "Terjadi masalah saat berkomunikasi dengan database.",
            "detail": str(exc)
        },
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handler untuk merapikan format error 422 (Validasi Pydantic) agar lebih mudah dibaca Frontend."""
    errors = [
        {"field": " -> ".join([str(x) for x in err.get("loc", [])]), "message": err.get("msg")}
        for err in exc.errors()
    ]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Validation Error",
            "message": "Data yang dikirimkan tidak sesuai dengan format yang diminta.",
            "detail": errors
        },
    )
