import streamlit as st
import re
import json
from pathlib import Path

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
# COURSE CATALOGUE (LOCAL - NO JSON KEY REQUIRED)
# =========================================================

COURSES = [
    "M.Tech. in VLSI Design & Semiconductor Technology",
    "MCA in Artificial Intelligence and Machine Learning",
    "B.Com. | Fintech",
    "M.Com | Fintech with AI Taxation",
    "B.Tech. | AI & DS",
    "Bachelor in Medical Radiology and Imaging Technology (MRIT)",
    "Bachelor in Anaesthesia and Operation Theatre Technology (AOTT)",
    "B.Sc. (Hons.) (Hospital Administration)",
    "B.Sc. (Hons.) (Medical Laboratory Technology)",
    "Bachelor of Optometry",
    "M.Sc. Information Technology (AI & ML)",
    "MCA",
    "B.Sc. Information Technology (AI & ML)",
    "BCA (AI & ML)",
    "BCA | Game Development",
    "BCA in Cloud Computing",
    "BCA | Data Science",
    "Bachelor of Computer Applications (BCA)",
    "LL.M. | Criminal Law",
    "LL.M. | Commercial Law",
    "LL.M. | Constitutional Law",
    "3-Year LL.B. (Bachelor of Laws)",
    "5-Year Integrated BBA LL.B. (Hons.)",
    "B.A., LL.B. (Hons.)",
    "M.Sc. Psychology | HRDM",
    "M.Sc. Psychology (Counselling)",
    "M.Sc. Clinical Psychology",
    "B.Sc. | Psychology",
    "B.A. Psychology, English, Journalism, Economics, Political Science, History, Sociology, Media Studies, Travel & Tourism",
    "E-MBA | Product Leadership",
    "MBA | Business Analytics & Business Intelligence",
    "MBA | Technology Management",
    "MBA | Dual Specialisation",
    "BBA | Tourism & Hospitality Management",
    "BBA | Logistics & SCM",
    "BBA | Data Science",
    "BBA | Fintech",
    "BBA | Business Analytics",
    "BBA | Digital Marketing",
    "BBA",
    "M.Tech. Artificial Intelligence",
    "M.Tech. Computer Science & Engineering",
    "B.Tech. Computer Engineering (AI & ML)",
    "B.Tech. ECE",
    "B.Tech. CST (AI & ML / IoT)",
    "B.Tech. IT",
    "B.Tech. CSE | Data Science",
    "B.Tech. Artificial Intelligence & Machine Learning",
    "B.Tech. Computer Science & Engineering",
    "B.Com. | US CMA",
    "B.Com. | Data Science",
    "B.Com. | International Accounting & Finance (ACCA)",
    "B.Com. | Professional CA-Integrated",
    "Bachelor of Commerce",
    "B.Sc. VFX & Animation",
    "B.Sc. Sound Engineering",
    "B.Des. Interior Design",
    "B.Des. Fashion Design",
    "B.Des. Product Design",
    "B.Des. Communication Design",
    "Bachelor of Architecture",
]

FEE_COURSES = list(COURSES)

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

# User-provided default annual fees for newly added catalogue courses.
# Existing values above are preserved exactly.
PG_PREFIXES = ("m.tech", "mca", "m.com", "m.sc", "mba", "e-mba", "ll.m")


def get_course_fee(course):
    """Return an existing fee, or the agreed default for a newly added course."""
    if course in COURSE_FEES:
        return COURSE_FEES[course]
    title = course.lower().strip()
    if title.startswith(PG_PREFIXES) or "master of" in title:
        return 150000
    return 135000

# Add a fee value for every listed course without overwriting legacy amounts.
for _course in COURSES:
    COURSE_FEES.setdefault(_course, get_course_fee(_course))
FEE_COURSES = list(COURSES)

# =========================================================
# COURSE EXPLANATIONS
# =========================================================

