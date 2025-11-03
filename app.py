import streamlit as st
import math
from dataclasses import dataclass
from typing import Dict, List, Tuple

st.set_page_config(page_title="Chakra Insight – 20Q-style", page_icon="🔮", layout="wide")

# -----------------------------
# Knowledge Base
# -----------------------------
# Seven candidates (primary-blockage hypothesis). Each candidate is a chakra.
# For each question (attribute), we store P(answer="yes" | chakra).
# "prob" values are in [0,1]. "unknown" answers will do a mild update.

QUESTIONS: List[Dict] = [
    {"id": "safety_finance", "text": "Do you often worry about safety, stability, or finances?"},
    {"id": "body_pain_legs", "text": "Do you feel heaviness/pain in legs, knees, or lower back?"},
    {"id": "guilt_shame", "text": "Do you feel guilt or shame around pleasure or expression?"},
    {"id": "creativity_flow", "text": "Is your creativity/libido low or inconsistent?"},
    {"id": "control_perfection", "text": "Do you feel a strong need to control or perfectionism?"},
    {"id": "digestive_issue", "text": "Do you face frequent digestive/acidity issues?"},
    {"id": "heart_walls", "text": "Do you keep emotional walls or find it hard to forgive?"},
    {"id": "grief_breathe", "text": "Do you carry grief or experience shallow breathing?"},
    {"id": "people_pleasing", "text": "Do you fear judgment or struggle to speak needs clearly?"},
    {"id": "throat_tension", "text": "Do you feel throat tension or frequent sore throat?"},
    {"id": "self_doubt", "text": "Do you feel self-doubt or overthinking blocks your intuition?"},
    {"id": "sleep_dreams", "text": "Are sleep/dreams restless or hard to remember?"},
    {"id": "disconnected_spirit", "text": "Do you feel disconnected from purpose/Divine guidance?"},
    {"id": "head_pressure", "text": "Do you feel heavy head/crown pressure during stress?"},
]

CHAKRAS = [
    "Root (Muladhara)",
    "Sacral (Svadhisthana)",
    "Solar Plexus (Manipura)",
    "Heart (Anahata)",
    "Throat (Vishuddha)",
    "Third Eye (Ajna)",
    "Crown (Sahasrara)",
]

# Likelihood table: P(yes | chakra, question)
LIKELIHOODS: Dict[str, Dict[str, float]] = {
    "Root (Muladhara)": {
        "safety_finance": 0.9,
        "body_pain_legs": 0.8,
        "guilt_shame": 0.2,
        "creativity_flow": 0.3,
        "control_perfection": 0.4,
        "digestive_issue": 0.3,
        "heart_walls": 0.3,
        "grief_breathe": 0.2,
        "people_pleasing": 0.4,
        "throat_tension": 0.3,
        "self_doubt": 0.5,
        "sleep_dreams": 0.4,
        "disconnected_spirit": 0.4,
        "head_pressure": 0.3,
    },
    "Sacral (Svadhisthana)": {
        "safety_finance": 0.4,
        "body_pain_legs": 0.3,
        "guilt_shame": 0.8,
        "creativity_flow": 0.8,
        "control_perfection": 0.3,
        "digestive_issue": 0.4,
        "heart_walls": 0.4,
        "grief_breathe": 0.3,
        "people_pleasing": 0.5,
        "throat_tension": 0.3,
        "self_doubt": 0.5,
        "sleep_dreams": 0.5,
        "disconnected_spirit": 0.4,
        "head_pressure": 0.3,
    },
    "Solar Plexus (Manipura)": {
        "safety_finance": 0.5,
        "body_pain_legs": 0.3,
        "guilt_shame": 0.4,
        "creativity_flow": 0.4,
        "control_perfection": 0.85,
        "digestive_issue": 0.8,
        "heart_walls": 0.5,
        "grief_breathe": 0.4,
        "people_pleasing": 0.7,
        "throat_tension": 0.4,
        "self_doubt": 0.6,
        "sleep_dreams": 0.5,
        "disconnected_spirit": 0.4,
        "head_pressure": 0.4,
    },
    "Heart (Anahata)": {
        "safety_finance": 0.4,
        "body_pain_legs": 0.3,
        "guilt_shame": 0.5,
        "creativity_flow": 0.5,
        "control_perfection": 0.4,
        "digestive_issue": 0.4,
        "heart_walls": 0.85,
        "grief_breathe": 0.8,
        "people_pleasing": 0.7,
        "throat_tension": 0.4,
        "self_doubt": 0.6,
        "sleep_dreams": 0.5,
        "disconnected_spirit": 0.5,
        "head_pressure": 0.4,
    },
    "Throat (Vishuddha)": {
        "safety_finance": 0.4,
        "body_pain_legs": 0.3,
        "guilt_shame": 0.6,
        "creativity_flow": 0.5,
        "control_perfection": 0.5,
        "digestive_issue": 0.3,
        "heart_walls": 0.5,
        "grief_breathe": 0.5,
        "people_pleasing": 0.85,
        "throat_tension": 0.85,
        "self_doubt": 0.6,
        "sleep_dreams": 0.5,
        "disconnected_spirit": 0.5,
        "head_pressure": 0.4,
    },
    "Third Eye (Ajna)": {
        "safety_finance": 0.4,
        "body_pain_legs": 0.3,
        "guilt_shame": 0.5,
        "creativity_flow": 0.6,
        "control_perfection": 0.5,
        "digestive_issue": 0.3,
        "heart_walls": 0.4,
        "grief_breathe": 0.4,
        "people_pleasing": 0.5,
        "throat_tension": 0.4,
        "self_doubt": 0.85,
        "sleep_dreams": 0.7,
        "disconnected_spirit": 0.7,
        "head_pressure": 0.5,
    },
    "Crown (Sahasrara)": {
        "safety_finance": 0.4,
        "body_pain_legs": 0.3,
        "guilt_shame": 0.5,
        "creativity_flow": 0.5,
        "control_perfection": 0.4,
        "digestive_issue": 0.3,
        "heart_walls": 0.4,
        "grief_breathe": 0.4,
        "people_pleasing": 0.4,
        "throat_tension": 0.3,
        "self_doubt": 0.6,
        "sleep_dreams": 0.6,
        "disconnected_spirit": 0.85,
        "head_pressure": 0.7,
    },
}

