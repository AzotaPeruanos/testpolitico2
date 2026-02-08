import streamlit as st
import base64

# 1. ESTÉTICA RADICAL: FONDO AZUL Y BOTONES COLOREADOS
st.set_page_config(page_title="Brújula Política: Edición Extrema", layout="centered")

st.markdown("""
    <style>
    /* Fondo Azul Profundo */
    .stApp { background-color: #001f3f; color: #ffffff; }
    
    /* Configuración de Botones (Burbujas Alargadas) */
    div.stButton > button {
        width: 100% !important;
        max-width: 650px;
        margin: 10px auto !important;
        display: block;
        border-radius: 50px;
        height: 3.5em;
        font-weight: bold;
        font-size: 18px;
        border: 2px solid #ffffff;
        transition: 0.3s;
    }

    /* Colores Específicos por Botón (Usando selectores de orden) */
    /* Totalmente de acuerdo - Verde Oscuro */
    div.stButton:nth-of-type(1) > button { background-color: #1b5e20 !important; color: white !important; }
    /* De acuerdo - Verde Claro */
    div.stButton:nth-of-type(2) > button { background-color: #81c784 !important; color: #1b5e20 !important; }
    /* Neutral - Blanco */
    div.stButton:nth-of-type(3) > button { background-color: #ffffff !important; color: #001f3f !important; }
    /* En desacuerdo - Rojo Claro */
    div.stButton:nth-of-type(4) > button { background-color: #e57373 !important; color: #b71c1c !important; }
    /* Totalmente en desacuerdo - Rojo Oscuro */
    div.stButton:nth-of-type(5) > button { background-color: #b71c1c !important; color: white !important; }

    div.stButton > button:hover { transform: scale(1.02); opacity: 0.9; }

    /* Contenedor del Mapa */
    .map-container {
        position: relative; width: 450px; height: 450px; 
        margin: 30px auto; border: 5px solid #64b5f6; border-radius: 10px;
        background-color: white; overflow: hidden;
    }
    .chart-img { width: 100%; height: 100%; display: block; }
    
    .dot { position: absolute; border-radius: 50%; border: 1px solid white; transform: translate(-50%, -50%); }
    .user-dot {
        width: 32px; height: 32px; background-color: #ff0000; z-index: 100;
        box-shadow: 0 0 20px #ff0000; border: 3px solid white; color: white;
        display: flex; align-items: center; justify-content: center; font-size: 10px; font-weight: bold;
    }
    .leader-dot { width: 14px; height: 14px; z-index: 50; }

    @media print {
        .stButton, .stProgress, header, footer { display: none !important; }
        .map-container { border: 2px solid black !important; }
    }
    </style>
    """, unsafe_allow_html=True)

# 2. MOTOR DE DATOS
if 'idx' not in st.session_state:
    st.session_state.update({'idx': 0, 'x': 0.0, 'y': 0.0, 'eco': 0.0, 'glob': 0.0, 'hist': []})

def get_points(m):
    # Radicalización: El valor extremo pesa mucho más que el moderado
    sign = 1 if m >= 0 else -1
    return (abs(m) ** 2.5) * sign * 4.0

LEADERS = [
    {"n": "Milei", "x": 170, "y": -160, "c": "#ffeb3b"},
    {"n": "Stalin", "x": -190, "y": 190, "c": "#b71c1c"},
    {"n": "Hitler", "x": 180, "y": 195, "c": "#424242"},
    {"n": "Mao", "x": -195, "y": 175, "c": "#f44336"},
    {"n": "Gandhi", "x": -130, "y": -170, "c": "#4caf50"},
    {"n": "Rothbard", "x": 198, "y": -198, "c": "#ff9800"},
    {"n": "Thatcher", "x": 150, "y": 110, "c": "#1565c0"},
    {"n": "Castro", "x": -165, "y": 140, "c": "#2e7d32"},
    {"n": "Kropotkin", "x": -190, "y": -190, "c": "#000000"}
]

