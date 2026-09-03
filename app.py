import streamlit as st
import re

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="CMR University Student Portal",
    page_icon="🎓",
    layout="wide"
)

# =========================================================
# BASIC COLLEGE INFORMATION
# =========================================================

COLLEGE_NAME = "CMR University"
COLLEGE_TIMINGS = "8:30 AM to 4:30 PM"
LIBRARY_TIMINGS = "8:30 AM to 5:00 PM"
ATTENDANCE = "75%"
CONTACT = "+91 9342900666"

# Unicode escape for correct ₹ symbol
RUPEE = "\u20b9"

# =========================================================
# COURSES
# =========================================================

COURSES = [
    "CSE",
    "ECE",
    "Data Science",
    "CST",
    "CE",
    "AIML",
    "B.Com",
    "BCA",
    "MBA"
]

# =========================================================
# COURSE FEES
# =========================================================

COURSE_FEES = {
    "CSE": 132475,
    "ECE": 132475,
    "Data Science": 132475,
    "CST": 132475,
    "CE": 132475,
    "AIML": 132475,
    "B.Com": 107245,
    "BCA": 107245,
    "MBA": 137000
}

# =========================================================
# COURSE EXPLANATIONS
# =========================================================

COURSE_EXPLANATIONS = {
    "CSE": (
        "CSE stands for Computer Science and Engineering. "
        "It focuses on programming, software development, "
        "data structures, algorithms, databases, operating systems, "
        "computer networks and other areas of computer science."
    ),

    "ECE": (
        "ECE stands for Electronics and Communication Engineering. "
        "It focuses on electronics, communication systems, digital electronics, "
        "embedded systems, signal processing and related technologies."
    ),

    "Data Science": (
        "Data Science is a field that focuses on collecting, analyzing "
        "and interpreting data. It involves statistics, programming, "
        "data analysis, machine learning and data visualization."
    ),

    "CST": (
        "CST stands for Computer Science and Technology. "
        "It focuses on computer science concepts, programming, "
        "software technologies, databases, networking and modern computing."
    ),

    "CE": (
        "CE stands for Civil Engineering. "
        "It focuses on construction, structural engineering, buildings, "
        "roads, transportation, surveying and infrastructure development."
    ),

    "AIML": (
        "AIML stands for Artificial Intelligence and Machine Learning. "
        "It focuses on artificial intelligence, machine learning, "
        "deep learning, data analysis and intelligent systems."
    ),

    "B.Com": (
        "B.Com stands for Bachelor of Commerce. "
        "It focuses on accounting, finance, business, economics, "
        "taxation and other commerce-related subjects."
    ),

    "BCA": (
        "BCA stands for Bachelor of Computer Applications. "
        "It focuses on computer applications, programming, databases, "
        "web development and software-related technologies."
    ),

    "MBA": (
        "MBA stands for Master of Business Administration. "
        "It focuses on business management, finance, marketing, "
        "human resources, operations and entrepreneurship."
    )
}

# =========================================================
# HOSTEL FEES
# =========================================================

BOYS_HOSTEL_FEES = {
    1: 200000,
    2: 175000,
    3: 150000,
    4: 125000
}

GIRLS_HOSTEL_FEES = {
    1: 225000,
    2: 200000,
    3: 175000,
    4: 150000
}

# =========================================================
# TRANSPORT FEES
# =========================================================

TRANSPORT_FEES = {
    "Yelahanka Old Town": 5000,
    "Hennur": 5500,
    "Reva Circle": 4300
}

# =========================================================
# HELPER FUNCTIONS
# =========================================================

def money(amount):
    """Format amount with ₹ symbol."""
    return f"{RUPEE}{amount:,}"


def has_word(text, word):
    """
    Checks for a complete word or phrase.
    Prevents CE from matching words such as 'place'.
    """
    pattern = (
        r"(?<![a-zA-Z0-9])"
        + re.escape(word.lower())
        + r"(?![a-zA-Z0-9])"
    )

    return re.search(pattern, text.lower()) is not None


def contains_any(text, phrases):
    """Returns True if any phrase is found."""
    return any(phrase in text for phrase in phrases)


