from pathlib import Path

import pandas as pd
import streamlit as st


DATA_PATH = Path(__file__).with_name("Teen_Mental_Health_Dataset.csv")

st.set_page_config(page_title="Teen Mental Health Dataset", page_icon="📊")


@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    data = pd.read_csv(path)
    if data.empty or len(data.columns) == 0:
        raise ValueError("The dataset contains no records or columns.")
    return data


title_col, action_col = st.columns([5, 1], vertical_alignment="top")
with title_col:
    st.title("Teen Mental Health Dataset")
    st.caption("Browse the dataset, review its entries, and download the records.")

if not DATA_PATH.is_file():
    st.error(f"Dataset not found: {DATA_PATH}")
    st.stop()

try:
    records = load_data(str(DATA_PATH))
except (OSError, pd.errors.ParserError, ValueError) as error:
    st.error(f"Unable to load the dataset: {error}")
    st.stop()

st.session_state.setdefault("current_page", "Home")
st.session_state.setdefault("dataset_page", "Overview")


def go_home() -> None:
    st.session_state["current_page"] = "Home"
    st.session_state["dataset_page"] = "Overview"


def open_login() -> None:
    st.session_state["current_page"] = "Log in"


def open_dashboard() -> None:
    st.session_state["current_page"] = "Dashboard"


with st.sidebar:
    st.button(
        "Dashboard",
        icon=":material/dashboard:",
        on_click=open_dashboard,
        width="stretch",
    )

with action_col:
    st.button("Home", icon=":material/home:", on_click=go_home, width="stretch")
    st.button("Log in", icon=":material/login:", on_click=open_login, width="stretch")

if st.session_state["current_page"] == "Log in":
    st.subheader("Patient details")
    st.info(
        "This demo does not verify identity. Details are kept only in the current "
        "session and are not written to a database."
    )
    with st.form("patient_details"):
        patient_name = st.text_input("Name")
        patient_age = st.number_input("Age", min_value=1, max_value=120, value=16, step=1)
        patient_gender = st.text_input("Gender")
        submitted = st.form_submit_button("Save details", type="primary")

    if submitted:
        if not patient_name.strip() or not patient_gender.strip():
            st.error("Enter a name and gender before saving.")
        else:
            st.session_state["patient_profile"] = {
                "name": patient_name.strip(),
                "age": patient_age,
                "gender": patient_gender.strip(),
            }
            st.session_state["current_page"] = "Dashboard"
            st.rerun()

elif st.session_state["current_page"] == "Dashboard":
    st.subheader("Patient dashboard")
    patient_profile = st.session_state.get("patient_profile")
    if patient_profile:
        st.write(f"**Name:** {patient_profile['name']}")
        st.write(f"**Age:** {patient_profile['age']}")
        st.write(f"**Gender:** {patient_profile['gender']}")
    else:
        st.info("No patient details saved. Select **Log in** to enter a profile.")

else:
    page = st.segmented_control(
        "Navigate",
        ["Overview", "Entries"],
        key="dataset_page",
        label_visibility="collapsed",
    )

    if page == "Overview":
        record_col, field_col = st.columns(2)
        record_col.metric("Records", f"{len(records):,}")
        field_col.metric("Fields", f"{len(records.columns):,}")
        st.subheader("About this dataset")
        st.write(
            "Use **Entries** to browse or search the recorded data. "
            "Download the CSV from that page when you need a local copy."
        )
    else:
        st.subheader("Dataset entries")
        query = st.text_input("Search entries", type="search")
        visible_records = records
        if query:
            matches = records.astype(str).apply(
                lambda column: column.str.contains(query, case=False, na=False, regex=False)
            )
            visible_records = records[matches.any(axis=1)]

        st.caption(f"Showing {len(visible_records):,} of {len(records):,} records.")
        st.dataframe(visible_records, hide_index=True)
        st.download_button(
            "Download CSV",
            data=records.to_csv(index=False),
            file_name=DATA_PATH.name,
            mime="text/csv",
        )