# 3. LAS 85 PREGUNTAS
questions = [
    {"t": "El mercado libre beneficia a todos a largo plazo.", "a": "x", "v": 1, "s": "ind"},
    {"t": "La sanidad debe ser 100% pública y gratuita.", "a": "x", "v": -1, "s": None},
    {"t": "El estado debe regular los precios del alquiler.", "a": "x", "v": -1, "s": None},
    {"t": "La privatización de empresas eléctricas es positiva.", "a": "x", "v": 1, "s": "ind"},
    {"t": "Los impuestos a las grandes fortunas deben subir.", "a": "x", "v": -1, "s": None},
    {"t": "El proteccionismo nacional protege el empleo.", "a": "x", "v": -1, "s": "sob"},
    {"t": "El salario mínimo debería eliminarse.", "a": "x", "v": 1, "s": None},
    {"t": "El medio ambiente es más importante que el PIB.", "a": "x", "v": -1, "s": "eco"},
    {"t": "Las subvenciones a empresas privadas deben desaparecer.", "a": "x", "v": 1, "s": None},
    {"t": "La herencia es un derecho familiar intocable.", "a": "x", "v": 1, "s": None},
    {"t": "La educación universitaria debe ser gratuita para todos.", "a": "x", "v": -1, "s": None},
    {"t": "La competencia siempre mejora la calidad de los servicios.", "a": "x", "v": 1, "s": "ind"},
    {"t": "El estado debe garantizar un puesto de trabajo a cada ciudadano.", "a": "x", "v": -1, "s": None},
    {"t": "La propiedad privada debe ser absoluta.", "a": "x", "v": 1, "s": None},
    {"t": "Los bancos centrales no deberían existir.", "a": "x", "v": 1, "s": None},
    {"t": "Las infraestructuras básicas deben ser estatales.", "a": "x", "v": -1, "s": None},
    {"t": "El comercio global es la vía para reducir la pobreza.", "a": "x", "v": 1, "s": "glob"},
    {"t": "La especulación financiera debería estar prohibida.", "a": "x", "v": -1, "s": None},
    {"t": "El gasto público excesivo daña la economía.", "a": "x", "v": 1, "s": None},
    {"t": "La caridad privada es más eficiente que el estado.", "a": "x", "v": 1, "s": None},
    {"t": "Los paraísos fiscales son legítimos.", "a": "x", "v": 1, "s": None},
    {"t": "El estado debe rescatar empresas estratégicas.", "a": "x", "v": -1, "s": None},
    {"t": "La austeridad fiscal es necesaria para crecer.", "a": "x", "v": 1, "s": None},
    {"t": "La desigualdad es un motor natural de progreso.", "a": "x", "v": 1, "s": None},
    {"t": "Los sindicatos tienen demasiado poder.", "a": "x", "v": 1, "s": None},
    {"t": "La moneda debe volver al patrón oro.", "a": "x", "v": 1, "s": None},
    {"t": "La automatización requiere una Renta Básica.", "a": "x", "v": -1, "s": None},
    {"t": "Las patentes farmacéuticas frenan el progreso.", "a": "x", "v": -1, "s": None},
    {"t": "El consumo masivo es fundamental.", "a": "x", "v": 1, "s": "ind"},
    {"t": "La jornada laboral debe ser de 30 horas.", "a": "x", "v": -1, "s": None},
    {"t": "La obediencia a la autoridad es una virtud.", "a": "y", "v": 1, "s": None},
    {"t": "El aborto debe ser legal y gratuito.", "a": "y", "v": -1, "s": None},
    {"t": "La religión no debe influir en las leyes.", "a": "y", "v": -1, "s": None},
    {"t": "Se necesita un líder fuerte para poner orden.", "a": "y", "v": 1, "s": None},
    {"t": "El consumo de drogas debe ser legal.", "a": "y", "v": -1, "s": None},
    {"t": "La cadena perpetua es necesaria.", "a": "y", "v": 1, "s": None},
    {"t": "El control de fronteras debe ser militar.", "a": "y", "v": 1, "s": "sob"},
    {"t": "El feminismo actual es justo.", "a": "y", "v": -1, "s": None},
    {"t": "La vigilancia masiva es aceptable contra el terror.", "a": "y", "v": 1, "s": None},
    {"t": "La libertad de expresión debe ser absoluta.", "a": "y", "v": -1, "s": None},
    {"t": "La eutanasia debe ser un derecho legal.", "a": "y", "v": -1, "s": None},
    {"t": "El servicio militar debe ser obligatorio.", "a": "y", "v": 1, "s": "sob"},
    {"t": "La familia tradicional es la base social.", "a": "y", "v": 1, "s": None},
    {"t": "La pornografía debería ser ilegal.", "a": "y", "v": 1, "s": None},
    {"t": "El arte nunca debe ser censurado.", "a": "y", "v": -1, "s": None},
    {"t": "La pena de muerte es justa en casos extremos.", "a": "y", "v": 1, "s": None},
    {"t": "La inmigración masiva daña la identidad nacional.", "a": "y", "v": 1, "s": "sob"},
    {"t": "El matrimonio solo entre hombre y mujer.", "a": "y", "v": 1, "s": None},
    {"t": "Las manifestaciones que bloquean calles deben prohibirse.", "a": "y", "v": 1, "s": None},
    {"t": "El género es una construcción social.", "a": "y", "v": -1, "s": None},
    {"t": "La monarquía debe desaparecer.", "a": "y", "v": -1, "s": None},
    {"t": "La policía necesita más autoridad.", "a": "y", "v": 1, "s": None},
    {"t": "La educación sexual es esencial.", "a": "y", "v": -1, "s": None},
    {"t": "Blasfemar no debería ser delito.", "a": "y", "v": -1, "s": None},
    {"t": "La bandera es sagrada.", "a": "y", "v": 1, "s": "sob"},
    {"t": "La clonación humana debe permitirse.", "a": "y", "v": -1, "s": "ind"},
    {"t": "La corrección política destruye la libertad.", "a": "y", "v": 1, "s": None},
    {"t": "El multiculturalismo ha fallado.", "a": "y", "v": 1, "s": "sob"},
    {"t": "La experimentación animal es necesaria.", "a": "y", "v": 1, "s": "ind"},
    {"t": "El estado debe fomentar la natalidad.", "a": "y", "v": 1, "s": None},
    {"t": "La piratería digital no es un crimen real.", "a": "y", "v": -1, "s": None},
    {"t": "La disciplina escolar debe ser estricta.", "a": "y", "v": 1, "s": None},
    {"t": "La IA debe ser controlada por el gobierno.", "a": "y", "v": 1, "s": "ind"},
    {"t": "La energía nuclear es la mejor solución.", "a": "x", "v": 1, "s": "ind"},
    {"t": "Los animales deberían tener derechos legales.", "a": "y", "v": -1, "s": "eco"},
    {"t": "La colonización espacial debe ser privada.", "a": "x", "v": 1, "s": "ind"},
    {"t": "Subvencionar cine es malgastar dinero.", "a": "x", "v": 1, "s": None},
    {"t": "La globalización destruye culturas.", "a": "y", "v": 1, "s": "sob"},
    {"t": "El capitalismo destruye el planeta.", "a": "x", "v": -1, "s": "eco"},
    {"t": "Votar leyes directamente por internet.", "a": "y", "v": -1, "s": None},
    {"t": "Cárceles para castigar, no reinsertar.", "a": "y", "v": 1, "s": None},
    {"t": "El éxito económico es puro mérito personal.", "a": "x", "v": 1, "s": None},
    {"t": "Internet debe ser un servicio público gratuito.", "a": "x", "v": -1, "s": None},
    {"t": "Religión obligatoria en las escuelas.", "a": "y", "v": 1, "s": None},
    {"t": "Intervención militar exterior por DDHH.", "a": "y", "v": 1, "s": "glob"},
    {"t": "Criptomonedas para la libertad económica.", "a": "x", "v": 1, "s": None},
    {"t": "Es justo que un CEO gane 500 veces más que un empleado.", "a": "x", "v": 1, "s": None},
    {"t": "Hay que prohibir la comida basura por razones relacionadas con la salud.", "a": "y", "v": 1, "s": "eco"},
    {"t": "La diversidad étnica fortalece la nación.", "a": "y", "v": -1, "s": "glob"},
    {"t": "Las huelgas generales suelen ser dañinas.", "a": "x", "v": 1, "s": None},
    {"t": "La tecnología nos deshumaniza.", "a": "y", "v": 1, "s": "eco"},
    {"t": "Deberían haber impuestos del 90% a los ricos.", "a": "x", "v": -1, "s": None},
    {"t": "Hay que prohibir los coches de combustión.", "a": "x", "v": -1, "s": "eco"},
    {"t": "Sin una jerarquía la sociedad colapsa.", "a": "y", "v": 1, "s": None},
    {"t": "Cualquier época del pasado fue mejor a la actualidad.", "a": "y", "v": 1, "s": None}
]

