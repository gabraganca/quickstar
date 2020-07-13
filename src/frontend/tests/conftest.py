from unittest.mock import patch
from functools import wraps

import pytest


def _mock_decorator(*args, **kwargs):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            return f(*args, **kwargs)

        return decorated_function

    return decorator


@pytest.fixture
def bypass_streamlit_cache():
    patcher = patch("streamlit.cache", _mock_decorator)
    patcher.start()
    yield
    patcher.stop()
