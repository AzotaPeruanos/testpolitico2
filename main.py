import streamlit as st
import streamlit.components.v1 as components

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Compás Político Estudiantil", layout="centered")

# 2. CSS PARA CENTRADO Y BOTONES UNIFORMES
st.markdown("""
    <style>
    .stApp { background-color: #F8FAFC; }
    .main-title { text-align: center; color: #1E3A8A; font-size: 35px; font-weight: 800; margin-bottom: 20px; }
    .question-text { 
        text-align: center; 
        font-size: 24px !important; 
        font-weight: 700; 
        color: #1E40AF; 
        margin: 25px 0;
        min-height: 60px;
    }
    /* Forzar que todos los botones de la columna central sean iguales */
    div.stButton > button {
        width: 100% !important;
        height: 50px !important;
        border-radius: 10px !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        background-color: #EBF8FF !important;
        color: #2C5282 !important;
        border: 2px solid #BEE3F8 !important;
        margin-bottom: 5px !important;
    }
    div.stButton > button:hover {
        background-color: #BEE3F8 !important;
        border-color: #90CDF4 !important;
    }
    /* Estilo para el contenedor de resultados */
    .result-box {
        background: white;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        text-align: center;
        border: 1px solid #E2E8F0;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. BASE DE DATOS DE LÍDERES (25)
LEADERS = [
    {"n": "Stalin", "x": -9, "y": 9, "c": "#C0392B"}, {"n": "Hitler", "x": 8, "y": 9, "c": "#2D3748"},
    {"n": "Mao", "x": -9.5, "y": 8, "c": "#C0392B"}, {"n": "Mussolini", "x": 7, "y": 8.5, "c": "#2D3748"},
    {"n": "Pinochet", "x": 8.5, "y": 7, "c": "#2D3748"}, {"n": "Fidel Castro", "x": -7, "y": 6, "c": "#1E8449"},
    {"n": "Kim Jong-un", "x": -9, "y": 9.5, "c": "#C0392B"}, {"n": "Thatcher", "x": 7, "y": 6, "c": "#2980B9"},
    {"n": "Obama", "x": 2, "y": 2, "c": "#3182CE"}, {"n": "Merkel", "x": 3, "y": 2.5, "c": "#3182CE"},
    {"n": "Macron", "x": 3, "y": 1.5, "c": "#3182CE"}, {"n": "Mandela", "x": -2.5, "y": -3, "c": "#48BB78"},
    {"n": "Lula", "x": -4, "y": 1.5, "c": "#E53E3E"}, {"n": "Gandhi", "x": -6.5, "y": -7, "c": "#48BB78"},
    {"n": "Chomsky", "x": -8.5, "y": -8, "c": "#48BB78"}, {"n": "Sanders", "x": -5, "y": -2, "c": "#4299E1"},
    {"n": "Kropotkin", "x": -9.5, "y": -9.5, "c": "#1A202C"}, {"n": "Friedman", "x": 7.5, "y": -6, "c": "#D69E2E"},
    {"n": "Milei", "x": 9, "y": -9, "c": "#ECC94B"}, {"n": "Rothbard", "x": 10, "y": -10, "c": "#D69E2E"},
    {"n": "Hayek", "x": 8, "y": -5, "c": "#D69E2E"}, {"n": "Locke", "x": 4.5, "y": -4, "c": "#D69E2E"},
    {"n": "Jefferson", "x": 5, "y": -7, "c": "#D69E2E"}, {"n": "Bakunin", "x": -9, "y": -9, "c": "#1A202C"},
    {"n": "Churchill", "x": 6, "y": 5, "c": "#2980B9"}
]

# 4. TODAS LAS PREGUNTAS (85)
questions = [
    # ECONÓMICAS (X)
    {"t": "El gobierno no debería decir a las empresas cuánto pagar.", "a": "x", "v": 1},
    {"t": "La sanidad debería ser gratis y pagada con impuestos.", "a": "x", "v": -1},
    {"t": "El Estado debería ser el dueño de empresas de luz y agua.", "a": "x", "v": -1},
    {"t": "Es mejor que los colegios sean privados para que compitan.", "a": "x", "v": 1},
    {"t": "Los que más ganan deben pagar muchos más impuestos.", "a": "x", "v": -1},
    {"t": "El gobierno debería poner límites al precio de la comida.", "a": "x", "v": -1},
    {"t": "Si una empresa va a quebrar, el gobierno no debe ayudarla.", "a": "x", "v": 1},
    {"t": "Es mejor comprar productos nacionales que importados.", "a": "x", "v": -1},
    {"t": "Abrir un negocio debería ser posible sin tantos permisos.", "a": "x", "v": 1},
    {"t": "Las huelgas hacen más daño que bien a la economía.", "a": "x", "v": 1},
    {"t": "El gobierno debe asegurar que todo el mundo tenga casa.", "a": "x", "v": -1},
    {"t": "El libre mercado es la mejor forma de que un país progrese.", "a": "x", "v": 1},
    {"t": "Hacerse rico es un mérito; el Estado no debe quitarte dinero.", "a": "x", "v": 1},
    {"t": "Los sindicatos tienen demasiado poder hoy en día.", "a": "x", "v": 1},
    {"t": "El transporte público debería ser totalmente gratuito.", "a": "x", "v": -1},
    {"t": "La competencia entre empresas baja los precios siempre.", "a": "x", "v": 1},
    {"t": "El Estado debería dar un sueldo básico a todos por igual.", "a": "x", "v": -1},
    {"t": "Los bancos no deberían cobrar intereses abusivos.", "a": "x", "v": -1},
    {"t": "Las herencias familiares no deberían tener impuestos.", "a": "x", "v": 1},
    {"t": "Los servicios públicos funcionan peor que los privados.", "a": "x", "v": 1},
    {"t": "Prohibiría despedir a gente si la empresa gana dinero.", "a": "x", "v": -1},
    {"t": "Los paraísos fiscales deberían estar prohibidos.", "a": "x", "v": -1},
    {"t": "El capitalismo es el sistema más justo para prosperar.", "a": "x", "v": 1},
    {"t": "Las grandes fortunas deberían repartirse entre los pobres.", "a": "x", "v": -1},
    {"t": "Si te esfuerzas más, es justo que ganes mucho más dinero.", "a": "x", "v": 1},
    {"t": "No debería haber impuestos especiales para la gasolina.", "a": "x", "v": 1},
    {"t": "Cualquier medicina debería ser gratis para quien la use.", "a": "x", "v": -1},
    {"t": "Bajar impuestos es mejor que dar ayudas públicas.", "a": "x", "v": 1},
    {"t": "El gobierno debe evitar que una empresa controle todo.", "a": "x", "v": -1},
    {"t": "Las multas a empresas que engañan deben ser altísimas.", "a": "x", "v": -1},
    {"t": "La propiedad privada es sagrada e intocable.", "a": "x", "v": 1},
    {"t": "El gobierno debería crear fábricas para dar empleo.", "a": "x", "v": -1},
    {"t": "El Banco Central hace que el dinero pierda su valor.", "a": "x", "v": 1},
    {"t": "Es natural que unos tengan mucho más dinero que otros.", "a": "x", "v": 1},
    {"t": "Gastar dinero público en cultura es un error.", "a": "x", "v": 1},
    {"t": "Leyes ambientales frenan el crecimiento económico.", "a": "x", "v": 1},
    {"t": "Bajar impuestos a los ricos crea empleo para todos.", "a": "x", "v": 1},
    {"t": "Las máquinas que sustituyen humanos deben pagar tasas.", "a": "x", "v": -1},
    {"t": "El Estado no debería pedir préstamos a futuro.", "a": "x", "v": 1},
    {"t": "El precio del alquiler debe estar regulado por ley.", "a": "x", "v": -1},
    {"t": "Vender órganos debería ser legal si hay acuerdo mutuo.", "a": "x", "v": 1},
    {"t": "El Estado gasta demasiado en políticos y burocracia.", "a": "x", "v": 1},
    {"t": "Tener riqueza acumulada excesiva debería ser ilegal.", "a": "x", "v": -1},
    # SOCIALES (Y)
    {"t": "La disciplina y obediencia son lo más importante.", "a": "y", "v": 1},
    {"t": "La libertad de expresión debe ser total y absoluta.", "a": "y", "v": -1},
    {"t": "Hace falta mucha más presencia policial en las calles.", "a": "y", "v": 1},
    {"t": "El aborto debe ser una decisión libre de la mujer.", "a": "y", "v": -1},
    {"t": "Un país necesita un líder fuerte para funcionar bien.", "a": "y", "v": 1},
    {"t": "La religión no tiene sitio en la política moderna.", "a": "y", "v": -1},
    {"t": "Gastar más dinero en el ejército es una prioridad.", "a": "y", "v": 1},
    {"t": "La eutanasia (muerte digna) debe ser legal.", "a": "y", "v": -1},
    {"t": "El gobierno debería poder controlar lo que hay en internet.", "a": "y", "v": 1},
    {"t": "Lo que haga un adulto en su casa no es asunto del Estado.", "a": "y", "v": -1},
    {"t": "Nuestra cultura nacional es superior a otras.", "a": "y", "v": 1},
    {"t": "La familia tradicional es la base de una buena sociedad.", "a": "y", "v": 1},
    {"t": "Las cámaras de vigilancia nos hacen sentir más seguros.", "a": "y", "v": 1},
    {"t": "Se debe legalizar el consumo de marihuana.", "a": "y", "v": -1},
    {"t": "Hay que cerrar o endurecer mucho las fronteras.", "a": "y", "v": 1},
    {"t": "La bandera es el símbolo más sagrado de un país.", "a": "y", "v": 1},
    {"t": "Cortar carreteras en protestas debe ser castigado con cárcel.", "a": "y", "v": 1},
    {"t": "Las tradiciones religiosas deben ser la base moral.", "a": "y", "v": 1},
    {"t": "El Estado no debería pedir documentos para todo.", "a": "y", "v": -1},
    {"t": "La cadena perpetua es necesaria para delitos graves.", "a": "y", "v": 1},
    {"t": "El orden es más importante que los derechos individuales.", "a": "y", "v": 1},
    {"t": "La justicia protege demasiado a los delincuentes.", "a": "y", "v": 1},
    {"t": "Los hijos pertenecen a los padres, no al Estado.", "a": "y", "v": 1},
    {"t": "Quemar la bandera debería ser un delito grave.", "a": "y", "v": 1},
    {"t": "El acceso a la pornografía debe estar muy controlado.", "a": "y", "v": 1},
    {"t": "Las cuotas de género en el trabajo son injustas.", "a": "y", "v": 1},
    {"t": "El servicio militar debería volver a ser obligatorio.", "a": "y", "v": 1},
    {"t": "La policía debe poder registrar casas sin orden judicial.", "a": "y", "v": 1},
    {"t": "No debe haber educación sexual en los colegios.", "a": "y", "v": 1},
    {"t": "Insultar a las religiones debe estar castigado.", "a": "y", "v": 1},
    {"t": "La globalización destruye nuestra identidad nacional.", "a": "y", "v": 1},
    {"t": "Experimentar con células madre debe ser libre.", "a": "y", "v": -1},
    {"t": "La autoridad del profesor en clase debe ser absoluta.", "a": "y", "v": 1},
    {"t": "El arte moderno a veces es una falta de respeto.", "a": "y", "v": 1},
    {"t": "Las cárceles deben ser lugares de castigo duro.", "a": "y", "v": 1},
    {"t": "Prohibiría el tabaco por completo si pudiera.", "a": "y", "v": 1},
    {"t": "La unidad del país es lo más sagrado que existe.", "a": "y", "v": 1},
    {"t": "El Estado debe premiar a quienes tengan muchos hijos.", "a": "y", "v": 1},
    {"t": "Las redes sociales nos están volviendo maleducados.", "a": "y", "v": 1},
    {"t": "Debería ser legal tener armas en casa para defensa.", "a": "y", "v": -1},
    {"t": "Nuestros antepasados y su historia son sagrados.", "a": "y", "v": 1},
    {"t": "Un buen ciudadano obedece la ley sin cuestionarla.", "a": "y", "v": 1}
]

# 5. LÓGICA DE ESTADO
if 'idx' not in st.session_state:
    st.session_state.update({'idx': 0, 'x': 0.0, 'y': 0.0, 'hist': []})

def responder(puntos):
    q = questions[st.session_state.idx]
    # Factor de escala para que el máximo sea +/- 10
    total_x = 43 # Preguntas X
    total_y = 42 # Preguntas Y
    factor = (10 / (total_x * 2)) if q["a"] == "x" else (10 / (total_y * 2))
    
    val = puntos * q["v"] * factor * 2 
    if q["a"] == "x": st.session_state.x += val
    else: st.session_state.y += val
    st.session_state.hist.append((val if q["a"]=="x" else 0, val if q["a"]=="y" else 0))
    st.session_state.idx += 1

# 6. LÓGICA DE IDEOLOGÍAS (30)
def get_ideology(x, y):
    if y > 7:
        if x < -7: return "Totalitarismo Estalinista", "Control total del estado y economía colectiva."
        if x > 7: return "Fascismo Clerical", "Nacionalismo extremo con bases religiosas y corporativistas."
        if x > 3: return "Nacional-Conservadurismo", "Defensa férrea de la nación y valores tradicionales."
        return "Autoritarismo de Estado", "Primacía del orden gubernamental sobre todo."
    if y < -7:
        if x < -7: return "Anarco-Comunismo", "Sociedad sin clases ni estado basada en comunas."
        if x > 7: return "Anarco-Capitalismo", "Soberanía individual total y mercado sin estado."
        if x > 4: return "Agorismo", "Libertarismo centrado en la contra-economía."
        return "Libertarismo Radical", "Oposición máxima a cualquier interferencia estatal."
    if x < -7:
        if y > 3: return "Socialismo de Estado", "Economía planificada con control social moderado."
        if y < -3: return "Socialismo Libertario", "Igualdad económica mediante gestión comunitaria."
        return "Socialismo Puro", "Propiedad pública de los medios de producción."
    if x > 7:
        if y > 3: return "Derecha Conservadora", "Libre mercado con leyes sociales estrictas."
        if y < -3: return "Minarquismo", "Estado reducido solo a justicia y seguridad."
        return "Neoliberalismo", "Apertura económica total y mínima regulación."
    if abs(x) < 1.5 and abs(y) < 1.5: return "Centrismo Puro", "Postura moderada y pragmática."
    if x < 0:
        if y > 3: return "Populismo de Izquierda", "Discurso social fuerte con control del estado."
        if y < -3: return "Progresismo Radical", "Reformas sociales profundas y libertades civiles."
        return "Socialdemocracia", "Capitalismo con fuertes servicios públicos."
    if x > 0:
        if y > 3: return "Conservadurismo Social", "Tradición religiosa y libre mercado."
        if y < -3: return "Liberalismo Progresista", "Mercado libre con libertades individuales amplias."
        return "Liberalismo Clásico", "Derechos individuales y economía de mercado."
    return "Social-Liberalismo", "Equilibrio entre mercado y bienestar social."

# --- INTERFAZ: PANTALLA RESULTADOS ---
if st.session_state.idx >= len(questions):
    st.markdown('<div class="main-title">Tu Perfil Político</div>', unsafe_allow_html=True)
    
    xf = max(-10, min(10, st.session_state.x))
    yf = max(-10, min(10, st.session_state.y))
    title, desc = get_ideology(xf, yf)

    st.markdown(f"""
        <div class="result-box">
            <h1 style="color:#1E40AF; margin:0;">{title}</h1>
            <hr style="width:50%; margin:15px auto; border:1px solid #E2E8F0;">
            <p style="font-size:18px; color:#475569;">{desc}</p>
        </div>
    """, unsafe_allow_html=True)

    # GRÁFICO 600px
    dots = "".join([f'<div class="dot" style="left:{50+(l["x"]*5)}%; top:{50-(l["y"]*5)}%; background:{l["c"]};" title="{l["n"]}"></div>' for l in LEADERS])
    
    chart_html = f"""
    <div style="display:flex; justify-content:center; margin: 30px 0;">
        <div style="position:relative; width:600px; height:600px; background:white; border:3px solid #000; overflow:hidden;">
            <div style="position:absolute; width:50%; height:50%; top:0; left:0; background:rgba(255,0,0,0.15);"></div>
            <div style="position:absolute; width:50%; height:50%; top:0; right:0; background:rgba(0,0,255,0.15);"></div>
            <div style="position:absolute; width:50%; height:50%; bottom:0; left:0; background:rgba(0,255,0,0.15);"></div>
            <div style="position:absolute; width:50%; height:50%; bottom:0; right:0; background:rgba(255,255,0,0.15);"></div>
            <div style="position:absolute; width:100%; height:2px; top:50%; background:#000;"></div>
            <div style="position:absolute; width:2px; height:100%; left:50%; background:#000;"></div>
            <style>
                .dot {{ position: absolute; width: 10px; height: 10px; border-radius: 50%; border: 1px solid #fff; transform: translate(-50%, -50%); }}
                .user {{ position: absolute; width: 26px; height: 26px; background: red; border: 4px solid white; border-radius: 50%; transform: translate(-50%, -50%); z-index: 10; box-shadow: 0 0 10px red; }}
                .label {{ position: absolute; font-size: 11px; font-weight: bold; color: #000; transform: translate(-50%, 10px); width: 60px; text-align: center; }}
            </style>
            {dots}
            <div class="user" style="left:{50+(xf*5)}%; top:{50-(yf*5)}%;"></div>
            <div style="position:absolute; top:10px; left:41%; font-weight:bold;">AUTORITARIO</div>
            <div style="position:absolute; bottom:10px; left:42%; font-weight:bold;">LIBERTARIO</div>
            <div style="position:absolute; top:48%; left:5px; font-weight:bold;">IZQUIERDA</div>
            <div style="position:absolute; top:48%; right:5px; font-weight:bold;">DERECHA</div>
        </div>
    </div>
    """
    components.html(chart_html, height=650)
    
    if st.button("🔄 REPETIR EL TEST"):
        st.session_state.update({'idx': 0, 'x': 0.0, 'y': 0.0, 'hist': []})
        st.rerun()

# --- INTERFAZ: PANTALLA PREGUNTAS ---
else:
    st.markdown('<div class="main-title">Compás Político Estudiantil</div>', unsafe_allow_html=True)
    st.progress(st.session_state.idx / len(questions))
    st.write(f"<p style='text-align:center;'>Pregunta {st.session_state.idx + 1} de {len(questions)}</p>", unsafe_allow_html=True)
    
    st.markdown(f'<div class="question-text">{questions[st.session_state.idx]["t"]}</div>', unsafe_allow_html=True)
    
    # Columna central para botones uniformes
    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        st.button("✅ Totalmente de acuerdo", on_click=responder, args=(2,))
        st.button("👍 De acuerdo", on_click=responder, args=(1,))
        st.button("😐 Neutral / No lo sé", on_click=responder, args=(0,))
        st.button("👎 En desacuerdo", on_click=responder, args=(-1,))
        st.button("❌ Totalmente en desacuerdo", on_click=responder, args=(-2,))

        if st.session_state.idx > 0:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("⬅️ VOLVER A LA PREGUNTA ANTERIOR"):
                px, py = st.session_state.hist.pop()
                st.session_state.x -= px
                st.session_state.y -= py
                st.session_state.idx -= 1
                st.rerun()
