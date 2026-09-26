import streamlit as st
import pandas as pd

from database import create_database, get_all_bugs
from inverted_index import build_inverted_index
from retrieval import get_best_solution, retrieve_bugs
from evaluation import evaluate
from ai_assistant import generate_solution


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="BugBase | Bug Retrieval System",
    page_icon="🐞",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS - LIGHT BACKGROUND + DARK TEXT
# =========================================================

st.markdown("""
<style>

    /* MAIN BACKGROUND */

    .stApp {
        background-color: #F6F7FB;
        color: #111827;
    }


    /* MAIN CONTENT */

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1450px;
    }


    /* SIDEBAR */

    [data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #1E1B4B 0%,
            #312E81 50%,
            #4338CA 100%
        );
    }

    [data-testid="stSidebar"] * {
        color: white !important;
    }


    /* REMOVE STREAMLIT DEFAULT HEADER */

    header[data-testid="stHeader"] {
        background: transparent;
    }


    /* HERO SECTION */

    .hero-box {
        background: linear-gradient(
            135deg,
            #4F46E5,
            #7C3AED
        );

        padding: 38px 45px;
        border-radius: 24px;

        margin-bottom: 30px;

        box-shadow:
            0px 10px 30px
            rgba(79, 70, 229, 0.20);
    }


    .hero-title {
        color: white;
        font-size: 48px;
        font-weight: 800;
        margin-bottom: 8px;
    }


    .hero-subtitle {
        color: #EDE9FE;
        font-size: 20px;
        margin-bottom: 15px;
    }


    .hero-description {
        color: #F5F3FF;
        font-size: 15px;
        line-height: 1.7;
        max-width: 850px;
    }


    /* SECTION HEADINGS */

    .section-title {
        color: #111827;
        font-size: 30px;
        font-weight: 750;
        margin-bottom: 5px;
    }


    .section-subtitle {
        color: #6B7280;
        font-size: 15px;
        margin-bottom: 25px;
    }


    /* NORMAL CARD */

    .custom-card {
        background: white;

        padding: 22px;

        border-radius: 18px;

        border: 1px solid #E5E7EB;

        box-shadow:
            0px 5px 20px
            rgba(0,0,0,0.05);

        color: #111827;
    }


    /* RESULT CARD */

    .result-card {

        background: white;

        padding: 25px;

        border-radius: 20px;

        border: 1px solid #E5E7EB;

        border-left: 6px solid #6366F1;

        margin-top: 15px;
        margin-bottom: 15px;

        box-shadow:
            0px 6px 22px
            rgba(0,0,0,0.06);

        color: #111827;
    }


    /* RESULT TITLE */

    .result-title {

        font-size: 25px;

        font-weight: 750;

        color: #111827;

        margin-bottom: 5px;
    }


    /* RESULT META */

    .result-meta {

        color: #6B7280;

        font-size: 14px;

        margin-bottom: 18px;
    }


    /* SOLUTION BOX */

    .solution-box {

        background: #ECFDF5;

        border-left: 5px solid #10B981;

        padding: 18px;

        border-radius: 12px;

        color: #064E3B;

        margin-top: 15px;
    }


    /* ANALYSIS BOX */

    .analysis-box {

        background: #EEF2FF;

        border-left: 5px solid #6366F1;

        padding: 17px;

        border-radius: 12px;

        color: #111827;

        margin-top: 12px;
        margin-bottom: 12px;
    }


    /* PIPELINE CARD */

    .pipeline-card {

        background: white;

        border: 1px solid #E5E7EB;

        border-radius: 18px;

        padding: 20px;

        margin-bottom: 10px;

        color: #111827;

        box-shadow:
            0px 4px 15px
            rgba(0,0,0,0.04);
    }


    /* PIPELINE NUMBER */

    .pipeline-number {

        background: #4F46E5;

        color: white;

        border-radius: 50%;

        width: 42px;

        height: 42px;

        display: inline-flex;

        align-items: center;

        justify-content: center;

        font-weight: bold;

        margin-right: 15px;
    }


    /* TAG */

    .tag {

        display: inline-block;

        background: #EEF2FF;

        color: #4338CA;

        padding: 6px 12px;

        border-radius: 20px;

        margin: 3px;

        font-size: 12px;

        font-weight: 600;
    }


    /* METRIC CARDS */

    div[data-testid="stMetric"] {

        background: white;

        padding: 18px;

        border-radius: 16px;

        border: 1px solid #E5E7EB;

        box-shadow:
            0px 4px 15px
            rgba(0,0,0,0.05);
    }


    /* INPUT */

    input {

        background-color: white !important;

        color: #111827 !important;

        border-radius: 10px !important;
    }


    /* =========================================================
       FORCE DARK TEXT ON WHITE BACKGROUNDS
       ========================================================= */

    /* Streamlit metric cards */

    [data-testid="stMetric"] {

        background-color: white !important;

        color: #111827 !important;
    }


    [data-testid="stMetric"] * {

        color: #111827 !important;
    }


    /* Metric value */

    [data-testid="stMetricValue"] {

        color: #111827 !important;
    }


    /* Metric label */

    [data-testid="stMetricLabel"] {

        color: #374151 !important;
    }


    /* Main white cards */

    .custom-card,
    .result-card,
    .pipeline-card {

        color: #111827 !important;
    }


    .custom-card *,
    .result-card *,
    .pipeline-card * {

        color: #111827 !important;
    }


    /* Keep secondary text slightly lighter */

    .result-meta {

        color: #6B7280 !important;
    }


    /* Solution box */

    .solution-box {

        color: #111827 !important;
    }


    .solution-box * {

        color: #111827 !important;
    }


    /* Input text */

    input,
    textarea {

        color: #111827 !important;
    }


    /* Selectbox text */

    [data-baseweb="select"] * {

        color: #111827 !important;
    }


    /* Dataframe text */

    [data-testid="stDataFrame"] * {

        color: #111827 !important;
    }


    /* Normal Streamlit text in main area */

    [data-testid="stMain"] p,
    [data-testid="stMain"] label,
    [data-testid="stMain"] span {

        color: #111827;
    }


    /* =========================================================
       SIDEBAR METRIC CARDS - BLACK TEXT ON WHITE
       ========================================================= */

    [data-testid="stSidebar"] [data-testid="stMetric"] {

        background-color: white !important;

        border-radius: 16px !important;

        padding: 18px !important;

        border: 1px solid #E5E7EB !important;
    }


    /* Metric label */

    [data-testid="stSidebar"] [data-testid="stMetricLabel"] {

        color: #374151 !important;
    }


    /* Metric value */

    [data-testid="stSidebar"] [data-testid="stMetricValue"] {

        color: #111827 !important;
    }


    /* All text inside sidebar metric */

    [data-testid="stSidebar"] [data-testid="stMetric"] * {

        color: #111827 !important;
    }


    /* BUTTON */

    .stButton > button {

        background: linear-gradient(
            135deg,
            #4F46E5,
            #7C3AED
        );

        color: white;

        border: none;

        border-radius: 10px;

        font-weight: 650;

        height: 42px;
    }


    .stButton > button:hover {

        background: linear-gradient(
            135deg,
            #4338CA,
            #6D28D9
        );

        color: white;
    }


    /* FOOTER */

    .footer {

        text-align: center;

        color: #6B7280;

        margin-top: 50px;

        padding-top: 25px;

        border-top: 1px solid #E5E7EB;
    }


    /* SIDEBAR TEXT */

    [data-testid="stSidebar"] {

        color: white !important;
    }


</style>
""", unsafe_allow_html=True)


