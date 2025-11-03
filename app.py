# app.py — Chakra Insight (Bayesian 20Q) + PDF + Logo + Crystal Links + Birth Hint + Summary + Fixes
import streamlit as st
import math, io, random, datetime
from typing import Dict, List

st.set_page_config(page_title="Chakra Insight – 20Q-style", page_icon="🔮", layout="wide")

# -----------------------------
# Branding
# -----------------------------
LOGO_URL = "https://ik.imagekit.io/86edsgbur/Untitled%20design%20(73)%20(3)%20(1).jpg?updatedAt=1759258123716"

CHAKRA_COLORS = {
    "Root (Muladhara)": "#E53935",
    "Sacral (Svadhisthana)": "#FB8C00",
    "Solar Plexus (Manipura)": "#FBC02D",
    "Heart (Anahata)": "#43A047",
    "Throat (Vishuddha)": "#1E88E5",
    "Third Eye (Ajna)": "#5E35B1",
    "Crown (Sahasrara)": "#8E24AA",
}
CHAKRA_COLOR_NAMES = {
    "Root (Muladhara)": "Red",
    "Sacral (Svadhisthana)": "Orange",
    "Solar Plexus (Manipura)": "Yellow",
    "Heart (Anahata)": "Green",
    "Throat (Vishuddha)": "Blue",
    "Third Eye (Ajna)": "Indigo",
    "Crown (Sahasrara)": "Violet",
}

# -----------------------------
# Knowledge Base
# -----------------------------
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

LIKELIHOODS: Dict[str, Dict[str, float]] = {
    "Root (Muladhara)": {
        "safety_finance": 0.9, "body_pain_legs": 0.8, "guilt_shame": 0.2, "creativity_flow": 0.3,
        "control_perfection": 0.4, "digestive_issue": 0.3, "heart_walls": 0.3, "grief_breathe": 0.2,
        "people_pleasing": 0.4, "throat_tension": 0.3, "self_doubt": 0.5, "sleep_dreams": 0.4,
        "disconnected_spirit": 0.4, "head_pressure": 0.3,
    },
    "Sacral (Svadhisthana)": {
        "safety_finance": 0.4, "body_pain_legs": 0.3, "guilt_shame": 0.8, "creativity_flow": 0.8,
        "control_perfection": 0.3, "digestive_issue": 0.4, "heart_walls": 0.4, "grief_breathe": 0.3,
        "people_pleasing": 0.5, "throat_tension": 0.3, "self_doubt": 0.5, "sleep_dreams": 0.5,
        "disconnected_spirit": 0.4, "head_pressure": 0.3,
    },
    "Solar Plexus (Manipura)": {
        "safety_finance": 0.5, "body_pain_legs": 0.3, "guilt_shame": 0.4, "creativity_flow": 0.4,
        "control_perfection": 0.85, "digestive_issue": 0.8, "heart_walls": 0.5, "grief_breathe": 0.4,
        "people_pleasing": 0.7, "throat_tension": 0.4, "self_doubt": 0.6, "sleep_dreams": 0.5,
        "disconnected_spirit": 0.4, "head_pressure": 0.4,
    },
    "Heart (Anahata)": {
        "safety_finance": 0.4, "body_pain_legs": 0.3, "guilt_shame": 0.5, "creativity_flow": 0.5,
        "control_perfection": 0.4, "digestive_issue": 0.4, "heart_walls": 0.85, "grief_breathe": 0.8,
        "people_pleasing": 0.7, "throat_tension": 0.4, "self_doubt": 0.6, "sleep_dreams": 0.5,
        "disconnected_spirit": 0.5, "head_pressure": 0.4,
    },
    "Throat (Vishuddha)": {
        "safety_finance": 0.4, "body_pain_legs": 0.3, "guilt_shame": 0.6, "creativity_flow": 0.5,
        "control_perfection": 0.5, "digestive_issue": 0.3, "heart_walls": 0.5, "grief_breathe": 0.5,
        "people_pleasing": 0.85, "throat_tension": 0.85, "self_doubt": 0.6, "sleep_dreams": 0.5,
        "disconnected_spirit": 0.5, "head_pressure": 0.4,
    },
    "Third Eye (Ajna)": {
        "safety_finance": 0.4, "body_pain_legs": 0.3, "guilt_shame": 0.5, "creativity_flow": 0.6,
        "control_perfection": 0.5, "digestive_issue": 0.3, "heart_walls": 0.4, "grief_breathe": 0.4,
        "people_pleasing": 0.5, "throat_tension": 0.4, "self_doubt": 0.85, "sleep_dreams": 0.7,
        "disconnected_spirit": 0.7, "head_pressure": 0.5,
    },
    "Crown (Sahasrara)": {
        "safety_finance": 0.4, "body_pain_legs": 0.3, "guilt_shame": 0.5, "creativity_flow": 0.5,
        "control_perfection": 0.4, "digestive_issue": 0.3, "heart_walls": 0.4, "grief_breathe": 0.4,
        "people_pleasing": 0.4, "throat_tension": 0.3, "self_doubt": 0.6, "sleep_dreams": 0.6,
        "disconnected_spirit": 0.85, "head_pressure": 0.7,
    },
}

