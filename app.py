import streamlit as st
from questions import questions, prizes
from PIL import Image
import base64
import time

# -------------------- PAGE CONFIG -----------------------

st.set_page_config(
    page_title="Millionaire Game",
    page_icon="assets/logo.png",
    layout="wide"
)

# -------------------- LOAD IMAGES -----------------------

logo = Image.open("assets/logo.png")


def get_base64(file):
    with open(file, "rb") as f:
        return base64.b64encode(f.read()).decode()


bg_image = get_base64("assets/background.jpeg")

# -------------------- CSS -----------------------

st.markdown(
    f"""
<style>

/* Background Image */
.stApp {{
    background: url("data:image/jpeg;base64,{bg_image}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    color: white;
}}

/* Dark overlay for readability */
[data-testid="stAppViewContainer"] {{
    background: rgba(0,0,0,0.45);
}}

.question-box {{
    background:#16213e;
    padding:25px;
    border-radius:20px;
    font-size:28px;
    font-weight:bold;
    margin-bottom:20px;
    border:2px solid gold;
}}

.prize-box {{
    background:#101937;
    padding:20px;
    border-radius:15px;
    text-align:center;
    font-size:24px;
    border:2px solid #ffd700;
}}

.correct {{
    background:#0d7d46;
    padding:10px;
    border-radius:10px;
}}

.wrong {{
    background:#8b0000;
    padding:10px;
    border-radius:10px;
}}

/* Hide Streamlit Menu */
#MainMenu {{
    visibility:hidden;
}}

footer {{
    visibility:hidden;
}}

/* Title Styling */
.game-title {{
    font-size:48px;
    font-weight:bold;
    color:white;
}}

</style>
""",
    unsafe_allow_html=True,
)

# ---------------- Timer Functions ----------------

QUESTION_TIME = 30

def get_time_remaining():
    elapsed = int(time.time() - st.session_state.question_start_time)
    remaining = QUESTION_TIME - elapsed
    return max(0, remaining)


# ---------------- Session State ----------------

if "question_no" not in st.session_state:
    st.session_state.question_no = 0

if "money" not in st.session_state:
    st.session_state.money = 0

if "game_over" not in st.session_state:
    st.session_state.game_over = False

# ---------- Timer ----------

QUESTION_TIME = 30

if "question_start_time" not in st.session_state:
    st.session_state.question_start_time = time.time()

if "last_question" not in st.session_state:
    st.session_state.last_question = 0

# Reset timer whenever a new question appears
if st.session_state.last_question != st.session_state.question_no:
    st.session_state.question_start_time = time.time()
    st.session_state.last_question = st.session_state.question_no

# ---------------- Sidebar ----------------------

st.sidebar.title("💰 Prize Ladder")

# ---------------- Timer ----------------

remaining = get_time_remaining()

progress_value = remaining / QUESTION_TIME

if remaining > 20:
    timer_color = "#00ff66"      # Green
elif remaining > 10:
    timer_color = "#ffb000"      # Orange
else:
    timer_color = "#ff2b2b"      # Red

st.markdown(
    f"""
    <h2 style='text-align:center;
               color:{timer_color};
               margin-bottom:5px;'>
        ⏰ {remaining} Seconds Remaining
    </h2>
    """,
    unsafe_allow_html=True,
)

st.progress(progress_value)

for i in reversed(range(len(prizes))):
    if i == st.session_state.question_no:
        st.sidebar.success(f"➡ Rs {prizes[i]:,}")
    else:
        st.sidebar.write(f"Rs {prizes[i]:,}")

# ---------------- Header -----------------------

col1, col2 = st.columns([1, 8])

with col1:
    st.image(logo, width=100)

with col2:
    st.markdown(
        """
        <div class="game-title">
        Who Wants To Be A Millionaire
        </div>
        """,
        unsafe_allow_html=True,
    )

progress = st.progress(
    st.session_state.question_no / len(questions)
)
left, right = st.columns([2, 1])

with left:

    st.markdown(
    f"""
    <div class="prize-box">
    Current Winnings
    <h2>Rs {st.session_state.money:,}</h2>
    </div>
    """,
    unsafe_allow_html=True
    )

with right:

    remaining = get_time_remaining()

    if remaining > 20:
        color = "#00ff66"
    elif remaining > 10:
        color = "#ffb000"
    else:
        color = "#ff2b2b"

    st.markdown(
        f"""
        <div style="
            background:#101937;
            border-radius:15px;
            border:2px solid gold;
            padding:18px;
            text-align:center;
        ">
        <h3 style="color:{color};">
        ⏰ {remaining}s
        </h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.progress(remaining / QUESTION_TIME)

# ---------------- Game Finished ----------------

if st.session_state.game_over:

    st.error("Game Over!")

    st.header(f"You won Rs {st.session_state.money:,}")

    if st.button("Play Again"):

        st.session_state.question_no = 0
        st.session_state.money = 0
        st.session_state.game_over = False

        st.session_state.question_start_time = time.time()
        st.session_state.last_question = 0

        if "answer" in st.session_state:
            del st.session_state["answer"]

        st.rerun()

# ---------------- Winner -----------------------

if st.session_state.question_no == len(questions):

    st.balloons()

    st.success("🏆 CONGRATULATIONS!")

    st.header(f"You won Rs {st.session_state.money:,}")

    if st.button("Play Again"):

        st.session_state.question_no = 0
        st.session_state.money = 0
        st.session_state.game_over = False

        st.session_state.question_start_time = time.time()
        st.session_state.last_question = 0

        if "answer" in st.session_state:
            del st.session_state["answer"]

        st.rerun()


# ---------------- Time's Up ----------------

if remaining <= 0:

    st.session_state.game_over = True

    st.error("⏰ Time's Up!")

    st.info(
        f"The correct answer was: {questions[st.session_state.question_no][questions[st.session_state.question_no][5]]}"
    )

    st.stop()
# ---------------- Current Question -------------

q = questions[st.session_state.question_no]

st.markdown(
    f"""
<div class="question-box">

Question {st.session_state.question_no+1}

<br><br>

{q[0]}

</div>
""",
    unsafe_allow_html=True,
)

answer = st.radio(
    "Choose your answer",
    [
        q[1],
        q[2],
        q[3],
        q[4]
    ],
    index=None,
    key="answer"
)

if st.button("Submit Answer", use_container_width=True):

    if answer is None:

        st.warning("Please choose an option.")

    else:

        selected = [q[1], q[2], q[3], q[4]].index(answer) + 1

        if selected == q[5]:

            st.success("✅ Correct Answer!")

            time.sleep(0.8)

            st.session_state.money = prizes[st.session_state.question_no]

            # Move to next question
            st.session_state.question_no += 1

            # Reset timer immediately
            st.session_state.question_start_time = time.time()
            st.session_state.last_question = st.session_state.question_no

            # Clear previous radio selection
            if "answer" in st.session_state:
                del st.session_state["answer"]

            st.rerun()

        else:

            st.error("❌ Wrong Answer!")

            st.info(
                f"Correct Answer: {q[q[5]]}"
            )

            st.session_state.game_over = True

            st.rerun()

# ---------------- Auto Refresh ----------------

if (
    not st.session_state.game_over
    and st.session_state.question_no < len(questions)
):
    time.sleep(1)
    st.rerun()

