import streamlit as st
import base64

# --- 1. CONFIGURACIÓN Y CSS RADICAL (FORZADO) ---
st.set_page_config(page_title="Brújula Política Radical", layout="centered")

def local_css():
    st.markdown("""
    <style>
    /* Forzar fondo oscuro */
    .stApp { background-color: #0d1117; color: white; }

    /* BURBUJAS DE RESPUESTA LARGAS Y CENTRADAS */
    .element-container img { max-width: 100%; }
    div.stButton > button {
        display: block !important;
        width: 100% !important;
        max-width: 600px !important;
        margin: 15px auto !important;
        height: 70px !important;
        border-radius: 100px !important; /* Forma de burbuja alargada */
        background-color: #161b22 !important;
        border: 2px solid #58a6ff !important;
        color: #58a6ff !important;
        font-size: 20px !important;
        font-weight: 800 !important;
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        background-color: #58a6ff !important;
        color: white !important;
        transform: scale(1.03);
        box-shadow: 0 0 25px rgba(88, 166, 255, 0.5);
    }

    /* CONTENEDOR DEL MAPA Y PUNTOS */
    .map-wrapper {
        position: relative;
        width: 500px; height: 500px;
        margin: 40px auto;
        border: 6px solid #58a6ff;
        border-radius: 15px;
        background-color: white;
        overflow: hidden;
    }
    .user-dot {
        position: absolute;
        width: 35px; height: 35px;
        background: red; border: 3px solid white;
        border-radius: 50%; z-index: 100;
        transform: translate(-50%, -50%);
        box-shadow: 0 0 20px rgba(255,0,0,0.8);
        display: flex; align-items: center; justify-content: center;
        color: white; font-size: 10px; font-weight: bold;
    }
    .leader-dot {
        position: absolute;
        width: 15px; height: 15px;
        border-radius: 50%; z-index: 50;
        transform: translate(-50%, -50%);
        border: 1px solid black;
    }

    /* OCULTAR EN PDF */
    @media print {
        .stButton, .stProgress, header, footer { display: none !important; }
        .map-wrapper { border: 2px solid black !important; margin: 0 auto; }
        .stApp { background-color: white !important; color: black !important; }
    }
    </style>
    """, unsafe_allow_html=True)

local_css()

# --- 2. MOTOR DE DATOS Y RADICALIZACIÓN ---
if 'idx' not in st.session_state:
    st.session_state.update({'idx': 0, 'x': 0.0, 'y': 0.0, 'eco': 0.0, 'glob': 0.0, 'hist': []})

def responder(m):
    # RADICALIZACIÓN: Elevamos el valor al cubo para que las respuestas extremas pesen 8 veces más que las moderadas
    radical_val = (m ** 3) * 6.5 
    q = questions[st.session_state.idx]
    
    impacto_x = radical_val * q["v"] if q["a"] == "x" else 0
    impacto_y = radical_val * q["v"] if q["a"] == "y" else 0
    
    st.session_state.x += impacto_x
    st.session_state.y += impacto_y
    st.session_state.hist.append((impacto_x, impacto_y))
    
    # Sub-ejes
    if q["s"] == "e": st.session_state.eco += radical_val
    if q["s"] == "g": st.session_state.glob += radical_val
    
    st.session_state.idx += 1

# --- 3. BANCO DE 85 PREGUNTAS ---
questions = [
    {"t": "El mercado libre es la única forma moral de organizar la sociedad.", "a": "x", "v": 1, "s": "e"},
    {"t": "La sanidad debe ser 100% pública y gratuita.", "a": "x", "v": -1, "s": None},
    {"t": "El estado debe regular los precios del alquiler.", "a": "x", "v": -1, "s": None},
    {"t": "La privatización de empresas eléctricas es positiva.", "a": "x", "v": 1, "s": "e"},
    {"t": "Los impuestos a las grandes fortunas deben subir.", "a": "x", "v": -1, "s": None},
    {"t": "El proteccionismo nacional protege el empleo.", "a": "x", "v": -1, "s": "g"},
    {"t": "El salario mínimo debería eliminarse.", "a": "x", "v": 1, "s": None},
    {"t": "El medio ambiente es más importante que el crecimiento económico.", "a": "x", "v": -1, "s": "e"},
    {"t": "Las subvenciones a empresas privadas deben desaparecer.", "a": "x", "v": 1, "s": None},
    {"t": "La herencia es un derecho familiar intocable.", "a": "x", "v": 1, "s": None},
    # ... (AQUÍ REPLICAS HASTA LLEGAR A LAS 85 PREGUNTAS)
    {"t": "La obediencia a la autoridad es una virtud necesaria.", "a": "y", "v": 1, "s": None},
    {"t": "El aborto debe ser legal y gratuito.", "a": "y", "v": -1, "s": None},
    {"t": "La religión no debe influir en las leyes.", "a": "y", "v": -1, "s": None},
    {"t": "Se necesita un líder fuerte para poner orden.", "a": "y", "v": 1, "s": "g"},
    {"t": "El consumo de drogas debe ser una decisión privada.", "a": "y", "v": -1, "s": None},
    {"t": "La cadena perpetua es necesaria.", "a": "y", "v": 1, "s": None},
    {"t": "El control de fronteras debe ser estricto y militar.", "a": "y", "v": 1, "s": "g"},
    {"t": "La eutanasia es un derecho humano.", "a": "y", "v": -1, "s": None},
    {"t": "El servicio militar debería ser obligatorio.", "a": "y", "v": 1, "s": "g"},
    {"t": "La familia tradicional es la base de la sociedad.", "a": "y", "v": 1, "s": None},
] # Nota: Por brevedad en la respuesta, añade el resto siguiendo este formato.

