from pathlib import Path

import pandas as pd
import streamlit as st
from streamlit.errors import StreamlitSecretNotFoundError




DATA_PATH = Path(__file__).with_name("Teen_Mental_Health_Dataset.csv")
REQUIRED_COLUMNS = {
    "age",
    "daily_social_media_hours",
    "sleep_hours",
    "screen_time_before_sleep",
    "physical_activity",
    "stress_level",
    "anxiety_level",
}

st.set_page_config(
    page_title="Zahanati Pulse | Teen wellbeing",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="auto",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');

    :root {
        --ink: #203b38;
        --muted: #71817d;
        --green: #2f7462;
        --mint: #e6f3ed;
        --paper: #f7faf7;
    }
    .stApp { background: var(--paper); color: var(--ink); }
    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
    h1, h2, h3 { font-family: 'Manrope', sans-serif; color: var(--ink); }
    .block-container { max-width: 1180px; padding-top: 2rem; padding-bottom: 3rem; }
    [data-testid="stSidebar"] { background: #eef5f0; border-right: 1px solid #e1ebe4; }
    [data-testid="stMetric"] {
        background: white; border: 1px solid #e7eee8; border-radius: 16px;
        padding: 18px 20px; box-shadow: 0 5px 18px rgba(32, 59, 56, .035);
    }
    [data-testid="stMetricLabel"] { color: #71817d; }
    [data-testid="stMetricValue"] { color: #203b38; font-family: 'Manrope', sans-serif; }
    .hero {
        background: linear-gradient(120deg, #e4f2e9 0%, #eff6ee 55%, #f6f2e5 100%);
        border: 1px solid #e2ece2; border-radius: 24px; padding: 30px 34px;
        margin: 0 0 24px 0;
    }
    .eyebrow { color: #54806c; font-size: .76rem; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; }
    .hero h1 { font-size: clamp(2rem, 4vw, 3rem); line-height: 1.12; margin: 8px 0 10px; }
    .hero p { color: #647772; max-width: 700px; font-size: 1.02rem; margin-bottom: 0; }
    .section-note { color: var(--muted); font-size: .92rem; margin-top: -8px; }
    .soft-card {
        background: white; border: 1px solid #e7eee8; border-radius: 18px;
        padding: 20px 22px; height: 100%;
    }
    .soft-card h3 { font-size: 1.02rem; margin: 0 0 8px; }
    .soft-card p { color: #71817d; font-size: .9rem; margin: 0; }
    .tiny-label { color: #71817d; font-size: .8rem; font-weight: 600; }
    div.stButton > button[kind="primary"] {
        background: #2f7462; border: 0; border-radius: 12px; color: white; font-weight: 700;
    }
    div.stButton > button[kind="primary"]:hover { background: #255e50; border: 0; }
    footer { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.html(
    """
    <style>
    .st-key-sidebar_brand h2,
    .st-key-header_brand h3 {
        color: #000000 !important;
        font-size: 24px !important;
        font-weight: 700 !important;
    }

    .st-key-patient_profile label {
        color: #000000 !important;
        font-size: 24px !important;
        font-weight: 600 !important;
    }
    </style>
    """
)


@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    data = pd.read_csv(path)
    missing_columns = REQUIRED_COLUMNS.difference(data.columns)
    if missing_columns:
        raise ValueError(f"Dataset is missing required columns: {', '.join(sorted(missing_columns))}")

    for column in REQUIRED_COLUMNS:
        data[column] = pd.to_numeric(data[column], errors="coerce")
    data = data.dropna(subset=sorted(REQUIRED_COLUMNS))
    if data.empty:
        raise ValueError("Dataset has no complete rows for the dashboard inputs.")
    return data


if not DATA_PATH.exists():
    st.error(f"Could not find the dataset at {DATA_PATH}. Place the CSV beside this app.")
    st.stop()

try:
    df = load_data(str(DATA_PATH))
except (OSError, pd.errors.ParserError, ValueError) as error:
    st.error(f"Unable to load the wellbeing dataset: {error}")
    st.stop()

if "current_page" not in st.session_state:
    st.session_state["current_page"] = "Home"


def navigate_to(page_name: str) -> None:
    st.session_state["current_page"] = page_name


with st.sidebar:
    st.markdown("## 🌿 Zahanati Pulse", key="sidebar_brand")
    st.caption("Your space for wellbeing.")
    with st.container(horizontal=True, vertical_alignment="center"):
        st.button(
            "Dashboard",
            icon=":material/dashboard:",
            type="primary" if st.session_state["current_page"] == "Dashboard" else "secondary",
            on_click=navigate_to,
            args=("Dashboard",),
            width="stretch",
            key="dashboard_navigation",
        )
        st.button(
            "How to use the app",
            icon=":material/help_outline:",
            type="primary" if st.session_state["current_page"] == "How to use the app" else "secondary",
            on_click=navigate_to,
            args=("How to use the app",),
            width="stretch",
            key="how_to_navigation",
        )
    st.markdown("---")
    st.markdown(
        "<span class='tiny-label'>A NOTE ON THIS SPACE</span>",
        unsafe_allow_html=True,
    )
    st.caption(
        "This is an educational wellbeing project, not a medical tool. "
        "Your entries are kept in this app session and are not written to a database."
    )

brand_col, home_col, login_col = st.columns([4, 1, 1], vertical_alignment="center")
with brand_col:
    st.markdown("### 🌿 Zahanati Pulse", key="header_brand")
with home_col:
    st.button(
        "Home",
        icon=":material/home:",
        type="primary" if st.session_state["current_page"] == "Home" else "secondary",
        on_click=navigate_to,
        args=("Home",),
        width="stretch",
        key="home_navigation",
    )

try:
    auth_configured = "auth" in st.secrets
except StreamlitSecretNotFoundError:
    auth_configured = False
with login_col:
    if auth_configured and st.user.is_logged_in:
        if st.button("Log out", icon=":material/logout:", width="stretch"):
            st.logout()
    elif st.button("Log in", icon=":material/login:", width="stretch"):
        if auth_configured:
            st.login()
        else:
            st.session_state["show_login_setup"] = True

if st.session_state.pop("show_login_setup", False):
    st.info(
        "Sign-in is not configured yet. To enable real log in, set up an OpenID Connect "
        "provider in `.streamlit/secrets.toml`. This demo does not authenticate users or "
        "protect patient data; do not enter identifying information."
    )

page = st.session_state["current_page"]


def show_hero(title: str, subtitle: str, eyebrow: str = "YOUR WELLBEING, IN PERSPECTIVE") -> None:
    st.markdown(
        f"""
        <div class="hero">
            <div class="eyebrow">{eyebrow}</div>
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


if page == "Home":
    show_hero(
        "Make space for how you feel.",
        "A private place to reflect on everyday habits and how you have been feeling. "
        "Use the dashboard to create a personal, non-diagnostic reference chart.",
    )

    card_a, card_b = st.columns(2)
    with card_a:
        st.markdown(
            '<div class="soft-card"><h3>Explore your own inputs</h3>'
            '<p>Enter age and everyday habit information in the dashboard to view how '
            'each value compares with records in the sample.</p></div>',
            unsafe_allow_html=True,
        )
    with card_b:
        st.markdown(
            '<div class="soft-card"><h3>Not a diagnosis</h3>'
            '<p>This educational project does not have a clinically validated model. '
            'Its chart is a dataset comparison, not a mental-health risk estimate.</p></div>',
            unsafe_allow_html=True,
        )

    st.subheader("Age distribution in the sample")
    st.caption("Each bar shows how many dataset records have that age.")
    age_counts = (
        df["age"]
        .value_counts()
        .sort_index()
        .rename_axis("Age")
        .reset_index(name="Records")
    )
    age_counts["Age"] = age_counts["Age"].astype(int)
    st.bar_chart(
        age_counts,
        x="Age",
        y="Records",
        x_label="Age",
        y_label="Number of records",
        color="#75a88a",
        alt="Number of dataset records for each age.",
    )
    st.caption(
        "Please do not enter identifying information. Dashboard inputs are kept in this "
        "app session and are not written to a database."
    )

elif page == "How to use the app":
    show_hero(
        "How to use the app.",
        "A quick guide to navigating your wellbeing dashboard and understanding its charts.",
        eyebrow="GETTING STARTED",
    )
    st.markdown(
        """
        1. Open **Dashboard** from the navigation on the left. On a small screen, use
           the sidebar toggle to open it.
        2. Enter the age and daily habit values requested by the form.
        3. Select **Compare with dataset** to see how each value compares with the
           corresponding values in the sample.
        4. Read the chart as a descriptive dataset comparison only. It is not a
           diagnosis or a probability of mental illness.
        """
    )
    st.warning(
        "Do not enter names or other identifying information. This app is an educational "
        "demo and does not provide clinical assessment."
    )

else:
    show_hero(
        "Your personal dashboard.",
        "Enter the requested information to see how each value sits within the dataset. "
        "This is a descriptive comparison, not a prediction about your mental health.",
        eyebrow="DATASET REFERENCE",
    )
    st.markdown("### Enter your information")
    st.caption(
        "Fill in each field using your usual daily routine. Do not enter your name or "
        "other identifying details."
    )

    with st.form("patient_profile"):
        age_col, social_col = st.columns(2)
        with age_col:
            age = st.number_input(
                "Age (years)",
                min_value=int(df["age"].min()),
                max_value=int(df["age"].max()),
                value=int((df["age"].min() + df["age"].max()) / 2),
                step=1,
                help="Enter your age in whole years.",
            )
            sleep = st.slider(
                "Average sleep per night (hours)",
                min_value=float(df["sleep_hours"].min()),
                max_value=float(df["sleep_hours"].max()),
                value=7.0,
                step=0.1,
                help="Estimate how many hours you usually sleep each night.",
            )
            screen_before_sleep = st.slider(
                "Screen time before bed (hours)",
                min_value=float(df["screen_time_before_sleep"].min()),
                max_value=float(df["screen_time_before_sleep"].max()),
                value=1.5,
                step=0.1,
                help="Estimate your screen use in the hours before going to sleep.",
            )
            physical_activity = st.slider(
                "Physical activity per day (hours)",
                min_value=float(df["physical_activity"].min()),
                max_value=float(df["physical_activity"].max()),
                value=1.0,
                step=0.1,
                help="Estimate the time you spend being physically active on a typical day.",
            )
        with social_col:
            social_media = st.slider(
                "Social media use per day (hours)",
                min_value=float(df["daily_social_media_hours"].min()),
                max_value=float(df["daily_social_media_hours"].max()),
                value=4.0,
                step=0.1,
                help="Estimate your total social media use on a typical day.",
            )
            stress = st.slider(
                "Stress level (1 = low, 10 = high)",
                min_value=int(df["stress_level"].min()),
                max_value=int(df["stress_level"].max()),
                value=5,
                help="Choose the number that best describes your stress level.",
            )
            anxiety = st.slider(
                "Anxiety level (1 = low, 10 = high)",
                min_value=int(df["anxiety_level"].min()),
                max_value=int(df["anxiety_level"].max()),
                value=5,
                help="Choose the number that best describes your anxiety level.",
            )

        submitted = st.form_submit_button(
            "Compare with dataset",
            type="primary",
            icon=":material/insights:",
        )

    if submitted:
        st.session_state["submitted_profile"] = {
            "Age": (age, "age"),
            "Daily social media": (social_media, "daily_social_media_hours"),
            "Sleep": (sleep, "sleep_hours"),
            "Screen time before sleep": (screen_before_sleep, "screen_time_before_sleep"),
            "Physical activity": (physical_activity, "physical_activity"),
            "Stress": (stress, "stress_level"),
            "Anxiety": (anxiety, "anxiety_level"),
        }

    patient_profile = st.session_state.get("submitted_profile")
    if patient_profile:
        percentiles = {
            label: float((df[column].dropna() <= value).mean() * 100)
            for label, (value, column) in patient_profile.items()
        }
        st.subheader("Your dataset reference chart")
        st.info(
            "This chart shows where each entered value falls compared with the "
            "corresponding values in this dataset. Percentiles are not probabilities "
            "of illness and do not indicate whether someone is mentally ill."
        )
        percentile_frame = pd.DataFrame(
            {"Position within dataset (%)": percentiles},
        )
        st.bar_chart(
            percentile_frame,
            y_label="Position within dataset (%)",
            color="#75a88a",
            alt="Percentile positions of your entered values within the dataset, not illness probabilities.",
        )
        st.caption(
            "The dataset's depression label is not a diagnosis, and this app does not "
            "use a clinically validated prediction model. A mental-health professional "
            "can help assess concerns."
        )

    st.markdown(
        """
        <div class="soft-card">
            <h3>Need more support?</h3>
            <p>If things feel overwhelming or you are worried about your safety, please reach
            out to a trusted adult, school counselor, or local mental health professional. If
            you are in immediate danger, contact your local emergency services.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )