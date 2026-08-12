
import streamlit as st
import json, os

st.set_page_config(page_title="Inglés ¡YA! — A1", page_icon="🌎", layout="wide")

PROGRESS_FILE = "progress.json"

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        try:
            return json.load(open(PROGRESS_FILE, "r", encoding="utf-8"))
        except:
            pass
    return {"completed": [], "xp": 0}

def save_progress(p):
    json.dump(p, open(PROGRESS_FILE, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

p = load_progress()

st.markdown("""
<style>
.block-container {max-width:1100px;padding-top:2rem}
.hero {padding:28px;border-radius:22px;background:linear-gradient(135deg,#0b3558,#146c94);color:white;margin-bottom:20px}
.card {border:1px solid #dfe6ec;border-radius:18px;padding:20px;margin:10px 0}
.small {opacity:.75}
div.stButton > button {border-radius:12px;min-height:46px;font-weight:700}
</style>
""", unsafe_allow_html=True)

sections = [
("Explore","🌎"),("Vocabulary","🔤"),("Grammar","🧩"),("Listening","🎧"),
("Pronunciation","🔊"),("Speaking","🗣️"),("Reading","📖"),
("Real English","💬"),("Writing","✍️"),("Review","🧠")
]

if "page" not in st.session_state:
    st.session_state.page = "Home"

def complete(name, xp=10):
    if name not in p["completed"]:
        p["completed"].append(name)
        p["xp"] += xp
        save_progress(p)
        st.success(f"Completed! +{xp} XP")

def nav():
    cols = st.columns(5)
    for i,(name,icon) in enumerate(sections):
        with cols[i%5]:
            if st.button(f"{icon} {name}", use_container_width=True):
                st.session_state.page=name
                st.rerun()

if st.session_state.page == "Home":
    done=len(p["completed"])
    percent=int(done/len(sections)*100)
    st.markdown(f"""
    <div class="hero">
    <h1>INGLÉS ¡YA! — A1</h1>
    <h2>Unit 1 · Meet People</h2>
    <p>Learn to introduce yourself, ask basic questions and meet people in English.</p>
    </div>
    """, unsafe_allow_html=True)
    c1,c2,c3=st.columns(3)
    c1.metric("Unit progress",f"{percent}%")
    c2.metric("XP",p["xp"])
    c3.metric("Lessons completed",f"{done}/10")
    st.progress(percent/100)
    st.subheader("Your learning path")
    nav()

else:
    if st.button("← Unit 1"):
        st.session_state.page="Home"; st.rerun()
    page=st.session_state.page
    st.title(dict((n,f"{i} {n}") for n,i in sections)[page])
    st.caption("Unit 1 · Meet People")

    if page=="Explore":
        st.subheader("People around the world")
        st.write("Imagine you arrive at an international event. You meet three new people. What information do people usually share when they meet?")
        st.multiselect("Choose:",["Name","Country","City","Job / studies","Bank password","Favorite color"])
        st.info("Goal: By the end of this unit, you can introduce yourself and ask another person basic questions.")
        if st.button("Complete Explore",use_container_width=True): complete(page)

    elif page=="Vocabulary":
        words=[
            ("name","/neɪm/","nombre"),("country","/ˈkʌntri/","país"),
            ("city","/ˈsɪti/","ciudad"),("student","/ˈstuːdənt/","estudiante"),
            ("teacher","/ˈtiːtʃər/","profesor/a"),("job","/dʒɑːb/","trabajo"),
            ("friend","/frend/","amigo/a"),("from","/frʌm/","de / desde")
        ]
        for w,ipa,es in words:
            st.markdown(f"### {w}  \n**{ipa}** · {es}")
        ans=st.radio("Which word means 'ciudad'?",["country","city","job"],index=None)
        if ans:
            st.success("Correct!" if ans=="city" else "Try again.")
        if st.button("Complete Vocabulary",use_container_width=True): complete(page)

    elif page=="Grammar":
        st.subheader("Verb BE")
        st.markdown("""
**I am** a student. → **I'm** a student.  
**You are** from Peru. → **You're** from Peru.  
**He is** a teacher. → **He's** a teacher.  
**She is** from Mexico. → **She's** from Mexico.

**Questions**  
What's your name?  
Where are you from?  
Are you a student?
""")
        a=st.selectbox("I ___ from Peru.",["Choose","am","is","are"])
        if a!="Choose": st.success("Correct!" if a=="am" else "Not yet — use 'am' with I.")
        if st.button("Complete Grammar",use_container_width=True): complete(page)

    elif page=="Listening":
        st.subheader("Listen for key information")
        st.info("Prototype transcript mode. Natural audio can be connected in the production version.")
        with st.expander("Play / reveal dialogue"):
            st.write("A: Hi! I'm Maya. What's your name?\n\nB: I'm Leo. Nice to meet you.\n\nA: Nice to meet you too. Where are you from?\n\nB: I'm from Peru, but I live in Madrid.")
        q=st.radio("Where is Leo from?",["Spain","Peru","Mexico"],index=None)
        if q: st.success("Correct!" if q=="Peru" else "Listen again.")
        if st.button("Complete Listening",use_container_width=True): complete(page)

    elif page=="Pronunciation":
        st.subheader("Contractions")
        st.markdown("**I am → I'm**  \n**You are → You're**  \n**What is → What's**  \n**She is → She's**")
        st.write("Say aloud: **Hi, I'm Alex. I'm from Lima. What's your name?**")
        if st.button("I practiced it",use_container_width=True): complete(page)

    elif page=="Speaking":
        st.subheader("Introduce yourself")
        name=st.text_input("Your name")
        country=st.text_input("Your country")
        city=st.text_input("Your city")
        role=st.text_input("Job / studies")
        if st.button("Build my introduction",use_container_width=True):
            st.success(f"Hi! I'm {name or '...'}. I'm from {country or '...'}. I live in {city or '...'}. I'm {role or '...'}. Nice to meet you!")
        if st.button("Complete Speaking",use_container_width=True): complete(page)

    elif page=="Reading":
        st.subheader("Three cities, three new friends")
        st.markdown("""
**Sofia** is 19. She's from Colombia and lives in Bogotá. She's a university student.  
**Kenji** is from Japan. He lives in Osaka and works in a hotel.  
**Emma** is 27. She's Canadian, but she lives in Lima. She's an English teacher.
""")
        q=st.radio("Who lives in Peru?",["Sofia","Kenji","Emma"],index=None)
        if q: st.success("Correct!" if q=="Emma" else "Read the profiles again.")
        if st.button("Complete Reading",use_container_width=True): complete(page)

    elif page=="Real English":
        st.subheader("Sound more natural")
        st.markdown("""
**Nice to meet you.** — Mucho gusto.  
**How about you?** — ¿Y tú?  
**Really?** — ¿En serio?  
**That's great!** — ¡Qué bien!  
**Me too.** — Yo también.
""")
        if st.button("Complete Real English",use_container_width=True): complete(page)

    elif page=="Writing":
        st.subheader("Write your profile")
        text=st.text_area("Write 4–5 sentences about yourself.",height=150,
                          placeholder="Hi! I'm ... I'm from ... I live in ...")
        if text and len(text.split())>=10:
            st.success("Good start! Your profile has enough information for this A1 task.")
        if st.button("Complete Writing",use_container_width=True): complete(page)

    elif page=="Review":
        st.subheader("Unit 1 Check")
        score=0
        q1=st.radio("1. I ___ a student.",["is","am","are"],index=None)
        q2=st.radio("2. She ___ from Brazil.",["am","are","is"],index=None)
        q3=st.radio("3. Best question for someone's country:",["How old are you?","Where are you from?","What's your job?"],index=None)
        if st.button("Check my score",use_container_width=True):
            score=(q1=="am")+(q2=="is")+(q3=="Where are you from?")
            st.metric("Score",f"{score}/3")
            if score==3:
                st.success("Excellent — Unit 1 review passed.")
                complete(page,20)
            else:
                st.warning("Review the unit and try again.")

    st.divider()
    nav()
