import streamlit as st

# 1. CONFIGURACIÓN Y ESTILO INYECTADO (Blindado)
st.set_page_config(page_title="Brújula Política Pro", layout="centered")

st.markdown("""
    <style>
    /* Fondo y Contenedor Principal */
    .stApp { background-color: #E3F2FD !important; }
    
    /* Preguntas: Centradas y Grandes */
    .stMarkdown div p {
        text-align: center !important;
        font-size: 28px !important;
        font-weight: 800 !important;
        color: #0D47A1 !important;
        padding: 20px 0 !important;
    }

    /* BOTONES DE RESPUESTA: Forzar mismo ancho y colores */
    div.stButton > button {
        width: 100% !important;
        height: 60px !important;
        border-radius: 30px !important;
        font-weight: bold !important;
        font-size: 18px !important;
        border: none !important;
        margin: 5px 0 !important;
        display: block !important;
    }

    /* Colores en Inglés para evitar errores de renderizado */
    /* Botón 1: Totalmente de Acuerdo */
    div[data-testid="stVerticalBlock"] > div:nth-child(2) button { background-color: green !important; color: white !important; }
    /* Botón 2: De Acuerdo */
    div[data-testid="stVerticalBlock"] > div:nth-child(3) button { background-color: lightgreen !important; color: black !important; }
    /* Botón 3: Neutral */
    div[data-testid="stVerticalBlock"] > div:nth-child(4) button { background-color: white !important; color: blue !important; border: 2px solid lightblue !important; }
    /* Botón 4: En Desacuerdo */
    div[data-testid="stVerticalBlock"] > div:nth-child(5) button { background-color: lightcoral !important; color: black !important; }
    /* Botón 5: Totalmente en Desacuerdo */
    div[data-testid="stVerticalBlock"] > div:nth-child(6) button { background-color: red !important; color: white !important; }

    /* BOTONES FINALES: Grandes, Negros y Estilo Burbuja */
    .final-btns button {
        background-color: black !important;
        color: white !important;
        height: 75px !important;
        font-size: 22px !important;
        border-radius: 15px !important;
        text-transform: uppercase !important;
        margin-top: 20px !important;
    }

    /* Etiquetas de Líderes en el Mapa (Sin fondo blanco) */
    .leader-label {
        position: absolute;
        font-size: 10px;
        font-weight: bold;
        color: black;
        text-shadow: 1px 1px 1px white, -1px -1px 1px white;
        pointer-events: none;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. LÓGICA DE DATOS
if 'idx' not in st.session_state:
    st.session_state.update({'idx': 0, 'x': 0.0, 'y': 0.0, 'hist': []})

def responder(pts):
    q = questions[st.session_state.idx]
    val = pts * 14.5 * q["v"]
    if q["a"] == "x": st.session_state.x += val
    else: st.session_state.y += val
    st.session_state.hist.append((val if q["a"]=="x" else 0, val if q["a"]=="y" else 0))
    st.session_state.idx += 1

# 3. LAS 85 PREGUNTAS
questions = [
    {"t": "Cualquier persona debería poder abrir un negocio sin que el gobierno le ponga muchas reglas.", "a": "x", "v": 1},
    {"t": "Los hospitales deberían ser siempre gratis y pagados con nuestros impuestos.", "a": "x", "v": -1},
    {"t": "El gobierno debería poner un límite al precio del alquiler de los pisos.", "a": "x", "v": -1},
    {"t": "Es mejor que la electricidad sea vendida por empresas privadas que por el gobierno.", "a": "x", "v": 1},
    {"t": "La gente que tiene mucho dinero debería pagar muchísimos más impuestos que el resto.", "a": "x", "v": -1},
    {"t": "Es mejor comprar productos fabricados aquí que traerlos de otros países.", "a": "x", "v": -1},
    {"t": "No debería existir un sueldo mínimo; cada uno debería pactar lo que cobra.", "a": "x", "v": 1},
    {"t": "Cuidar el planeta es más importante que ganar mucho dinero como país.", "a": "x", "v": -1},
    {"t": "El gobierno no debería dar dinero a ninguna empresa privada.", "a": "x", "v": 1},
    {"t": "Si mis padres mueren, todo su dinero debería ser mío sin pagar impuestos.", "a": "x", "v": 1},
    {"t": "Ir a la universidad debería ser totalmente gratis para todo el mundo.", "a": "x", "v": -1},
    {"t": "Si las empresas compiten entre ellas, los servicios serán mejores.", "a": "x", "v": 1},
    {"t": "El gobierno debe asegurar que todo el mundo tenga un trabajo.", "a": "x", "v": -1},
    {"t": "Nadie tiene derecho a quitarle nada a una persona si es su propiedad privada.", "a": "x", "v": 1},
    {"t": "Los bancos centrales deberían desaparecer.", "a": "x", "v": 1},
    {"t": "El agua y la luz deberían estar siempre en manos del gobierno.", "a": "x", "v": -1},
    {"t": "Comprar y vender cosas con todo el mundo ayuda a que haya menos pobreza.", "a": "x", "v": 1},
    {"t": "Debería estar prohibido ganar dinero solo apostando en la bolsa.", "a": "x", "v": -1},
    {"t": "Que el gobierno gaste mucho dinero es lo que crea las crisis.", "a": "x", "v": 1},
    {"t": "Las personas ayudan mejor a los pobres que el gobierno.", "a": "x", "v": 1},
    {"t": "Los países que no cobran impuestos a las empresas son algo justo.", "a": "x", "v": 1},
    {"t": "El gobierno debe ayudar con dinero a las empresas grandes si van a cerrar.", "a": "x", "v": -1},
    {"t": "Para que un país vaya bien, hay que gastar menos de lo que se gana.", "a": "x", "v": 1},
    {"t": "Es normal que haya gente rica y pobre; eso hace que la gente se esfuerce.", "a": "x", "v": 1},
    {"t": "Los sindicatos de trabajadores tienen demasiado poder hoy en día.", "a": "x", "v": 1},
    {"t": "El dinero debería valer por el oro que tenga el país.", "a": "x", "v": 1},
    {"t": "Como las máquinas harán los trabajos, el gobierno debería darnos un sueldo a todos.", "a": "x", "v": -1},
    {"t": "Las medicinas no deberían tener dueño ni patentes privadas.", "a": "x", "v": -1},
    {"t": "Comprar muchas cosas es bueno para que la economía funcione.", "a": "x", "v": 1},
    {"t": "Por ley, nadie debería trabajar más de 30 horas a la semana.", "a": "x", "v": -1},
    {"t": "Obedecer a la autoridad es lo más importante que debe aprender un niño.", "a": "y", "v": 1},
    {"t": "Cualquier mujer debería poder decidir si quiere abortar gratis.", "a": "y", "v": -1},
    {"t": "La religión no debería influir en las leyes del país.", "a": "y", "v": -1},
    {"t": "Hace falta un líder fuerte que mande con mano dura para poner orden.", "a": "y", "v": 1},
    {"t": "Cada uno debería poder drogarse si quiere, es su propia vida.", "a": "y", "v": -1},
    {"t": "Los criminales peligrosos no deberían salir nunca de la cárcel.", "a": "y", "v": 1},
    {"t": "El ejército debería vigilar las fronteras para que nadie entre sin permiso.", "a": "y", "v": 1},
    {"t": "La lucha de las mujeres por la igualdad es totalmente justa.", "a": "y", "v": -1},
    {"t": "El gobierno puede espiarnos para evitar ataques terroristas.", "a": "y", "v": 1},
    {"t": "Cada uno puede decir lo que quiera, aunque alguien se sienta insultado.", "a": "y", "v": -1},
    {"t": "Si alguien muy enfermo quiere morir, el médico debería ayudarle.", "a": "y", "v": -1},
    {"t": "Todos los jóvenes deberían hacer el servicio militar obligatorio.", "a": "y", "v": 1},
    {"t": "La familia tradicional es la mejor base para la sociedad.", "a": "y", "v": 1},
    {"t": "Ver películas para adultos debería estar prohibido por ley.", "a": "y", "v": 1},
    {"t": "Nadie debería prohibir una obra de arte, aunque sea ofensiva.", "a": "y", "v": -1},
    {"t": "La pena de muerte está bien para los peores criminales.", "a": "y", "v": 1},
    {"t": "Que venga mucha gente de fuera hace que nuestra cultura se pierda.", "a": "y", "v": 1},
    {"t": "El matrimonio solo debería ser entre un hombre y una mujer.", "a": "y", "v": 1},
    {"t": "Debería estar prohibido cortar calles para hacer manifestaciones.", "a": "y", "v": 1},
    {"t": "Uno elige lo que quiere ser, no nace con ello.", "a": "y", "v": -1},
    {"t": "La monarquía ya no debería existir.", "a": "y", "v": -1},
    {"t": "La policía necesita mucho más poder.", "a": "y", "v": 1},
    {"t": "Aprender sobre sexo en el colegio es fundamental.", "a": "y", "v": -1},
    {"t": "Insultar a la religión no debería ser un delito.", "a": "y", "v": -1},
    {"t": "La bandera de nuestro país es algo sagrado.", "a": "y", "v": 1},
    {"t": "Los científicos deberían poder clonar humanos para curar enfermedades.", "a": "y", "v": -1},
    {"t": "Hoy en día hay demasiada piel fina para todo.", "a": "y", "v": 1},
    {"t": "Mezclar muchas culturas en el mismo barrio no funciona.", "a": "y", "v": 1},
    {"t": "Es necesario probar medicinas con animales.", "a": "y", "v": 1},
    {"t": "El gobierno debería pagar dinero por tener hijos.", "a": "y", "v": 1},
    {"t": "Bajarse películas sin pagar no es un crimen.", "a": "y", "v": -1},
    {"t": "En el colegio debería haber mucha más disciplina.", "a": "y", "v": 1},
    {"t": "El gobierno debe controlar la IA.", "a": "y", "v": 1},
    {"t": "La energía nuclear es la mejor solución.", "a": "x", "v": 1},
    {"t": "Los animales deberían tener los mismos derechos.", "a": "y", "v": -1},
    {"t": "Llegar al espacio deberían hacerlo empresas privadas.", "a": "x", "v": 1},
    {"t": "Dar dinero para el cine es malgastar impuestos.", "a": "x", "v": 1},
    {"t": "La globalización destruye nuestras costumbres.", "a": "y", "v": 1},
    {"t": "El capitalismo está rompiendo el planeta.", "a": "x", "v": -1},
    {"t": "Votar todas las leyes por internet es buena idea.", "a": "y", "v": -1},
    {"t": "La cárcel debe ser un castigo duro.", "a": "y", "v": 1},
    {"t": "Si eres rico es porque te has esforzado.", "a": "x", "v": 1},
    {"t": "Internet debería ser gratis.", "a": "x", "v": -1},
    {"t": "Clases de religión obligatorias.", "a": "y", "v": 1},
    {"t": "El ejército debería intervenir en guerras externas.", "a": "y", "v": 1},
    {"t": "Las criptomonedas son libertad.", "a": "x", "v": 1},
    {"t": "Es justo que un jefe gane mucho más.", "a": "x", "v": 1},
    {"t": "Prohibir la comida basura por salud.", "a": "y", "v": 1},
    {"t": "La diversidad de razas fortalece al país.", "a": "y", "v": -1},
    {"t": "Las huelgas solo sirven para perder tiempo.", "a": "x", "v": 1},
    {"t": "La tecnología nos hace menos humanos.", "a": "y", "v": 1},
    {"t": "Los multimillonarios deben dar su dinero al Estado.", "a": "x", "v": -1},
    {"t": "Prohibir pronto los coches de gasolina.", "a": "x", "v": -1},
    {"t": "Sin autoridad la sociedad sería un caos.", "a": "y", "v": 1},
    {"t": "Cualquier tiempo pasado fue mejor.", "a": "y", "v": 1}
]

# 4. LÍDERES (15)
LEADERS = [
    {"n": "Milei", "x": 185, "y": -180, "c": "orange"},
    {"n": "Stalin", "x": -190, "y": 190, "c": "red"},
    {"n": "Hitler", "x": 160, "y": 180, "c": "black"},
    {"n": "Mao", "x": -195, "y": 170, "c": "darkred"},
    {"n": "Gandhi", "x": -140, "y": -150, "c": "green"},
    {"n": "Rothbard", "x": 195, "y": -195, "c": "gold"},
    {"n": "Thatcher", "x": 150, "y": 130, "c": "blue"},
    {"n": "Castro", "x": -170, "y": 150, "c": "darkgreen"},
    {"n": "Pinochet", "x": 175, "y": 170, "c": "gray"},
    {"n": "Che Guevara", "x": -185, "y": -90, "c": "black"},
    {"n": "Friedman", "x": 170, "y": -120, "c": "lime"},
    {"n": "Mussolini", "x": 140, "y": 195, "c": "black"},
    {"n": "Sanders", "x": -130, "y": -100, "c": "cyan"},
    {"n": "John Locke", "x": 120, "y": -140, "c": "brown"},
    {"n": "Kropotkin", "x": -195, "y": -195, "c": "purple"}
]

# --- PANTALLA RESULTADOS ---
if st.session_state.idx >= len(questions):
    x, y = st.session_state.x, st.session_state.y
    
    # Determinación de Ideología (Simplificada a 15 tipos)
    if y > 60:
        if x > 60: id_n = "FASCISMO"
        elif x < -60: id_n = "ESTALINISMO"
        else: id_n = "TOTALITARISMO"
    elif y < -60:
        if x > 60: id_n = "ANARCOCAPITALISMO"
        elif x < -60: id_n = "ANARCOCOMUNISMO"
        else: id_n = "ANARQUISMO"
    else:
        if x > 50: id_n = "NEOLIBERALISMO"
        elif x < -50: id_n = "SOCIALDEMOCRACIA"
        else: id_n = "CENTRISMO"

    st.markdown(f'<h1 style="text-align:center; color:#0D47A1;">TU RESULTADO: {id_n}</h1>', unsafe_allow_html=True)

    # Mapa Político
    l_html = "".join([f'<div class="leader-label" style="left:{50+(l["x"]*0.24)}%; top:{50-(l["y"]*0.24)}%;">'
                      f'<div style="width:8px; height:8px; background:{l["c"]}; border-radius:50%; margin:auto;"></div>{l["n"]}</div>' for l in LEADERS])
    
    ux, uy = 50 + (x * 0.24), 50 - (y * 0.24)
    st.markdown(f"""
        <div style="position:relative; width:100%; max-width:500px; height:500px; margin:auto; background:white; border:2px solid black; overflow:hidden;">
            <div style="position:absolute; width:100%; height:2px; background:black; top:50%;"></div>
            <div style="position:absolute; width:2px; height:100%; background:black; left:50%;"></div>
            {l_html}
            <div style="position:absolute; left:{ux}%; top:{uy}%; transform:translate(-50%,-50%); z-index:99;">
                <div style="width:25px; height:25px; background:red; border-radius:50%; border:3px solid white; box-shadow:0 0 10px red;"></div>
                <div style="background:red; color:white; font-weight:bold; padding:2px 5px; border-radius:5px; margin-top:5px; text-align:center;">TÚ</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Botones Finales
    st.markdown('<div class="final-btns">', unsafe_allow_html=True)
    c_a, c_b = st.columns(2)
    with c_a:
        if st.button("🔄 REINICIAR TEST", use_container_width=True):
            st.session_state.update({'idx':0, 'x':0, 'y':0, 'hist':[]})
            st.rerun()
    with c_b:
        if st.button("🖨️ GUARDAR PDF", use_container_width=True):
            st.components.v1.html("<script>window.print();</script>", height=0)
    st.markdown('</div>', unsafe_allow_html=True)

# --- PANTALLA PREGUNTAS ---
else:
    st.progress(st.session_state.idx / len(questions))
    st.write(questions[st.session_state.idx]["t"])
    
    st.button("Totalmente de acuerdo", on_click=responder, args=(2,))
    st.button("De acuerdo", on_click=responder, args=(1,))
    st.button("No estoy seguro / Neutral", on_click=responder, args=(0,))
    st.button("En desacuerdo", on_click=responder, args=(-1,))
    st.button("Totalmente en desacuerdo", on_click=responder, args=(-2,))

    if st.session_state.idx > 0:
        if st.button("⬅️ VOLVER A LA ANTERIOR", use_container_width=True):
            px, py = st.session_state.hist.pop()
            st.session_state.x -= px; st.session_state.y -= py
            st.session_state.idx -= 1
            st.rerun()
