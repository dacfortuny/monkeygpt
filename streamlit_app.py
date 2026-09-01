import time
from pathlib import Path

import streamlit as st

from src.game import Game
from src.utils import get_mistral_api_key

IMAGES_DIR = Path(__file__).parent / "resources" / "images"
PIRATE_AVATAR = IMAGES_DIR / "pirate.png"
USER_AVATAR = IMAGES_DIR / "user.png"

st.set_page_config(page_title="MI: Battles of the Northwest Wind", page_icon="⚔️")

st.html("""
<style>
div[data-testid="stChatMessage"] {
    background-color: transparent !important;
    padding-right: 0 !important;
}
div[data-testid="stChatMessage"] div[data-testid="stChatMessageContent"] {
    flex-grow: 0;
    max-width: 75%;
    padding: 0.5rem 0.9rem;
    border-radius: 1rem;
    margin: 0 !important;
}
div[data-testid="stChatMessage"]:has(div[aria-label="Chat message from user"]) {
    flex-direction: row-reverse;
}
div[data-testid="stChatMessage"]:has(div[aria-label="Chat message from user"]) div[data-testid="stChatMessageContent"] {
    background-color: rgba(37, 211, 102, 0.25);
}
div[data-testid="stChatMessage"]:has(div[aria-label="Chat message from assistant"]) div[data-testid="stChatMessageContent"] {
    background-color: rgba(120, 120, 120, 0.18);
}
.st-key-battle_title,
.st-key-battle_title div,
[class*="st-key-point_caption"],
[class*="st-key-point_caption"] div,
[class*="st-key-point_caption"] p {
    text-align: center !important;
}
div[data-testid="stSpinner"] > div {
    justify-content: center;
}
div[data-testid="stElementContainer"]:has(> div[data-testid="stSpinner"]) {
    align-self: center !important;
}
</style>
""")


def show_clash_animation(duration=4):
    placeholder = st.empty()
    placeholder.html("""
    <style>
    @keyframes mgpt-clash-left {
        0%, 100% { transform: translateX(0) rotate(-25deg); }
        50% { transform: translateX(18px) rotate(-5deg); }
    }
    @keyframes mgpt-clash-right {
        0%, 100% { transform: translateX(0) rotate(25deg); }
        50% { transform: translateX(-18px) rotate(5deg); }
    }
    .mgpt-clash-row {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 0.5rem;
        font-size: 3rem;
        padding: 1rem 0;
    }
    .mgpt-sword {
        display: inline-block;
    }
    .mgpt-sword-left {
        animation: mgpt-clash-left 0.35s ease-in-out infinite;
    }
    .mgpt-sword-right {
        animation: mgpt-clash-right 0.35s ease-in-out infinite;
    }
    .mgpt-flip-both {
        display: inline-block;
        transform: scaleX(-1) scaleY(-1);
    }
    .mgpt-flip-vertical {
        display: inline-block;
        transform: scaleY(-1);
    }
    </style>
    <div class="mgpt-clash-row">
        <span class="mgpt-sword mgpt-sword-left"><span class="mgpt-flip-both">🗡️</span></span>
        <span class="mgpt-sword mgpt-sword-right"><span class="mgpt-flip-vertical">🗡️</span></span>
    </div>
    """)
    time.sleep(duration)
    placeholder.empty()


def start_game(name):
    st.session_state.game = Game(name=name.strip() or "G.T.")
    st.session_state.rounds = []
    st.session_state.pending_insult = None


def reset_game():
    st.session_state.game = None
    st.session_state.rounds = []
    st.session_state.pending_insult = None


st.session_state.setdefault("game", None)
st.session_state.setdefault("rounds", [])
st.session_state.setdefault("pending_insult", None)

st.title("MI: Battles of the Northwest Wind")
st.caption("Insult the pirate, dodge their comebacks. First to 3 points wins.")

try:
    get_mistral_api_key()
except Exception:
    st.error(
        "No Mistral API key found. Set `MISTRAL_API_KEY` as an environment variable, "
        "or add it to `api_key.yaml` (see `api_key_template.yaml`).",
        icon=":material/vpn_key:",
    )
    st.stop()

game = st.session_state.game

if game is None:
    with st.form("start_form"):
        name = st.text_input("Your name", placeholder="G.T.")
        submitted = st.form_submit_button("Start battle", icon=":material/sailing:")
    if submitted:
        start_game(name)
        st.rerun()
    st.stop()

with st.container(key="battle_title"):
    st.subheader(f"{game.user.name} vs. {game.pirate.name}")

with st.sidebar:
    st.subheader("Score")
    st.metric(game.user.name, game.user.score)
    st.metric(game.pirate.name, game.pirate.score)

with st.chat_message("user", avatar=USER_AVATAR):
    st.write(f"My name is {game.user.name}. Prepare to die!")

for i, round_ in enumerate(st.session_state.rounds):
    thrower_role = "assistant" if round_.thrower == "pirate" else "user"
    answerer_role = "assistant" if round_.answerer == "pirate" else "user"
    thrower_avatar = PIRATE_AVATAR if round_.thrower == "pirate" else USER_AVATAR
    answerer_avatar = PIRATE_AVATAR if round_.answerer == "pirate" else USER_AVATAR

    with st.chat_message(thrower_role, avatar=thrower_avatar):
        st.write(round_.insult)
    with st.chat_message(answerer_role, avatar=answerer_avatar):
        st.write(round_.answer)

    winner_name = game.user.name if round_.round_winner == "user" else game.pirate.name
    with st.container(key=f"point_caption_history_{i}"):
        st.caption(f":material/swords: Point to {winner_name}")

if game.winner:
    if game.winner == "user":
        st.success(f"Congratulations, {game.user.name}! You won!", icon=":material/celebration:")
    else:
        st.error(f"{game.pirate.name} wins! Try again.", icon=":material/skull:")
    if st.button("Play again", icon=":material/refresh:"):
        reset_game()
        st.rerun()
    st.stop()

if game.user_turn:
    prompt = st.chat_input("Throw an insult!")
    if prompt:
        with st.chat_message("user", avatar=USER_AVATAR):
            st.write(prompt)
        with st.spinner(f"{game.pirate.name} is thinking of a comeback..."):
            result = game.resolve_user_turn(prompt)
        with st.chat_message("assistant", avatar=PIRATE_AVATAR):
            st.write(result.answer)
        show_clash_animation()
        winner_name = game.user.name if result.round_winner == "user" else game.pirate.name
        with st.container(key="point_caption_user"):
            st.caption(f":material/swords: Point to {winner_name}")
        st.session_state.rounds.append(result)
        st.rerun()
else:
    if st.session_state.pending_insult is None:
        with st.spinner(f"{game.pirate.name} is thinking of an insult..."):
            st.session_state.pending_insult = game.throw_pirate_insult()

    with st.chat_message("assistant", avatar=PIRATE_AVATAR):
        st.write(st.session_state.pending_insult.insult)

    prompt = st.chat_input("Write your comeback!")
    if prompt:
        with st.chat_message("user", avatar=USER_AVATAR):
            st.write(prompt)
        show_clash_animation()
        with st.spinner("Judging your comeback..."):
            result = game.resolve_pirate_turn(st.session_state.pending_insult, prompt)
        winner_name = game.user.name if result.round_winner == "user" else game.pirate.name
        with st.container(key="point_caption_pirate"):
            st.caption(f":material/swords: Point to {winner_name}")
        st.session_state.rounds.append(result)
        st.session_state.pending_insult = None
        st.rerun()
