from uuid import UUID
from fastapi import FastAPI, Response, Request

from app import schemas
from app import crud

app = FastAPI()


@app.post("/synspec/", response_model=schemas.TaskBase)
async def create_spectrum(parameters: schemas.SynspecParameters):
    return crud.create_spectrum(**parameters.dict())


@app.head("/synspec/{task_id}",)
@app.get(
    "/synspec/{task_id}",
    response_model=schemas.TaskResult,
    response_model_exclude_unset=True,
)
async def fetch_result(
    request: Request,
    response: Response,
    task_id: UUID,
    page: int = 1,
    per_page: int = 20,
):
    page = page if page > 0 else 1
    content = crud.get_task(task_id, page, per_page)
    if "total_count" in content:
        total_count = content["total_count"]
        n_pages = (total_count // per_page) + (1 if (total_count % per_page) else 0)
        if page <= n_pages:
            base_url = request.base_url
            link = "".join(
                [
                    f"<{base_url}synspec/{task_id}?",
                    "page={page}",
                    f"&per_page={per_page}>; ",
                    'rel="{pos}"',
                ]
            )
            links = []
            if page > 1:
                links.extend(
                    [
                        link.format(page=page - 1, pos="prev"),
                        link.format(page=1, pos="first"),
                    ]
                )
            if page < n_pages:
                links.insert(1, link.format(page=page + 1, pos="next"))
                links.insert(2, link.format(page=n_pages, pos="last"))

            response.headers["link"] = ", ".join(links)
    return content


@app.get("/health/", response_model=schemas.Health)
def health():
    return {"status": True}