def get_sharing_number(question):
    """
    Detect sharing numbers from questions such as:

    boys 1 sharing
    girls 2 sharing
    3 sharing hostel
    4 share hostel
    """

    patterns = [
        r"([1-4])\s*sharing",
        r"sharing\s*([1-4])",
        r"([1-4])\s*share"
    ]

    for pattern in patterns:
        match = re.search(pattern, question)

        if match:
            return int(match.group(1))

    return None


# =========================================================
# MAIN CHATBOT FUNCTION
# =========================================================

def find_answer(user_question):

    question = user_question.lower().strip()

    # =====================================================
    # 1. GREETINGS
    # =====================================================

    if question in [
        "hi",
        "hello",
        "hey",
        "hii",
        "hiii"
    ]:

        return (
            f"Hello! 👋 Welcome to the {COLLEGE_NAME} Chatbot.\n\n"
            "I can help you with courses, fees, hostel, transport, "
            "timings, library, placements, attendance and contact information."
        )

    # =====================================================
    # 2. THANK YOU
    # =====================================================

    if question in [
        "thanks",
        "thank you",
        "thankyou",
        "thank u",
        "thx"
    ]:

        return "You're welcome! 😊"

    # =====================================================
    # 3. HOSTEL - SPECIFIC FEES FIRST
    # =====================================================

    has_boys = contains_any(
        question,
        [
            "boys",
            "boy",
            "boys hostel",
            "boy hostel"
        ]
    )

    has_girls = contains_any(
        question,
        [
            "girls",
            "girl",
            "girls hostel",
            "girl hostel"
        ]
    )

    has_hostel = contains_any(
        question,
        [
            "hostel",
            "hostel fee",
            "hostel fees",
            "hostel cost",
            "hostel price"
        ]
    )

    sharing = get_sharing_number(question)

    # Boys specific sharing

    if has_boys and sharing is not None:

        fee = BOYS_HOSTEL_FEES[sharing]

        return (
            f"Boys hostel {sharing}-sharing fee is "
            f"{money(fee)} per year."
        )

    # Girls specific sharing

    if has_girls and sharing is not None:

        fee = GIRLS_HOSTEL_FEES[sharing]

        return (
            f"Girls hostel {sharing}-sharing fee is "
            f"{money(fee)} per year."
        )

    # General boys hostel fee

    if has_boys and contains_any(
        question,
        [
            "fee",
            "fees",
            "cost",
            "price",
            "charges"
        ]
    ):

        return (
            "Boys hostel fees per year are:\n\n"
            f"• 1 sharing: {money(200000)}\n"
            f"• 2 sharing: {money(175000)}\n"
            f"• 3 sharing: {money(150000)}\n"
            f"• 4 sharing: {money(125000)}"
        )

    # General girls hostel fee

    if has_girls and contains_any(
        question,
        [
            "fee",
            "fees",
            "cost",
            "price",
            "charges"
        ]
    ):

        return (
            "Girls hostel fees per year are:\n\n"
            f"• 1 sharing: {money(225000)}\n"
            f"• 2 sharing: {money(200000)}\n"
            f"• 3 sharing: {money(175000)}\n"
            f"• 4 sharing: {money(150000)}"
        )

    # General hostel question

    if has_hostel:

        return (
            "Yes, hostel facilities are available for both boys and girls.\n\n"
            "You can ask me about specific sharing options and fees, "
            "for example:\n"
            "• Boys 1 sharing fee\n"
            "• Boys 3 sharing fee\n"
            "• Girls 2 sharing fee\n"
            "• Girls 4 sharing fee"
        )

    # =====================================================
    # 4. TRANSPORT - SPECIFIC ROUTES FIRST
    # =====================================================

    transport_words = [
        "bus",
        "transport",
        "transportation",
        "college bus",
        "college buses",
        "bus service",
        "bus facility"
    ]

    has_transport_question = contains_any(
        question,
        transport_words
    )

    # Yelahanka

    if (
        has_transport_question
        and (
            "yelahanka old town" in question
            or has_word(question, "yelahanka")
        )
    ):

        return (
            f"Bus/transport fee from Yelahanka Old Town is "
            f"{money(5000)} per year."
        )

    # Hennur

    if (
        has_transport_question
        and has_word(question, "hennur")
    ):

        return (
            f"Bus/transport fee from Hennur is "
            f"{money(5500)} per year."
        )

    # Reva Circle

    if (
        has_transport_question
        and "reva circle" in question
    ):

        return (
            f"Bus/transport fee from Reva Circle is "
            f"{money(4300)} per year."
        )

    # General transport

    if has_transport_question:

        return (
            "College buses are available.\n\n"
            "Annual transport fees are:\n\n"
            f"• Yelahanka Old Town: {money(5000)}\n"
            f"• Hennur: {money(5500)}\n"
            f"• Reva Circle: {money(4300)}"
        )

    # =====================================================
    # 5. COURSE FEES
    # =====================================================

    asking_fee = contains_any(
        question,
        [
            "fee",
            "fees",
            "cost",
            "price",
            "tuition"
        ]
    )

    if asking_fee:

        if has_word(question, "cse"):

            return (
                f"CSE course fee is "
                f"{money(COURSE_FEES['CSE'])} per year."
            )

        if has_word(question, "ece"):

            return (
                f"ECE course fee is "
                f"{money(COURSE_FEES['ECE'])} per year."
            )

        if "data science" in question:

            return (
                f"Data Science course fee is "
                f"{money(COURSE_FEES['Data Science'])} per year."
            )

        if has_word(question, "cst"):

            return (
                f"CST course fee is "
                f"{money(COURSE_FEES['CST'])} per year."
            )

        if has_word(question, "ce"):

            return (
                f"CE course fee is "
                f"{money(COURSE_FEES['CE'])} per year."
            )

        if has_word(question, "aiml"):

            return (
                f"AIML course fee is "
                f"{money(COURSE_FEES['AIML'])} per year."
            )

        if (
            has_word(question, "b.com")
            or "bcom" in question
            or "b com" in question
        ):

            return (
                f"B.Com course fee is "
                f"{money(COURSE_FEES['B.Com'])} per year."
            )

        if has_word(question, "bca"):

            return (
                f"BCA course fee is "
                f"{money(COURSE_FEES['BCA'])} per year."
            )

        if has_word(question, "mba"):

            return (
                f"MBA course fee is "
                f"{money(COURSE_FEES['MBA'])} per year."
            )

        return (
            "Course fees per year are:\n\n"
            f"• CSE: {money(132475)}\n"
            f"• ECE: {money(132475)}\n"
            f"• Data Science: {money(132475)}\n"
            f"• CST: {money(132475)}\n"
            f"• CE: {money(132475)}\n"
            f"• AIML: {money(132475)}\n"
            f"• B.Com: {money(107245)}\n"
            f"• BCA: {money(107245)}\n"
            f"• MBA: {money(137000)}"
        )

    # =====================================================
    # 6. COURSE EXPLANATIONS
    # =====================================================

    if has_word(question, "cse"):
        return COURSE_EXPLANATIONS["CSE"]

    if has_word(question, "ece"):
        return COURSE_EXPLANATIONS["ECE"]

    if "data science" in question:
        return COURSE_EXPLANATIONS["Data Science"]

    if has_word(question, "cst"):
        return COURSE_EXPLANATIONS["CST"]

    if has_word(question, "ce"):
        return COURSE_EXPLANATIONS["CE"]

    if has_word(question, "aiml"):
        return COURSE_EXPLANATIONS["AIML"]

    if (
        has_word(question, "b.com")
        or "bcom" in question
        or "b com" in question
    ):
        return COURSE_EXPLANATIONS["B.Com"]

    if has_word(question, "bca"):
        return COURSE_EXPLANATIONS["BCA"]

    if has_word(question, "mba"):
        return COURSE_EXPLANATIONS["MBA"]

    # =====================================================
    # 7. LIST OF COURSES
    # =====================================================

    if contains_any(
        question,
        [
            "courses offered",
            "courses available",
            "what courses",
            "which courses",
            "courses in cmr",
            "courses in college",
            "list of courses"
        ]
    ):

        return (
            "The courses available are:\n\n"
            "• CSE\n"
            "• ECE\n"
            "• Data Science\n"
            "• CST\n"
            "• CE\n"
            "• AIML\n"
            "• B.Com\n"
            "• BCA\n"
            "• MBA"
        )

    # =====================================================
    # 8. COLLEGE TIMINGS
    # =====================================================

    if contains_any(
        question,
        [
            "college timing",
            "college timings",
            "college opens",
            "college open",
            "what time does college open",
            "when does college open",
            "college working hours",
            "college hours"
        ]
    ):

        return (
            f"{COLLEGE_NAME} college timings are "
            f"{COLLEGE_TIMINGS}."
        )

    # =====================================================
    # 9. LIBRARY TIMINGS
    # =====================================================

    if contains_any(
        question,
        [
            "library timing",
            "library timings",
            "library open",
            "library opens",
            "library hours",
            "what time is library"
        ]
    ):

        return f"Library timings are {LIBRARY_TIMINGS}."

    # =====================================================
    # 10. ATTENDANCE
    # =====================================================

    if contains_any(
        question,
        [
            "attendance",
            "minimum attendance",
            "attendance requirement",
            "how much attendance"
        ]
    ):

        return (
            f"The minimum attendance requirement is "
            f"{ATTENDANCE}."
        )

    # =====================================================
    # 11. PLACEMENTS
    # =====================================================

    if contains_any(
        question,
        [
            "placement",
            "placements",
            "placement cell",
            "job placement",
            "campus placement"
        ]
    ):

        return (
            "CMR University has a placement cell "
            "that supports students with placement-related activities."
        )

    # =====================================================
    # 12. CONTACT
    # =====================================================

    if contains_any(
        question,
        [
            "contact",
            "contact number",
            "phone number",
            "mobile number",
            "telephone",
            "how to contact"
        ]
    ):

        return (
            f"You can contact {COLLEGE_NAME} at "
            f"{CONTACT}."
        )

    # =====================================================
    # 13. COLLEGE NAME
    # =====================================================

    if contains_any(
        question,
        [
            "college name",
            "name of college",
            "which college",
            "what college"
        ]
    ):

        return f"The college name is {COLLEGE_NAME}."

    # =====================================================
    # 14. UNKNOWN QUESTIONS
    # =====================================================

    return (
        "Sorry, I don't know the answer to that question. 😕\n\n"
        "You can ask me about:\n"
        "• Courses\n"
        "• Course fees\n"
        "• Hostel fees\n"
        "• Transport fees\n"
        "• College timings\n"
        "• Library timings\n"
        "• Placements\n"
        "• Attendance\n"
        "• Contact information"
    )