def responder(m):
    q = questions[st.session_state.idx]
    p = get_points(m) * q["v"]
    st.session_state.hist.append((p if q["a"]=="x" else 0, p if q["a"]=="y" else 0))
    if q["a"] == "x": st.session_state.x += p
    else: st.session_state.y += p
    if q["s"] == "ind": st.session_state.eco += p
    if q["s"] == "glob": st.session_state.glob += p
    st.session_state.idx += 1

# --- PANTALLAS ---
if st.session_state.idx >= len(questions):
    st.markdown("<h1 style='text-align:center;'>📊 Resultado Final</h1>", unsafe_allow_html=True)
    x, y = st.session_state.x, st.session_state.y
    
    # Clasificación Extrema
    if x > 80 and y > 80: n, d = "TOTALITARISMO DE DERECHA", "Orden absoluto y mercado jerárquico."
    elif x < -80 and y > 80: n, d = "STALINISMO", "Control estatal total y colectivización forzosa."
    elif x > 80 and y < -80: n, d = "ANARCOCAPITALISMO", "Soberanía individual y propiedad privada absoluta."
    elif x < -80 and y < -80: n, d = "ANARCOCOMUNISMO", "Abolición de toda jerarquía y propiedad."
    else: n, d = "MODERACIÓN", "Tus puntos de vista son equilibrados."

    st.success(f"### {n}")
    st.info(d)

    # Mapa
    def to_b64(f):
        try:
            with open(f, "rb") as b: return base64.b64encode(b.read()).decode()
        except: return ""

    img = to_b64("chart.png")
    l_html = ""
    for l in LEADERS:
        lx, ly = 50 + (l["x"] * 0.23), 50 - (l["y"] * 0.23)
        l_html += f'<div class="dot leader-dot" style="left:{lx}%; top:{ly}%; background:{l["c"]};"></div>'

    ux, uy = 50 + (x * 0.23), 50 - (y * 0.23)
    st.markdown(f"""
        <div class="map-container">
            <img src="data:image/png;base64,{img}" class="chart-img">
            {l_html}
            <div class="dot user-dot" style="left:{ux}%; top:{uy}%;">TÚ</div>
        </div>
    """, unsafe_allow_html=True)

    if st.button("📄 GUARDAR PDF"):
        st.components.v1.html("<script>window.print();</script>", height=0)
    
    if st.button("🔄 REINICIAR"):
        st.session_state.update({'idx':0, 'x':0, 'y':0, 'eco':0, 'glob':0, 'hist':[]})
        st.rerun()

else:
    st.progress(st.session_state.idx / len(questions))
    st.markdown(f"<h3 style='text-align:center; min-height:100px;'>{questions[st.session_state.idx]['t']}</h3>", unsafe_allow_html=True)
    
    if st.button("Totalmente de acuerdo"): responder(2); st.rerun()
    if st.button("De acuerdo"): responder(1); st.rerun()
    if st.button("Neutral"): responder(0); st.rerun()
    if st.button("En desacuerdo"): responder(-1); st.rerun()
    if st.button("Totalmente en desacuerdo"): responder(-2); st.rerun()

    if st.session_state.idx > 0:
        if st.button("⬅️ ATRÁS"):
            px, py = st.session_state.hist.pop()
            st.session_state.x -= px; st.session_state.y -= py
            st.session_state.idx -= 1; st.rerun()
