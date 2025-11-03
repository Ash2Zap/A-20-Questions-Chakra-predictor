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
        "why": "Safety, survival, and belonging themes dominate. Body seeks ground and routine.",
        "do": "Grounding walk barefoot, money-clarity ritual, red foods, LAM x108, EFT on fear.",
        "crystal": "Red Jasper / Hematite",
        "affirm": "I am safe. I am supported. I belong.",
        "ritual": "Morning: 5-minute box-breath (4-4-4-4), 10-minute barefoot walk; Evening: write 3 safety wins + Ho’oponopono for 'money/safety'.",
        "journal": "What makes my body feel safe? One tiny action I can take today.",
        "food": "Root vegetables, proteins, warm soups.",
        "oil": "Vetiver / Patchouli",
        "mudra": "Prithvi Mudra (ring finger + thumb).",
        "link": "https://myaurabliss.com/product/sulemani-hakik-stone-bracelet-stone-bracelet-for-men-and-women/"
    },
    "Sacral (Svadhisthana)": {
        "why": "Guilt/shame around pleasure/expressiveness blocks flow.",
        "do": "Hip-opening yoga, joyful movement/dance, orange foods, VAM x108, forgiveness/Ho’oponopono.",
        "crystal": "Carnelian / Moonstone",
        "affirm": "I allow myself to feel and create.",
        "ritual": "5 minutes pelvis circles + 60s laughter practice; create something small (voice note, doodle).",
        "journal": "Where do I withhold joy? What would playful look like today?",
        "food": "Orange fruits, healthy fats.",
        "oil": "Orange / Ylang-Ylang",
        "mudra": "Varun Mudra (little finger + thumb).",
        "link": "https://myaurabliss.com/product/reiki-crystal-carnelian-bracelet-reiki-healing-crystal-stone/"
    },
    "Solar Plexus (Manipura)": {
        "why": "Control and self-judgment exhaust personal power.",
        "do": "Breath of fire, core strengthening, yellow foods, RAM x108, release perfection journaling.",
        "crystal": "Citrine / Tiger’s Eye",
        "affirm": "My power is kind and steady.",
        "ritual": "Morning: 3 rounds Breath of Fire (30s each) → 1 minute plank; Midday: choose ONE priority and finish it; Night: write 3 ways you used kind power, burn one perfection thought.",
        "journal": "If I wasn’t trying to be perfect, I would… What tiny brave act can I do in 2 minutes?",
        "food": "Ginger tea, turmeric, yellow dals/grains.",
        "oil": "Lemon / Rosemary",
        "mudra": "Rudra Mudra (index + ring + thumb).",
        "link": "https://myaurabliss.com/product/natural-citrine-bracelet/"
    },
    "Heart (Anahata)": {
        "why": "Unprocessed grief and guardedness limit love circulation.",
        "do": "Heart-coherent breathing, green foods, YAM x108, loving-kindness practice, forgiveness letters.",
        "crystal": "Rose Quartz / Green Aventurine",
        "affirm": "My heart is open and safe.",
        "ritual": "Inhale 5s / exhale 5s focusing on heart; send kindness to self→close one; self-hug 60s.",
        "journal": "Where am I still holding a wall? What boundary would keep love flowing?",
        "food": "Leafy greens, cacao (mindful).",
        "oil": "Rose / Geranium",
        "mudra": "Hridaya Mudra.",
        "link": "https://myaurabliss.com/product/natural-green-aventurine-unisex-stone-bracelet/"
    },
    "Throat (Vishuddha)": {
        "why": "People-pleasing and fear of judgment compress expression.",
        "do": "Humming/chanting, boundary scripts, journaling truths, HAM x108, sky-gazing.",
        "crystal": "Blue Lace Agate / Aquamarine",
        "affirm": "I speak my truth with love.",
        "ritual": "1 minute humming; speak one clear request today; 3 lines 'What I really want to say is…'.",
        "journal": "Where did I betray my voice? What is one loving 'no'?",
        "food": "Warm water with honey/ginger.",
        "oil": "Peppermint / Eucalyptus",
        "mudra": "Granthi Mudra.",
        "link": "https://myaurabliss.com/product/turquoise-firoza-beads-bracelet/"
    },
    "Third Eye (Ajna)": {
        "why": "Overthinking clouds intuition and imagery.",
        "do": "Trataka (candle-gazing), screen detox, AM x108, dream journal, intuition walks.",
        "crystal": "Amethyst / Lapis Lazuli",
        "affirm": "I trust my inner guidance.",
        "ritual": "2 minutes candle-gaze; ask one question before walk; write the first symbol/color you notice.",
        "journal": "What did my body whisper today?",
        "food": "Blueberries, purple foods.",
        "oil": "Frankincense / Clary Sage",
        "mudra": "Kalesvara Mudra.",
        "link": "https://myaurabliss.com/product/unlocking-the-power-of-lapis-lazuli-experience-benefits-of-wearing-a-lapis-bracelet/"
    },
    "Crown (Sahasrara)": {
        "why": "Spiritual disconnection and meaning-drift.",
        "do": "Morning silence, gratitude, OM x108, service act, white/light foods, nature time.",
        "crystal": "Clear Quartz / Selenite",
        "affirm": "I am one with Divine light.",
        "ritual": "3 minutes stillness on waking; list 5 gratitudes; one tiny act of service.",
        "journal": "Where did grace touch my day?",
        "food": "Coconut water, sattvic simplicity.",
        "oil": "Lavender / Sandalwood",
        "mudra": "Sahasrara Mudra (open palms up).",
        "link": "https://myaurabliss.com/product/selenite-bracelet/"
    },
}

