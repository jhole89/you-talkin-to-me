from app import run
import pytest


@pytest.fixture(scope='session')
def app():
    return run.app
