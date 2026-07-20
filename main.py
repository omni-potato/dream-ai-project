
import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(page_title="English Guardian", page_icon="🥚", layout="wide")

defaults = {

    "debug_mode": True,

    "page": "main",
    "name": "Potato",
    "level": 20,
    "personality": "Engineer",
    "dictionary_count": 30,
    "dictionary_total": 200,
    "rare_collection": 22,
    "last_feed_time": None,
    "recommended_phrasal_verb": "look into",
    "feed_message": "",
    "feed_history": [],
    "attribute_points": {
        "🔥 Fire": 22,
        "💧 Water": 1,
        "⚡ Light": 4,
        "🌳 Plant": 66,
        "⚙️ Metal": 10,
        "🌌 Universe": 1,
    },
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

def go_to(page):
    st.session_state.page = page
    st.rerun()

def feeding_status():
    if st.session_state.debug_mode:
        return True, "Debug Mode"

    last_feed = st.session_state.last_feed_time

    if last_feed is None:
        return True, "Ready to feed!"

    remaining = last_feed + timedelta(hours=6) - datetime.now()

    if remaining.total_seconds() <= 0:
        return True, "Ready to feed!"

    seconds = int(remaining.total_seconds())
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    return False, f"Waiting time {hours:02d}:{minutes:02d}:{seconds:02d}"

def main_screen():
    st.title("English Guardian")
    left, center, right = st.columns([1.05, 1.45, 1.05], gap="large")

    with left:
        st.subheader("Profile")
        st.write(f"**Name:** {st.session_state.name}")
        st.write(f"**Lv:** {st.session_state.level}")
        st.write(f"**Personality:** {st.session_state.personality}")
        st.divider()
        st.subheader("Attribute Points")
        st.toggle(
            "🐞 Debug Mode",
            key="debug_mode"
        )
        for attribute, points in st.session_state.attribute_points.items():
            st.write(f"**{attribute}**")
            st.progress(min(points / 100, 1.0), text=f"{points} points")

    with center:
        st.markdown(
            """
            <div style="text-align:center;padding:24px;border:1px solid rgba(128,128,128,.25);
            border-radius:20px;min-height:310px;display:flex;flex-direction:column;
            justify-content:center;">
                <div style="font-size:110px;">🥚</div>
                <h2 style="margin-bottom:0;">English Guardian</h2>
                <p style="opacity:.7;">Feed me English and help me grow.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        can_feed, waiting_text = feeding_status()
        st.caption(waiting_text)
        if st.button("🍖 Feed", use_container_width=True, type="primary", disabled=not can_feed):
            go_to("feed")

        a, b = st.columns(2)
        with a:
            if st.button("🏋️ Training", use_container_width=True):
                st.info("Training will be added later.")
        with b:
            if st.button("🏆 Award", use_container_width=True):
                st.info("Award will be added later.")

    with right:
        st.subheader("Collection")
        st.metric("Dictionary", f"{st.session_state.dictionary_count}/{st.session_state.dictionary_total}")
        st.metric("Rare Collection", st.session_state.rare_collection)
        st.divider()

        if st.button("📖 Dictionary", use_container_width=True):
            go_to("dictionary")

        if st.button("🧬 Character Collection", use_container_width=True):
            st.info("This screen will be added later.")

        if st.button("🕘 History", use_container_width=True):
            go_to("history")

def feed_screen():
    top_left, top_right = st.columns([5, 1])
    with top_left:
        st.title("Feed")
    with top_right:
        if st.button("← Main", use_container_width=True):
            go_to("main")

    recommended = st.session_state.recommended_phrasal_verb
    st.markdown(
        f"""
        <div style="padding:22px;margin:12px 0 24px;border:1px solid rgba(128,128,128,.25);
        border-radius:18px;">
            <div style="font-size:52px;">🥚</div>
            <h3 style="margin:4px 0;">I'm hungry...</h3>
            <p style="font-size:20px;">Can you use <b>{recommended}</b> today?</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    sentence = st.text_area(
        "Enter your writing",
        value=st.session_state.feed_message,
        placeholder="Example: I looked into the problem yesterday.",
        height=150,
        max_chars=300,
    )
    st.session_state.feed_message = sentence

    can_feed, waiting_text = feeding_status()
    if not can_feed:
        st.warning(waiting_text)

    if st.button("🍖 Feed", use_container_width=True, type="primary", disabled=not can_feed):
        cleaned = sentence.strip()
        if not cleaned:
            st.error("Please enter an English sentence.")
        elif recommended.lower() not in cleaned.lower():
            st.error(f'Please use "{recommended}" in your sentence.')
        else:
            st.session_state.last_feed_time = datetime.now()
            st.session_state.feed_history.append({
                "sentence": cleaned,
                "phrasal_verb": recommended,
                "fed_at": datetime.now().isoformat(timespec="seconds"),
            })
            st.session_state.attribute_points["🔥 Fire"] += 1
            st.session_state.feed_message = ""
            st.success("Yum! Your English Guardian enjoyed the sentence.")
            st.balloons()

def history_screen():
    top_left, top_right = st.columns([5, 1])

    with top_left:
        st.title("🕘 Feed History")

    with top_right:
        if st.button("← Main", use_container_width=True):
            go_to("main")

    st.divider()

    if not st.session_state.feed_history:
        st.info("No feeding history yet.")
        return

    for item in reversed(st.session_state.feed_history):

        with st.container(border=True):

            st.subheader(item["phrasal_verb"])

            st.caption(item["fed_at"])

            st.write(item["sentence"])

            st.markdown("**Corrected Sentence**")
            st.write("(AI correction will appear here.)")

            st.markdown("**Attribute**")
            st.write("🔥 Fire")

            st.markdown("**Maturity**")
            st.progress(0.25, text="★☆☆☆☆")

def dictionary_screen():
    top_left, top_right = st.columns([5, 1])

    with top_left:
        st.title("📖 Dictionary")

    with top_right:
        if st.button("← Main", use_container_width=True):
            go_to("main")

    st.divider()

    if not st.session_state.feed_history:
        st.info("No dictionary entries yet.")
        return

    counts = {}

    for item in st.session_state.feed_history:
        verb = item["phrasal_verb"]
        counts[verb] = counts.get(verb, 0) + 1

    sorted_items = sorted(
        counts.items(),
        key=lambda x: x[1],
        reverse=True
    )

    for verb, used in sorted_items:
        with st.container(border=True):
            st.subheader(verb)
            st.write(f"Used: {used}")

if st.session_state.page == "feed":
    feed_screen()

elif st.session_state.page == "history":
    history_screen()

elif st.session_state.page == "dictionary":
    dictionary_screen()

else:
    main_screen()