# =========================================================
# DATABASE INITIALIZATION
# =========================================================

create_database()

df = get_all_bugs()

index = build_inverted_index(df)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("# 🐞 BugBase")

    st.caption(
        "Software Bug & Solution Retrieval System"
    )

    st.divider()

    page = st.radio(

        "Navigation",

        [
            "🔎 Search Bugs",
            "⚙️ IR Pipeline",
            "🗂️ Inverted Index",
            "📊 Evaluation",
            "📚 Dataset",
            "ℹ️ About"
        ]
    )

    st.divider()

    st.markdown("### 📊 System Statistics")

    st.metric(
        "Total Bug Records",
        len(df)
    )

    st.metric(
        "Indexed Terms",
        len(index)
    )

    st.divider()

    st.markdown("### 💻 Languages")

    language_counts = df["Language"].value_counts()

    for language, count in language_counts.items():

        st.write(
            f"**{language}** — {count} bugs"
        )

    st.divider()

    st.markdown("### 🧠 IR Techniques")

    st.write("✓ Text Preprocessing")
    st.write("✓ Tokenization")
    st.write("✓ Stop Word Removal")
    st.write("✓ Stemming")
    st.write("✓ Query Expansion")
    st.write("✓ Pattern Matching")
    st.write("✓ Inverted Index")
    st.write("✓ TF-IDF")
    st.write("✓ Cosine Similarity")
    st.write("✓ Ranking")
    st.write("✓ Evaluation")