REMEDIES: Dict[str, Dict[str, str]] = {
    "Root (Muladhara)": {
        "why": "Safety, survival, and belonging themes dominate. Body seeks ground and routine.",
        "do": "Grounding walk barefoot, money-clarity ritual, red foods, LAM x108, EFT on fear.",
        "crystal": "Red Jasper / Hematite",
        "affirm": "I am safe. I am supported. I belong.",
        "ritual": "Morning: 5-minute box-breath (4-4-4-4), 10-minute barefoot walk; Evening: write 3 safety wins + Ho’oponopono for 'money/safety'.",
        "journal": "What makes my body feel safe? One tiny action I can take today.",
        "food": "Root vegetables, proteins, warm soups.",
        "oil": "Vetiver / Patchouli",
        "mudra": "Prithvi Mudra (ring finger + thumb)."
    },
    "Sacral (Svadhisthana)": {
        "why": "Guilt/shame around pleasure/expressiveness blocks flow.",
        "do": "Hip-opening yoga, joyful movement/dance, orange foods, VAM x108, forgiveness/Ho’oponopono.",
        "crystal": "Carnelian / Moonstone",
        "affirm": "I allow myself to feel and create.",
        "ritual": "5 minutes pelvis circles + 60s laughter practice; create something small (voice note, doodle).",
        "journal": "Where do I withhold joy? What would playful look like today?",
        "food": "Orange fruits, healthy fats.",
        "oil": "Orange / Ylang-Ylang",
        "mudra": "Varun Mudra (little finger + thumb)."
    },
    "Solar Plexus (Manipura)": {
        "why": "Control and self-judgment exhaust personal power.",
        "do": "Breath of fire, core strengthening, yellow foods, RAM x108, release perfection journaling.",
        "crystal": "Citrine / Tiger’s Eye",
        "affirm": "My power is kind and steady.",
        "ritual": "Morning: 3 rounds Breath of Fire (30s each) → 1 minute plank; Midday: choose ONE priority and finish it; Night: write 3 ways you used kind power, burn one perfection thought.",
        "journal": "If I wasn’t trying to be perfect, I would… What tiny brave act can I do in 2 minutes?",
        "food": "Ginger tea, turmeric, yellow dals/grains.",
        "oil": "Lemon / Rosemary",
        "mudra": "Rudra Mudra (index + ring + thumb)."
    },
    "Heart (Anahata)": {
        "why": "Unprocessed grief and guardedness limit love circulation.",
        "do": "Heart-coherent breathing, green foods, YAM x108, loving-kindness practice, forgiveness letters.",
        "crystal": "Rose Quartz / Green Aventurine",
        "affirm": "My heart is open and safe.",
        "ritual": "Inhale 5s / exhale 5s focusing on heart; send kindness to self→close one; self-hug 60s.",
        "journal": "Where am I still holding a wall? What boundary would keep love flowing?",
        "food": "Leafy greens, cacao (mindful).",
        "oil": "Rose / Geranium",
        "mudra": "Hridaya Mudra."
    },
    "Throat (Vishuddha)": {
        "why": "People-pleasing and fear of judgment compress expression.",
        "do": "Humming/chanting, boundary scripts, journaling truths, HAM x108, sky-gazing.",
        "crystal": "Blue Lace Agate / Aquamarine",
        "affirm": "I speak my truth with love.",
        "ritual": "1 minute humming; speak one clear request today; 3 lines 'What I really want to say is…'.",
        "journal": "Where did I betray my voice? What is one loving 'no'?",
        "food": "Warm water with honey/ginger.",
        "oil": "Peppermint / Eucalyptus",
        "mudra": "Granthi Mudra."
    },
    "Third Eye (Ajna)": {
        "why": "Overthinking clouds intuition and imagery.",
        "do": "Trataka (candle-gazing), screen detox, AM x108, dream journal, intuition walks.",
        "crystal": "Amethyst / Lapis Lazuli",
        "affirm": "I trust my inner guidance.",
        "ritual": "2 minutes candle-gaze; ask one question before walk; write the first symbol/color you notice.",
        "journal": "What did my body whisper today?",
        "food": "Blueberries, purple foods.",
        "oil": "Frankincense / Clary Sage",
        "mudra": "Kalesvara Mudra."
    },
    "Crown (Sahasrara)": {
        "why": "Spiritual disconnection and meaning-drift.",
        "do": "Morning silence, gratitude, OM x108, service act, white/light foods, nature time.",
        "crystal": "Clear Quartz / Selenite",
        "affirm": "I am one with Divine light.",
        "ritual": "3 minutes stillness on waking; list 5 gratitudes; one tiny act of service.",
        "journal": "Where did grace touch my day?",
        "food": "Coconut water, sattvic simplicity.",
        "oil": "Lavender / Sandalwood",
        "mudra": "Sahasrara Mudra (open palms up)."
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
stop_threshold = 0.88  # auto threshold; hidden from UI

# Show posterior bar chart
st.subheader("Current Probabilities")
# Colored chakra bars
CHAKRA_COLORS = {
    "Root (Muladhara)": "#E53935",
    "Sacral (Svadhisthana)": "#FB8C00",
    "Solar Plexus (Manipura)": "#FBC02D",
    "Heart (Anahata)": "#43A047",
    "Throat (Vishuddha)": "#1E88E5",
    "Third Eye (Ajna)": "#5E35B1",
    "Crown (Sahasrara)": "#8E24AA",
}
for name, p in posterior.items():
    pct = f"{p*100:.1f}%"
    bar = f"<div style='background:{CHAKRA_COLORS[name]};height:16px;width:{p*100}%;border-radius:8px'></div>"
    st.markdown(f"**{name}** — {pct}")
    st.markdown(bar, unsafe_allow_html=True)
    st.markdown("")

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
            st.markdown(f"**Mudra:** {REMEDIES[winner]['mudra']}")
            st.markdown(f"**Essential oil:** {REMEDIES[winner]['oil']}")
        with cols[1]:
            st.markdown(f"**Affirmation:** _{affirm}_")
            st.markdown(f"**Food focus:** {REMEDIES[winner]['food']}")
            st.markdown(f"**Journal prompt:** {REMEDIES[winner]['journal']}")
        st.markdown(f"**Mini-ritual:** {REMEDIES[winner]['ritual']}")

    # 🎁 Surprise Insight (seeded by your answers — repeatable)
    import random
    seed = hash(str(st.session_state.answers)) % (10**8)
    rnd = random.Random(seed)
    surprise_bits = [
        f"Bīja mantra cadence today: **{('LAM','VAM','RAM','YAM','HAM','OM','OM')[CHAKRAS.index(winner)]}** — slow 6×18.",
        f"Best 7-minute window: **{rnd.choice(['morning light','noon sun','sunset glow','pre-sleep quiet'])}**.",
        f"Power color: **{CHAKRA_COLORS[winner]}** — use it in clothes or a note on your desk.",
        f"Kind challenge: **{rnd.choice(['send a gratitude text','drink warm water hourly','walk barefoot 3 minutes','one loving boundary today'])}**.",
    ]
    st.info("
".join(["**Surprise Insight**:"] + [f"• {s}" for s in surprise_bits]))

    st.markdown("---")
    st.subheader("All Chakras – Colored Overview")
    ordered = sorted(posterior.items(), key=lambda kv: kv[1], reverse=True)
    for name, p in ordered:
        pct = f"{p*100:.1f}%";
        chip = f"<span style='background:{CHAKRA_COLORS[name]};padding:4px 10px;border-radius:999px;color:white'>{name}</span>"
        st.markdown(f"{chip} — **{pct}**", unsafe_allow_html=True)
        st.caption(f"Why: {REMEDIES[name]['why']}  |  Affirmation: {REMEDIES[name]['affirm']}")

    st.markdown("---")
    st.caption("Restart if you want to re-answer.")
    if st.button("🔁 Restart session", type="secondary"):
        st.session_state.posterior = normalize({c: 1.0 for c in CHAKRAS})
        st.session_state.asked = []
        st.session_state.answers = {}
        st.rerun()
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
            st.rerun()

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


