import streamlit as st

from src.game import Game
from src.utils import get_mistral_api_key

PIRATE_AVATAR = "🏴‍☠️"

st.set_page_config(page_title="MI: Battles of the Northwest Wind", page_icon="⚔️")


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
st.caption("Trade insults and comebacks with an LLM-powered pirate.")

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
        name = st.text_input("Your name", placeholder="Guybrush Threepwood")
        submitted = st.form_submit_button("Start battle", icon=":material/sailing:")
    if submitted:
        start_game(name)
        st.rerun()
    st.stop()

st.subheader(f"{game.user.name} vs. {game.pirate.name}")

score_col1, score_col2 = st.columns(2)
score_col1.metric(game.user.name, game.user.score)
score_col2.metric(game.pirate.name, game.pirate.score)

for round_ in st.session_state.rounds:
    thrower_role = "assistant" if round_.thrower == "pirate" else "user"
    answerer_role = "assistant" if round_.answerer == "pirate" else "user"
    thrower_avatar = PIRATE_AVATAR if round_.thrower == "pirate" else None
    answerer_avatar = PIRATE_AVATAR if round_.answerer == "pirate" else None

    with st.chat_message(thrower_role, avatar=thrower_avatar):
        st.write(round_.insult)
    with st.chat_message(answerer_role, avatar=answerer_avatar):
        st.write(round_.answer)

    winner_name = game.user.name if round_.round_winner == "user" else game.pirate.name
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
        with st.chat_message("user"):
            st.write(prompt)
        with st.spinner(f"{game.pirate.name} is thinking of a comeback..."):
            result = game.resolve_user_turn(prompt)
        with st.chat_message("assistant", avatar=PIRATE_AVATAR):
            st.write(result.answer)
        winner_name = game.user.name if result.round_winner == "user" else game.pirate.name
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
        with st.chat_message("user"):
            st.write(prompt)
        with st.spinner("Judging your comeback..."):
            result = game.resolve_pirate_turn(st.session_state.pending_insult, prompt)
        winner_name = game.user.name if result.round_winner == "user" else game.pirate.name
        st.caption(f":material/swords: Point to {winner_name}")
        st.session_state.rounds.append(result)
        st.session_state.pending_insult = None
        st.rerun()
