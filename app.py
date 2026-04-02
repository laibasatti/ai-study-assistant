import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="🎓",
    layout="centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* { margin: 0; padding: 0; box-sizing: border-box; }

.stApp {
    background: #000000;
    font-family: 'Inter', sans-serif;
}

h1 {
    font-family: 'Inter', sans-serif !important;
    font-weight: 700 !important;
    font-size: 3.5em !important;
    text-align: center !important;
    background: linear-gradient(135deg, #fff 0%, #a78bfa 40%, #38bdf8 70%, #fff 100%);
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    letter-spacing: -1px !important;
    margin-bottom: 8px !important;
}

.subtitle {
    text-align: center;
    color: rgba(255,255,255,0.45);
    font-size: 1.05em;
    margin-bottom: 10px;
}

.genz-msg {
    text-align: center;
    margin-top: 30px;
    margin-bottom: 20px;
}

.genz-msg p {
    color: rgba(255,255,255,0.3);
    font-size: 1em;
    margin-bottom: 8px;
}

.genz-msg span {
    display: inline-block;
    background: linear-gradient(135deg, #f472b6, #a78bfa, #38bdf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 600;
    font-size: 1.1em;
}

.user-bubble {
    display: flex;
    justify-content: flex-end;
    margin: 12px 0;
    animation: fadeSlideUp 0.4s ease;
}

.user-bubble-inner {
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    color: white;
    padding: 12px 18px;
    border-radius: 18px 18px 4px 18px;
    max-width: 75%;
    font-size: 0.95em;
    line-height: 1.5;
    box-shadow: 0 4px 20px rgba(99,102,241,0.3);
}

.ai-bubble {
    display: flex;
    justify-content: flex-start;
    margin: 12px 0;
    animation: fadeSlideUp 0.4s ease;
}

.ai-bubble-inner {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.1);
    color: rgba(255,255,255,0.9);
    padding: 12px 18px;
    border-radius: 18px 18px 18px 4px;
    max-width: 75%;
    font-size: 0.95em;
    line-height: 1.6;
}

.ai-label {
    font-size: 0.7em;
    color: rgba(255,255,255,0.3);
    margin-bottom: 4px;
    margin-left: 4px;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

.user-label {
    font-size: 0.7em;
    color: rgba(255,255,255,0.3);
    margin-bottom: 4px;
    margin-right: 4px;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    text-align: right;
}

@keyframes fadeSlideUp {
    from { opacity: 0; transform: translateY(15px); }
    to { opacity: 1; transform: translateY(0); }
}

.stTextInput input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 16px !important;
    color: white !important;
    padding: 16px 20px !important;
    font-size: 0.95em !important;
    font-family: 'Inter', sans-serif !important;
    transition: all 0.3s ease !important;
}

.stTextInput input:focus {
    border: 1px solid rgba(139,92,246,0.6) !important;
    box-shadow: 0 0 0 3px rgba(139,92,246,0.15) !important;
}

.stTextInput input::placeholder {
    color: rgba(255,255,255,0.25) !important;
}

.stButton:first-of-type button {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a78bfa 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 14px 28px !important;
    font-size: 0.95em !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    width: 100% !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 20px rgba(99,102,241,0.35) !important;
    white-space: nowrap !important;
}

.stButton:first-of-type button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(99,102,241,0.5) !important;
}

.stButton:last-of-type button {
    background: rgba(255,255,255,0.05) !important;
    color: rgba(255,255,255,0.5) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 14px !important;
    padding: 14px 10px !important;
    font-size: 0.85em !important;
    font-family: 'Inter', sans-serif !important;
    width: 100% !important;
    transition: all 0.3s ease !important;
    white-space: nowrap !important;
}

.stButton:last-of-type button:hover {
    background: rgba(255,80,80,0.1) !important;
    color: rgba(255,100,100,0.8) !important;
    border: 1px solid rgba(255,80,80,0.2) !important;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(139,92,246,0.4); border-radius: 10px; }

.empty-state {
    text-align: center;
    padding: 30px 20px;
    color: rgba(255,255,255,0.2);
    font-size: 0.95em;
}
</style>

<canvas id="bgCanvas" style="position:fixed;top:0;left:0;width:100%;height:100%;z-index:0;pointer-events:none;"></canvas>

