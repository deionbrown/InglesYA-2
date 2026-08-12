import asyncio
import hashlib
import io
import json
import re
import unicodedata
from pathlib import Path
from difflib import SequenceMatcher

import streamlit as st
import edge_tts
import speech_recognition as sr

from curriculum import LEVELS, LEVEL_LABELS, CURRICULUM, lesson
from lesson_content import lesson_pack, workbook_tasks_for
from grammar_helpers import TO_BE, DEMONSTRATIVES, TENSES, kind
from speaking_utils import score_transcript

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
AUDIO_CACHE = ROOT / "audio_cache"
AUDIO_CACHE.mkdir(exist_ok=True)
VOICE = "en-US-BrianNeural"

st.set_page_config(page_title="Inglés ¡YA!", page_icon="🇬🇧", layout="wide")

st.markdown("""
<style>
:root { --navy:#0E3769; --navy2:#174D82; --gold:#FFB719; --sky:#EAF5FB; --cream:#FFF8E9; --text:#0E315F; --muted:#66829A; }
[data-testid="stAppViewContainer"] { background: #f7fbfe; }
[data-testid="stSidebar"] { background: linear-gradient(180deg,#0E3769,#123f72); }
[data-testid="stSidebar"] * { color: white; }
.brand {font-size:2rem;font-weight:900;line-height:1.0;color:white;margin:0 0 .2rem}
.brand span {color:#FFB719;font-size:2.25rem}
.hero {background:white;border:1px solid #dbe9f2;border-radius:20px;padding:22px 24px;margin-bottom:14px;box-shadow:0 8px 28px rgba(14,55,105,.06)}
.lesson-title {font-size:2rem;font-weight:850;color:#0E315F;margin:0 0 5px}
.goal {color:#375f82;font-size:1rem}
.card {background:white;border:1px solid #dbe9f2;border-radius:16px;padding:16px 18px;margin:8px 0 12px;box-shadow:0 5px 18px rgba(14,55,105,.04)}
.en {font-size:1.05rem;font-weight:750;color:#0E315F}.es {font-size:.92rem;color:#66829A;margin-top:2px}
.badge {display:inline-block;background:#FFF0C3;color:#0E315F;border-radius:999px;padding:5px 10px;font-weight:700;font-size:.85rem;margin-right:6px}
.section-note {color:#66829A;margin-top:-8px;margin-bottom:12px}
.progress-box {background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.16);padding:14px;border-radius:14px;margin-top:16px}
div[data-testid="stTabs"] button {font-weight:700;}
.stButton > button {border-radius:10px;font-weight:750;}
</style>
""", unsafe_allow_html=True)


def init_state():
    st.session_state.setdefault("level", "A1")
    st.session_state.setdefault("unit", 1)
    st.session_state.setdefault("letter", "A")
    st.session_state.setdefault("progress", {})


def lesson_key(level, unit, letter):
    return f"{level}-{unit}{letter}"