# =========================================================
# STITCH-STYLE UI
# =========================================================

st.markdown(
    """
    <style>

    /* ---------- GLOBAL ---------- */

    .stApp {
        background: #f5f7fb;
    }

    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 4rem;
        max-width: 1450px;
    }

    /* ---------- SIDEBAR ---------- */

    section[data-testid="stSidebar"] {
        background: #071a33;
        border-right: 1px solid #102b4d;
    }

    section[data-testid="stSidebar"] * {
        color: white;
    }

    section[data-testid="stSidebar"] .stButton > button {
        background: transparent;
        border: 1px solid transparent;
        color: #dbe7f5;
        text-align: left;
        border-radius: 10px;
        padding: 0.65rem 0.8rem;
        margin-bottom: 0.2rem;
        font-weight: 500;
    }

    section[data-testid="stSidebar"] .stButton > button:hover {
        background: #102b4d;
        border-color: #1b426d;
        color: white;
    }

    /* ---------- HERO ---------- */

    .hero {
        background: linear-gradient(135deg, #071a33 0%, #0d3159 100%);
        border-radius: 20px;
        padding: 2.2rem 2.5rem;
        margin-bottom: 1.6rem;
        color: white;
        box-shadow: 0 12px 35px rgba(7, 26, 51, 0.16);
    }

    .hero-small {
        color: #b9cee5;
        font-size: 0.95rem;
        margin-bottom: 0.4rem;
        letter-spacing: 0.5px;
    }

    .hero-title {
        font-size: 2.3rem;
        font-weight: 800;
        margin: 0;
    }

    .hero-description {
        color: #d9e6f4;
        margin-top: 0.7rem;
        font-size: 1rem;
    }

    /* ---------- SECTION TITLES ---------- */

    .section-title {
        font-size: 1.35rem;
        font-weight: 750;
        color: #10233f;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }

    /* ---------- METRIC CARDS ---------- */

    .metric-card {
        background: white;
        border: 1px solid #e5eaf1;
        border-radius: 16px;
        padding: 1.15rem;
        min-height: 125px;
        box-shadow: 0 5px 18px rgba(15, 35, 60, 0.05);
    }

    .metric-icon {
        font-size: 1.4rem;
        margin-bottom: 0.4rem;
    }

    .metric-label {
        color: #68778c;
        font-size: 0.82rem;
        font-weight: 600;
    }

    .metric-value {
        color: #10233f;
        font-size: 1.2rem;
        font-weight: 750;
        margin-top: 0.3rem;
    }

    /* ---------- RESOURCE CARDS ---------- */

    .resource-card {
        background: white;
        border: 1px solid #e5eaf1;
        border-radius: 16px;
        padding: 1.2rem;
        min-height: 155px;
        box-shadow: 0 5px 18px rgba(15, 35, 60, 0.05);
    }

    .resource-icon {
        font-size: 1.6rem;
        margin-bottom: 0.6rem;
    }

    .resource-title {
        color: #10233f;
        font-size: 1rem;
        font-weight: 750;
    }

    .resource-text {
        color: #6b7788;
        font-size: 0.85rem;
        margin-top: 0.35rem;
    }

    /* ---------- DASHBOARD INFO ---------- */

    .info-panel {
        background: white;
        border: 1px solid #e4e9f0;
        border-radius: 18px;
        padding: 1.5rem;
        margin-top: 1rem;
        box-shadow: 0 5px 18px rgba(15, 35, 60, 0.05);
    }

    /* ---------- COURSE CARDS ---------- */

    .course-card {
        background: white;
        border: 1px solid #e4e9f0;
        border-radius: 14px;
        padding: 1rem;
        margin-bottom: 0.7rem;
        box-shadow: 0 3px 12px rgba(15, 35, 60, 0.04);
    }

    .course-name {
        color: #10233f;
        font-weight: 750;
        font-size: 1rem;
    }

    .course-fee {
        color: #9b6b12;
        font-weight: 700;
        margin-top: 0.25rem;
    }

    /* ---------- CHAT ---------- */

    .chat-header {
        background: #071a33;
        color: white;
        padding: 1rem 1.3rem;
        border-radius: 14px 14px 0 0;
        font-weight: 750;
    }

    /* ---------- BUTTONS ---------- */

    .stButton > button {
        border-radius: 10px;
        border: 1px solid #d9e1eb;
        font-weight: 600;
    }

    /* ---------- DIVIDER ---------- */

    hr {
        border-color: #e1e7ef;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    # Logo
    logo_path = "cmru_logo.png"

    try:
        st.image(logo_path, width=150)
    except:
        st.markdown(
            "<h1 style='font-size:40px;'>🎓</h1>",
            unsafe_allow_html=True
        )

    st.markdown(
        """
        <div style="
            color:#a9bfd8;
            font-size:0.8rem;
            margin-top:-8px;
            margin-bottom:20px;
        ">
        STUDENT INFORMATION PORTAL
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        "<h3 style='color:white;'>Dashboard</h3>",
        unsafe_allow_html=True
    )

    # Initialize selected dashboard topic
    if "selected_topic" not in st.session_state:
        st.session_state.selected_topic = None

    # Dashboard buttons

    if st.button(
        "🏫  College Timings",
        use_container_width=True
    ):
        st.session_state.selected_topic = "college"

    if st.button(
        "📚  Library",
        use_container_width=True
    ):
        st.session_state.selected_topic = "library"

    if st.button(
        "🎓  Courses",
        use_container_width=True
    ):
        st.session_state.selected_topic = "courses"

    if st.button(
        "💰  Fees",
        use_container_width=True
    ):
        st.session_state.selected_topic = "fees"

    if st.button(
        "🏠  Hostel",
        use_container_width=True
    ):
        st.session_state.selected_topic = "hostel"

    if st.button(
        "🚌  Transport",
        use_container_width=True
    ):
        st.session_state.selected_topic = "transport"

    if st.button(
        "💼  Placements",
        use_container_width=True
    ):
        st.session_state.selected_topic = "placements"

    if st.button(
        "📊  Attendance",
        use_container_width=True
    ):
        st.session_state.selected_topic = "attendance"

    if st.button(
        "📞  Contact",
        use_container_width=True
    ):
        st.session_state.selected_topic = "contact"

    st.divider()

    if st.button(
        "🗑️  Clear Chat",
        use_container_width=True
    ):
        st.session_state.messages = []
        st.rerun()


