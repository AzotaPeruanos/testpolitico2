import streamlit as st
import streamlit.components.v1 as components
import math

# 1. CONFIGURACIÓN Y ESTILO
st.set_page_config(page_title="Compás Político Definitivo", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #E0F2FE; }
    .main-title { font-size: 50px; font-weight: 950; color: #1E3A8A; text-align: center; margin-bottom: 5px; }
    .welcome-text { font-size: 19px; color: #1E40AF; text-align: center; margin-bottom: 20px; font-weight: 500; }
    .warning-box { background-color: #FFFFFF; border: 2px solid #3B82F6; border-radius: 15px; padding: 20px; text-align: center; color: #1E40AF; font-weight: 700; margin-bottom: 30px; }
    
    .q-counter { font-size: 18px; color: #1E40AF; font-weight: 800; margin-bottom: 20px; display: block; text-transform: uppercase; }
    .stProgress { margin-bottom: 35px !important; }
    
    .question-container { margin: 30px 0; text-align: center; min-height: 110px; display: flex; align-items: center; justify-content: center; }
    .question-text { font-size: 30px !important; font-weight: 800; color: #1E3A8A; line-height: 1.2; }
    
    div.stButton > button { width: 100% !important; height: 52px !important; border-radius: 12px !important; font-size: 18px !important; font-weight: 700; margin-bottom: 10px !important; }

    @media print {
        .stButton, .q-counter, .stProgress, .welcome-text, .warning-box, header, [data-testid="stSidebar"] { display: none !important; }
        .stApp { background-color: white !important; }
        .result-bubble { border: 2px solid black !important; box-shadow: none !important; margin-top: 20px; page-break-inside: avoid; }
        .svg-container { width: 100% !important; display: block !important; }
    }
    
    .result-bubble { background-color: white; border-radius: 25px; padding: 30px; border: 3px solid #60A5FA; margin-bottom: 20px; }
    .ideology-title { font-size: 36px !important; font-weight: 900; color: #2563EB; text-align: center; text-transform: uppercase; margin: 0; }
    .ideology-desc { font-size: 17px; color: #334155; text-align: justify; margin-top: 15px; line-height: 1.5; }
    </style>
    """, unsafe_allow_html=True)

# 2. BASE DE DATOS DE LÍDERES
LEADERS = [
    {"n": "Stalin", "x": -9, "y": 9, "c": "#C53030"}, {"n": "Hitler", "x": 8, "y": 9.5, "c": "#2D3748"},
    {"n": "Mao", "x": -9.5, "y": 8.5, "c": "#E53E3E"}, {"n": "Gandhi", "x": -6.5, "y": -7.5, "c": "#48BB78"},
    {"n": "Thatcher", "x": 7.5, "y": 6.5, "c": "#3182CE"}, {"n": "Milei", "x": 9.2, "y": -8.8, "c": "#D69E2E"},
    {"n": "Castro", "x": -8.5, "y": 7, "c": "#2F855A"}, {"n": "Friedman", "x": 8.5, "y": -6, "c": "#ECC94B"},
    {"n": "Pinochet", "x": 8.8, "y": 8, "c": "#1A202C"}, {"n": "Chomsky", "x": -8.5, "y": -8.5, "c": "#38A169"},
    {"n": "Obama", "x": 2.5, "y": 1.5, "c": "#2B6CB0"}, {"n": "Trump", "x": 6.5, "y": 5.5, "c": "#E53E3E"},
    {"n": "Bukele", "x": 5, "y": 7, "c": "#2D3748"}, {"n": "Sánchez", "x": -2.5, "y": 1, "c": "#F56565"},
    {"n": "Kim Jong-un", "x": -9.5, "y": 10, "c": "#E53E3E"}, {"n": "Mujica", "x": -7, "y": -4, "c": "#48BB78"},
    {"n": "Macron", "x": 4, "y": 3, "c": "#3182CE"}, {"n": "Bolsonaro", "x": 8, "y": 6.5, "c": "#48BB78"}
]

# 3. LAS 85 PREGUNTAS (Eje X: Economía, Eje Y: Social)
questions = [
    # ECONÓMICAS (43 preguntas aprox)
    {"t": "El salario mínimo es una interferencia innecesaria en el mercado.", "a": "x", "v": 1},
    {"t": "La sanidad debe ser financiada exclusivamente mediante impuestos.", "a": "x", "v": -1},
    {"t": "Las empresas de suministro de agua deben ser siempre públicas.", "a": "x", "v": -1},
    {"t": "El proteccionismo económico es necesario para salvar empleos.", "a": "x", "v": -1},
    {"t": "La propiedad privada debe ser protegida por encima de todo.", "a": "x", "v": 1},
    {"t": "El Estado debe intervenir para evitar los monopolios.", "a": "x", "v": -1},
    {"t": "Los impuestos sobre la herencia son un robo estatal.", "a": "x", "v": 1},
    {"t": "El libre comercio beneficia a todos los países a largo plazo.", "a": "x", "v": 1},
    {"t": "Es justo que el Estado redistribuya la riqueza de los más ricos.", "a": "x", "v": -1},
    {"t": "Las huelgas sindicales suelen ser perjudiciales para la economía.", "a": "x", "v": 1},
    {"t": "El gobierno debería garantizar una Renta Básica Universal.", "a": "x", "v": -1},
    {"t": "Los servicios públicos son menos eficientes que los privados.", "a": "x", "v": 1},
    {"t": "El capitalismo es el único sistema que genera prosperidad.", "a": "x", "v": 1},
    {"t": "La vivienda es un derecho que el Estado debe proveer.", "a": "x", "v": -1},
    {"t": "Las regulaciones medioambientales frenan el progreso.", "a": "x", "v": 1},
    {"t": "El Banco Central debería ser eliminado.", "a": "x", "v": 1},
    {"t": "El Estado no debe rescatar a bancos que quiebran.", "a": "x", "v": 1},
    {"t": "La educación universitaria debería ser gratuita para todos.", "a": "x", "v": -1},
    {"t": "Es moralmente correcto que existan los multimillonarios.", "a": "x", "v": 1},
    {"t": "El control de precios por el gobierno siempre falla.", "a": "x", "v": 1},
    {"t": "La desigualdad económica es un motor de esfuerzo personal.", "a": "x", "v": 1},
    {"t": "Los paraísos fiscales deberían ser perseguidos penalmente.", "a": "x", "v": -1},
    {"t": "La deuda pública es una carga injusta para el futuro.", "a": "x", "v": 1},
    {"t": "El Estado debe controlar el precio de los alquileres.", "a": "x", "v": -1},
    {"t": "La privatización de carreteras mejora el transporte.", "a": "x", "v": 1},
    {"t": "El bienestar colectivo debe estar por encima del lucro individual.", "a": "x", "v": -1},
    {"t": "Pagar impuestos es una obligación patriótica y moral.", "a": "x", "v": -1},
    {"t": "La innovación solo ocurre bajo incentivos de mercado libre.", "a": "x", "v": 1},
    {"t": "El trabajo es un derecho que el Estado debe asegurar.", "a": "x", "v": -1},
    {"t": "Las criptomonedas no deberían ser reguladas por el Estado.", "a": "x", "v": 1},
    {"t": "Los subsidios al desempleo fomentan la vagancia.", "a": "x", "v": 1},
    {"t": "La banca debería ser nacionalizada.", "a": "x", "v": -1},
    {"t": "Los derechos de autor y patentes deben ser protegidos.", "a": "x", "v": 1},
    {"t": "El Estado gasta demasiado dinero en burocracia inútil.", "a": "x", "v": 1},
    {"t": "Las cooperativas son mejores que las empresas jerárquicas.", "a": "x", "v": -1},
    {"t": "El crecimiento económico infinito en un planeta finito es imposible.", "a": "x", "v": -1},
    {"t": "La bolsa de valores es solo un casino para ricos.", "a": "x", "v": -1},
    {"t": "El oro debería volver a ser la base del dinero.", "a": "x", "v": 1},
    {"t": "La publicidad comercial debería estar más regulada.", "a": "x", "v": -1},
    {"t": "La explotación de recursos naturales debe ser nacionalizada.", "a": "x", "v": -1},
    {"t": "El consumo excesivo es el principal problema del sistema actual.", "a": "x", "v": -1},
    {"t": "La austeridad fiscal es necesaria para una economía sana.", "a": "x", "v": 1},
    {"t": "Vender órganos debería ser legal si hay consentimiento.", "a": "x", "v": 1},

    # SOCIALES (42 preguntas)
    {"t": "El aborto debe ser legal, seguro y gratuito.", "a": "y", "v": -1},
    {"t": "La eutanasia es un derecho fundamental del individuo.", "a": "y", "v": -1},
    {"t": "Se necesita mano dura y más policía en las calles.", "a": "y", "v": 1},
    {"t": "Las tradiciones religiosas deben ser protegidas por el Estado.", "a": "y", "v": 1},
    {"t": "El consumo de marihuana debe ser totalmente legal.", "a": "y", "v": -1},
    {"t": "La cadena perpetua es un castigo justo.", "a": "y", "v": 1},
    {"t": "La identidad nacional es más importante que los derechos globales.", "a": "y", "v": 1},
    {"t": "El matrimonio solo puede existir entre hombre y mujer.", "a": "y", "v": 1},
    {"t": "La libertad de expresión debe permitir incluso el discurso de odio.", "a": "y", "v": -1},
    {"t": "La prostitución debería ser una actividad legal y regulada.", "a": "y", "v": -1},
    {"t": "La patria es un concepto sagrado.", "a": "y", "v": 1},
    {"t": "Las fronteras deberían ser eliminadas gradualmente.", "a": "y", "v": -1},
    {"t": "El servicio militar debería ser obligatorio.", "a": "y", "v": 1},
    {"t": "La educación sexual en niños debe ser decisión de los padres.", "a": "y", "v": 1},
    {"t": "La vigilancia masiva es necesaria para combatir el terrorismo.", "a": "y", "v": 1},
    {"t": "Quemar la bandera de tu país debería ser delito.", "a": "y", "v": 1},
    {"t": "Los criminales tienen demasiados derechos hoy en día.", "a": "y", "v": 1},
    {"t": "La experimentación con células madre debe ser libre.", "a": "y", "v": -1},
    {"t": "El Estado debe proteger la cultura nacional de influencias externas.", "a": "y", "v": 1},
    {"t": "Tener un arma para autodefensa es un derecho básico.", "a": "y", "v": -1},
    {"t": "La meritocracia es la forma más justa de organizar la sociedad.", "a": "y", "v": 1},
    {"t": "La religión solo hace daño a la sociedad moderna.", "a": "y", "v": -1},
    {"t": "El orden público es más importante que el derecho a manifestarse.", "a": "y", "v": 1},
    {"t": "La inmigración descontrolada destruye nuestra cultura.", "a": "y", "v": 1},
    {"t": "Un líder fuerte es mejor que una democracia débil.", "a": "y", "v": 1},
    {"t": "El Estado no debe meterse en lo que los adultos hacen en privado.", "a": "y", "v": -1},
    {"t": "La obediencia a la autoridad es una virtud que se ha perdido.", "a": "y", "v": 1},
    {"t": "Las cuotas de género en empresas son injustas.", "a": "y", "v": 1},
    {"t": "El arte ofensivo debería ser censurado o no subvencionado.", "a": "y", "v": 1},
    {"t": "La globalización ha sido un error histórico.", "a": "y", "v": 1},
    {"t": "La familia tradicional es la base de la civilización.", "a": "y", "v": 1},
    {"t": "La pornografía debería estar prohibida.", "a": "y", "v": 1},
    {"t": "La clonación humana debería ser permitida por la ciencia.", "a": "y", "v": -1},
    {"t": "El castigo físico a niños debería ser legal en el hogar.", "a": "y", "v": 1},
    {"t": "La tecnología nos está robando nuestra humanidad.", "a": "y", "v": 1},
    {"t": "El gobierno debería controlar los algoritmos de redes sociales.", "a": "y", "v": 1},
    {"t": "La libertad es más importante que la igualdad.", "a": "y", "v": -1},
    {"t": "No existe la verdad objetiva, todo es una construcción social.", "a": "y", "v": -1},
    {"t": "La pena de muerte debería aplicarse en casos extremos.", "a": "y", "v": 1},
    {"t": "Los antepasados y la historia deben ser venerados.", "a": "y", "v": 1},
    {"t": "La monogamia es un constructo opresivo.", "a": "y", "v": -1},
    {"t": "El Estado debería obligar a vacunar a toda la población.", "a": "y", "v": 1}
]

# 4. LÓGICA DE IDEOLOGÍAS (25 CATEGORÍAS)
def get_detailed_ideology(x, y):
    if y > 6:
        if x < -6: return "Marxismo-Leninismo", "Crees en un Estado total que dirija la economía y elimine las clases sociales por la fuerza si es necesario."
        if x < -2: return "Socialismo Nacionalista", "Economía controlada y un fuerte enfoque en la identidad nacional y el orden estatal."
        if x < 2: return "Totalitarismo Central", "El Estado es el eje de todo; buscas control absoluto tanto en lo moral como en lo material."
        if x < 6: return "Fascismo Clásico", "Unidad nacional, rechazo a la lucha de clases y un Estado autoritario que corporativiza la economía."
        return "Derecha Radical Autoritaria", "Capitalismo de Estado y represión social severa para mantener jerarquías tradicionales."
    elif y > 2:
        if x < -6: return "Socialismo de Estado", "Priorizas la igualdad económica mediante un gobierno fuerte que gestione los recursos."
        if x < -2: return "Populismo de Izquierda", "Protección del trabajador frente a las élites mediante el poder político del Estado."
        if x < 2: return "Estatismo", "Crees que el Estado debe ser el árbitro que regule el mercado y la conducta social."
        if x < 6: return "Conservadurismo", "Defensa de las instituciones tradicionales, el libre mercado y el orden público."
        return "Derecha Autoritaria", "Mercado muy libre pero con leyes sociales y policiales muy estrictas."
    elif y > -2:
        if x < -6: return "Socialismo Democrático", "Buscas la propiedad colectiva mediante procesos electorales y libertad de prensa."
        if x < -2: return "Socialdemocracia", "Capitalismo con altos impuestos para financiar un Estado de Bienestar potente."
        if x < 2: return "Centrismo", "Equilibrio pragmático entre libertad económica y justicia social."
        if x < 6: return "Liberalismo Moderno", "Libertad individual plena y un mercado dinámico con red de seguridad social."
        return "Liberalismo Clásico", "El Estado debe limitarse a proteger la vida, la libertad y la propiedad privada."
    elif y > -6:
        if x < -6: return "Anarcosindicalismo", "Sociedad organizada en sindicatos de trabajadores sin jefes ni Estado."
        if x < -2: return "Socialismo Libertario", "Crees en comunidades autogestionadas donde la propiedad es común pero la libertad es máxima."
        if x < 2: return "Geolibertarismo", "Libertad personal absoluta, pero los recursos naturales pertenecen a todos."
        if x < 6: return "Minarquismo", "El Estado solo debe existir para la policía y los jueces; el resto debe ser privado."
        return "Paleolibertarismo", "Libre mercado radical combinado con una moral personal conservadora voluntaria."
    else:
        if x < -6: return "Anarcocomunismo", "Abolición total del Estado y del dinero; vida en comunas voluntarias."
        if x < -2: return "Mutualismo", "Economía de mercado basada en el intercambio justo y cooperativas sin Estado."
        if x < 2: return "Anarquismo Individualista", "Soberanía absoluta del individuo frente a cualquier colectividad."
        if x < 6: return "Voluntarismo", "Toda relación humana debe ser consentida; el Estado es una agresión ilegítima."
        return "Anarcocapitalismo", "Privatización total de la sociedad. La ley y la seguridad deben ser servicios de mercado."

# 5. LÓGICA DE NAVEGACIÓN
if 'idx' not in st.session_state:
    st.session_state.update({'idx': 0, 'x': 0.0, 'y': 0.0})

def handle_click(p):
    q = questions[st.session_state.idx]
    # Factor para que el máximo sea 10 (2 pts * num_preguntas / factor = 10)
    num_x = len([q for q in questions if q['a'] == 'x'])
    num_y = len([q for q in questions if q['a'] == 'y'])
    
    if q['a'] == 'x': st.session_state.x += (p * q['v']) / (num_x / 5)
    else: st.session_state.y += (p * q['v']) / (num_y / 5)
    st.session_state.idx += 1

# --- UI: RESULTADOS ---
if st.session_state.idx >= len(questions):
    st.markdown('<h1 class="main-title">Tu Perfil Político</h1>', unsafe_allow_html=True)
    ux, uy = max(min(st.session_state.x, 10), -10), max(min(st.session_state.y, 10), -10)
    name, desc = get_detailed_ideology(ux, uy)
    
    st.markdown(f'<div class="result-bubble"><p class="ideology-title">{name}</p><p class="ideology-desc">{desc}</p></div>', unsafe_allow_html=True)
    
    # SVG GRÁFICO
    px, py = 200 + (ux * 18), 200 - (uy * 18)
    leaders_svg = "".join([f'<circle cx="{200+(l["x"]*18)}" cy="{200-(l["y"]*18)}" r="4" fill="{l["c"]}" stroke="black"/><text x="{200+(l["x"]*18)}" y="{200-(l["y"]*18)+12}" font-size="9" text-anchor="middle" font-family="Arial" font-weight="bold">{l["n"]}</text>' for l in LEADERS])
    
    svg_code = f"""
    <div style="text-align:center; background:white; padding:20px; border-radius:15px;">
        <svg width="400" height="400" viewBox="0 0 400 400" style="border:3px solid #333; font-family:Arial;">
            <rect width="200" height="200" fill="#FFB2B2" opacity="0.5"/><rect x="200" width="200" height="200" fill="#B2B2FF" opacity="0.5"/>
            <rect y="200" width="200" height="200" fill="#B2FFB2" opacity="0.5"/><rect x="200" y="200" width="200" height="200" fill="#FFFFB2" opacity="0.5"/>
            <line x1="200" y1="0" x2="200" y2="400" stroke="black" stroke-width="2"/><line x1="0" y1="200" x2="400" y2="200" stroke="black" stroke-width="2"/>
            <text x="340" y="215" font-weight="bold" font-size="12">DERECHA</text><text x="10" y="215" font-weight="bold" font-size="12">IZQUIERDA</text>
            <text x="210" y="20" font-weight="bold" font-size="12">AUTORITARIO</text><text x="210" y="390" font-weight="bold" font-size="12">LIBERTARIO</text>
            {leaders_svg}
            <circle cx="{px}" cy="{py}" r="8" fill="red" stroke="white" stroke-width="3"/><text x="{px}" y="{py-12}" fill="red" font-weight="900" text-anchor="middle">TÚ</text>
        </svg>
    </div>
    """
    components.html(svg_code, height=450)

    if st.button("🖨️ GUARDAR RESULTADOS (PDF)"):
        components.html("<script>window.print();</script>", height=0)
    if st.button("🔄 REPETIR EL TEST"):
        st.session_state.update({'idx': 0, 'x': 0.0, 'y': 0.0})
        st.rerun()

# --- UI: PREGUNTAS ---
else:
    st.markdown('<h1 class="main-title">Compás Político</h1>', unsafe_allow_html=True)
    
    if st.session_state.idx == 0:
        st.markdown('<p class="welcome-text">¡Hola! Vamos a descubrir dónde encajas en el mapa político. No hay respuestas malas, solo tu opinión sincera.</p>', unsafe_allow_html=True)
        st.markdown('<div class="warning-box">⚠️ Responde con honestidad. Si una pregunta no te queda clara o no tienes una opinión formada, dale a "Neutral".</div>', unsafe_allow_html=True)
    
    st.markdown(f'<span class="q-counter">Pregunta {st.session_state.idx + 1} de {len(questions)}</span>', unsafe_allow_html=True)
    st.progress(st.session_state.idx / len(questions))
    
    st.markdown(f'<div class="question-container"><p class="question-text">{questions[st.session_state.idx]["t"]}</p></div>', unsafe_allow_html=True)
    
    st.button("✅ Totalmente de acuerdo", on_click=handle_click, args=(2,))
    st.button("👍 De acuerdo", on_click=handle_click, args=(1,))
    st.button("😐 Neutral / No lo sé", on_click=handle_click, args=(0,))
    st.button("👎 En desacuerdo", on_click=handle_click, args=(-1,))
    st.button("❌ Totalmente en desacuerdo", on_click=handle_click, args=(-2,))
