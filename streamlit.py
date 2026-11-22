from pathlib import Path

import pandas as pd
import streamlit as st


DATA_PATH = Path(__file__).with_name("Teen_Mental_Health_Dataset.csv")
REQUIRED_COLUMNS = {
    "age",
    "daily_social_media_hours",
    "platform_usage",
    "sleep_hours",
    "screen_time_before_sleep",
    "physical_activity",
    "social_interaction_level",
    "stress_level",
    "anxiety_level",
}

st.set_page_config(
    page_title="Zahanati Pulse | Teen wellbeing",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
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


@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    data = pd.read_csv(path)
    missing_columns = REQUIRED_COLUMNS.difference(data.columns)
    if missing_columns:
        raise ValueError(f"Dataset is missing required columns: {', '.join(sorted(missing_columns))}")

    for column in REQUIRED_COLUMNS:
        if column != "platform_usage" and column != "social_interaction_level":
            data[column] = pd.to_numeric(data[column], errors="coerce")
    return data.dropna(subset=["age", "daily_social_media_hours", "sleep_hours"])


if not DATA_PATH.exists():
    st.error(f"Could not find the dataset at {DATA_PATH}. Place the CSV beside this app.")
    st.stop()

try:
    df = load_data(str(DATA_PATH))
except (OSError, pd.errors.ParserError, ValueError) as error:
    st.error(f"Unable to load the wellbeing dataset: {error}")
    st.stop()

with st.sidebar:
    st.markdown("## 🌿 Zahanati Pulse")
    st.caption("A little more awareness, a little more balance.")
    page = st.radio(
        "Your space",
        ["Overview", "Explore patterns", "My check-in"],
        label_visibility="collapsed",
    )
    st.divider()
    st.markdown(
        "<span class='tiny-label'>A NOTE ON THIS SPACE</span>",
        unsafe_allow_html=True,
    )
    st.caption(
        "This is an educational wellbeing project, not a medical tool. "
        "Your check-in stays in this browser session."
    )


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


if page == "Overview":
    show_hero(
        "Make space for how you feel.",
        "Explore everyday patterns around screen time, rest, and connection. "
        "Small observations can be a helpful place to start.",
    )

    total_records = len(df)
    avg_sleep = df["sleep_hours"].mean()
    avg_social = df["daily_social_media_hours"].mean()
    avg_screen_before_bed = df["screen_time_before_sleep"].mean()
    metric_a, metric_b, metric_c, metric_d = st.columns(4)
    metric_a.metric("Young people represented", f"{total_records:,}", help="Records in the sample dataset")
    metric_b.metric("Average sleep", f"{avg_sleep:.1f} hrs")
    metric_c.metric("Daily social media", f"{avg_social:.1f} hrs")
    metric_d.metric("Screen time before bed", f"{avg_screen_before_bed:.1f} hrs")

    st.write("")
    left, right = st.columns([1.2, 1])
    with left:
        st.subheader("A day in the dataset")
        st.markdown(
            "<p class='section-note'>Average daily social media use and sleep by age.</p>",
            unsafe_allow_html=True,
        )
        by_age = (
            df.groupby("age", as_index=True)[["daily_social_media_hours", "sleep_hours"]]
            .mean()
            .rename(
                columns={
                    "daily_social_media_hours": "Social media (hrs)",
                    "sleep_hours": "Sleep (hrs)",
                }
            )
        )
        st.line_chart(by_age, color=["#5b9b7e", "#d4a65a"], height=300)
    with right:
        st.subheader("What shapes the sample?")
        st.markdown(
            "<p class='section-note'>Records by the most-used platform.</p>",
            unsafe_allow_html=True,
        )
        platform_counts = (
            df["platform_usage"]
            .value_counts()
            .rename_axis("Platform")
            .to_frame("Records")
        )
        st.bar_chart(platform_counts, color="#75a88a", height=300)

    st.write("")
    card_a, card_b, card_c = st.columns(3)
    with card_a:
        st.markdown(
            '<div class="soft-card"><h3>🌙 Rest is a rhythm</h3>'
            '<p>Notice whether late-night scrolling leaves enough room to wind down.</p></div>',
            unsafe_allow_html=True,
        )
    with card_b:
        st.markdown(
            '<div class="soft-card"><h3>🤝 Connection counts</h3>'
            '<p>Make time for the people and activities that help you feel grounded.</p></div>',
            unsafe_allow_html=True,
        )
    with card_c:
        st.markdown(
            '<div class="soft-card"><h3>💚 You are more than a number</h3>'
            '<p>These group patterns describe a sample, not any one person’s experience.</p></div>',
            unsafe_allow_html=True,
        )
    st.caption(
        "Dataset snapshot for learning only. Group averages are descriptive and do not "
        "identify causes or predict an individual's mental health."
    )

elif page == "Explore patterns":
    show_hero(
        "Look a little closer.",
        "Filter the sample to explore how everyday habits vary. "
        "These charts show associations in the data, not cause and effect.",
        eyebrow="EXPLORE THE SAMPLE",
    )

    filter_col, chart_col = st.columns([1, 2.4])
    with filter_col:
        st.subheader("Choose a group")
        min_age = int(df["age"].min())
        max_age = int(df["age"].max())
        age_range = st.slider("Age range", min_age, max_age, (min_age, max_age))
        platforms = sorted(df["platform_usage"].dropna().unique().tolist())
        selected_platforms = st.multiselect("Platform", platforms, default=platforms)
        filtered = df[df["age"].between(age_range[0], age_range[1])]
        if selected_platforms:
            filtered = filtered[filtered["platform_usage"].isin(selected_platforms)]
        else:
            filtered = filtered.iloc[0:0]
        st.caption(f"{len(filtered):,} records in this view")

    with chart_col:
        st.subheader("Sleep and screen time")
        st.markdown(
            "<p class='section-note'>Average hours by age for your selected group.</p>",
            unsafe_allow_html=True,
        )
        if filtered.empty:
            st.info("Choose at least one platform to see the sample.")
        else:
            habits_by_age = (
                filtered.groupby("age")[["sleep_hours", "screen_time_before_sleep"]]
                .mean()
                .rename(
                    columns={
                        "sleep_hours": "Sleep (hrs)",
                        "screen_time_before_sleep": "Screen time before bed (hrs)",
                    }
                )
            )
            st.line_chart(habits_by_age, color=["#5b9b7e", "#d4a65a"], height=310)

    st.subheader("Everyday wellbeing indicators")
    if not filtered.empty:
        indicators = (
            filtered.groupby("social_interaction_level")[
                ["stress_level", "anxiety_level", "physical_activity"]
            ]
            .mean()
            .rename(
                columns={
                    "stress_level": "Stress (average)",
                    "anxiety_level": "Anxiety (average)",
                    "physical_activity": "Physical activity (hrs)",
                }
            )
        )
        st.bar_chart(indicators, color=["#d69a72", "#8b91bd", "#75a88a"], height=280)
    st.caption(
        "Stress and anxiety scores reflect the dataset's own scales. They are not "
        "clinical measurements, diagnoses, or recommendations."
    )

else:
    show_hero(
        "Pause and check in.",
        "Take a moment to notice what you need today. There are no right answers, "
        "and this reflection is not a diagnosis.",
        eyebrow="A MOMENT FOR YOU",
    )
    st.markdown("### How are things feeling right now?")
    st.caption("Your answers are not saved or sent anywhere; they last only for this session.")

    with st.form("wellbeing_check_in"):
        stress = st.slider("How much stress are you carrying?", 0, 10, 5)
        energy = st.slider("How is your energy today?", 0, 10, 5)
        sleep_quality = st.select_slider(
            "How did rest feel last night?",
            options=["Not restful", "A little restless", "Okay", "Restful", "Very restful"],
            value="Okay",
        )
        submitted = st.form_submit_button("See a gentle suggestion", type="primary")

    if submitted:
        if stress >= 7:
            suggestion = "Try taking one small thing off your plate, then take a few slow breaths or talk with someone you trust."
        elif energy <= 3:
            suggestion = "A little water, a stretch, or a few minutes away from your screen may help you reset."
        elif sleep_quality in ("Not restful", "A little restless"):
            suggestion = "A calm, screen-free wind-down tonight might make it easier to settle."
        else:
            suggestion = "Notice what has been helping today, and make a little room for more of it."
        st.success(f"One gentle idea: {suggestion}")

    st.markdown(
        """
        <div class="soft-card">
            <h3>Need more support?</h3>
            <p>If things feel overwhelming or you are worried about your safety, please reach out
            to a trusted adult, school counselor, or local mental health professional. If you are
            in immediate danger, contact your local emergency services.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )