import streamlit as st
from questions import questions, prizes
from PIL import Image
import base64

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

# ---------------- Session State ----------------

if "question_no" not in st.session_state:
    st.session_state.question_no = 0

if "money" not in st.session_state:
    st.session_state.money = 0

if "game_over" not in st.session_state:
    st.session_state.game_over = False

# ---------------- Sidebar ----------------------

st.sidebar.title("💰 Prize Ladder")

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

st.markdown(
    f"""
<div class="prize-box">
Current Winnings
<h2>Rs {st.session_state.money:,}</h2>
</div>
""",
    unsafe_allow_html=True,
)

# ---------------- Game Finished ----------------

if st.session_state.game_over:

    st.error("Game Over!")

    st.header(f"You won Rs {st.session_state.money:,}")

    if st.button("Play Again"):

        st.session_state.question_no = 0
        st.session_state.money = 0
        st.session_state.game_over = False
        st.rerun()

    st.stop()

# ---------------- Winner -----------------------

if st.session_state.question_no == len(questions):

    st.balloons()

    st.success("🏆 CONGRATULATIONS!")

    st.header(f"You won Rs {st.session_state.money:,}")

    if st.button("Play Again"):

        st.session_state.question_no = 0
        st.session_state.money = 0
        st.session_state.game_over = False
        st.rerun()

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
        q[4],
    ],
    index=None,
)

if st.button("Submit Answer", use_container_width=True):

    if answer is None:

        st.warning("Please choose an option.")

    else:

        selected = [q[1], q[2], q[3], q[4]].index(answer) + 1

        if selected == q[5]:

            st.success("✅ Correct Answer!")

            st.session_state.money = prizes[st.session_state.question_no]

            st.session_state.question_no += 1

            st.rerun()

        else:

            st.error("❌ Wrong Answer!")

            st.info(
                f"Correct Answer: {q[q[5]]}"
            )

            st.session_state.game_over = True

            st.rerun()