# =========================================================
# HERO
# =========================================================

st.markdown("""

<div class="hero-box">

<div class="hero-title">
🐞 BugBase
</div>

<div class="hero-subtitle">
Software Bug & Solution Retrieval System
</div>

<div class="hero-description">

An Information Retrieval based search system that helps programmers
find relevant software bugs and their solutions from a local database.

The system uses Text Preprocessing, Query Expansion, Pattern Matching,
Inverted Indexing, TF-IDF, Cosine Similarity and Document Ranking.

</div>

</div>

""", unsafe_allow_html=True)


# =========================================================
# SEARCH PAGE
# =========================================================

if page == "🔎 Search Bugs":

    st.markdown(
        '<div class="section-title">🔎 Search Software Bugs</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">Enter an error, bug name or keyword to find the most relevant solution.</div>',
        unsafe_allow_html=True
    )


    with st.form("search_form"):

        col1, col2 = st.columns([5, 1])

        with col1:

            query = st.text_input(

                "Search",

                placeholder="Example: Java null pointer exception",

                label_visibility="collapsed"
            )

        with col2:

            top_k = st.selectbox(

                "Results",

                [3, 5, 10],

                index=1
            )


        search_button = st.form_submit_button(

            "🚀 Search BugBase",

            use_container_width=True
        )


    # =====================================================
    # SAMPLE QUERIES
    # =====================================================

    st.markdown("### 💡 Example Searches")

    examples = st.columns(6)

    sample_queries = [

        "Java null pointer",

        "NPE",

        "Python index error",

        "C++ memory leak",

        "C buffer overflow",

        "Web CORS error"
    ]


    for i, sample in enumerate(sample_queries):

        with examples[i]:

            st.info(sample)


    # =====================================================
    # SEARCH
    # =====================================================

    if search_button:

        if not query.strip():

            st.warning(
                "⚠️ Please enter a search query."
            )

        else:

            results, info = retrieve_bugs(
                query,
                df,
                index,
                top_k
            )


            # =================================================
            # BEST RECOMMENDED SOLUTION
            # =================================================

            best_bug = get_best_solution(results)


            if best_bug is not None:

                st.markdown(
                    "## ⭐ Best Recommended Solution"
                )


                best_relevance = (
                    float(best_bug["FinalScore"]) * 100
                )


                st.success(

                    f"Based on the highest relevance score, "
                    f"the best matching solution is from "
                    f"**{best_bug['ErrorName']}** "
                    f"({best_relevance:.1f}% relevance)."
                )


                st.markdown(
                    "### 💡 Solution"
                )


                st.info(
                    best_bug["Solution"]
                )


            # =================================================
            # SEARCH PROCESSING
            # =================================================

            st.divider()

            st.markdown(
                "## 🔬 Search Processing"
            )


            # =================================================
            # METRICS
            # =================================================

            c1, c2, c3, c4 = st.columns(4)


            c1.metric(
                "Original Tokens",
                len(info["original_tokens"])
            )


            c2.metric(
                "Expanded Tokens",
                len(info["expanded_tokens"])
            )


            c3.metric(
                "Candidate Documents",
                info["candidate_count"]
            )


            c4.metric(
                "Results Retrieved",
                len(results)
            )


            # =================================================
            # STEP 1 - PREPROCESSING
            # =================================================

            st.markdown(

                """
                <div class="analysis-box">

                <b>🧹 Step 1: Query Preprocessing</b>

                <br><br>

                Lowercase → Tokenization → Stop Word Removal → Stemming

                </div>
                """,

                unsafe_allow_html=True
            )


            st.code(

                " → ".join(
                    info["original_tokens"]
                )
            )


            # =================================================
            # STEP 2 - QUERY EXPANSION
            # =================================================

            st.markdown(

                """
                <div class="analysis-box">

                <b>🔄 Step 2: Query Expansion</b>

                <br><br>

                Related words and abbreviations are added
                to improve retrieval.

                </div>
                """,

                unsafe_allow_html=True
            )


            st.code(

                " → ".join(
                    info["expanded_tokens"]
                )
            )


            # =================================================
            # STEP 3 - INVERTED INDEX
            # =================================================

            st.markdown(

                """
                <div class="analysis-box">

                <b>🗂️ Step 3: Inverted Index Search</b>

                </div>
                """,

                unsafe_allow_html=True
            )


            if info["matched_terms"]:

                st.write(

                    "Matched Indexed Terms: **"
                    + ", ".join(
                        info["matched_terms"]
                    )
                    + "**"
                )

            else:

                st.write(
                    "No exact indexed term found."
                )


            st.divider()


            # =================================================
            # RESULTS
            # =================================================

            st.markdown(
                f"## 🏆 Top {len(results)} Matching Results"
            )


            if results.empty:

                st.warning(
                    "No matching bugs found."
                )

            else:

                for rank, (_, bug) in enumerate(

                    results.iterrows(),

                    start=1
                ):


                    relevance = min(

                        max(

                            float(
                                bug["FinalScore"]
                            ) * 100,

                            0
                        ),

                        100
                    )


                    cosine_score = float(

                        bug["TFIDF_Cosine"]

                    ) * 100


                    st.markdown(

                        '<div class="result-card">',

                        unsafe_allow_html=True
                    )


                    r1, r2 = st.columns([5, 1])


                    with r1:

                        st.markdown(

                            f'''

                            <div class="result-title">

                            #{rank} 🐛
                            {bug["ErrorName"]}

                            </div>

                            <div class="result-meta">

                            Bug ID:
                            BUG-{int(bug["BugID"]):03d}

                            &nbsp; | &nbsp;

                            {bug["Language"]}

                            </div>

                            ''',

                            unsafe_allow_html=True
                        )


                    with r2:

                        st.metric(

                            "Relevance",

                            f"{relevance:.1f}%"
                        )


                    st.progress(
                        relevance / 100
                    )


                    st.markdown(
                        "### 📝 Description"
                    )


                    st.write(
                        bug["Description"]
                    )


                    st.markdown(
                        "### ⚠️ Possible Cause"
                    )


                    st.write(
                        bug["Cause"]
                    )


                    st.markdown(

                        f'''

                        <div class="solution-box">

                        <b>💡 Recommended Solution</b>

                        <br><br>

                        {bug["Solution"]}

                        </div>

                        ''',

                        unsafe_allow_html=True
                    )


                    st.markdown(
                        "### 🔬 Retrieval Details"
                    )


                    d1, d2 = st.columns(2)


                    with d1:

                        st.metric(

                            "TF-IDF + Cosine",

                            f"{cosine_score:.2f}%"
                        )


                    with d2:

                        pattern = (

                            "✓ Matched"

                            if bug["PatternMatch"]

                            else "No Exact Match"
                        )


                        st.metric(

                            "Pattern Matching",

                            pattern
                        )


                    # =================================================
                    # KEYWORDS
                    # =================================================

                    keywords = str(

                        bug["Keywords"]

                    ).split(",")


                    tags = ""


                    for keyword in keywords:

                        tags += (

                            f'<span class="tag">'

                            f'{keyword.strip()}'

                            f'</span>'
                        )


                    st.markdown(

                        f"""

                        <br>

                        <b>🏷️ Keywords</b>

                        <br>

                        {tags}

                        """,

                        unsafe_allow_html=True
                    )


                    st.markdown(
                        "</div>",
                        unsafe_allow_html=True
                    )


    else:

        st.markdown("""

        <div class="custom-card">

        <h2 style="color:#111827;">
        🚀 How BugBase Works
        </h2>

        <p style="color:#374151; font-size:16px;">

        Enter a software error or bug description.

        BugBase processes the query and retrieves
        the most relevant software bug and solution
        using Information Retrieval techniques.

        </p>

        <br>

        <h4 style="color:#4F46E5;">

        Query → Preprocessing → Expansion →
        Inverted Index → TF-IDF →
        Cosine Similarity → Ranking → Solution

        </h4>

        </div>

        """, unsafe_allow_html=True)


