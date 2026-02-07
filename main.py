import streamlit as st
import base64

# 1. CONFIGURACIÓN E INYECCIÓN DE ESTILO (Burbujas y Mapa)
st.set_page_config(page_title="Brújula Política Radical v5", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: white; }
    
    /* BURBUJAS DE RESPUESTA: Alargadas y Centradas */
    .stButton > button {
        display: block !important;
        width: 100% !important;
        max-width: 750px !important;
        margin: 12px auto !important;
        height: 65px !important;
        border-radius: 60px !important;
        background-color: #1a1f29 !important;
        border: 2px solid #3b82f6 !important;
        color: white !important;
        font-size: 19px !important;
        font-weight: bold !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        background-color: #3b82f6 !important;
        transform: scale(1.02) !important;
        box-shadow: 0 0 25px rgba(59, 130, 246, 0.7) !important;
    }

    /* CONTENEDOR DEL MAPA */
    .map-frame {
        position: relative;
        width: 500px; height: 500px;
        margin: 30px auto;
        border: 5px solid #3b82f6;
        background-color: white;
        border-radius: 15px;
        overflow: hidden;
    }
    .chart-bg { width: 100%; height: 100%; object-fit: cover; }
    
    /* MARCADORES (Líderes y Usuario) */
    .dot {
        position: absolute;
        transform: translate(-50%, -50%);
        border-radius: 50%;
        border: 1px solid white;
        display: flex; align-items: center; justify-content: center;
    }
    .user-dot {
        width: 35px; height: 35px; background: #ff0000;
        z-index: 100; box-shadow: 0 0 20px #ff0000;
        color: white; font-size: 11px; font-weight: bold;
    }
    .leader-dot { width: 16px; height: 16px; z-index: 50; }

    /* ESTILO DE IMPRESIÓN PDF */
    @media print {
        header, footer, .stButton, .stProgress, .stMetric, .stAlert { display: none !important; }
        .map-frame { border: 3px solid black !important; margin: 0 auto !important; width: 450px; height: 450px; }
        .stApp { background-color: white !important; color: black !important; }
    }
    </style>
    """, unsafe_allow_html=True)

# 2. MOTOR DE RADICALIZACIÓN Y VARIABLES
if 'idx' not in st.session_state:
    st.session_state.update({'idx': 0, 'x': 0.0, 'y': 0.0, 'eco': 0.0, 'glob': 0.0, 'hist': []})

def radical_pow(m):
    # Potencia cúbica para forzar los extremos del mapa
    return (m ** 3) * 5.0

# Coordenadas de Líderes (Normalizadas -100 a 100)
LEADERS = [
    {"n": "Milei", "x": 88, "y": -80, "c": "#facc15"},
    {"n": "Stalin", "x": -95, "y": 95, "c": "#ef4444"},
    {"n": "Hitler", "x": 92, "y": 98, "c": "#4b5563"},
    {"n": "Mao", "x": -98, "y": 88, "c": "#dc2626"},
    {"n": "Pol Pot", "x": -100, "y": 75, "c": "#7f1d1d"},
    {"n": "Pinochet", "x": 98, "y": 92, "c": "#1d4ed8"},
    {"n": "Rothbard", "x": 100, "y": -100, "c": "#f97316"},
    {"n": "Gandhi", "x": -70, "y": -85, "c": "#22c55e"}
]

# 3. BANCO COMPLETO DE 85 PREGUNTAS
# a: eje (x/y), v: dirección, s: sub-eje (e=eco, g=global)
questions = [
    {"t": "El mercado libre es el único sistema moral de cooperación.", "a": "x", "v": 1, "s": "e"},
    {"t": "La sanidad debe ser 100% pública y gratuita.", "a": "x", "v": -1, "s": None},
    {"t": "El estado debe regular los precios del alquiler.", "a": "x", "v": -1, "s": None},
    {"t": "La privatización de empresas eléctricas es positiva.", "a": "x", "v": 1, "s": "e"},
    {"t": "Los impuestos a las grandes fortunas deben subir.", "a": "x", "v": -1, "s": None},
    {"t": "El proteccionismo protege el empleo local.", "a": "x", "v": -1, "s": "g"},
    {"t": "El salario mínimo debería eliminarse.", "a": "x", "v": 1, "s": None},
    {"t": "El medio ambiente es más importante que el PIB.", "a": "x", "v": -1, "s": "e"},
    {"t": "Las subvenciones a empresas deben desaparecer.", "a": "x", "v": 1, "s": None},
    {"t": "La herencia es un derecho familiar intocable.", "a": "x", "v": 1, "s": None},
    {"t": "Educación universitaria gratuita para todos.", "a": "x", "v": -1, "s": None},
    {"t": "La competencia siempre mejora la calidad.", "a": "x", "v": 1, "s": "e"},
    {"t": "El estado debe garantizar trabajo a todos.", "a": "x", "v": -1, "s": None},
    {"t": "La propiedad privada debe ser absoluta.", "a": "x", "v": 1, "s": None},
    {"t": "Los bancos centrales no deberían existir.", "a": "x", "v": 1, "s": None},
    {"t": "Infraestructuras básicas deben ser estatales.", "a": "x", "v": -1, "s": None},
    {"t": "El comercio global reduce la pobreza.", "a": "x", "v": 1, "s": "g"},
    {"t": "La especulación financiera debe prohibirse.", "a": "x", "v": -1, "s": None},
    {"t": "El gasto público excesivo daña la nación.", "a": "x", "v": 1, "s": None},
    {"t": "La caridad privada supera al bienestar estatal.", "a": "x", "v": 1, "s": None},
    {"t": "Los paraísos fiscales son legítimos.", "a": "x", "v": 1, "s": None},
    {"t": "Rescate estatal a empresas en crisis.", "a": "x", "v": -1, "s": None},
    {"t": "Austeridad fiscal en tiempos de crisis.", "a": "x", "v": 1, "s": None},
    {"t": "La desigualdad es un motor natural.", "a": "x", "v": 1, "s": None},
    {"t": "Los sindicatos tienen demasiado poder.", "a": "x", "v": 1, "s": None},
    {"t": "Volver al patrón oro.", "a": "x", "v": 1, "s": None},
    {"t": "Renta básica por automatización.", "a": "x", "v": -1, "s": None},
    {"t": "Abolir patentes farmacéuticas.", "a": "x", "v": -1, "s": None},
    {"t": "El consumo masivo es progreso.", "a": "x", "v": 1, "s": "e"},
    {"t": "Jornada laboral de 30 horas por ley.", "a": "x", "v": -1, "s": None},
    {"t": "Obedecer a la autoridad es una virtud.", "a": "y", "v": 1, "s": None},
    {"t": "Aborto legal, seguro y gratuito.", "a": "y", "v": -1, "s": None},
    {"t": "Separación absoluta Iglesia-Estado.", "a": "y", "v": -1, "s": None},
    {"t": "Un líder fuerte para poner orden.", "a": "y", "v": 1, "s": None},
    {"t": "Legalización total de la marihuana.", "a": "y", "v": -1, "s": None},
    {"t": "Cadena perpetua para crímenes graves.", "a": "y", "v": 1, "s": None},
    {"t": "Control fronterizo militarizado.", "a": "y", "v": 1, "s": "g"},
    {"t": "El feminismo actual es necesario.", "a": "y", "v": -1, "s": None},
    {"t": "Vigilancia masiva contra terrorismo.", "a": "y", "v": 1, "s": None},
    {"t": "Libertad de expresión total (ofensa incluida).", "a": "y", "v": -1, "s": None},
    {"t": "Eutanasia como derecho legal.", "a": "y", "v": -1, "s": None},
    {"t": "Servicio militar obligatorio.", "a": "y", "v": 1, "s": "g"},
    {"t": "Familia tradicional como base social.", "a": "y", "v": 1, "s": None},
    {"t": "Prohibición de la pornografía.", "a": "y", "v": 1, "s": None},
    {"t": "El arte nunca debe ser censurado.", "a": "y", "v": -1, "s": None},
    {"t": "Pena de muerte en casos extremos.", "a": "y", "v": 1, "s": None},
    {"t": "La inmigración diluye la identidad nacional.", "a": "y", "v": 1, "s": "g"},
    {"t": "Matrimonio solo hombre-mujer.", "a": "y", "v": 1, "s": None},
    {"t": "Prohibir protestas que corten calles.", "a": "y", "v": 1, "s": None},
    {"t": "Género como construcción social.", "a": "y", "v": -1, "s": None},
    {"t": "Abolición de la monarquía.", "a": "y", "v": -1, "s": None},
    {"t": "Más poderes para la policía.", "a": "y", "v": 1, "s": None},
    {"t": "Educación sexual obligatoria.", "a": "y", "v": -1, "s": None},
    {"t": "No debe existir el delito de blasfemia.", "a": "y", "v": -1, "s": None},
    {"t": "La bandera es el símbolo máximo.", "a": "y", "v": 1, "s": "g"},
    {"t": "Permitir clonación humana.", "a": "y", "v": -1, "s": "e"},
    {"t": "La corrección política es censura.", "a": "y", "v": 1, "s": None},
    {"t": "El multiculturalismo ha fallado.", "a": "y", "v": 1, "s": "g"},
    {"t": "Experimentación animal necesaria.", "a": "y", "v": 1, "s": "e"},
    {"t": "Fomentar natalidad desde el estado.", "a": "y", "v": 1, "s": None},
    {"t": "La piratería digital no es robo.", "a": "y", "v": -1, "s": None},
    {"t": "Disciplina escolar estricta.", "a": "y", "v": 1, "s": None},
    {"t": "Control gubernamental de la IA.", "a": "y", "v": 1, "s": "e"},
    {"t": "Energía nuclear como solución.", "a": "x", "v": 1, "s": "e"},
    {"t": "Derechos legales para animales.", "a": "y", "v": -1, "s": "e"},
    {"t": "Colonización espacial privada.", "a": "x", "v": 1, "s": "e"},
    {"t": "Derecho a portar armas.", "a": "y", "v": -1, "s": None},
    {"t": "Subvencionar cine y cultura.", "a": "x", "v": -1, "s": None},
    {"t": "La globalización mata culturas locales.", "a": "y", "v": 1, "s": "g"},
    {"t": "El capitalismo destruye el planeta.", "a": "x", "v": -1, "s": "e"},
    {"t": "Democracia directa por internet.", "a": "y", "v": -1, "s": None},
    {"t": "Cárceles para castigo, no reinserción.", "a": "y", "v": 1, "s": None},
    {"t": "La riqueza es mérito individual.", "a": "x", "v": 1, "s": None},
    {"t": "Internet como derecho humano básico.", "a": "x", "v": -1, "s": None},
    {"t": "Religión obligatoria en escuelas.", "a": "y", "v": 1, "s": None},
    {"t": "Intervención militar por DDHH.", "a": "y", "v": 1, "s": "g"},
    {"t": "Criptomonedas sobre moneda estatal.", "a": "x", "v": 1, "s": None},
    {"t": "CEO ganando 500x que empleado es justo.", "a": "x", "v": 1, "s": None},
    {"t": "Prohibir comida basura por salud.", "a": "y", "v": 1, "s": "e"},
    {"t": "La diversidad es nuestra fuerza.", "a": "y", "v": -1, "s": "g"},
    {"t": "Las huelgas dañan la nación.", "a": "x", "v": 1, "s": None},
    {"t": "La tecnología nos deshumaniza.", "a": "y", "v": 1, "s": "e"},
    {"t": "Impuestos del 90% a millonarios.", "a": "x", "v": -1, "s": None},
    {"t": "Prohibir coches diésel mañana.", "a": "x", "v": -1, "s": "e"},
    {"t": "Sin jerarquía la sociedad colapsa.", "a": "y", "v": 1, "s": None}
]

def responder(m):
    q = questions[st.session_state.idx]
    val = radical_pow(m) * q["v"]
    st.session_state.hist.append((val if q["a"]=="x" else 0, val if q["a"]=="y" else 0))
    if q["a"] == "x": st.session_state.x += val
    else: st.session_state.y += val
    if q["s"] == "e": st.session_state.eco += val
    if q["s"] == "g": st.session_state.glob += val
    st.session_state.idx += 1

# --- PANTALLA FINAL ---
if st.session_state.idx >= len(questions):
    st.markdown("## 📊 ANÁLISIS DE IDEOLOGÍA RADICAL")
    x, y = st.session_state.x, st.session_state.y
    
    if x > 45 and y > 45: res, desc = "AUTORITARISMO NACIONAL", "Orden, tradición y mercado bajo un control soberano férreo."
    elif x < -45 and y > 45: res, desc = "ESTALINISMO TOTALITARIO", "Control estatal absoluto y abolición total de la propiedad."
    elif x > 45 and y < -45: res, desc = "ANARCOCAPITALISMO", "Soberanía individual total. El Estado es un robo."
    elif x < -45 and y < -45: res, desc = "ANARCOCOMUNISMO", "Comunas libres sin jerarquías ni capital."
    else: res, desc = "CENTRISMO", "Posiciones equilibradas."

    st.success(f"### Resultado: {res}")
    st.write(desc)

    c1, c2 = st.columns(2)
    with c1: st.metric("🏭 Desarrollo", "Industrialista" if st.session_state.eco >= 0 else "Ecologista")
    with c2: st.metric("🌐 Diplomacia", "Soberanista" if st.session_state.glob >= 0 else "Globalista")

    # MAPA
    def get_b64(path):
        try:
            with open(path, "rb") as f: return base64.b64encode(f.read()).decode()
        except: return ""

    b64 = get_b64("chart.png")
    l_html = ""
    for l in LEADERS:
        px, py = 50 + (l["x"]/2), 50 - (l["y"]/2)
        l_html += f'<div class="dot leader-dot" style="left:{px}%; top:{py}%; background:{l["c"]};"></div>'

    ux, uy = max(min(x, 100), -100), max(min(y, 100), -100)
    st.markdown(f"""
        <div class="map-frame">
            <img src="data:image/png;base64,{b64}" class="chart-bg">
            {l_html}
            <div class="dot user-dot" style="left:{50 + ux/2}%; top:{50 - uy/2}%;">TÚ</div>
        </div>
    """, unsafe_allow_html=True)

    if st.button("📄 GUARDAR COMO PDF"):
        st.components.v1.html("<script>window.print();</script>", height=0)

    if st.button("🔄 REINICIAR"):
        st.session_state.update({'idx': 0, 'x': 0, 'y': 0, 'eco': 0, 'glob': 0, 'hist': []})
        st.rerun()

# --- CUESTIONARIO ---
else:
    st.progress(st.session_state.idx / len(questions))
    st.markdown(f"<h2 style='text-align:center; padding: 20px;'>{questions[st.session_state.idx]['t']}</h2>", unsafe_allow_html=True)
    
    if st.button("✨ Totalmente de acuerdo"): responder(2); st.rerun()
    if st.button("👍 De acuerdo"): responder(1); st.rerun()
    if st.button("⚪ Neutral / No sé"): responder(0); st.rerun()
    if st.button("👎 En desacuerdo"): responder(-1); st.rerun()
    if st.button("🔥 Totalmente en desacuerdo"): responder(-2); st.rerun()

    if st.session_state.idx > 0:
        if st.button("⬅️ Atrás"):
            st.session_state.idx -= 1
            hx, hy = st.session_state.hist.pop()
            st.session_state.x -= hx; st.session_state.y -= hy
            st.rerun()
