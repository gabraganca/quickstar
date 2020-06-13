from uuid import UUID
from app.settings import celery_app


def create_spectrum(teff: float, logg: float, wstart: float, wend: float, **kwargs):
    task = celery_app.send_task(
        "app.tasks.run_synspec",
        kwargs=dict(teff=teff, logg=logg, wstart=wstart, wend=wend, **kwargs),
    )
    return {"id": task.id}


def get_task(task_id: UUID, page: int = 1, per_page: int = 20):
    task_result = celery_app.AsyncResult(str(task_id))
    response = dict(id=task_id, status=task_result.status)
    if task_result.ready():
        response.update(
            dict(
                results=task_result.result[per_page * (page - 1) : per_page * (page)],
                finished_at=task_result.date_done,
            )
        )
        response["total_count"] = len(task_result.result)

    return response
