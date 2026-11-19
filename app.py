
import os
import uuid
import streamlit as st

from src.ingestion.indexing import index_uploaded_documents
from src.rag_pipeline import RAGPipeline
from src.teaching.summary_generator import SummaryGenerator


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="StudyDesk | AI Teaching Assistant",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

/* GLOBAL THEME */

.stApp {
    background-color: #F5F7F4 !important;
    color: #26352C !important;
}

html, body, [class*="css"] {
    color: #26352C;
}

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Hide Streamlit toolbar and Deploy button */

[data-testid="stHeader"] {
    background: transparent !important;
}

[data-testid="stToolbar"],
[data-testid="stDeployButton"] {
    display: none !important;
}


/* SIDEBAR */

[data-testid="stSidebar"] {
    background-color: #EAF1E9 !important;
    border-right: 1px solid #D5E0D5;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span {
    color: #263D2E !important;
}


/* HEADINGS AND TEXT */

h1, h2, h3, h4 {
    color: #17452D !important;
    font-weight: 750 !important;
}

p, li, label {
    color: #35483B;
}


/* TEXT INPUTS */

.stTextInput input,
.stTextArea textarea,
.stNumberInput input {
    background-color: #FFFFFF !important;
    color: #202B24 !important;
    -webkit-text-fill-color: #202B24 !important;
    border: 1px solid #AAB9AC !important;
    border-radius: 8px !important;
    caret-color: #16834A !important;
}

.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: #78867B !important;
    -webkit-text-fill-color: #78867B !important;
    opacity: 1 !important;
}


/* SELECTBOX */

[data-testid="stSelectbox"] [data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    border: 1px solid #AAB9AC !important;
    border-radius: 8px !important;
}

[data-testid="stSelectbox"] [data-baseweb="select"] div {
    color: #202B24 !important;
    -webkit-text-fill-color: #202B24 !important;
}

[data-testid="stSelectbox"] svg {
    fill: #263D2E !important;
    color: #263D2E !important;
}


/* DROPDOWN MENU */

[data-baseweb="popover"] {
    background-color: #FFFFFF !important;
    border: 1px solid #D5E0D5 !important;
}

[data-baseweb="popover"] [role="listbox"] {
    background-color: #FFFFFF !important;
}

[data-baseweb="popover"] [role="option"] {
    background-color: #FFFFFF !important;
    color: #26352C !important;
    -webkit-text-fill-color: #26352C !important;
}

[data-baseweb="popover"] [role="option"] * {
    color: #26352C !important;
    -webkit-text-fill-color: #26352C !important;
}

[data-baseweb="popover"] [role="option"]:hover {
    background-color: #E8F2E8 !important;
}


/* BUTTONS */

.stButton > button,
.stFormSubmitButton > button,
[data-testid="stFormSubmitButton"] button {
    background-color: #16834A !important;
    color: #FFFFFF !important;
    border: 1px solid #16834A !important;
    border-radius: 8px !important;
    min-height: 44px !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    box-shadow: none !important;
}