# =========================================================
# IR PIPELINE
# =========================================================

elif page == "⚙️ IR Pipeline":

    st.markdown(
        '<div class="section-title">⚙️ Information Retrieval Pipeline</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">Complete working flow of the BugBase retrieval system.</div>',
        unsafe_allow_html=True
    )


    pipeline = [

        (
            "1",
            "🔎 User Query",
            "The user enters a software error, bug name or keyword."
        ),

        (
            "2",
            "🧹 Text Preprocessing",
            "Converts text to lowercase, tokenizes it, removes stop words and applies stemming."
        ),

        (
            "3",
            "🔄 Query Expansion",
            "Adds related terms and abbreviations such as NPE → Null Pointer Exception."
        ),

        (
            "4",
            "🎯 Pattern Matching",
            "Checks exact phrases and individual query terms against bug records."
        ),

        (
            "5",
            "🗂️ Inverted Index",
            "Maps every important term to the BugIDs containing that term."
        ),

        (
            "6",
            "📊 TF-IDF",
            "Calculates the importance of query terms in candidate documents."
        ),

        (
            "7",
            "📐 Cosine Similarity",
            "Measures similarity between the query vector and bug document vectors."
        ),

        (
            "8",
            "🏆 Ranking",
            "Sorts the retrieved bug documents based on relevance score."
        ),

        (
            "9",
            "💡 Solution Retrieval",
            "Displays the most relevant bug, its cause and recommended solution."
        )
    ]


    for number, title, description in pipeline:

        st.markdown(

            f'''

            <div class="pipeline-card">

            <span class="pipeline-number">

            {number}

            </span>

            <span style="
                font-size:20px;
                font-weight:700;
                color:#111827;
            ">

            {title}

            </span>

            <p style="
                margin-left:58px;
                color:#4B5563;
                margin-top:10px;
            ">

            {description}

            </p>

            </div>

            ''',

            unsafe_allow_html=True
        )


        if number != "9":

            st.markdown(

                "<div style='text-align:center; font-size:25px; color:#6366F1;'>↓</div>",

                unsafe_allow_html=True
            )


