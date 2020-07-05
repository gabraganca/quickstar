from fastapi.testclient import TestClient

from app import crud


_TEST_UUID = "413023e5-81ee-418e-acf3-87a26c95557d"
_TEST_TASK_RESULT = {
    "id": _TEST_UUID,
    "status": "SUCCESS",
    "results": [
        {"wavelength": 4400, "flux": 35080000},
        {"wavelength": 4400.01, "flux": 35070000},
    ],
    "finished_at": "2020-05-23T02:11:08.338810",
    "total_count": 42,
}


def _mock_crud_get_task(id, page=1, per_page=20):
    return _TEST_TASK_RESULT


def test_health_route(client: TestClient):
    response = client.get("/health/")

    assert response.status_code == 200  # nosec
    assert response.json() == {"status": True}  # nosec


def test_synspec_post_route(client: TestClient, monkeypatch):
    test_request_payload = dict(teff=20000, logg=4, wstart=4460, wend=4500)
    test_response_payload = {"id": _TEST_UUID}

    def mock_post(**payload):
        return {"id": _TEST_UUID}

    monkeypatch.setattr(crud, "create_spectrum", mock_post)

    response = client.post("/synspec/", json=test_request_payload)
    assert response.status_code == 200  # nosec
    assert response.json() == test_response_payload  # nosec


def test_synspec_post_route_missing_arg(client: TestClient, monkeypatch):
    test_request_payload = dict(logg=4, wstart=4460, wend=4500)  # missing teff
    test_response_payload = {
        "detail": [
            {
                "loc": ["body", "teff"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ]
    }

    response = client.post("/synspec/", json=test_request_payload)
    assert response.status_code == 422  # nosec
    assert response.json() == test_response_payload  # nosec


def test_synspec_get_route(client: TestClient, monkeypatch):
    monkeypatch.setattr(crud, "get_task", _mock_crud_get_task)

    response = client.get(f"/synspec/{_TEST_UUID}")
    assert response.status_code == 200  # nosec
    assert response.json() == _TEST_TASK_RESULT  # nosec


def test_pagination_links(client: TestClient, monkeypatch):
    monkeypatch.setattr(crud, "get_task", _mock_crud_get_task)

    page = 1
    response = client.get(f"/synspec/{_TEST_UUID}?page={page}")
    assert response.status_code == 200  # nosec
    assert "first" not in response.links  # nosec
    assert "prev" not in response.links  # nosec
    assert "next" in response.links  # nosec
    assert "last" in response.links  # nosec

    page = 2
    response = client.get(f"/synspec/{_TEST_UUID}?page={page}")
    assert response.status_code == 200  # nosec
    assert "first" in response.links  # nosec
    assert "prev" in response.links  # nosec
    assert "next" in response.links  # nosec
    assert "last" in response.links  # nosec

    page = 3
    response = client.get(f"/synspec/{_TEST_UUID}?page={page}")
    assert response.status_code == 200  # nosec
    assert "first" in response.links  # nosec
    assert "prev" in response.links  # nosec
    assert "next" not in response.links  # nosec
    assert "last" not in response.links  # nosec


def test_pagination_no_links(client: TestClient, monkeypatch):
    def mock_crud_get_task(id, page=1, per_page=20):
        return dict(id=_TEST_UUID, status="PENDING")

    monkeypatch.setattr(crud, "get_task", mock_crud_get_task)

    response = client.get(f"/synspec/{_TEST_UUID}")
    assert response.status_code == 200  # nosec
    assert not response.links  # nosec