REMEDIES: Dict[str, Dict[str, str]] = {
    "Root (Muladhara)": {
        "why": "Safety, survival, and belonging themes dominate. Body seeks ground and routine.",
        "do": "Grounding walk barefoot, money-clarity ritual, red foods, LAM x108, EFT on fear.",
        "crystal": "Red Jasper / Hematite",
        "affirm": "I am safe. I am supported. I belong.",
        "ritual": "Morning: 5-min box-breath (4-4-4-4), 10-min barefoot walk; Night: 3 safety wins + Ho’oponopono for 'money/safety'.",
        "journal": "What makes my body feel safe? One tiny action I can take today.",
        "food": "Root vegetables, proteins, warm soups.",
        "oil": "Vetiver / Patchouli",
        "mudra": "Prithvi Mudra (ring finger + thumb)",
        "link": "https://myaurabliss.com/product/sulemani-hakik-stone-bracelet-stone-bracelet-for-men-and-women/",
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
        "mudra": "Varun Mudra (little finger + thumb)",
        "link": "https://myaurabliss.com/product/reiki-crystal-carnelian-bracelet-reiki-healing-crystal-stone/",
    },
    "Solar Plexus (Manipura)": {
        "why": "Control and self-judgment exhaust personal power.",
        "do": "Breath of fire, core strengthening, yellow foods, RAM x108, release perfection journaling.",
        "crystal": "Citrine / Tiger’s Eye",
        "affirm": "My power is kind and steady.",
        "ritual": "Morning: 3×(30s) Breath of Fire → 1-min plank; Midday: finish ONE priority; Night: note 3 ways you used kind power; burn one perfection thought.",
        "journal": "If I wasn’t trying to be perfect, I would… What tiny brave act can I do in 2 minutes?",
        "food": "Ginger tea, turmeric, yellow dals/grains.",
        "oil": "Lemon / Rosemary",
        "mudra": "Rudra Mudra (index + ring + thumb)",
        "link": "https://myaurabliss.com/product/natural-citrine-bracelet/",
    },
    "Heart (Anahata)": {
        "why": "Unprocessed grief and guardedness limit love circulation.",
        "do": "Heart-coherent breathing, green foods, YAM x108, loving-kindness practice, forgiveness letters.",
        "crystal": "Rose Quartz / Green Aventurine",
        "affirm": "My heart is open and safe.",
        "ritual": "Inhale 5s / exhale 5s at heart; send kindness to self→one person; self-hug 60s.",
        "journal": "Where am I holding a wall? What boundary would keep love flowing?",
        "food": "Leafy greens, mindful cacao.",
        "oil": "Rose / Geranium",
        "mudra": "Hridaya Mudra",
        "link": "https://myaurabliss.com/product/natural-green-aventurine-unisex-stone-bracelet/",
    },
    "Throat (Vishuddha)": {
        "why": "People-pleasing and fear of judgment compress expression.",
        "do": "Humming/chanting, boundary scripts, journaling truths, HAM x108, sky-gazing.",
        "crystal": "Blue Lace Agate / Aquamarine / Turquoise",
        "affirm": "I speak my truth with love.",
        "ritual": "1 min humming; speak one clear request today; write 3 lines: 'What I really want to say is…'",
        "journal": "Where did I betray my voice? What is one loving 'no'?",
        "food": "Warm water with honey/ginger.",
        "oil": "Peppermint / Eucalyptus",
        "mudra": "Granthi Mudra",
        "link": "https://myaurabliss.com/product/turquoise-firoza-beads-bracelet/",
    },
    "Third Eye (Ajna)": {
        "why": "Overthinking clouds intuition and imagery.",
        "do": "Trataka (candle-gazing), screen detox, AM x108, dream journal, intuition walks.",
        "crystal": "Amethyst / Lapis Lazuli",
        "affirm": "I trust my inner guidance.",
        "ritual": "2 minutes candle-gaze; ask one question before walk; note the first symbol/color you notice.",
        "journal": "What did my body whisper today?",
        "food": "Blueberries, purple foods.",
        "oil": "Frankincense / Clary Sage",
        "mudra": "Kalesvara Mudra",
        "link": "https://myaurabliss.com/product/unlocking-the-power-of-lapis-lazuli-experience-benefits-of-wearing-a-lapis-bracelet/",
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
        "mudra": "Sahasrara Mudra (open palms up)",
        "link": "https://myaurabliss.com/product/selenite-bracelet/",
    },
}