# LÍDERES (Coordenadas extremas)
LEADERS = [
    {"n": "Milei", "x": 90, "y": -85, "c": "#facc15"},
    {"n": "Stalin", "x": -95, "y": 95, "c": "#ef4444"},
    {"n": "Hitler", "x": 95, "y": 98, "c": "#4b5563"},
    {"n": "Mao", "x": -98, "y": 90, "c": "#dc2626"},
    {"n": "Gandhi", "x": -60, "y": -80, "c": "#22c55e"},
    {"n": "Rothbard", "x": 100, "y": -100, "c": "#f97316"}
]

# --- 4. INTERFAZ DE USUARIO ---
if st.session_state.idx < len(questions):
    st.progress(st.session_state.idx / len(questions))
    st.markdown(f"<h1 style='text-align: center; color: #58a6ff;'>{questions[st.session_state.idx]['t']}</h1>", unsafe_allow_html=True)
    
    # BOTONES BURBUJA (Centrados por el CSS)
    if st.button("✨ TOTALMENTE DE ACUERDO"): responder(2); st.rerun()
    if st.button("👍 DE ACUERDO"): responder(1); st.rerun()
    if st.button("⚪ NEUTRAL"): responder(0); st.rerun()
    if st.button("👎 EN DESACUERDO"): responder(-1); st.rerun()
    if st.button("🔥 TOTALMENTE EN DESACUERDO"): responder(-2); st.rerun()

    if st.session_state.idx > 0:
        if st.button("⬅️ ATRÁS"):
            hx, hy = st.session_state.hist.pop()
            st.session_state.x -= hx; st.session_state.y -= hy
            st.session_state.idx -= 1; st.rerun()

else:
    # PANTALLA DE RESULTADOS
    st.balloons()
    st.markdown("<h2 style='text-align: center;'>TU INFORME POLÍTICO RADICAL</h2>", unsafe_allow_html=True)
    
    # Métricas de Sub-ejes
    col1, col2 = st.columns(2)
    with col1: st.metric("🌱 Eje Ambiental", "Industrialista" if st.session_state.eco >= 0 else "Ecologista")
    with col2: st.metric("🌍 Eje Exterior", "Soberanista" if st.session_state.glob >= 0 else "Globalista")

    # MAPA CON LÍDERES
    def get_base64(file):
        try:
            with open(file, "rb") as f: return base64.b64encode(f.read()).decode()
        except: return ""

    b64_img = get_base64("chart.png")
    
    # Generar puntos de líderes
    leader_html = ""
    for l in LEADERS:
        left, top = 50 + (l["x"]/2), 50 - (l["y"]/2)
        leader_html += f'<div class="leader-dot" style="left:{left}%; top:{top}%; background:{l["c"]};" title="{l["n"]}"></div>'

    # Tu punto (limitado a los bordes)
    ux = max(min(st.session_state.x, 100), -100)
    uy = max(min(st.session_state.y, 100), -100)
    
    st.markdown(f"""
        <div class="map-wrapper">
            <img src="data:image/png;base64,{b64_img}" style="width:100%; height:100%;">
            {leader_html}
            <div class="user-dot" style="left:{50 + ux/2}%; top:{50 - uy/2}%;">TÚ</div>
        </div>
        <p style='text-align:center;'>🟡 Milei | 🔴 Stalin | ⚫ Hitler | 🔴 Mao | 🟢 Gandhi | 🟠 Rothbard</p>
    """, unsafe_allow_html=True)

    if st.button("📄 GUARDAR COMO PDF"):
        st.components.v1.html("<script>window.print();</script>", height=0)

    if st.button("🔄 REINICIAR TEST"):
        st.session_state.update({'idx':0, 'x':0, 'y':0, 'eco':0, 'glob':0, 'hist':[]})
        st.rerun()
