from uuid import UUID
import os
import json
import requests
import pandas as pd
import streamlit as st

from app.settings import BACKEND_URL, CACHE_TTL


@st.cache(show_spinner=False, ttl=CACHE_TTL)
def submit_task(**stellar_parameters) -> UUID:
    try:
        post_response = requests.post(
            os.path.join(BACKEND_URL, "synspec"), data=json.dumps(stellar_parameters)
        )
        post_response.raise_for_status()
    except requests.exceptions.HTTPError:
        raise RuntimeError("It was not possible to submit task")

    return json.loads(post_response.text)["id"]


# @st.cache(show_spinner=False, ttl=CACHE_TTL)
def get_spectrum(task_id: UUID) -> pd.DataFrame:
    while True:
        get_response = requests.get(os.path.join(BACKEND_URL, "synspec", task_id))

        if get_response.ok:
            data = json.loads(get_response.text)
            status = data["status"].lower()
            if status == "success":
                break

    spectrum = []
    spectrum.extend(data.get("results", []))

    # Paginate to get the rest of the spectrum
    while "next" in get_response.links:
        get_response = requests.get(get_response.links["next"]["url"])
        if get_response.ok:
            spectrum.extend(json.loads(get_response.text).get("results", []))

    return pd.DataFrame(spectrum)
