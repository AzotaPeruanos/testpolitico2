import streamlit as st
import base64

# 1. ESTÉTICA DEFINITIVA: CENTRADO FORZADO Y PREGUNTAS GRANDES
st.set_page_config(page_title="Brújula Política Estudiantil", layout="centered")

st.markdown("""
    <style>
    /* Fondo Azul Claro */
    .stApp { background-color: #E3F2FD; color: #1565C0; }
    
    /* PREGUNTAS MÁS GRANDES */
    .question-text {
        text-align: center;
        font-size: 32px; /* Aumentado */
        font-weight: 800;
        color: #0D47A1;
        margin-bottom: 40px;
        padding: 20px;
        line-height: 1.2;
    }

    /* CONTENEDOR PARA CENTRAR BOTONES Y DARLES MISMA LONGITUD */
    div.stButton {
        text-align: center;
    }
    
    div.stButton > button {
        width: 100% !important;
        max-width: 550px !important; /* Longitud fija */
        margin-left: auto !important;
        margin-right: auto !important;
        border-radius: 50px !important;
        height: 4em !important;
        font-weight: bold !important;
        font-size: 20px !important;
        border: none !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1) !important;
        transition: 0.3s !important;
        display: block !important;
    }

    /* COLORES ACORDE A LA RESPUESTA */
    /* 1. Totalmente de acuerdo - Verde Oscuro */
    div.stButton:nth-of-type(2) > button { background: #1B5E20 !important; color: white !important; }
    /* 2. De acuerdo - Verde Claro */
    div.stButton:nth-of-type(3) > button { background: #81C784 !important; color: #052b08 !important; }
    /* 3. Neutral - Blanco */
    div.stButton:nth-of-type(4) > button { background: #FFFFFF !important; color: #1565C0 !important; border: 1px solid #BBDEFB !important; }
    /* 4. En desacuerdo - Rojo Claro */
    div.stButton:nth-of-type(5) > button { background: #EF9A9A !important; color: #7f0000 !important; }
    /* 5. Totalmente en desacuerdo - Rojo Oscuro */
    div.stButton:nth-of-type(6) > button { background: #B71C1C !important; color: white !important; }

    /* Botón Volver (distinto para no confundir) */
    div.stButton:last-of-type > button { 
        background: #546E7A !important; 
        color: white !important; 
        margin-top: 30px !important;
        max-width: 300px !important;
        font-size: 14px !important;
        height: 3em !important;
    }

    div.stButton > button:hover { transform: scale(1.02); box-shadow: 0 6px 15px rgba(0,0,0,0.2); }

    /* RESULTADOS */
    .result-card {
        background-color: white; padding: 40px; border-radius: 30px;
        text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin-bottom: 30px; border: 4px solid #1976D2;
    }
    .result-title { font-size: 45px; font-weight: 900; color: #0D47A1; }
    .result-desc { font-size: 22px; color: #455A64; }

    .map-container {
        position: relative; width: 450px; height: 450px; 
        margin: 20px auto; border: 8px solid white; border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2); overflow: hidden;
    }
    .dot { position: absolute; border-radius: 50%; border: 1px solid white; transform: translate(-50%, -50%); }
    .user-dot {
        width: 38px; height: 38px; background-color: #FF1744; z-index: 100;
        box-shadow: 0 0 20px #FF1744; border: 4px solid white; color: white;
        display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: bold;
    }
    .legend-box {
        background: white; padding: 15px; border-radius: 15px;
        display: flex; flex-wrap: wrap; justify-content: center; gap: 15px;
        margin-top: 20px; border: 1px solid #BBDEFB;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. MOTOR Y LÍDERES
if 'idx' not in st.session_state:
    st.session_state.update({'idx': 0, 'x': 0.0, 'y': 0.0, 'hist': []})

def responder(m):
    radical = (m ** 3) * 5.5 
    q = questions[st.session_state.idx]
    val = radical * q["v"]
    if q["a"] == "x": st.session_state.x += val
    else: st.session_state.y += val
    st.session_state.hist.append((val if q["a"]=="x" else 0, val if q["a"]=="y" else 0))
    st.session_state.idx += 1

LEADERS = [
    {"n": "Milei", "x": 170, "y": -160, "c": "#FFD600"},
    {"n": "Stalin", "x": -190, "y": 190, "c": "#D32F2F"},
    {"n": "Hitler", "x": 180, "y": 195, "c": "#37474F"},
    {"n": "Mao", "x": -195, "y": 175, "c": "#F44336"},
    {"n": "Gandhi", "x": -130, "y": -170, "c": "#4CAF50"},
    {"n": "Rothbard", "x": 198, "y": -198, "c": "#FF9800"},
    {"n": "Thatcher", "x": 150, "y": 110, "c": "#1976D2"},
    {"n": "Castro", "x": -165, "y": 140, "c": "#2E7D32"}
]

# 3. 85 PREGUNTAS (Simplificadas)
questions = [
    {"t": "Cualquier persona debería poder abrir un negocio sin que el gobierno le ponga muchas reglas.", "a": "x", "v": 1},
    {"t": "Los hospitales deberían ser siempre gratis y pagados con nuestros impuestos.", "a": "x", "v": -1},
    {"t": "El gobierno debería poner un límite al precio del alquiler de los pisos.", "a": "x", "v": -1},
    {"t": "Es mejor que la electricidad sea vendida por empresas privadas que por el gobierno.", "a": "x", "v": 1},
    {"t": "La gente que tiene mucho dinero debería pagar muchísimos más impuestos que el resto.", "a": "x", "v": -1},
    {"t": "Es mejor comprar productos fabricados aquí que traerlos de otros países.", "a": "x", "v": -1},
    {"t": "No debería existir un sueldo mínimo; cada uno debería pactar lo que cobra.", "a": "x", "v": 1},
    {"t": "Cuidar el planeta es más importante que ganar mucho dinero como país.", "a": "x", "v": -1},
    {"t": "El gobierno no debería dar dinero (ayudas) a ninguna empresa privada.", "a": "x", "v": 1},
    {"t": "Si mis padres mueren, todo su dinero debería ser mío sin pagar impuestos al estado.", "a": "x", "v": 1},
    {"t": "Ir a la universidad debería ser totalmente gratis para todo el mundo.", "a": "x", "v": -1},
    {"t": "Si las empresas compiten entre ellas, los servicios serán mejores para nosotros.", "a": "x", "v": 1},
    {"t": "El gobierno debe asegurar que todo el mundo tenga un trabajo.", "a": "x", "v": -1},
    {"t": "Nadie tiene derecho a quitarle nada a una persona si es su propiedad privada.", "a": "x", "v": 1},
    {"t": "Los bancos centrales (que fabrican el dinero) deberían desaparecer.", "a": "x", "v": 1},
    {"t": "El agua y la luz son tan básicas que el gobierno debería controlarlas siempre.", "a": "x", "v": -1},
    {"t": "Comprar y vender cosas con todo el mundo ayuda a que haya menos pobreza.", "a": "x", "v": 1},
    {"t": "Debería estar prohibido ganar dinero solo apostando en la bolsa.", "a": "x", "v": -1},
    {"t": "Que el gobierno gaste mucho dinero es lo que crea las crisis.", "a": "x", "v": 1},
    {"t": "Las personas ayudan mejor a los pobres que el gobierno.", "a": "x", "v": 1},
    {"t": "Los países que no cobran impuestos (paraísos fiscales) son algo justo.", "a": "x", "v": 1},
    {"t": "El gobierno debe ayudar con dinero a las empresas grandes si van a quebrar.", "a": "x", "v": -1},
    {"t": "Para que un país vaya bien, hay que gastar menos de lo que se gana.", "a": "x", "v": 1},
    {"t": "Es normal que haya gente rica y pobre; es lo que hace que la gente se esfuerce.", "a": "x", "v": 1},
    {"t": "Los sindicatos (grupos de trabajadores) tienen demasiado poder hoy en día.", "a": "x", "v": 1},
    {"t": "El dinero debería valer por el oro que tenga el país, no por lo que diga el gobierno.", "a": "x", "v": 1},
    {"t": "Como las máquinas harán los trabajos, el gobierno debería darnos un sueldo a todos.", "a": "x", "v": -1},
    {"t": "Las medicinas deberían ser de todos y no tener dueño ni patente.", "a": "x", "v": -1},
    {"t": "Comprar muchas cosas es bueno para que la sociedad sea feliz.", "a": "x", "v": 1},
    {"t": "Por ley, nadie debería trabajar más de 30 horas a la semana.", "a": "x", "v": -1},
    {"t": "Obedecer a los que mandan es una lección que todos los niños deben aprender.", "a": "y", "v": 1},
    {"t": "Cualquier mujer debería poder decidir si quiere abortar gratis.", "a": "y", "v": -1},
    {"t": "La religión no debería decirnos qué leyes hay que poner.", "a": "y", "v": -1},
    {"t": "Hace falta un jefe fuerte que mande con mano dura para que el país funcione.", "a": "y", "v": 1},
    {"t": "Cada uno debería poder drogarse si quiere, es su propia vida.", "a": "y", "v": -1},
    {"t": "Los criminales peligrosos no deberían salir nunca de la cárcel.", "a": "y", "v": 1},
    {"t": "El ejército debería vigilar las fronteras para que nadie entre sin permiso.", "a": "y", "v": 1},
    {"t": "La lucha de las mujeres por la igualdad es totalmente justa hoy.", "a": "y", "v": -1},
    {"t": "El gobierno puede espiarnos si es para evitar ataques terroristas.", "a": "y", "v": 1},
    {"t": "Cada uno puede decir lo que quiera, aunque alguien se sienta insultado.", "a": "y", "v": -1},
    {"t": "Si alguien está muy enfermo y quiere morir, el médico debería ayudarle.", "a": "y", "v": -1},
    {"t": "Todos los jóvenes deberían hacer el servicio militar obligatorio.", "a": "y", "v": 1},
    {"t": "La familia de padre y madre es la mejor base para la sociedad.", "a": "y", "v": 1},
    {"t": "Ver películas para adultos (porno) debería estar prohibido.", "a": "y", "v": 1},
    {"t": "Nadie debería prohibir una obra de arte, aunque sea fea o rara.", "a": "y", "v": -1},
    {"t": "La pena de muerte está bien para castigar los peores crímenes.", "a": "y", "v": 1},
    {"t": "Que venga mucha gente de otros países hace que nuestra cultura se pierda.", "a": "y", "v": 1},
    {"t": "El matrimonio solo puede ser entre un hombre y una mujer.", "a": "y", "v": 1},
    {"t": "Debería estar prohibido cortar las calles para hacer manifestaciones.", "a": "y", "v": 1},
    {"t": "Uno no nace hombre o mujer, sino que se siente lo que quiere ser.", "a": "y", "v": -1},
    {"t": "La monarquía (reyes) es algo antiguo que ya no debería existir.", "a": "y", "v": -1},
    {"t": "La policía necesita más poder y que no les castiguen tanto por actuar.", "a": "y", "v": 1},
    {"t": "Aprender sobre sexo en el colegio es muy importante para los niños.", "a": "y", "v": -1},
    {"t": "Insultar a la religión no debería ser un delito castigado por la ley.", "a": "y", "v": -1},
    {"t": "La bandera de nuestro país es lo más sagrado que tenemos.", "a": "y", "v": 1},
    {"t": "Los científicos deberían poder crear humanos iguales (clones) para curar enfermedades.", "a": "y", "v": -1},
    {"t": "Hoy en día no se puede decir nada sin que alguien se ofenda, y eso es malo.", "a": "y", "v": 1},
    {"t": "Mezclar muchas culturas en un solo barrio nunca sale bien.", "a": "y", "v": 1},
    {"t": "Es necesario probar medicinas con animales para salvar a personas.", "a": "y", "v": 1},
    {"t": "El gobierno debería dar dinero a la gente para que tenga más hijos.", "a": "y", "v": 1},
    {"t": "Bajarse películas o música de internet sin pagar no es un robo de verdad.", "a": "y", "v": -1},
    {"t": "En el colegio debería haber mucha más disciplina y respeto al profesor.", "a": "y", "v": 1},
    {"t": "El gobierno debe controlar la Inteligencia Artificial antes de que sea peligrosa.", "a": "y", "v": 1},
    {"t": "La energía nuclear es la mejor forma de no contaminar el aire.", "a": "x", "v": 1},
    {"t": "Los animales deberían tener los mismos derechos legales que las personas.", "a": "y", "v": -1},
    {"t": "Llegar al espacio deberían hacerlo empresas privadas, no el gobierno.", "a": "x", "v": 1},
    {"t": "Dar dinero público para el cine o el teatro es tirar el dinero.", "a": "x", "v": 1},
    {"t": "El mundo está tan conectado que estamos perdiendo nuestras costumbres.", "a": "y", "v": 1},
    {"t": "El capitalismo está rompiendo el planeta poco a poco.", "a": "x", "v": -1},
    {"t": "Deberíamos votar todas las leyes por internet desde casa.", "a": "y", "v": -1},
    {"t": "La cárcel tiene que ser para que el malo sufra, no para que aprenda.", "a": "y", "v": 1},
    {"t": "Si eres rico es porque te has esforzado más que el que es pobre.", "a": "x", "v": 1},
    {"t": "Internet debería ser gratis para todo el mundo porque es un derecho.", "a": "x", "v": -1},
    {"t": "Debería haber clases de religión obligatorias en todos los colegios.", "a": "y", "v": 1},
    {"t": "Nuestro ejército debería poder ir a otros países si es para salvar vidas.", "a": "y", "v": 1},
    {"t": "Las monedas digitales (Bitcoins) son el futuro de la libertad.", "a": "x", "v": 1},
    {"t": "Es justo que el jefe gane mil veces más que el que limpia la oficina.", "a": "x", "v": 1},
    {"t": "El gobierno debería prohibir la comida basura para que no estemos gordos.", "a": "y", "v": 1},
    {"t": "Tener vecinos de muchas razas distintas hace que un país sea mejor.", "a": "y", "v": -1},
    {"t": "Las huelgas solo sirven para que el país pierda dinero y tiempo.", "a": "x", "v": 1},
    {"t": "La tecnología nos está volviendo tontos y menos humanos.", "a": "y", "v": 1},
    {"t": "Los multimillonarios deberían dar casi todo su dinero al estado.", "a": "x", "v": -1},
    {"t": "Habría que prohibir los coches de gasolina muy pronto.", "a": "x", "v": -1},
    {"t": "Sin alguien que mande y ponga orden, la gente se portaría fatal.", "a": "y", "v": 1},
    {"t": "Cualquier tiempo pasado fue mucho mejor que el de ahora.", "a": "y", "v": 1}
]

# --- LÓGICA DE PANTALLAS ---
if st.session_state.idx >= len(questions):
    x, y = st.session_state.x, st.session_state.y
    
    if x > 100 and y > 100: n, d = "DERECHA AUTORITARIA", "Crees en un país con mucha ley y orden, donde el mercado es libre pero la autoridad manda."
    elif x < -100 and y > 100: n, d = "IZQUIERDA AUTORITARIA", "Crees que el gobierno debe controlar la economía para que todos sean iguales."
    elif x > 100 and y < -100: n, d = "LIBERALISMO RADICAL", "Para ti, la libertad individual es lo primero. El gobierno no debe meterse en nada."
    elif x < -100 and y < -100: n, d = "IZQUIERDA LIBERTARIA", "Buscas un mundo sin jefes ni gobiernos, donde la gente se ayude voluntariamente."
    else: n, d = "CENTRO POLÍTICO", "Eres una persona equilibrada. Prefieres soluciones moderadas para los problemas."

    st.markdown(f"""
        <div class="result-card">
            <div class="result-title">{n}</div>
            <div class="result-desc">{d}</div>
        </div>
    """, unsafe_allow_html=True)

    def get_b64(f):
        try:
            with open(f, "rb") as b: return base64.b64encode(b.read()).decode()
        except: return ""

    img_data = get_b64("chart.png")
    l_html = ""
    for l in LEADERS:
        lx = 50 + (l["x"] * 0.23); ly = 50 - (l["y"] * 0.23)
        l_html += f'<div class="dot leader-dot" style="left:{lx}%; top:{ly}%; background:{l["c"]};"></div>'

    ux = 50 + (x * 0.23); uy = 50 - (y * 0.23)
    ux, uy = max(5, min(95, ux)), max(5, min(95, uy))
    
    st.markdown(f"""
        <div class="map-container">
            <img src="data:image/png;base64,{img_data}" style="width:100%; height:100%;">
            {l_html}
            <div class="dot user-dot" style="left:{ux}%; top:{uy}%;">Tú</div>
        </div>
    """, unsafe_allow_html=True)

    l_items = "".join([f'<div style="display:flex; align-items:center; font-size:14px; font-weight:bold;"><div style="width:12px; height:12px; border-radius:50%; background:{l["c"]}; margin-right:5px;"></div>{l["n"]}</div>' for l in LEADERS])
    st.markdown(f'<div class="legend-box">{l_items}</div>', unsafe_allow_html=True)

    if st.button("📄 GUARDAR PDF"):
        st.components.v1.html("<script>window.print();</script>", height=0)
    
    if st.button("🔄 REPETIR"):
        st.session_state.update({'idx':0, 'x':0, 'y':0, 'hist':[]})
        st.rerun()

else:
    st.progress(st.session_state.idx / len(questions))
    st.markdown(f'<div class="question-text">{questions[st.session_state.idx]["t"]}</div>', unsafe_allow_html=True)
    
    # BOTONES EN BLOQUE PARA FORZAR EL CENTRADO CSS
    st.button("Totalmente de acuerdo", on_click=responder, args=(2,))
    st.button("De acuerdo", on_click=responder, args=(1,))
    st.button("No estoy seguro / Neutral", on_click=responder, args=(0,))
    st.button("En desacuerdo", on_click=responder, args=(-1,))
    st.button("Totalmente en desacuerdo", on_click=responder, args=(-2,))

    if st.session_state.idx > 0:
        if st.button("⬅️ VOLVER A LA PREGUNTA ANTERIOR"):
            px, py = st.session_state.hist.pop()
            st.session_state.x -= px; st.session_state.y -= py
            st.session_state.idx -= 1
            st.rerun()
