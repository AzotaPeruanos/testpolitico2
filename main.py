import streamlit as st
import streamlit.components.v1 as components

# 1. CONFIGURACIÓN Y ESTILO CENTRADO
st.set_page_config(page_title="Compás Político Elite", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #F8FAFC; display: flex; justify-content: center; }
    .main .block-container { max-width: 900px; padding-top: 2rem; text-align: center; }
    
    .main-title { font-size: 55px; font-weight: 950; color: #1E3A8A; margin-bottom: 10px; }
    .q-counter { font-size: 20px; color: #64748B; font-weight: 700; display: block; margin-bottom: 15px; }
    
    /* Contenedor de Pregunta */
    .question-container { 
        margin: 50px auto; 
        min-height: 150px; 
        display: flex; 
        align-items: center; 
        justify-content: center;
        max-width: 800px;
    }
    .question-text { font-size: 34px !important; font-weight: 800; color: #0F172A; line-height: 1.3; }

    /* Botones de Colores Pastel con misma longitud */
    div.stButton > button {
        width: 100% !important;
        height: 60px !important;
        border-radius: 15px !important;
        font-size: 20px !important;
        font-weight: 700 !important;
        margin-bottom: 15px !important;
        border: none !important;
        transition: transform 0.2s;
    }
    div.stButton > button:hover { transform: scale(1.02); }

    /* Asignación de colores específicos */
    /* Totalmente de acuerdo - Verde Esmeralda */
    div.stButton:nth-of-type(1) > button { background-color: #A7F3D0 !important; color: #065F46 !important; }
    /* De acuerdo - Verde Claro */
    div.stButton:nth-of-type(2) > button { background-color: #DCFCE7 !important; color: #166534 !important; }
    /* Neutral - Gris */
    div.stButton:nth-of-type(3) > button { background-color: #F1F5F9 !important; color: #475569 !important; }
    /* En desacuerdo - Rojo Claro */
    div.stButton:nth-of-type(4) > button { background-color: #FEE2E2 !important; color: #991B1B !important; }
    /* Totalmente en desacuerdo - Rojo Oscuro Pastel */
    div.stButton:nth-of-type(5) > button { background-color: #FECACA !important; color: #7F1D1D !important; }

    .result-bubble { 
        background-color: white; 
        border-radius: 30px; 
        padding: 40px; 
        border: 5px solid #3B82F6; 
        margin: 30px auto; 
        max-width: 800px;
    }
    .ideology-title { font-size: 48px !important; font-weight: 900; color: #1D4ED8; text-transform: uppercase; }
    .ideology-desc { font-size: 20px; color: #334155; margin-top: 20px; line-height: 1.6; }
    </style>
    """, unsafe_allow_html=True)

# 2. BASE DE DATOS DE LÍDERES
LEADERS = [
    {"n": "Stalin", "x": -9, "y": 9, "c": "#C53030"}, {"n": "Hitler", "x": 8, "y": 9.5, "c": "#2D3748"},
    {"n": "Mao", "x": -9.5, "y": 8.5, "c": "#E53E3E"}, {"n": "Gandhi", "x": -6.5, "y": -7.5, "c": "#48BB78"},
    {"n": "Thatcher", "x": 7.5, "y": 6.5, "c": "#3182CE"}, {"n": "Milei", "x": 9.2, "y": -8.8, "c": "#D69E2E"},
    {"n": "Castro", "x": -8.5, "y": 7, "c": "#2F855A"}, {"n": "Friedman", "x": 8.5, "y": -6, "c": "#ECC94B"},
    {"n": "Sanders", "x": -5.5, "y": -2, "c": "#4299E1"}, {"n": "Pinochet", "x": 8.8, "y": 8, "c": "#1A202C"},
    {"n": "Chomsky", "x": -8.5, "y": -8.5, "c": "#38A169"}, {"n": "Rothbard", "x": 10, "y": -10, "c": "#F6E05E"},
    {"n": "Obama", "x": 2.5, "y": 1.5, "c": "#2B6CB0"}, {"n": "Trump", "x": 6.5, "y": 5.5, "c": "#E53E3E"},
    {"n": "Biden", "x": 3, "y": 2, "c": "#3182CE"}, {"n": "Bukele", "x": 5, "y": 7, "c": "#2D3748"},
    {"n": "Putin", "x": 7, "y": 8.5, "c": "#2B6CB0"}, {"n": "Sánchez", "x": -2.5, "y": 1, "c": "#F56565"},
    {"n": "Lula", "x": -4.5, "y": 1.5, "c": "#E53E3E"}, {"n": "Kropotkin", "x": -10, "y": -10, "c": "#000000"},
    {"n": "Hayek", "x": 9, "y": -7, "c": "#F6E05E"}, {"n": "Jefferson", "x": 4, "y": -7.5, "c": "#D69E2E"}
    # ... Se pueden añadir todos los 45 mencionados anteriormente
]

# 3. PREGUNTAS (85)
questions = [
    {"t": "El mercado libre, sin intervención estatal, es la forma más eficiente de organizar la economía.", "a": "x", "v": 1},
    {"t": "El acceso a la sanidad debe ser un derecho gratuito financiado por el Estado.", "a": "x", "v": -1},
    {"t": "Es necesario que el Estado regule los precios de productos básicos para proteger al consumidor.", "a": "x", "v": -1},
    {"t": "La privatización de empresas estatales suele mejorar la calidad del servicio.", "a": "x", "v": 1},
    # ... Añadir el resto de las 85 aquí ...
]

# 4. LÓGICA DE IDEOLOGÍAS (2 Líneas)
def get_ideology(x, y):
    if y > 5:
        if x < -5: return "Marxismo-Leninismo", "Buscas la abolición de las clases mediante un Estado con control total de la economía.\nDefiendes la planificación central como método para eliminar la explotación y la desigualdad."
        if x > 5: return "Fascismo / Derecha Radical", "Priorizas la unidad nacional y el orden jerárquico bajo un Estado autoritario y fuerte.\nCrees en un mercado dirigido que sirva a los intereses de la nación y la tradición."
        return "Totalitarismo", "Consideras que el Estado debe regir de forma absoluta todos los aspectos de la vida ciudadana.\nEl orden y la disciplina colectiva son superiores a cualquier libertad individual o de mercado."
    elif y < -5:
        if x < -5: return "Anarcocomunismo", "Deseas una sociedad sin Estado ni propiedad privada basada en la ayuda mutua voluntaria.\nCrees en la autogestión comunal absoluta y la eliminación de toda jerarquía coercitiva."
        if x > 5: return "Anarcocapitalismo", "Defiendes la soberanía individual total y la sustitución del Estado por contratos privados.\nEl mercado libre absoluto es el único mecanismo legítimo para organizar toda la sociedad."
        return "Libertarismo", "Priorizas la libertad personal y económica reduciendo el Estado a su mínima o nula expresión.\nConsideras que el individuo debe ser el único dueño de su destino sin interferencias gubernamentales."
    else:
        if x < -5: return "Socialismo Democrático", "Buscas la justicia social y la igualdad económica a través de instituciones democráticas.\nDefiendes servicios públicos universales y una regulación fuerte del capital privado."
        if x > 5: return "Liberalismo Clásico", "Abogas por un Estado limitado que solo proteja los derechos naturales de vida y propiedad.\nEl libre intercambio y la responsabilidad individual son los motores del progreso humano."
        return "Centrismo", "Evitas los extremos y buscas un equilibrio pragmático entre libertad y protección social.\nCrees en la economía de mercado con regulaciones justas y libertades civiles estables."

# 5. ESTADO Y NAVEGACIÓN
if 'idx' not in st.session_state:
    st.session_state.update({'idx': 0, 'x': 0.0, 'y': 0.0})

def responder(p):
    q = questions[st.session_state.idx]
    num_x = len([qu for qu in questions if qu['a'] == 'x']) or 1
    num_y = len([qu for qu in questions if qu['a'] == 'y']) or 1
    if q['a'] == 'x': st.session_state.x += (p * q['v']) / (num_x / 5)
    else: st.session_state.y += (p * q['v']) / (num_y / 5)
    st.session_state.idx += 1

# --- PANTALLA RESULTADOS ---
if st.session_state.idx >= len(questions):
    st.markdown('<h1 class="main-title">Tu Posición</h1>', unsafe_allow_html=True)
    ux, uy = max(min(st.session_state.x, 10), -10), max(min(st.session_state.y, 10), -10)
    name, desc = get_ideology(ux, uy)
    
    st.markdown(f'<div class="result-bubble"><p class="ideology-title">{name}</p><p class="ideology-desc">{desc}</p></div>', unsafe_allow_html=True)
    
    # SVG ULTRA-GRANDE (800x800)
    scale = 35 # Factor de escala para 800px
    px, py = 400 + (ux * scale), 400 - (uy * scale)
    leaders_svg = "".join([f'<circle cx="{400+(l["x"]*scale)}" cy="{400-(l["y"]*scale)}" r="6" fill="{l["c"]}" stroke="black"/><text x="{400+(l["x"]*scale)}" y="{400-(l["y"]*scale)+18}" font-size="12" text-anchor="middle" font-family="Arial" font-weight="bold">{l["n"]}</text>' for l in LEADERS])
    
    svg_code = f"""
    <div style="display:flex; justify-content:center; padding:20px;">
        <svg width="800" height="800" viewBox="0 0 800 800" style="border:5px solid #000; background:white; width:100%; max-width:800px;">
            <rect width="400" height="400" fill="#FFB2B2" opacity="0.6"/><rect x="400" width="400" height="400" fill="#B2B2FF" opacity="0.6"/>
            <rect y="400" width="400" height="400" fill="#B2FFB2" opacity="0.6"/><rect x="400" y="400" width="400" height="400" fill="#FFFFB2" opacity="0.6"/>
            <line x1="400" y1="0" x2="400" y2="800" stroke="black" stroke-width="4"/><line x1="0" y1="400" x2="800" y2="400" stroke="black" stroke-width="4"/>
            <text x="700" y="430" font-weight="900" font-size="20">DERECHA</text><text x="20" y="430" font-weight="900" font-size="20">IZQUIERDA</text>
            <text x="415" y="40" font-weight="900" font-size="20">AUTORITARIO</text><text x="415" y="780" font-weight="900" font-size="20">LIBERTARIO</text>
            {leaders_svg}
            <circle cx="{px}" cy="{py}" r="15" fill="red" stroke="white" stroke-width="5"/>
            <text x="{px}" y="{py-25}" fill="red" font-weight="950" font-size="28" text-anchor="middle">TÚ</text>
        </svg>
    </div>
    """
    components.html(svg_code, height=850)
    
    if st.button("🔄 REPETIR EL TEST"):
        st.session_state.update({'idx': 0, 'x': 0.0, 'y': 0.0})
        st.rerun()

# --- PANTALLA PREGUNTAS ---
else:
    st.markdown('<h1 class="main-title">Compás Político</h1>', unsafe_allow_html=True)
    st.markdown(f'<span class="q-counter">Pregunta {st.session_state.idx + 1} de {len(questions)}</span>', unsafe_allow_html=True)
    st.progress(st.session_state.idx / len(questions))
    
    st.markdown(f'<div class="question-container"><p class="question-text">{questions[st.session_state.idx]["t"]}</p></div>', unsafe_allow_html=True)
    
    st.button("✅ Totalmente de acuerdo", on_click=responder, args=(2,))
    st.button("👍 De acuerdo", on_click=responder, args=(1,))
    st.button("😐 Neutral / No lo sé", on_click=responder, args=(0,))
    st.button("👎 En desacuerdo", on_click=responder, args=(-1,))
    st.button("❌ Totalmente en desacuerdo", on_click=responder, args=(-2,))