# =========================================================
# INVERTED INDEX
# =========================================================

elif page == "🗂️ Inverted Index":

    st.markdown(
        '<div class="section-title">🗂️ Inverted Index Explorer</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">Search a term and view the documents containing it.</div>',
        unsafe_allow_html=True
    )


    index_term = st.text_input(

        "Enter a term",

        placeholder="Example: pointer"
    )


    if index_term:

        term = index_term.lower().strip()


        if term in index:

            bug_ids = sorted(
                index[term]
            )


            c1, c2, c3 = st.columns(3)


            c1.metric(
                "Search Term",
                term
            )


            c2.metric(
                "Document Frequency",
                len(bug_ids)
            )


            c3.metric(
                "Total Indexed Terms",
                len(index)
            )


            st.success(
                f"'{term}' was found in {len(bug_ids)} bug documents."
            )


            st.subheader(
                "📌 Posting List"
            )


            st.code(

                "\n".join(

                    f"BUG-{int(bug_id):03d}"

                    for bug_id in bug_ids
                )
            )


            st.subheader(
                "📚 Matching Documents"
            )


            matching = df[

                df["BugID"].isin(
                    bug_ids
                )

            ][

                [
                    "BugID",
                    "ErrorName",
                    "Language",
                    "Description"
                ]

            ]


            st.dataframe(

                matching,

                use_container_width=True,

                hide_index=True
            )


        else:

            st.warning(
                f"'{term}' was not found in the inverted index."
            )


    st.divider()


    st.subheader(
        "🔤 Most Indexed Terms"
    )


    frequency_data = pd.DataFrame(

        [

            (
                term,
                len(ids)
            )

            for term, ids in index.items()

        ],

        columns=[

            "Term",

            "Document Frequency"
        ]

    ).sort_values(

        "Document Frequency",

        ascending=False

    ).head(30)


    st.dataframe(

        frequency_data,

        use_container_width=True,

        hide_index=True
    )


# =========================================================
# EVALUATION
# =========================================================