# =========================================================
# MAIN HERO
# =========================================================

st.markdown(
    f"""
    <div class="hero">
        <div class="hero-small">WELCOME TO</div>
        <div class="hero-title">CMR University Student Portal</div>
        <div class="hero-description">
            Your simple student information assistant for courses,
            fees, hostel, transportation and campus information.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# OVERVIEW
# =========================================================

st.markdown(
    '<div class="section-title">Overview</div>',
    unsafe_allow_html=True
)

metric_cols = st.columns(4)

with metric_cols[0]:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-icon">🕐</div>
            <div class="metric-label">College Timings</div>
            <div class="metric-value">{COLLEGE_TIMINGS}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with metric_cols[1]:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-icon">📚</div>
            <div class="metric-label">Library</div>
            <div class="metric-value">{LIBRARY_TIMINGS}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with metric_cols[2]:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-icon">🎓</div>
            <div class="metric-label">Courses</div>
            <div class="metric-value">{len(COURSES)} Programs</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with metric_cols[3]:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-icon">📊</div>
            <div class="metric-label">Minimum Attendance</div>
            <div class="metric-value">{ATTENDANCE}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# QUICK RESOURCES
# =========================================================

st.markdown(
    '<div class="section-title">Quick Resources</div>',
    unsafe_allow_html=True
)

resource_cols = st.columns(4)

with resource_cols[0]:

    st.markdown(
        """
        <div class="resource-card">
            <div class="resource-icon">🎓</div>
            <div class="resource-title">Courses & Programs</div>
            <div class="resource-text">
                Explore available programs and understand what each course focuses on.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("View Courses", key="quick_courses", use_container_width=True):
        st.session_state.selected_topic = "courses"

with resource_cols[1]:

    st.markdown(
        """
        <div class="resource-card">
            <div class="resource-icon">💰</div>
            <div class="resource-title">Course Fees</div>
            <div class="resource-text">
                Check the annual fee structure for the available courses.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("View Fees", key="quick_fees", use_container_width=True):
        st.session_state.selected_topic = "fees"

with resource_cols[2]:

    st.markdown(
        """
        <div class="resource-card">
            <div class="resource-icon">🏠</div>
            <div class="resource-title">Hostel</div>
            <div class="resource-text">
                Check hostel availability and sharing-wise fees for students.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("View Hostel", key="quick_hostel", use_container_width=True):
        st.session_state.selected_topic = "hostel"

with resource_cols[3]:

    st.markdown(
        """
        <div class="resource-card">
            <div class="resource-icon">🚌</div>
            <div class="resource-title">Transportation</div>
            <div class="resource-text">
                Check available college bus routes and annual transport fees.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("View Transport", key="quick_transport", use_container_width=True):
        st.session_state.selected_topic = "transport"


# =========================================================
# DASHBOARD INFORMATION DISPLAY
# =========================================================

selected_topic = st.session_state.get(
    "selected_topic",
    None
)

if selected_topic is not None:

    st.markdown(
        '<div class="section-title">Information</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="info-panel">',
        unsafe_allow_html=True
    )

    # =====================================================
    # COLLEGE TIMINGS
    # =====================================================

    if selected_topic == "college":

        st.subheader("🏫 College Timings")

        st.info(
            f"CMR University college timings are "
            f"**{COLLEGE_TIMINGS}**."
        )

        st.write(
            "Students are expected to follow the regular "
            "college working hours."
        )

    # =====================================================
    # LIBRARY
    # =====================================================

    elif selected_topic == "library":

        st.subheader("📚 Library")

        st.info(
            f"Library timings: **{LIBRARY_TIMINGS}**"
        )

        st.write(
            "The library is available for students during "
            "the listed working hours."
        )

    # =====================================================
    # COURSES
    # =====================================================

    elif selected_topic == "courses":

        st.subheader("🎓 Courses Offered")

        course_cols = st.columns(3)

        for index, course in enumerate(COURSES):

            with course_cols[index % 3]:

                st.markdown(
                    f"""
                    <div class="course-card">
                        <div class="course-name">{course}</div>
                        <div style="
                            color:#68778c;
                            font-size:0.82rem;
                            margin-top:8px;
                            line-height:1.5;
                        ">
                        {COURSE_EXPLANATIONS[course]}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    # =====================================================
    # FEES
    # =====================================================

    elif selected_topic == "fees":

        st.subheader("💰 Course Fees")

        st.write("Course fees per year:")

        fee_cols = st.columns(3)

        for index, course in enumerate(COURSES):

            with fee_cols[index % 3]:

                st.markdown(
                    f"""
                    <div class="course-card">
                        <div class="course-name">{course}</div>
                        <div class="course-fee">
                            {money(COURSE_FEES[course])} / year
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    # =====================================================
    # HOSTEL
    # =====================================================

    elif selected_topic == "hostel":

        st.subheader("🏠 Hostel Facilities")

        st.write(
            "Hostel facilities are available for both "
            "boys and girls."
        )

        hostel_cols = st.columns(2)

        with hostel_cols[0]:

            st.markdown("### 👨 Boys Hostel")

            for sharing, fee in BOYS_HOSTEL_FEES.items():

                st.markdown(
                    f"""
                    <div class="course-card">
                        <div class="course-name">
                            {sharing} Sharing
                        </div>
                        <div class="course-fee">
                            {money(fee)} / year
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        with hostel_cols[1]:

            st.markdown("### 👩 Girls Hostel")

            for sharing, fee in GIRLS_HOSTEL_FEES.items():

                st.markdown(
                    f"""
                    <div class="course-card">
                        <div class="course-name">
                            {sharing} Sharing
                        </div>
                        <div class="course-fee">
                            {money(fee)} / year
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    # =====================================================
    # TRANSPORT
    # =====================================================

    elif selected_topic == "transport":

        st.subheader("🚌 Transportation")

        st.write(
            "College buses are available for students."
        )

        transport_cols = st.columns(3)

        for index, (route, fee) in enumerate(
            TRANSPORT_FEES.items()
        ):

            with transport_cols[index]:

                st.markdown(
                    f"""
                    <div class="course-card">
                        <div class="course-name">
                            🚌 {route}
                        </div>
                        <div class="course-fee">
                            {money(fee)} / year
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    # =====================================================
    # PLACEMENTS
    # =====================================================

    elif selected_topic == "placements":

        st.subheader("💼 Placements")

        st.info(
            "CMR University has a placement cell "
            "that supports students with placement-related activities."
        )

        st.write(
            "Students can ask the chatbot about "
            "placement-related information."
        )

    # =====================================================
    # ATTENDANCE
    # =====================================================

    elif selected_topic == "attendance":

        st.subheader("📊 Attendance Requirement")

        st.metric(
            "Minimum Attendance",
            ATTENDANCE
        )

        st.write(
            "Students need to maintain the minimum "
            "attendance requirement."
        )

    # =====================================================
    # CONTACT
    # =====================================================

    elif selected_topic == "contact":

        st.subheader("📞 Contact Information")

        st.info(
            f"CMR University Contact Number: **{CONTACT}**"
        )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# =========================================================
# CHAT SECTION
# =========================================================

st.markdown(
    '<div class="section-title">CMR University Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="chat-header">
        💬 Chat with CMR University
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# CHAT HISTORY INITIALIZATION
# =========================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


# =========================================================
# DISPLAY CHAT HISTORY
# =========================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# =========================================================
# CHAT INPUT
# =========================================================

user_question = st.chat_input(
    "Ask about courses, fees, hostel, transport, timings..."
)


if user_question:

    # Add user message

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_question
        }
    )

    # Generate answer

    answer = find_answer(user_question)

    # Add chatbot answer

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    # Refresh page

    st.rerun()