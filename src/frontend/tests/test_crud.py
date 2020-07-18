import json

import pytest
from requests.exceptions import HTTPError

_TEST_UUID = "413023e5-81ee-418e-acf3-87a26c95557d"


def test_submit_task(mocker, bypass_streamlit_cache):
    test_args = dict(teff=20000, logg=4, wstart=4460, wend=4500)

    class MockRequestTrueResponse:
        text = json.dumps({"id": _TEST_UUID})

        @staticmethod
        def raise_for_status():
            pass

    mocker.patch("app.crud.requests.post", return_value=MockRequestTrueResponse)

    from app import crud

    result = crud.submit_task(**test_args)

    assert result == _TEST_UUID  # nosec


def test_submit_task_error(mocker, bypass_streamlit_cache):
    test_args = dict(teff=20000, logg=4, wstart=4460, wend=4500)

    class MockRequestFalseResponse:
        @staticmethod
        def raise_for_status():
            raise HTTPError()

    mocker.patch("app.crud.requests.post", return_value=MockRequestFalseResponse)

    from app import crud

    with pytest.raises(RuntimeError):
        _ = crud.submit_task(**test_args)