# -----------------------------
# Utilities
# -----------------------------
def normalize(probs: Dict[str, float]) -> Dict[str, float]:
    total = sum(probs.values())
    if total == 0:
        return {k: 1.0/len(probs) for k in probs}
    return {k: v/total for k, v in probs.items()}

def entropy(probs: Dict[str, float]) -> float:
    return -sum(p * math.log2(p) for p in probs.values() if p > 0)

def expected_information_gain(current: Dict[str, float], qid: str) -> float:
    ans_ps = {
        "yes": sum(current[c] * LIKELIHOODS[c][qid] for c in current),
        "no": sum(current[c] * (1 - LIKELIHOODS[c][qid]) for c in current),
        "unknown": 0.05,
    }
    base_H = entropy(current)
    eg = 0.0
    for a, pa in ans_ps.items():
        if pa <= 0:
            continue
        post = {}
        for c in current:
            like = LIKELIHOODS[c][qid] if a == "yes" else (1 - LIKELIHOODS[c][qid] if a == "no" else 0.5)
            post[c] = current[c] * like
        post = normalize(post)
        eg += pa * (base_H - entropy(post))
    return eg

def choose_next_question(asked_ids: set, posterior: Dict[str, float]) -> Dict:
    candidates = [q for q in QUESTIONS if q["id"] not in asked_ids]
    if not candidates:
        return None
    return max(candidates, key=lambda q: expected_information_gain(posterior, q["id"]))

def update_posterior(posterior: Dict[str, float], qid: str, answer: str) -> Dict[str, float]:
    updated = {}
    for c in posterior:
        like = {"Yes": LIKELIHOODS[c][qid], "No": 1 - LIKELIHOODS[c][qid]}.get(answer, 0.5)
        updated[c] = posterior[c] * like
    return normalize(updated)

def chakra_from_birth(dob: datetime.date | None) -> str | None:
    if not dob:
        return None
    idx = ((dob.day + dob.month) % 7) or 7
    return CHAKRAS[idx - 1]

def make_summary(name: str, birth_chakra: str | None, winner: str, ordered: List):
    # ordered = list of (chakra, prob) sorted desc
    top2 = ordered[1][0] if len(ordered) > 1 else None
    lines = []
    who = name or "Dear Soul"
    if birth_chakra:
        lines.append(f"{who}, your birth energy gently leans toward **{birth_chakra}**.")
    lines.append(
        f"Today’s answers highlight **{winner}** as the primary chakra to balance, "
        f"with {top2} offering a supportive theme." if top2 else
        f"Today’s answers highlight **{winner}** as the primary chakra to balance."
    )
    lines.append(
        f"Your power color for the day is **{CHAKRA_COLOR_NAMES[winner]}** — keep it close (clothes, journal, or a tiny swatch)."
    )
    lines.append(
        f"Crystal allies: **{REMEDIES[winner]['crystal']}**. Affirm: _{REMEDIES[winner]['affirm']}_"
    )
    lines.append(
        "Tiny plan: 7 minutes of practice → 3 minutes breath, 2 minutes movement, 2 minutes journaling."
    )
    return " ".join(lines)