elif page == "📊 Evaluation":

    st.markdown(
        '<div class="section-title">📊 IR System Evaluation</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">Performance measurement using Precision, Recall and F1 Score.</div>',
        unsafe_allow_html=True
    )


    evaluation = evaluate(

        df,

        index
    )


    precision = evaluation["precision"]

    recall = evaluation["recall"]

    f1 = evaluation["f1"]


    c1, c2, c3, c4 = st.columns(4)


    c1.metric(
        "Precision",
        f"{precision:.3f}"
    )


    c2.metric(
        "Recall",
        f"{recall:.3f}"
    )


    c3.metric(
        "F1 Score",
        f"{f1:.3f}"
    )


    c4.metric(
        "Successful Queries",
        f"{evaluation['hits']} / {evaluation['total']}"
    )


    st.subheader(
        "📋 Query-wise Evaluation"
    )


    st.dataframe(

        evaluation["table"],

        use_container_width=True,

        hide_index=True
    )


    st.info("""

    **Precision** measures how many retrieved results are relevant.

    **Recall** measures how many relevant documents were retrieved.

    **F1 Score** provides a combined measure of Precision and Recall.

    """)


# =========================================================
# DATASET
# =========================================================

elif page == "📚 Dataset":

    st.markdown(
        '<div class="section-title">📚 BugBase Dataset</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">Local software bug knowledge base used by the Information Retrieval system.</div>',
        unsafe_allow_html=True
    )


    c1, c2, c3, c4 = st.columns(4)


    c1.metric(
        "Total Bugs",
        len(df)
    )


    c2.metric(
        "Languages",
        df["Language"].nunique()
    )


    c3.metric(
        "Java Bugs",
        len(
            df[
                df["Language"] == "Java"
            ]
        )
    )


    c4.metric(
        "Python Bugs",
        len(
            df[
                df["Language"] == "Python"
            ]
        )
    )


    col1, col2 = st.columns(2)


    with col1:

        language_filter = st.selectbox(

            "Filter by Language",

            ["All"] +

            sorted(
                df["Language"]
                .unique()
                .tolist()
            )
        )


    with col2:

        dataset_search = st.text_input(

            "Search Dataset",

            placeholder="Search any bug..."
        )


    filtered_df = df.copy()


    if language_filter != "All":

        filtered_df = filtered_df[

            filtered_df["Language"]

            == language_filter
        ]


    if dataset_search:

        mask = filtered_df.astype(str).apply(

            lambda column:

            column.str.contains(

                dataset_search,

                case=False,

                na=False
            )

        ).any(axis=1)


        filtered_df = filtered_df[mask]


    st.dataframe(

        filtered_df,

        use_container_width=True,

        hide_index=True,

        height=550
    )


# =========================================================
# ABOUT
# =========================================================

elif page == "ℹ️ About":

    st.markdown(
        '<div class="section-title">ℹ️ About BugBase</div>',
        unsafe_allow_html=True
    )


    st.markdown("""

    <div class="custom-card">

    <h2 style="color:#111827;">
    🐞 Project Objective
    </h2>

    <p style="color:#374151; font-size:16px;">

    BugBase is an Information Retrieval based
    Software Bug & Solution Retrieval System.

    It allows programmers to enter a bug or error
    and retrieve the most relevant bug information
    and solution from a local software bug database.

    </p>

    </div>

    """, unsafe_allow_html=True)


    st.markdown(
        "## 🧠 Information Retrieval Techniques"
    )


    techniques = [

        "Text Preprocessing",

        "Tokenization",

        "Stop Word Removal",

        "Stemming",

        "Query Expansion",

        "Pattern Matching",

        "Inverted Index",

        "TF-IDF",

        "Cosine Similarity",

        "Document Ranking",

        "Precision",

        "Recall",

        "F1 Score"
    ]


    columns = st.columns(3)


    for i, technique in enumerate(techniques):

        with columns[i % 3]:

            st.success(
                "✓ " + technique
            )


    st.markdown(
        "## 💻 Technology Stack"
    )


    t1, t2, t3, t4 = st.columns(4)


    t1.metric(
        "🐍 Python",
        "Backend"
    )


    t2.metric(
        "🎨 Streamlit",
        "Frontend"
    )


    t3.metric(
        "📊 Scikit-learn",
        "TF-IDF"
    )


    t4.metric(
        "🗄️ SQLite",
        "Database"
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown("""

<div class="footer">

<b>🐞 BugBase</b>

<br>

Software Bug & Solution Retrieval System

<br>

<small>
Information Retrieval Mini Project
</small>

</div>

""", unsafe_allow_html=True)