REMEDIES: Dict[str, Dict[str, str]] = {
    "Root (Muladhara)": {
        "why": "Safety, survival, and belonging themes dominate. Body seeks ground and routine.",
        "do": "Grounding walk barefoot, money-clarity ritual, red foods, muladhara mantra LAM x108, EFT on fear.",
        "crystal": "Red Jasper / Hematite",
        "affirm": "I am safe. I am supported. I belong.",
    },
    "Sacral (Svadhisthana)": {
        "why": "Guilt/shame around pleasure/expressiveness blocks flow.",
        "do": "Hip-opening yoga, joyful movement/dance, orange foods, VAM x108, forgiveness/Ho’oponopono.",
        "crystal": "Carnelian / Moonstone",
        "affirm": "I allow myself to feel and create.",
    },
    "Solar Plexus (Manipura)": {
        "why": "Control and self-judgment exhaust personal power.",
        "do": "Breath of fire, core strengthening, yellow foods, RAM x108, release perfection journaling.",
        "crystal": "Citrine / Tiger’s Eye",
        "affirm": "My power is kind and steady.",
    },
    "Heart (Anahata)": {
        "why": "Unprocessed grief and guardedness limit love circulation.",
        "do": "Heart-coherent breathing, green foods, YAM x108, loving-kindness practice, forgiveness letters.",
        "crystal": "Rose Quartz / Green Aventurine",
        "affirm": "My heart is open and safe.",
    },
    "Throat (Vishuddha)": {
        "why": "People-pleasing and fear of judgment compress expression.",
        "do": "Humming/chanting, boundary scripts, journaling truths, HAM x108, sky-gazing.",
        "crystal": "Blue Lace Agate / Aquamarine",
        "affirm": "I speak my truth with love.",
    },
    "Third Eye (Ajna)": {
        "why": "Overthinking clouds intuition and imagery.",
        "do": "Trataka (candle-gazing), screen detox, AM x108, dream journal, intuition walks.",
        "crystal": "Amethyst / Lapis Lazuli",
        "affirm": "I trust my inner guidance.",
    },
    "Crown (Sahasrara)": {
        "why": "Spiritual disconnection and meaning-drift.",
        "do": "Morning silence, gratitude, OM x108, service act, white/light foods, nature time.",
        "crystal": "Clear Quartz / Selenite",
        "affirm": "I am one with Divine light.",
    },
}

# -----------------------------
# Utility functions
# -----------------------------

def normalize(probs: Dict[str, float]) -> Dict[str, float]:
    total = sum(probs.values())
    if total == 0:
        # fallback uniform
        return {k: 1.0/len(probs) for k in probs}
    return {k: v/total for k, v in probs.items()}


def entropy(probs: Dict[str, float]) -> float:
    return -sum(p * math.log2(p) for p in probs.values() if p > 0)


def expected_information_gain(current: Dict[str, float], qid: str) -> float:
    # possible answers: yes, no, maybe (unknown)
    ans_ps = {
        "yes": sum(current[c] * LIKELIHOODS[c][qid] for c in current),
        "no": sum(current[c] * (1 - LIKELIHOODS[c][qid]) for c in current),
        # Treat unknown as weak-noise around 0.5; approximate weight
        "unknown": 0.05,
    }
    base_H = entropy(current)

    eg = 0.0
    for a, pa in ans_ps.items():
        if pa <= 0:
            continue
        # posterior if answer a
        post = {}
        for c in current:
            if a == "yes":
                like = LIKELIHOODS[c][qid]
            elif a == "no":
                like = 1 - LIKELIHOODS[c][qid]
            else:
                like = 0.5  # unknown
            post[c] = current[c] * like
        post = normalize(post)
        eg += pa * (base_H - entropy(post))
    return eg


