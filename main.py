import streamlit as st

# 1. Configuración y Estética (CSS Crítico)
st.set_page_config(page_title="Brújula Política Pro", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #e3f2fd; }
    
    /* Forzar botones a ser idénticos y centrados */
    div.stButton > button {
        width: 100% !important;
        display: block;
        margin: 0 auto;
        border-radius: 12px;
        height: 3.5em;
        font-weight: bold;
        background-color: white;
        border: 2px solid #1565c0;
        color: #1565c0;
    }

    /* Caja de Ideología: Azul más oscuro que el fondo */
    .ideologia-box {
        background-color: #90caf9; /* Azul intermedio */
        color: #0d47a1; /* Azul oscuro para el texto */
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        font-weight: bold;
        border: 2px solid #1565c0;
        margin-bottom: 25px;
    }

    /* Contenedor relativo para el mapa y el punto */
    .map-wrapper {
        position: relative;
        width: 350px;
        height: 350px;
        margin: 0 auto;
    }
    .chart-img {
        width: 100%;
        height: 100%;
        border-radius: 10px;
    }
    .red-dot {
        position: absolute;
        width: 14px;
        height: 14px;
        background-color: red;
        border-radius: 50%;
        border: 2px solid white;
        transform: translate(-50%, -50%);
        z-index: 100;
        box-shadow: 0px 0px 5px rgba(0,0,0,0.5);
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Estado del Test
if 'idx' not in st.session_state:
    st.session_state.idx, st.session_state.x, st.session_state.y = 0, 0.0, 0.0
    st.session_state.history = []

# (Aquí van tus 85 preguntas...)
questions = [
    # ... [Las 85 preguntas que definimos antes] ...
    # Nota: Asegúrate de incluirlas todas en tu código de GitHub
    {"t": "1. El mercado libre beneficia a todos a largo plazo.", "a": "x", "v": 1},
    {"t": "2. La sanidad debe ser 100% pública y gratuita.", "a": "x", "v": -1},
    # ... Añade aquí el resto hasta la 85 ...
]

def responder(m):
    q = questions[st.session_state.idx]
    p = m * q["v"]
    st.session_state.history.append((p if q["a"]=="x" else 0, p if q["a"]=="y" else 0))
    if q["a"]=="x": st.session_state.x += p
    else: st.session_state.y += p
    st.session_state.idx += 1

# --- PANTALLA DE RESULTADOS ---
if st.session_state.idx >= len(questions):
    st.markdown("<h1 style='text-align: center; color: #0d47a1;'>Tu Resultado Final</h1>", unsafe_allow_html=True)
    
    # Lógica de ideología
    x, y = st.session_state.x, st.session_state.y
    if x > 15 and y > 15: id_text = "Autoritarismo de Derecha"
    elif x < -15 and y > 15: id_text = "Autoritarismo de Izquierda"
    elif x > 15 and y < -15: id_text = "Libertarismo de Derecha"
    elif x < -15 and y < -15: id_text = "Libertarismo de Izquierda"
    else: id_text = "Centrismo / Moderado"

    st.markdown(f"<div class='ideologia-box'><h2>{id_text}</h2></div>", unsafe_allow_html=True)

    # Cálculo del punto (Mapeo visual: el centro de la imagen es 50%, 50%)
    # Ajustamos el multiplicador para que el punto no se salga del mapa (85 preguntas)
    left_p = 50 + (x * 0.3) 
    top_p = 50 - (y * 0.3)

    # Renderizado del mapa con el punto rojo encima
    # IMPORTANTE: Streamlit necesita que la imagen esté disponible para HTML.
    # Usaremos una técnica para mostrar la imagen local 'chart.png' dentro de HTML
    import base64
    def get_base64(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    
    try:
        bin_str = get_base64("chart.png")
        st.markdown(f"""
            <div class="map-wrapper">
                <img src="data:image/png;base64,{bin_str}" class="chart-img">
                <div class="red-dot" style="left: {left_p}%; top: {top_p}%;"></div>
            </div>
        """, unsafe_allow_html=True)
    except:
        st.error("No se pudo cargar chart.png. Asegúrate de que esté en la raíz de GitHub.")

    st.write("")
    if st.button("🔄 Reiniciar"):
        st.session_state.idx, st.session_state.x, st.session_state.y = 0, 0.0, 0.0
        st.session_state.history = []
        st.rerun()

# --- PANTALLA DE PREGUNTAS ---
else:
    st.markdown(f"<p style='text-align: center;'>Pregunta {st.session_state.idx + 1} de {len(questions)}</p>", unsafe_allow_html=True)
    st.progress(st.session_state.idx / len(questions))
    st.markdown(f"<h3 style='text-align: center; color: #1565c0;'>{questions[st.session_state.idx]['t']}</h3>", unsafe_allow_html=True)
    
    # Crear una columna central para que todos los botones midan lo mismo
    _, col_mid, _ = st.columns([1, 4, 1])
    
    with col_mid:
        if st.button("✨ Totalmente de acuerdo"): responder(2); st.rerun()
        if st.button("👍 De acuerdo"): responder(1); st.rerun()
        if st.button("😐 Neutral / No sé"): responder(0); st.rerun()
        if st.button("👎 En desacuerdo"): responder(-1); st.rerun()
        if st.button("🔥 Totalmente en desacuerdo"): responder(-2); st.rerun()
        
        if st.session_state.idx > 0:
            st.write("")
            if st.button("⬅️ Volver atrás"):
                st.session_state.idx -= 1
                px, py = st.session_state.history.pop()
                st.session_state.x -= px
                st.session_state.y -= py
                st.rerun()