COURSE_EXPLANATIONS = {
    course: "Program listed in the CMR University course catalogue. Contact the university for curriculum, eligibility and admission details."
    for course in COURSES
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

def normalize_text(value):
    """Normalize punctuation, symbols and whitespace for tolerant matching."""
    value = str(value).lower().replace("&", " and ")
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def ask_optional_gemini(question):
    """External AI is deliberately disabled. The app works locally without API keys."""
    return None


def phrase_match(question, phrases):
    """Match a phrase exactly or tolerate small typing mistakes using stdlib only."""
    q = normalize_text(question)
    if not q:
        return False
    words = q.split()
    for phrase in phrases:
        target = normalize_text(phrase)
        if not target:
            continue
        if target in q:
            return True
        target_words = target.split()
        # Compare short user tokens against the target phrase tokens.
        if len(target_words) == 1:
            token = target_words[0]
            if any(len(w) >= 4 and __import__('difflib').SequenceMatcher(None, w, token).ratio() >= 0.82 for w in words):
                return True
    return False


def find_answer(user_question):
    """Answer college-portal questions using local data only; no API is called."""
    q = normalize_text(user_question)
    if not q:
        return "Please type a question so I can help."

    # Greetings and conversational messages
    if q in {"hi", "hello", "hey", "hii", "hiii", "good morning", "good afternoon", "good evening"}:
        return (f"Hello! Welcome to the {COLLEGE_NAME} Student Assistant. "
                "Ask me about courses, fees, hostel, transport, timings, library, "
                "placements, attendance, examinations or contact details.")
    if q in {"thanks", "thank you", "thankyou", "thank u", "thx"}:
        return "You're welcome! 😊"
    if any(x in q for x in ("who are you", "what are you", "your name")):
        return "I am the CMR University Student Assistant. I can help with the college information available in this portal."

    # College timings (including misspellings and conversational variants)
    college_context = any(x in q for x in ("college", "university", "campus", "class", "classes", "working hours"))
    time_context = any(x in q for x in ("time", "timing", "timings", "timimgs", "open", "opens", "close", "closes", "start", "starts", "end", "ends", "hours", "schedule"))
    if (college_context and time_context) or phrase_match(q, [
        "timings of college", "timing of college", "tell me the timings", "when does college open",
        "when does college close", "when do classes start", "when do classes end", "college schedule",
        "college working hours", "timimgs of college", "tell me college timings"
    ]):
        return f"{COLLEGE_NAME} college timings are {COLLEGE_TIMINGS}."

    # Library timings and information
    if "library" in q:
        if any(x in q for x in ("time", "timing", "timings", "open", "close", "hour", "when", "schedule")):
            return f"Library timings are {LIBRARY_TIMINGS}."
        return f"The university library is available from {LIBRARY_TIMINGS}."

    # Hostel and sharing-wise fees
    hostel_context = any(x in q for x in ("hostel", "accommodation", "residence", "student housing", "stay facility"))
    fee_context = any(x in q for x in ("fee", "fees", "cost", "price", "tuition", "charge", "charges", "how much"))
    if hostel_context:
        m = re.search(r"\b([1-4])\s*(?:sharing|share)\b|\b(?:sharing|share)\s*([1-4])\b", q)
        sharing = int(next(g for g in m.groups() if g)) if m else None
        boys = any(x in q for x in ("boy", "boys", "male"))
        girls = any(x in q for x in ("girl", "girls", "female"))
        if fee_context or "fee" in q or "charge" in q or "cost" in q:
            if boys and sharing:
                return f"Boys hostel {sharing}-sharing fee is {money(BOYS_HOSTEL_FEES[sharing])} per year."
            if girls and sharing:
                return f"Girls hostel {sharing}-sharing fee is {money(GIRLS_HOSTEL_FEES[sharing])} per year."
            if boys:
                return "Boys hostel fees per year:\n\n" + "\n".join(f"• {n}-sharing: {money(v)}" for n, v in BOYS_HOSTEL_FEES.items())
            if girls:
                return "Girls hostel fees per year:\n\n" + "\n".join(f"• {n}-sharing: {money(v)}" for n, v in GIRLS_HOSTEL_FEES.items())
            return ("Hostel fees per year:\n\nBOYS HOSTEL\n" + "\n".join(f"• {n}-sharing: {money(v)}" for n, v in BOYS_HOSTEL_FEES.items()) +
                    "\n\nGIRLS HOSTEL\n" + "\n".join(f"• {n}-sharing: {money(v)}" for n, v in GIRLS_HOSTEL_FEES.items()))
        return "Hostel facilities are listed for boys and girls. Ask for boys' or girls' hostel fees and 1-, 2-, 3- or 4-sharing options."

       # =====================================================
    # TRANSPORT AVAILABILITY AND ROUTE FEES
    # =====================================================

    transport_keywords = [
        "bus",
        "transport",
        "transportation",
        "commute",
        "college vehicle",
        "travel",
        "travelling",
        "travelling cost",
        "travel cost",
        "travel charges",
        "bus fare",
        "bus charges",
        "pickup",
        "pick up",
        "drop",
        "distance from",
        "how much to travel",
        "cost of travelling",
        "cost of traveling"
    ]

    is_transport_question = any(
        keyword in q for keyword in transport_keywords
    )

    if is_transport_question:

        if fee_context or any(
            keyword in q
            for keyword in ["cost", "price", "fee", "fees", "charge", "fare", "how much"]
        ):

            for route, amount in TRANSPORT_FEES.items():

                route_name = normalize_text(route)

                if route_name in q or normalize_text(route.split()[0]) in q:

                    return (
                        f"Annual transport fee from {route} "
                        f"is {money(amount)}."
                    )

            return (
                "I couldn't identify that pickup location. "
                "Currently available transport routes are:\n\n"
                + "\n".join(
                    f"• {route}: {money(amount)} per year"
                    for route, amount in TRANSPORT_FEES.items()
                )
            )

        return (
            "Yes, CMR University provides transportation "
            "on selected routes:\n\n"
            + "\n".join(
                f"• {route}: {money(amount)} per year"
                for route, amount in TRANSPORT_FEES.items()
            )
        )
    # Course fees: preserve the old recorded fee values; use requested defaults for new programs.
    if fee_context:
        matched = []
        for course in COURSES:
            title = normalize_text(course)
            if title and title in q:
                matched.append(course)
        aliases = {
            "mca": ("mca", "master of computer applications"),
            "bca": ("bca", "bachelor of computer applications"),
            "mba": ("mba", "master of business administration"),
            "bba": ("bba", "bachelor of business administration"),
            "bcom": ("b com", "bcom", "bachelor of commerce"),
            "mcom": ("m com", "mcom", "master of commerce"),
            "btech": ("b tech", "btech", "bachelor of technology"),
            "mtech": ("m tech", "mtech", "master of technology"),
            "cse": ("cse", "computer science engineering", "computer science and engineering"),
            "ece": ("ece", "electronics and communication"),
            "aiml": ("aiml", "ai and ml", "artificial intelligence and machine learning"),
            "vlsi": ("vlsi", "semiconductor"),
            "fashion design": ("fashion design",),
            "psychology": ("psychology",),
            "optometry": ("optometry", "optom"),
        }
        if not matched:
            for aliases in aliases.values():
                if any(normalize_text(a) in q for a in aliases):
                    for course in COURSES:
                        title = normalize_text(course)
                        if any(normalize_text(a) in title for a in aliases) and course not in matched:
                            matched.append(course)
        if matched:
            return "Annual course fees (project-provided amounts):\n\n" + "\n".join(f"• {c}: {money(get_course_fee(c))}" for c in matched)
        return "Annual course fees for the listed programs:\n\n" + "\n".join(f"• {c}: {money(get_course_fee(c))}" for c in COURSES)

    # Course catalogue and category matching
    category_map = {
        "engineering": ("b.tech", "m.tech", "engineering", "computer engineering"),
        "medical": ("medical", "anaesthesia", "optometry", "hospital administration", "laboratory technology", "mrit", "aott", "mlt"),
        "healthcare": ("medical", "anaesthesia", "optometry", "hospital administration", "laboratory technology", "mrit", "aott", "mlt"),
        "commerce": ("b.com", "m.com", "commerce", "fintech", "accounting"),
        "management": ("bba", "mba", "e-mba", "management", "business"),
        "computer applications": ("bca", "mca"),
        "design": ("design", "architecture", "vfx", "animation"),
        "law": ("ll.b", "ll.m", "law"),
        "psychology": ("psychology",),
        "postgraduate": ("m.tech", "mca", "m.com", "m.sc", "mba", "e-mba", "ll.m"),
        "undergraduate": ("b.tech", "bca", "b.com", "bba", "b.sc", "b.des", "bachelor", "b.arch", "ll.b"),
    }
    for category, markers in category_map.items():
        if category in q:
            results = [c for c in COURSES if any(m in c.lower() for m in markers)]
            if results:
                return f"{category.title()} programs in the CMR course catalogue:\n\n" + "\n".join(f"• {c}" for c in results)

    course_words = ("course", "courses", "program", "programs", "programme", "programmes", "study", "offer", "offered", "available", "specialisation", "specialization")
    if any(w in q for w in course_words):
        matched = [c for c in COURSES if normalize_text(c) in q]
        if not matched:
            aliases = ("mca", "bca", "mba", "bba", "b com", "bcom", "m com", "mcom", "cse", "ece", "aiml", "data science", "fintech", "cloud computing", "game development", "vlsi", "semiconductor", "mrit", "aott", "anaesthesia", "mlt", "optometry", "psychology", "law", "fashion design", "interior design", "product design", "communication design", "architecture", "sound engineering", "vfx", "animation", "tourism", "hospitality", "logistics", "digital marketing", "business analytics", "technology management", "journalism", "computer science", "artificial intelligence")
            hits = [a for a in aliases if normalize_text(a) in q]
            if hits:
                matched = [c for c in COURSES if any(normalize_text(a) in normalize_text(c) for a in hits)]
        if matched:
            return "These programs match your question:\n\n" + "\n".join(f"• {c}" for c in matched)
        return f"The CMR course catalogue contains {len(COURSES)} programs:\n\n" + "\n".join(f"{i}. {c}" for i, c in enumerate(COURSES, 1))

    # Attendance
    if any(x in q for x in ("attendance", "absent", "attend", "minimum percentage", "how many percent", "percentage required")):
        return f"The attendance requirement recorded in this portal is {ATTENDANCE}. Please confirm the current regulation with the university."

    # Exams
    if any(x in q for x in ("exam", "examination", "semester test", "internal test", "exam date", "timetable", "test date")):
        return "The semester examination schedule is announced by the examination department. Please check the latest university notice or contact the examination office."

    # Placements
    if any(x in q for x in ("placement", "job", "recruit", "career opportunity", "campus drive", "companies visit")):
        return "CMR University has a placement cell that supports placement-related activities. For current recruiters, statistics and eligibility, contact the university placement cell."

    # Contact
    if any(x in q for x in ("contact", "phone", "mobile", "telephone", "call", "number", "reach the college", "email", "address")):
        return f"You can contact {COLLEGE_NAME} at {CONTACT}."

    if any(x in q for x in ("which college", "college name", "name of college", "what university")):
        return f"This student portal is for {COLLEGE_NAME}."

    # Local fallback: do not advertise API setup or make an external request.
    return (
        "I can answer questions using the information built into this CMR University portal. "
        "Try asking about courses, a specific program, annual fees, hostel sharing, "
        "transport routes, college or library timings, attendance, exams, placements or contact details. "
        "I don't have a live general-purpose AI engine, so I won't invent answers to unrelated or unavailable questions."
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

    /* ---------- CHAT READABILITY FIX ---------- */
    [data-testid="stChatMessage"] {
        background: #ffffff !important;
        border: 1px solid #dce5f0 !important;
        border-radius: 14px !important;
        padding: 0.9rem 1rem !important;
        margin-bottom: 0.75rem !important;
    }

    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] li,
    [data-testid="stChatMessage"] div,
    [data-testid="stChatMessage"] span {
        color: #10233f !important;
    }

    [data-testid="stChatMessage"] h1,
    [data-testid="stChatMessage"] h2,
    [data-testid="stChatMessage"] h3 {
        color: #071a33 !important;
    }

    [data-testid="stChatInput"] {
        background: #292929 !important;
        border: 1px solid #596579 !important;
        border-radius: 12px !important;
    }

    [data-testid="stChatInput"] textarea {
        color: #ffffff !important;
        caret-color: #ffffff !important;
    }

    [data-testid="stChatInput"] textarea::placeholder {
        color: #d1d9e4 !important;
        opacity: 1 !important;
    }

    [data-testid="stChatInput"] button {
        color: #ffffff !important;
        background: #46566b !important;
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
# CHAT STATE INITIALIZATION
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    # Logo
    logo_path = str(Path(__file__).parent / "cmru_logo.png")

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

        for index, course in enumerate(FEE_COURSES):

            with fee_cols[index % 3]:

                st.markdown(
                    f"""
                    <div class="course-card">
                        <div class="course-name">{course}</div>
                        <div class="course-fee">
                            {money(get_course_fee(course))} / year
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