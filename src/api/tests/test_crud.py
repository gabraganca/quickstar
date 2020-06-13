from collections import namedtuple

from app import crud

_TEST_UUID = "413023e5-81ee-418e-acf3-87a26c95557d"


def test_create_spectrum(celery_app, mocker):
    test_args = dict(teff=20000, logg=4, wstart=4460, wend=4500)
    test_returned_value = {"id": _TEST_UUID}

    Task = namedtuple("Task", ("id"))
    mocker.patch("app.settings.celery_app.send_task", return_value=Task(_TEST_UUID))

    result = crud.create_spectrum(**test_args)

    assert result == test_returned_value  # nosec


def test_get_result_ready(celery_app, mocker):
    test_datetime = "2020-05-23T02:11:08.338810"
    test_status = "SUCCESS"
    test_results = [
        {"wavelength": 1, "flux": 1},
        {"wavelength": 2, "flux": 2},
        {"wavelength": 3, "flux": 3},
    ]

    test_response_payload = {
        "id": _TEST_UUID,
        "status": test_status,
        "results": [{"wavelength": 1, "flux": 1}, {"wavelength": 2, "flux": 2}],
        "finished_at": test_datetime,
        "total_count": len(test_results),
    }

    class AsyncResult:
        status = test_status
        result = test_results
        date_done = test_datetime

        @staticmethod
        def ready():
            return True

    mocker.patch(
        "app.crud.celery_app.AsyncResult", return_value=AsyncResult,
    )

    per_page = 2
    result = crud.get_task(_TEST_UUID, page=1, per_page=per_page)
    assert result == test_response_payload  # nosec
    assert len(result["results"]) == per_page  # nosec


def test_get_result_not_ready(celery_app, mocker):
    test_status = "PENDING"

    test_response_payload = {
        "id": _TEST_UUID,
        "status": test_status,
    }

    class AsyncResult:
        status = test_status

        @staticmethod
        def ready():
            return False

    mocker.patch(
        "app.settings.celery_app.AsyncResult", return_value=AsyncResult,
    )

    result = crud.get_task(_TEST_UUID)
    assert result == test_response_payload  # nosec