# -----------------------------
# State
# -----------------------------
if "posterior" not in st.session_state:
    st.session_state.posterior = normalize({c: 1.0 for c in CHAKRAS})
if "asked" not in st.session_state:
    st.session_state.asked = []
if "answers" not in st.session_state:
    st.session_state.answers = {}

# -----------------------------
# Header + User Details
# -----------------------------
left, right = st.columns([0.35, 0.65])
with left:
    st.image(LOGO_URL, width=220)
with right:
    st.markdown("# 🔮 Chakra Insight – Interactive Predictor")
    st.markdown("Answer a few quick questions. We update probabilities live and infer your **primary chakra to balance**.")

st.markdown("### 🌸 Enter Your Details")
name = st.text_input("Full Name")
email = st.text_input("Email Address")
phone = st.text_input("Phone Number")
today = datetime.date.today()
dob = st.date_input("Birth Date", value=None, min_value=datetime.date(1900, 1, 1), max_value=today)

birth_chakra = chakra_from_birth(dob)
if birth_chakra:
    bc = REMEDIES[birth_chakra]
    st.success(
        f"🌙 As per your birth vibration, your guiding chakra is **{birth_chakra}**. "
        f"Crystal: {bc['crystal']} • Affirmation: _{bc['affirm']}_"
    )

posterior = st.session_state.posterior
asked_ids = set(st.session_state.asked)
stop_threshold = 0.88

# Prob bars
st.subheader("Current Probabilities")
for c_name, p in posterior.items():
    pct = f"{p*100:.1f}%"
    bar = f"<div style='background:{CHAKRA_COLORS[c_name]};height:16px;width:{p*100}%;border-radius:8px'></div>"
    st.markdown(f"**{c_name}** — {pct}")
    st.markdown(bar, unsafe_allow_html=True)
    st.markdown("")

# Decide whether to stop
winner = max(posterior, key=posterior.get)
conf = posterior[winner]