def normalize_answer(text):
    text = str(text).strip().lower()
    text = unicodedata.normalize("NFD", text)
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    text = text.replace("’", "'").replace("‘", "'").replace("´", "'")
    text = re.sub(r"[^a-z0-9\s']", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def answer_alternatives(expected):
    raw = str(expected).strip()
    if not raw:
        return []
    if "respuesta abierta" in raw.lower():
        return ["__OPEN__"]
    parts = re.split(r"\s*(?:/|;|\bor\b|\bo\b|\|)\s*", raw, flags=re.I)
    ans = []
    for p in parts:
        p = p.strip(" .,:;()[]{}")
        if not p:
            continue
        for candidate in [p, re.sub(r"\s*\([^)]*\)\s*", "", p).strip()]:
            n = normalize_answer(candidate)
            if n and n not in ans:
                ans.append(n)
    return ans


def grade_answer(user, expected):
    alts = answer_alternatives(expected)
    if "__OPEN__" in alts:
        return "open", "Respuesta abierta: compárala con la guía y revisa que comunique la idea con claridad."
    u = normalize_answer(user)
    if not u:
        return "empty", "Escribe una respuesta antes de corregir."
    if any(u == a for a in alts):
        return "ok", "✅ Correcto."
    best = max((SequenceMatcher(None, u, a).ratio() for a in alts), default=0)
    if best >= .82:
        return "near", f"🟡 Muy cerca. Guía: {expected}"
    return "bad", f"❌ Revisa tu respuesta. Forma esperada: {expected}"


def audio_path(text, slow=False):
    key = hashlib.md5((VOICE + str(slow) + text).encode("utf-8")).hexdigest()
    return AUDIO_CACHE / f"{key}.mp3"


async def _make_audio(text, slow, path):
    rate = "-18%" if slow else "+0%"
    await edge_tts.Communicate(text=text, voice=VOICE, rate=rate).save(str(path))


def ensure_audio(text, slow=False):
    path = audio_path(text, slow)
    if path.exists() and path.stat().st_size > 0:
        return path
    try:
        asyncio.run(_make_audio(text, slow, path))
        return path if path.exists() else None
    except Exception:
        try:
            if path.exists(): path.unlink()
        except Exception:
            pass
        return None


def audio_player(text, slow=False, key=None):
    label = "🐢 Audio lento" if slow else "🔊 Audio normal"
    with st.expander(label, expanded=False):
        path = ensure_audio(text, slow)
        if path:
            st.audio(str(path), format="audio/mp3")
        else:
            st.warning("El audio no pudo generarse en este momento. Comprueba la conexión del servidor.")


def bilingual_card(en, es, audio=True, slow=False, key=""):
    st.markdown(f'<div class="card"><div class="en">{en}</div><div class="es">{es}</div></div>', unsafe_allow_html=True)
    if audio:
        audio_player(en, slow, key)


def render_sidebar():
    with st.sidebar:
        st.markdown('<div class="brand">Inglés<br><span>¡YA!</span></div>', unsafe_allow_html=True)
        level = st.selectbox("NIVEL", LEVELS, index=LEVELS.index(st.session_state.level))
        if level != st.session_state.level:
            st.session_state.level, st.session_state.unit, st.session_state.letter = level, 1, "A"
            st.rerun()
        unit = st.selectbox("UNIDAD", list(range(1, 11)), index=st.session_state.unit - 1)
        letter = st.radio("LECCIÓN", ["A", "B", "C", "D"], index="ABCD".index(st.session_state.letter), horizontal=True)
        st.session_state.unit, st.session_state.letter = unit, letter
        d = lesson(level, unit, letter)
        st.caption(f"{unit}{letter} · {d['title']}")
        done = sum(1 for v in st.session_state.progress.values() if v)
        total = len(LEVELS) * 40
        pct = round(done / total * 100) if total else 0
        st.markdown('<div class="progress-box">', unsafe_allow_html=True)
        st.markdown("**PROGRESO GENERAL**")
        st.progress(pct / 100)
        st.caption(f"{done} / {total} lecciones · {pct}%")
        st.markdown('</div>', unsafe_allow_html=True)


def lesson_navigation(level, unit, letter):
    idx = (unit - 1) * 4 + "ABCD".index(letter)
    c1, c2 = st.columns([1,1])
    with c1:
        if st.button("‹ Lección anterior", disabled=idx == 0, use_container_width=True):
            idx2 = idx - 1
            st.session_state.unit, st.session_state.letter = idx2 // 4 + 1, "ABCD"[idx2 % 4]
            st.rerun()
    with c2:
        if st.button("Lección siguiente ›", disabled=idx == 39, use_container_width=True, type="primary"):
            idx2 = idx + 1
            st.session_state.unit, st.session_state.letter = idx2 // 4 + 1, "ABCD"[idx2 % 4]
            st.rerun()


def render_vocabulary(pack):
    st.subheader("📚 Vocabulario")
    st.caption("Palabras y expresiones útiles de la lección.")
    for i, (en, es) in enumerate(pack["vocabulary"]):
        c1, c2 = st.columns([5,2])
        with c1:
            st.markdown(f'<div class="card"><div class="en">{en}</div><div class="es">{es}</div></div>', unsafe_allow_html=True)
        with c2:
            audio_player(en, False, f"v{i}")


def render_pronunciation(pack):
    st.subheader("🔊 Pronunciación")
    st.caption("Escucha cada frase primero lento y después a velocidad normal.")
    for i, (en, es) in enumerate(pack["examples"]):
        st.markdown(f'<div class="card"><div class="en">{en}</div><div class="es">{es}</div></div>', unsafe_allow_html=True)
        a,b = st.columns(2)
        with a: audio_player(en, True, f"ps{i}")
        with b: audio_player(en, False, f"pn{i}")


def render_grammar(d, pack):
    st.subheader("📖 Gramática")
    st.markdown(f'<span class="badge">Enfoque: {d["grammar"]}</span><span class="badge">Pronunciación: {d["pron"]}</span>', unsafe_allow_html=True)
    st.write("")
    st.info(f"En esta lección practicarás **{d['grammar']}** para poder: {d['goal']}")
    for en, es in pack["examples"]:
        bilingual_card(en, es, audio=False)


def render_dialogue(pack):
    st.subheader("💬 Diálogo")
    st.caption("Conversación completa. Inglés arriba y traducción debajo.")
    full = " ".join(en for speaker,en,es in pack["dialogue"])
    audio_player(full, True, "dialogue_full")
    for i,(speaker,en,es) in enumerate(pack["dialogue"]):
        st.markdown(f'<div class="card"><div class="en"><b>{speaker}:</b> {en}</div><div class="es">{es}</div></div>', unsafe_allow_html=True)
        audio_player(en, True, f"dlg{i}")


def render_reading(pack):
    st.subheader("📘 Lectura")
    st.caption("Lee el texto completo y utiliza la traducción como apoyo.")
    text = " ".join(en for en,es in pack["reading"])
    audio_player(text, True, "reading_full")
    for en,es in pack["reading"]:
        bilingual_card(en, es, audio=False)


def render_exercises(d):
    st.subheader("✏️ Ejercicios")
    qs = [f"Escribe una oración usando: {d['grammar']}.", f"Usa vocabulario relacionado con: {d['vocab']}.", f"Responde al objetivo: {d['goal']}"]
    for i,q in enumerate(qs,1):
        st.text_area(f"{i}. {q}", key=f"ex_{i}_{st.session_state.level}_{st.session_state.unit}_{st.session_state.letter}")


def render_speaking(pack):
    st.subheader("🎤 Práctica oral")
    st.caption("Escucha la frase, repítela y grábate. La web intentará reconocer tu inglés y compararlo con la frase objetivo.")
    for i,(en,es) in enumerate(pack["examples"]):
        st.markdown(f'<div class="card"><div class="en">{en}</div><div class="es">{es}</div></div>', unsafe_allow_html=True)
        a,b=st.columns(2)
        with a: audio_player(en, True, f"sp_s{i}")
        with b: audio_player(en, False, f"sp_n{i}")
        clip = st.audio_input("🎤 Graba tu respuesta", key=f"mic_{i}_{st.session_state.level}_{st.session_state.unit}_{st.session_state.letter}")
        if clip:
            try:
                recognizer = sr.Recognizer()
                with sr.AudioFile(io.BytesIO(clip.getvalue())) as source:
                    audio = recognizer.record(source)
                heard = recognizer.recognize_google(audio, language="en-US")
                score, missing = score_transcript(en, heard)
                if score >= 90: st.success(f"{score}% · Excelente. Entendido: {heard}")
                elif score >= 75: st.warning(f"{score}% · Bien. Entendido: {heard}")
                else: st.error(f"{score}% · Inténtalo otra vez. Entendido: {heard}")
                if missing: st.caption("Practica: " + ", ".join(missing[:6]))
            except Exception as ex:
                st.warning(f"No se pudo reconocer esta grabación. Puedes volver a intentarlo. ({type(ex).__name__})")


def render_evaluation(pack):
    st.subheader("🧠 Evaluación")
    st.caption("Responde primero y utiliza el corrector después.")
    for i,(q,expected) in enumerate(pack["evaluation"],1):
        keybase=f"eval_{st.session_state.level}_{st.session_state.unit}_{st.session_state.letter}_{i}"
        ans=st.text_input(f"{i}. {q}", key=keybase)
        c1,c2=st.columns([1,1])
        with c1:
            if st.button("✅ Corregir", key=keybase+"_check", use_container_width=True):
                status,msg=grade_answer(ans, expected)
                st.session_state[keybase+"_msg"]=(status,msg)
        with c2:
            with st.popover("📖 Ver guía", use_container_width=True): st.write(expected)
        if keybase+"_msg" in st.session_state:
            status,msg=st.session_state[keybase+"_msg"]
            {"ok":st.success,"near":st.warning,"bad":st.error,"empty":st.info,"open":st.info}.get(status,st.info)(msg)


def render_tasks(d):
    st.subheader("📒 Tareas")
    tasks = workbook_tasks_for(d["title"], st.session_state.level, d["goal"], d["grammar"])
    for ti,task in enumerate(tasks):
        with st.expander(task.get("title",f"Tarea {ti+1}"), expanded=ti==0):
            st.write(task.get("instruction",""))
            for j,item in enumerate(task.get("items",[])):
                prompt, expected = item[0], item[1]
                key=f"task_{st.session_state.level}_{st.session_state.unit}_{st.session_state.letter}_{ti}_{j}"
                ans=st.text_input(prompt, key=key)
                if st.button("Corregir respuesta", key=key+"_b"):
                    status,msg=grade_answer(ans, expected)
                    {"ok":st.success,"near":st.warning,"bad":st.error,"empty":st.info,"open":st.info}.get(status,st.info)(msg)
                with st.expander("Ver guía"):
                    st.write(expected)


init_state()
render_sidebar()
level, unit, letter = st.session_state.level, st.session_state.unit, st.session_state.letter
d = lesson(level, unit, letter)
pack = lesson_pack(d["title"], level, d["goal"], d["grammar"])

st.caption(f"{level} - {LEVEL_LABELS[level]}  ›  Unidad {unit}  ›  {unit}{letter} - {d['title']}")
st.markdown(f'<div class="hero"><div class="lesson-title">{unit}{letter} - {d["title"]}</div><div class="goal">🎯 <b>Objetivo:</b> {d["goal"]}</div></div>', unsafe_allow_html=True)
lesson_navigation(level,unit,letter)

names=["📚 Vocabulario","🔊 Pronunciación","📖 Gramática","💬 Diálogo","📘 Lectura","✏️ Ejercicios","🎤 Práctica oral","🧠 Evaluación","📒 Tareas"]
tabs=st.tabs(names)
with tabs[0]: render_vocabulary(pack)
with tabs[1]: render_pronunciation(pack)
with tabs[2]: render_grammar(d,pack)
with tabs[3]: render_dialogue(pack)
with tabs[4]: render_reading(pack)
with tabs[5]: render_exercises(d)
with tabs[6]: render_speaking(pack)
with tabs[7]: render_evaluation(pack)
with tabs[8]: render_tasks(d)

st.divider()
key=lesson_key(level,unit,letter)
completed=bool(st.session_state.progress.get(key))
if st.checkbox("✅ Marcar esta lección como completada", value=completed, key=f"done_{key}") != completed:
    st.session_state.progress[key]=not completed
    st.rerun()