def choose_next_question(asked_ids: set, posterior: Dict[str, float]) -> Dict:
    candidates = [q for q in QUESTIONS if q["id"] not in asked_ids]
    if not candidates:
        return None
    best_q, best_gain = None, -1
    for q in candidates:
        gain = expected_information_gain(posterior, q["id"])
        if gain > best_gain:
            best_q, best_gain = q, gain
    return best_q


def update_posterior(posterior: Dict[str, float], qid: str, answer: str) -> Dict[str, float]:
    updated = {}
    for c in posterior:
        if answer == "Yes":
            like = LIKELIHOODS[c][qid]
        elif answer == "No":
            like = 1 - LIKELIHOODS[c][qid]
        else:  # "Not sure"
            like = 0.5
        updated[c] = posterior[c] * like
    return normalize(updated)

# -----------------------------
# UI State
# -----------------------------
if "posterior" not in st.session_state:
    st.session_state.posterior = normalize({c: 1.0 for c in CHAKRAS})
if "asked" not in st.session_state:
    st.session_state.asked = []
if "answers" not in st.session_state:
    st.session_state.answers = {}

# -----------------------------
# Header
# -----------------------------
left, right = st.columns([0.6, 0.4])
with left:
    st.markdown("""
    # 🔮 Chakra Insight – Interactive Predictor
    Answer a few quick questions. We update probabilities live (Bayesian 20Q style) and infer your **primary chakra to balance**.
    """)
with right:
    st.markdown("""
    **How it works**  
    • We maintain probabilities for each chakra.  
    • Each answer updates beliefs.  
    • We pick questions with highest information gain.
    """)

# -----------------------------
# Main flow
# -----------------------------
posterior = st.session_state.posterior
asked_ids = set(st.session_state.asked)

# Decide whether to stop (confidence threshold)
winner = max(posterior, key=posterior.get)
conf = posterior[winner]
stop_threshold = st.slider("Confidence threshold to show result", 0.5, 0.99, 0.88, 0.01)

# Show posterior bar chart
st.subheader("Current Probabilities")
st.bar_chart({"Probability": posterior})

if conf >= stop_threshold or len(asked_ids) >= len(QUESTIONS):
    st.success(f"Top Insight: **{winner}** (confidence {conf:.2%})")
    why = REMEDIES[winner]["why"]
    do = REMEDIES[winner]["do"]
    crystal = REMEDIES[winner]["crystal"]
    affirm = REMEDIES[winner]["affirm"]

    with st.expander("Personalized Guidance (Why / What to do / Crystal / Affirmation)", expanded=True):
        st.markdown(f"**Why now:** {why}")
        st.markdown(f"**Do this next:** {do}")
        cols = st.columns(2)
        with cols[0]:
            st.markdown(f"**Crystal support:** {crystal}")
        with cols[1]:
            st.markdown(f"**Affirmation:** _{affirm}_")

    st.markdown("---")
    st.caption("Restart if you want to re-answer.")
    if st.button("🔁 Restart session", type="secondary"):
        st.session_state.posterior = normalize({c: 1.0 for c in CHAKRAS})
        st.session_state.asked = []
        st.session_state.answers = {}
        st.experimental_rerun()
else:
    next_q = choose_next_question(asked_ids, posterior)
    if next_q is None:
        st.info("All questions answered. Adjust threshold or restart.")
    else:
        st.subheader("Question")
        st.markdown(f"**{len(asked_ids)+1}. {next_q['text']}**")
        colA, colB, colC = st.columns(3)
        chosen = None
        with colA:
            if st.button("Yes", use_container_width=True):
                chosen = "Yes"
        with colB:
            if st.button("No", use_container_width=True):
                chosen = "No"
        with colC:
            if st.button("Not sure", use_container_width=True):
                chosen = "Not sure"

        if chosen:
            st.session_state.asked.append(next_q["id"])
            st.session_state.answers[next_q["id"]] = chosen
            st.session_state.posterior = update_posterior(posterior, next_q["id"], chosen)
            st.experimental_rerun()

# -----------------------------
# Sidebar: Session Log & Export
# -----------------------------
st.sidebar.header("Session Log")
if st.session_state.answers:
    for i, qid in enumerate(st.session_state.asked, 1):
        label = next(q["text"] for q in QUESTIONS if q["id"] == qid)
        st.sidebar.write(f"{i}. {label}\n- Answer: **{st.session_state.answers[qid]}**")

st.sidebar.markdown("---")
st.sidebar.markdown("**Tips**: Use 8–12 answers for a strong signal. You can tune the threshold above.")

# -----------------------------
# Footer: How to deploy
# -----------------------------
with st.expander("Deployment Notes"):
    st.markdown(
        """
        **Run locally**
        ```bash
        pip install streamlit
        streamlit run app.py
        ```
        **Deploy on Streamlit Cloud**
        1) Push this `app.py` to a GitHub repo.
        2) On streamlit.io → Deploy app → point to `app.py`.
        3) Set app URL and share.

        **Customize**
        - Edit `QUESTIONS`, `LIKELIHOODS`, and `REMEDIES` to match your protocols.
        - Add more nuanced answers (e.g., Likert scale) by adjusting `update_posterior`.
        - For multi-chakra reports, convert posterior into a 7-bar profile PDF.
        """
    )
