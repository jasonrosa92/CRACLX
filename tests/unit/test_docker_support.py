from pathlib import Path


def test_dockerfile_documents_backend_runtime() -> None:
    dockerfile = Path("Dockerfile").read_text(encoding="utf-8")

    assert "FROM python:3.12-slim" in dockerfile
    assert "USER app" in dockerfile
    assert "EXPOSE 8000" in dockerfile
    assert "craclx.bootstrap.app:create_app" in dockerfile


def test_dockerignore_excludes_local_and_secret_files() -> None:
    dockerignore = Path(".dockerignore").read_text(encoding="utf-8")

    assert ".env" in dockerignore
    assert ".git" in dockerignore
    assert ".venv" in dockerignore
    assert "__pycache__" in dockerignore