.stButton > button *,
.stFormSubmitButton > button *,
[data-testid="stFormSubmitButton"] button * {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover,
[data-testid="stFormSubmitButton"] button:hover {
    background-color: #106B3B !important;
    border-color: #106B3B !important;
}

.stButton > button:disabled,
.stFormSubmitButton > button:disabled {
    background-color: #AAB9AC !important;
    border-color: #AAB9AC !important;
    color: #FFFFFF !important;
}


/* FILE UPLOADER */

[data-testid="stFileUploader"] {
    background-color: #FFFFFF !important;
    border: 1px solid #D5E0D5 !important;
    border-radius: 10px !important;
    padding: 12px !important;
}

[data-testid="stFileUploaderDropzone"] {
    background-color: #F0F5EF !important;
    border: 1px dashed #8BAA91 !important;
    border-radius: 8px !important;
}

[data-testid="stFileUploaderDropzone"] * {
    color: #263D2E !important;
    -webkit-text-fill-color: #263D2E !important;
}

[data-testid="stFileUploaderDropzone"] button {
    background-color: #16834A !important;
    border: 1px solid #16834A !important;
}

[data-testid="stFileUploaderDropzone"] button * {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}

[data-testid="stFileUploader"] small,
[data-testid="stFileUploader"] p {
    color: #35483B !important;
    -webkit-text-fill-color: #35483B !important;
}

/* Hide uploaded file name previews */

[data-testid="stFileUploaderFile"] {
    display: none !important;
}


/* ALERT MESSAGES */

[data-testid="stAlert"] {
    background-color: #E8F5E9 !important;
    border: 1px solid #81C784 !important;
    border-radius: 9px !important;
    padding: 14px 16px !important;
}

[data-testid="stAlert"] > div {
    background-color: transparent !important;
}

[data-testid="stAlert"] p,
[data-testid="stAlert"] span,
[data-testid="stAlert"] div,
[data-testid="stAlert"] svg {
    color: #17452D !important;
    -webkit-text-fill-color: #17452D !important;
}

/* Success */

[data-testid="stAlert"][kind="success"] {
    background-color: #E8F5E9 !important;
    border: 1px solid #81C784 !important;
}

[data-testid="stAlert"][kind="success"] * {
    color: #17452D !important;
    -webkit-text-fill-color: #17452D !important;
    background-color: transparent !important;
}

/* Error */

[data-testid="stAlert"][kind="error"] {
    background-color: #FDECEC !important;
    border-color: #E5A09B !important;
}

/* Warning */

[data-testid="stAlert"][kind="warning"] {
    background-color: #FFF5DF !important;
    border-color: #E5C77D !important;
}

/* Info */

[data-testid="stAlert"][kind="info"] {
    background-color: #EAF2FA !important;
    border-color: #A9C7DF !important;
}


/* HERO SECTION */

.hero {
    background-color: #E7F0E6;
    border: 1px solid #D5E4D4;
    border-radius: 13px;
    padding: 25px;
    margin-bottom: 25px;
}

.hero-title {
    color: #17452D !important;
    font-size: 29px;
    font-weight: 800;
}

.hero-subtitle {
    color: #405747 !important;
    font-size: 15px;
    margin-top: 7px;
}


/* PROGRESS BAR */

[data-testid="stProgressBar"] > div {
    background-color: #DCE7DC !important;
}

[data-testid="stProgressBar"] > div > div {
    background-color: #16834A !important;
}


/* STATUS CONTAINER */

[data-testid="stStatusWidget"] {
    color: #26352C !important;
}


/* DIVIDER */

hr {
    border-color: #D5E0D5 !important;
}


/* CHAT MESSAGES */

[data-testid="stChatMessage"] {
    background-color: #FFFFFF;
    border: 1px solid #D5E0D5;
    border-radius: 10px;
    padding: 15px;
}


/* FOOTER */

.footer {
    text-align: center;
    color: #68776C !important;
    font-size: 12px;
    padding: 25px 0 10px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# CONVERSATION SESSION
# =========================================================

if "study_session_id" not in st.session_state:

    st.session_state.study_session_id = str(uuid.uuid4())


# =========================================================
# CACHED AI COMPONENTS
# =========================================================

@st.cache_resource
def get_rag_pipeline():

    return RAGPipeline(top_k=3)


@st.cache_resource
def get_summary_generator():

    return SummaryGenerator(top_k=5)


# =========================================================
# COMMON FUNCTIONS
# =========================================================

def show_hero(title, subtitle):

    st.markdown(
        f"""
        <div class="hero">
            <div class="hero-title">{title}</div>
            <div class="hero-subtitle">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def show_sources(sources):

    if not sources:
        return

    pages = []

    for source in sources:

        source = str(source)

        if ", Page " in source:

            page = source.split(", Page ", 1)[1]

            label = f"Page {page}"

        else:

            label = "Reference material"

        if label not in pages:

            pages.append(label)

    if pages:

        st.markdown("**Reference pages**")

        st.write(" · ".join(pages))


# =========================================================
# SIDEBAR NAVIGATION
# =========================================================

with st.sidebar:

    st.markdown("# StudyDesk")

    st.caption("AI-powered learning workspace")

    st.divider()

    page = st.selectbox(
        "WORKSPACE",
        [
            "My Documents",
            "Ask a Question",
            "Study Notes"
        ],
        key="workspace_navigation"
    )

    st.divider()

    st.markdown("### Learning Workspace")

    st.caption(
        "Upload study materials, understand concepts, "
        "and prepare organized study notes."
    )


# =========================================================
# PAGE 1 - MY DOCUMENTS
# =========================================================

if page == "My Documents":

    show_hero(
        "Welcome to StudyDesk",
        "Upload your study materials and turn them into "
        "interactive learning experiences."
    )

    st.header("Upload Study Materials")

    st.write(
        "Supported formats: PDF and DOCX. "
        "Multiple documents are supported."
    )

    # ---------------------------------------------
    # UPLOAD FORM
    # ---------------------------------------------

    with st.form("upload_form", clear_on_submit=True):

        uploaded_files = st.file_uploader(
            "Select your documents",
            type=["pdf", "docx"],
            accept_multiple_files=True
        )

        upload_clicked = st.form_submit_button(
            "Upload Documents",
            type="primary",
            use_container_width=True
        )

    if upload_clicked:

        if not uploaded_files:

            st.warning(
                "Please select at least one PDF or DOCX document."
            )

        else:

            folder = "data/uploads"

            os.makedirs(folder, exist_ok=True)

            saved_count = 0

            try:

                for uploaded_file in uploaded_files:

                    filename = os.path.basename(
                        uploaded_file.name
                    )

                    name, extension = os.path.splitext(filename)

                    file_path = os.path.join(
                        folder,
                        filename
                    )

                    counter = 1

                    while os.path.exists(file_path):

                        new_filename = (
                            f"{name}_{counter}{extension}"
                        )

                        file_path = os.path.join(
                            folder,
                            new_filename
                        )

                        counter += 1

                    with open(file_path, "wb") as file:

                        file.write(uploaded_file.getbuffer())

                    saved_count += 1

                st.success(
                    f"Upload complete! {saved_count} document(s) "
                    "successfully saved. Now click Process Documents."
                )

            except Exception as error:

                st.error(f"Upload failed: {error}")

                st.exception(error)

    st.divider()

    # ---------------------------------------------
    # DOCUMENT PROCESSING
    # ---------------------------------------------

    st.header("Prepare Learning Library")

    st.write(
        "Process uploaded materials to make them available "
        "for questions and study notes."
    )

    if st.button(
        "Process Documents",
        type="primary",
        use_container_width=True
    ):

        status = st.status(
            "Processing your study materials...",
            expanded=True
        )

        try:

            status.write(
                "Extracting document text, creating chunks, "
                "generating embeddings and storing learning data."
            )

            total_chunks = index_uploaded_documents()

            if total_chunks > 0:

                status.update(
                    label="Document processing completed successfully.",
                    state="complete",
                    expanded=False
                )

                st.success(
                    "Your learning materials are ready. "
                    "You can now ask questions and generate study notes."
                )

            else:

                status.update(
                    label="No readable content found.",
                    state="error",
                    expanded=True
                )

                st.warning(
                    "No readable text was found. "
                    "Check whether your PDF or DOCX contains text."
                )

        except Exception as error:

            status.update(
                label="Document processing failed.",
                state="error",
                expanded=True
            )

            st.error(f"Processing error: {error}")

            st.exception(error)


# =========================================================
# PAGE 2 - ASK A QUESTION WITH CONVERSATION MEMORY
# =========================================================

elif page == "Ask a Question":

    show_hero(
        "Ask a Question",
        "Get explanations based on your uploaded study materials."
    )

    pipeline = get_rag_pipeline()

    session_id = st.session_state.study_session_id

    st.header("Conversation")

    # ---------------------------------------------
    # CLEAR CONVERSATION
    # ---------------------------------------------

    if st.button("Clear Conversation"):

        pipeline.memory.clear_history(session_id)

        st.success("Conversation cleared!")

        st.rerun()

    # ---------------------------------------------
    # DISPLAY CONVERSATION HISTORY
    # ---------------------------------------------

    history = pipeline.memory.get_history(session_id)

    if history:

        for message in history:

            with st.chat_message(message["role"]):

                st.markdown(message["content"])

    else:

        st.info(
            "No conversation yet. Ask your first question!"
        )

    st.divider()

    # ---------------------------------------------
    # QUESTION INPUT FORM
    # ---------------------------------------------

    st.header("Your Question")

    with st.form("question_form", clear_on_submit=True):

        question = st.text_area(
            "Enter your question",
            placeholder="What would you like to understand?",
            height=120
        )

        level = st.selectbox(
            "Explanation Level",
            [
                "beginner",
                "intermediate",
                "advanced"
            ],
            format_func=str.capitalize
        )

        # NEW: TEACHING MODE

        teaching_mode = st.selectbox(
            "Teaching Mode",
            options=[
                "concept",
                "real_world",
                "step_by_step"
            ],
            format_func=lambda mode: {
                "concept": "Concept Explanation",
                "real_world": "Real-World Example",
                "step_by_step": "Step-by-Step Explanation"
            }[mode]
        )

        submit_question = st.form_submit_button(
            "Generate Explanation",
            type="primary",
            use_container_width=True
        )

    # ---------------------------------------------
    # GENERATE ANSWER
    # ---------------------------------------------

    if submit_question:

        if not question.strip():

            st.warning("Please enter a question.")

        else:

            with st.spinner("Preparing your explanation..."):

                try:

                    result = pipeline.ask(
                        question=question.strip(),
                        level=level,
                        session_id=session_id,
                        teaching_mode=teaching_mode
                    )

                    # Refresh UI to display updated history

                    st.rerun()

                except Exception as error:

                    st.error(
                        f"Unable to generate explanation: {error}"
                    )

                    st.exception(error)


# =========================================================
# PAGE 3 - STUDY NOTES
# =========================================================

elif page == "Study Notes":

    show_hero(
        "Study Notes",
        "Generate organized study notes from your uploaded materials."
    )

    topic = st.text_input(
        "Study Topic",
        placeholder="Enter the topic you want to study..."
    )

    if st.button(
        "Generate Study Notes",
        type="primary",
        use_container_width=True
    ):

        if not topic.strip():

            st.warning("Please enter a topic.")

        else:

            with st.spinner("Generating your study notes..."):

                try:

                    result = get_summary_generator().generate(
                        topic.strip()
                    )

                    st.divider()

                    st.header("Your Study Notes")

                    st.markdown(result["summary"])

                    show_sources(
                        result.get("sources", [])
                    )

                except Exception as error:

                    st.error(
                        f"Unable to generate study notes: {error}"
                    )

                    st.exception(error)


# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div class="footer">
    StudyDesk | AI Teaching Assistant
</div>
""", unsafe_allow_html=True)
