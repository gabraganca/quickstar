from random import random, seed

import pandas as pd
import streamlit as st

from app.crud import submit_task, get_spectrum

seed(42)  # To keep the dummy plot static


st.title("Quickstar")
st.write("Synthesize spectrum of OB stars with Synspec.")
spectrum_plot = st.empty()
user_message = st.empty()

dummy_data = pd.DataFrame(
    [{"wavelength": i, "flux": random()} for i in range(4000, 4050)]  # nosec
)
spectrum_plot.line_chart(dummy_data.set_index("wavelength")["flux"])


st.sidebar.text("Set the stellar parameters:")
teff = st.sidebar.number_input("Effective Temperature (Teff)", 15000, 30000, 20000)
logg = st.sidebar.number_input("Superficial gravity (logg)", 3.5, 4.49, 4.0)
wstart = st.sidebar.number_input("Starting wavelength", 3000, 9000, 4450)
wend = st.sidebar.number_input("Ending wavelength", 3000, 9000, 4500)
is_normalized = st.sidebar.checkbox("Normalized?")
gen_spectrum_button = st.sidebar.button("Synthesize spectrum")
error_msg = st.sidebar.empty()

if wstart > wend:
    text_msg = (
        ":no_entry: Ending wavelength should be greater than starting wavelength."
    )
    error_msg.markdown(text_msg)
elif wend - wstart > 100:
    text_msg = "no_entry: Wavelength range should be less than 100 Angstrons."
    error_msg.markdown(text_msg)
elif gen_spectrum_button:
    try:
        task_id = submit_task(
            teff=teff, logg=logg, wstart=wstart, wend=wend, relative=is_normalized
        )
    except RuntimeError:
        st.write(
            ":boom: Something bad happened and it was not possible to create spectrum."
        )
    else:
        df = get_spectrum(task_id)
        spectrum_plot.line_chart(df.set_index("wavelength")["flux"])