<script>
const canvas = document.getElementById('bgCanvas');
const ctx = canvas.getContext('2d');
function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}
resize();
window.addEventListener('resize', resize);
const orbs = [
    { x: 0.2, y: 0.3, r: 300, color: '244,114,182', speed: 0.0003 },
    { x: 0.8, y: 0.7, r: 250, color: '139,92,246', speed: 0.0004 },
    { x: 0.5, y: 0.1, r: 200, color: '56,189,248', speed: 0.0005 },
    { x: 0.9, y: 0.4, r: 180, color: '167,139,250', speed: 0.0002 },
];
const particles = [];
for(let i = 0; i < 100; i++) {
    particles.push({
        x: Math.random() * window.innerWidth,
        y: Math.random() * window.innerHeight,
        r: Math.random() * 1.5 + 0.3,
        speedX: (Math.random() - 0.5) * 0.4,
        speedY: -Math.random() * 0.5 - 0.1,
        opacity: Math.random() * 0.5 + 0.1,
        pulse: Math.random() * Math.PI * 2
    });
}
let time = 0;
function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    orbs.forEach((orb, i) => {
        const x = orb.x * canvas.width + Math.sin(time * orb.speed * 1000 + i) * 100;
        const y = orb.y * canvas.height + Math.cos(time * orb.speed * 1000 + i) * 80;
        const gradient = ctx.createRadialGradient(x, y, 0, x, y, orb.r);
        gradient.addColorStop(0, `rgba(${orb.color}, 0.12)`);
        gradient.addColorStop(1, `rgba(${orb.color}, 0)`);
        ctx.beginPath();
        ctx.arc(x, y, orb.r, 0, Math.PI * 2);
        ctx.fillStyle = gradient;
        ctx.fill();
    });
    particles.forEach(p => {
        p.pulse += 0.02;
        p.x += p.speedX;
        p.y += p.speedY;
        if(p.y < -5) { p.y = canvas.height + 5; p.x = Math.random() * canvas.width; }
        if(p.x < -5) p.x = canvas.width + 5;
        if(p.x > canvas.width + 5) p.x = -5;
        const opacity = p.opacity * (0.7 + Math.sin(p.pulse) * 0.3);
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(255, 255, 255, ${opacity})`;
        ctx.fill();
    });
    time++;
    requestAnimationFrame(animate);
}
animate();
</script>
""", unsafe_allow_html=True)

# Session states
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_started" not in st.session_state:
    st.session_state.chat_started = False

# Title always visible
st.markdown("<h1>🎓 AI Study Assistant</h1>", unsafe_allow_html=True)
st.markdown('<p class="subtitle">Your personal AI-powered study companion ✦</p>', unsafe_allow_html=True)

# Welcome screen
if not st.session_state.chat_started:
    st.markdown("""
    <div class="genz-msg">
        <p>bestie ur about to get the most fire study help 🔥</p>
        <span>this AI actually gets ur syllabus, slay! 💅✨</span>
        <br><br>
        <p style="color:rgba(255,255,255,0.2); font-size:0.85em;">Mathematics • Science • Programming • History • and more</p>
    </div>
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("let's gooo 🚀"):
            st.session_state.chat_started = True
            st.rerun()
    st.stop()

# Chat screen
if len(st.session_state.messages) == 0:
    st.markdown("""
    <div class="empty-state">
        <p style="font-size:2em;">💬</p>
        <p style="margin-top:10px;">ask me anything bestie 👇</p>
    </div>
    """, unsafe_allow_html=True)
else:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="user-label">You</div>
            <div class="user-bubble">
                <div class="user-bubble-inner">{msg["content"]}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="ai-label">🎓 AI Assistant</div>
            <div class="ai-bubble">
                <div class="ai-bubble-inner">{msg["content"]}</div>
            </div>
            """, unsafe_allow_html=True)

# Input
question = st.text_input("", placeholder="✦  ask anything about ur studies...")

# Buttons
col1, col2 = st.columns([5, 1])
with col1:
    ask_button = st.button("✦  Get Answer")
with col2:
    clear_button = st.button("🗑️")

# Clear
if clear_button:
    st.session_state.messages = []
    st.rerun()

# Answer
if ask_button:
    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.spinner("thinking fr fr... 🤔"):
            client = Groq(api_key=st.secrets["GROQ_API_KEY"])
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are a helpful study assistant for university students. Give clear and concise answers."},
                    {"role": "user", "content": question}
                ]
            )
            answer = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": answer})
        st.rerun()
    else:
        st.warning("bestie type something first 💀")