if conf >= stop_threshold or len(asked_ids) >= len(QUESTIONS):
    st.success(f"Top Insight: **{winner}** (confidence {conf:.2%})")
    ordered = sorted(posterior.items(), key=lambda kv: kv[1], reverse=True)

    # Soulful Summary (astro-style narrative)
    summary_text = make_summary(name or "Dear Soul", birth_chakra, winner, ordered)
    st.markdown("### ✨ Soulful Summary")
    st.write(summary_text)

    # Guidance block
    data = REMEDIES[winner]
    with st.expander("Personalized Guidance (Why / What to do / Crystal / Affirmation)", expanded=True):
        st.markdown(f"**Why now:** {data['why']}")
        st.markdown(f"**Do this next:** {data['do']}")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"**Crystal support:** {data['crystal']}")
            st.markdown(f"**Shop:** {data['link']}")
            st.markdown(f"**Mudra:** {data['mudra']}")
            st.markdown(f"**Essential oil:** {data['oil']}")
        with c2:
            st.markdown(f"**Affirmation:** _{data['affirm']}_")
            st.markdown(f"**Food focus:** {data['food']}")
            st.markdown(f"**Journal prompt:** {data['journal']}")
        st.markdown(f"**Mini-ritual:** {data['ritual']}")

    # Surprise Insight (with color name + swatch)
    seed = hash(str(st.session_state.answers)) % (10**8)
    rnd = random.Random(seed)
    color_name = CHAKRA_COLOR_NAMES[winner]
    color_hex = CHAKRA_COLORS[winner]
    swatch = f"<span style='background:{color_hex};display:inline-block;width:14px;height:14px;border-radius:3px;margin:0 6px -2px 6px'></span>"
    surprise_bits = [
        f"Bīja mantra cadence today: **{('LAM','VAM','RAM','YAM','HAM','OM','OM')[CHAKRAS.index(winner)]}** — slow 6×18.",
        f"Best 7-minute window: **{rnd.choice(['morning light','noon sun','sunset glow','pre-sleep quiet'])}**.",
        f"Power color: **{color_name}** {swatch} (use it on your body or desk).",
        f"Kind challenge: **{rnd.choice(['send a gratitude text','drink warm water hourly','walk barefoot 3 minutes','set one loving boundary'])}**.",
    ]
    st.info("\n".join(["**Surprise Insight**:"] + [f"• {s}" for s in surprise_bits]), icon="✨")

    # Overview
    st.markdown("---")
    st.subheader("All Chakras – Colored Overview")
    for c_name, p in ordered:
        pct = f"{p*100:.1f}%"
        chip = f"<span style='background:{CHAKRA_COLORS[c_name]};padding:4px 10px;border-radius:999px;color:white'>{CHAKRA_COLOR_NAMES[c_name]} • {c_name}</span>"
        st.markdown(f"{chip} — **{pct}**", unsafe_allow_html=True)
        st.caption(
            f"Why: {REMEDIES[c_name]['why']}  |  Affirmation: {REMEDIES[c_name]['affirm']}  |  "
            f"Crystals: {REMEDIES[c_name]['crystal']}  |  Shop: {REMEDIES[c_name]['link']}"
        )

    # -------- PDF Report (with proper wrapping + margins) --------
    from reportlab.pdfgen import canvas as pdfcanvas
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors as rlcolors
    from reportlab.lib.utils import ImageReader
    from reportlab.platypus import Paragraph, Frame, KeepInFrame
    from reportlab.lib.styles import getSampleStyleSheet

    def pdf_color(hexcol):
        r = int(hexcol[1:3],16)/255; g = int(hexcol[3:5],16)/255; b = int(hexcol[5:7],16)/255
        return rlcolors.Color(r,g,b)

    def generate_pdf(buf: io.BytesIO):
        W, H = A4
        MLEFT, MRIGHT, MTOP, MBOT = 40, 40, 40, 40
        c = pdfcanvas.Canvas(buf, pagesize=A4)

        # Header
        try:
            img = ImageReader(LOGO_URL)
            c.drawImage(img, MLEFT, H-MTOP-60, width=160, height=60, preserveAspectRatio=True, mask='auto')
        except Exception:
            pass
        c.setFont("Helvetica-Bold", 18); c.drawString(MLEFT+180, H-MTOP-10, "Chakra Insight Report")
        c.setFont("Helvetica", 10)
        c.drawString(MLEFT+180, H-MTOP-25, f"Top Insight: {winner} (confidence {conf:.0%})")
        c.drawString(MLEFT, H-MTOP-85, f"Name: {name or '-'}")
        c.drawString(MLEFT+180, H-MTOP-85, f"Email: {email or '-'}")
        c.drawString(MLEFT+360, H-MTOP-85, f"DOB: {dob if dob else '-'}")

        # Bars
        c.setFont("Helvetica-Bold", 12); c.drawString(MLEFT, H-MTOP-105, "Profile")
        y = H-MTOP-120
        for c_name, p in ordered:
            pct = int(p*100)
            c.setFont("Helvetica", 10); c.drawString(MLEFT, y+4, c_name)
            c.setFillColor(rlcolors.Color(0.92,0.92,0.92)); c.roundRect(MLEFT+160, y, 300, 12, 4, fill=True, stroke=0)
            c.setFillColor(pdf_color(CHAKRA_COLORS[c_name])); c.roundRect(MLEFT+160, y, 3*pct, 12, 4, fill=True, stroke=0)
            c.setFillColor(rlcolors.black); c.drawRightString(MLEFT+470, y+4, f"{pct}%")
            y -= 18

        # Soulful Summary
        style = getSampleStyleSheet()['BodyText']; style.fontName = 'Helvetica'; style.leading = 13
        c.setFont("Helvetica-Bold", 12); c.drawString(MLEFT, y-10, "Soulful Summary")
        y -= 26
        def draw_paragraph(text, y, height=80):
            p = Paragraph(text.replace("\n"," "), style)
            frame = Frame(MLEFT, y-height, W-MLEFT-MRIGHT, height, showBoundary=0)
            req_h = p.wrap(W-MLEFT-MRIGHT, height)[1]
            if y - req_h < MBOT + 40:
                c.showPage();  # new page header minimal
                return H-MTOP-40, p
            frame.addFromList([p], c)
            return y - max(24, req_h+6), None

        y, _ = draw_paragraph(summary_text, y, height=90)

        # Guidance (ordered labels, auto page-break)
        c.setFont("Helvetica-Bold", 12); c.drawString(MLEFT, y-10, "Personalized Guidance")
        y -= 26

        def draw_label_value(label, value, y, height=60):
            p = Paragraph(f"<b>{label}:</b> {value}", style)
            frame = Frame(MLEFT, y-height, W-MLEFT-MRIGHT, height, showBoundary=0)
            req_h = p.wrap(W-MLEFT-MRIGHT, height)[1]
            if y - req_h < MBOT + 40:
                c.showPage();  # start fresh section header on new page
                # (Re-draw section title on new page)
                c.setFont("Helvetica-Bold", 12); c.drawString(MLEFT, H-MTOP-40, "Personalized Guidance")
                _y = H-MTOP-60
                frame = Frame(MLEFT, _y-height, W-MLEFT-MRIGHT, height, showBoundary=0)
                frame.addFromList([p], c)
                return _y - max(24, req_h+6)
            frame.addFromList([p], c)
            return y - max(24, req_h+6)

        d = REMEDIES[winner]
        y = draw_label_value("Why now", d["why"], y, 60)
        y = draw_label_value("Do this next", d["do"], y, 60)
        y = draw_label_value("Crystal", f"{d['crystal']}  (Shop: {d['link']})", y, 40)
        y = draw_label_value("Affirmation", d["affirm"], y, 40)
        y = draw_label_value("Mudra", d["mudra"], y, 40)
        y = draw_label_value("Essential oil", d["oil"], y, 40)
        y = draw_label_value("Food focus", d["food"], y, 40)
        y = draw_label_value("Journal prompt", d["journal"], y, 40)
        y = draw_label_value("Mini-ritual", d["ritual"], y, 60)

        c.showPage(); c.save()

    st.markdown("---")
    pdf_buf = io.BytesIO()
    generate_pdf(pdf_buf)
    st.download_button(
        "📄 Download PDF Report",
        data=pdf_buf.getvalue(),
        file_name="chakra_insight_report.pdf",
        mime="application/pdf",
    )

    if st.button("🔁 Restart session", type="secondary"):
        st.session_state.posterior = normalize({c: 1.0 for c in CHAKRAS})
        st.session_state.asked = []
        st.session_state.answers = {}
        st.rerun()

else:
    next_q = choose_next_question(asked_ids, posterior)
    st.subheader("Question")
    st.markdown(f"**{len(asked_ids)+1}. {next_q['text']}**")
    colA, colB, colC = st.columns(3)
    chosen = None
    with colA:
        if st.button("Yes", use_container_width=True): chosen = "Yes"
    with colB:
        if st.button("No", use_container_width=True): chosen = "No"
    with colC:
        if st.button("Not sure", use_container_width=True): chosen = "Not sure"
    if chosen:
        st.session_state.asked.append(next_q["id"])
        st.session_state.answers[next_q["id"]] = chosen
        st.session_state.posterior = update_posterior(posterior, next_q["id"], chosen)
        st.rerun()

# Sidebar log
st.sidebar.header("Session Log")
if st.session_state.answers:
    for i, qid in enumerate(st.session_state.asked, 1):
        label = next(q["text"] for q in QUESTIONS if q["id"] == qid)
        st.sidebar.write(f"{i}. {label}\n- Answer: **{st.session_state.answers[qid]}**")
st.sidebar.markdown("---")
st.sidebar.markdown("**Tip:** You’ll get strong results with ~8–12 answers.")
