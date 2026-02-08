import streamlit as st
import base64

# 1. CSS ULTRA-AGRESIVO (Corrige transparencia y botones unidos)
st.set_page_config(page_title="Brújula Política Estudiantil", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #F0F4F8; }
    
    /* Forzar visibilidad del texto en botones */
    button p {
        color: black !important;
        font-weight: 800 !important;
        font-size: 18px !important;
    }

    /* Contenedor de preguntas */
    .question-box {
        text-align: center;
        padding: 40px;
        background: white;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        margin-bottom: 30px;
    }

    /* BOTONES DE RESPUESTA: Colores sólidos y anchos */
    div.stButton > button {
        width: 100% !important;
        max-width: 700px !important;
        height: 60px !important;
        margin: 10px auto !important;
        display: block !important;
        border-radius: 15px !important;
        border: 2px solid rgba(0,0,0,0.1) !important;
    }

    /* Colores específicos por posición de botón */
    div[data-testid="stVerticalBlock"] > div:nth-child(2) button { background-color: #2E7D32 !important; } /* Verde Oscuro */
    div[data-testid="stVerticalBlock"] > div:nth-child(3) button { background-color: #A5D6A7 !important; } /* Verde Claro */
    div[data-testid="stVerticalBlock"] > div:nth-child(4) button { background-color: #FFFFFF !important; } /* Blanco */
    div[data-testid="stVerticalBlock"] > div:nth-child(5) button { background-color: #EF9A9A !important; } /* Rojo Claro */
    div[data-testid="stVerticalBlock"] > div:nth-child(6) button { background-color: #C62828 !important; } /* Rojo Oscuro */
    
    /* Ajuste texto para botones oscuros */
    div[data-testid="stVerticalBlock"] > div:nth-child(2) button p,
    div[data-testid="stVerticalBlock"] > div:nth-child(6) button p { color: white !important; }

    /* Botones de control (Gris) */
    .control-btn button {
        background-color: #546E7A !important;
        color: white !important;
        height: 50px !important;
        width: 250px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. LÓGICA DE DATOS
if 'idx' not in st.session_state:
    st.session_state.update({'idx': 0, 'x': 0.0, 'y': 0.0, 'hist': []})

def responder(puntos):
    q = questions[st.session_state.idx]
    val = puntos * 15.0 * q["v"] 
    if q["a"] == "x": st.session_state.x += val
    else: st.session_state.y += val
    st.session_state.hist.append((val if q["a"]=="x" else 0, val if q["a"]=="y" else 0))
    st.session_state.idx += 1

LEADERS = [
    {"n": "Milei", "x": 170, "y": -160, "c": "#FFD600"},
    {"n": "Stalin", "x": -180, "y": 180, "c": "#D32F2F"},
    {"n": "Hitler", "x": 150, "y": 170, "c": "#37474F"},
    {"n": "Mao", "x": -190, "y": 150, "c": "#F44336"},
    {"n": "Gandhi", "x": -120, "y": -150, "c": "#4CAF50"},
    {"n": "Rothbard", "x": 185, "y": -190, "c": "#FF9800"},
    {"n": "Thatcher", "x": 130, "y": 100, "c": "#1976D2"},
    {"n": "Castro", "x": -150, "y": 130, "c": "#2E7D32"}
]

# (Aquí van las 85 preguntas que ya definimos, las mantengo en la estructura)
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

# --- PANTALLA DE RESULTADOS ---
if st.session_state.idx >= len(questions):
    x, y = st.session_state.x, st.session_state.y
    
    # 9 IDEOLOGÍAS DETALLADAS
    if y > 60:
        if x > 60: n, d = "FASCISMO / AUTORITARISMO DE DERECHAS", "Estado central fuerte, valores tradicionales y economía nacionalista corporativa."
        elif x < -60: n, d = "COMUNISMO / ESTALINISMO", "Control total del Estado sobre la economía y la vida social para eliminar clases."
        else: n, d = "ESTATISMO", "Crees que el gobierno debe dirigir la sociedad en todos sus aspectos."
    elif y < -60:
        if x > 60: n, d = "ANARCOCAPITALISMO", "Soberanía individual total. El Estado no debería existir, solo la propiedad privada."
        elif x < -60: n, d = "ANARCOCOMUNISMO", "Abolición del Estado y del dinero. Sociedad basada en la ayuda mutua voluntaria."
        else: n, d = "LIBERTARISMO", "Máxima libertad personal y escepticismo ante cualquier poder centralizado."
    else:
        if x > 60: n, d = "NEOLIBERALISMO", "Defensa del libre mercado, impuestos bajos y responsabilidad individual."
        elif x < -60: n, d = "SOCIALDEMOCRACIA", "Sistema democrático con fuertes ayudas sociales y regulación económica."
        else: n, d = "CENTRISMO", "Equilibrio entre libertad y seguridad, buscando soluciones pragmáticas."

    st.markdown(f'<div style="background:white; padding:30px; border-radius:15px; border-left:10px solid #1976D2; margin-bottom:20px;">'
                f'<h1 style="color:#0D47A1; margin:0;">{n}</h1>'
                f'<p style="font-size:18px; color:#444;">{d}</p></div>', unsafe_allow_html=True)

    # Sub-ejes
    c1, c2 = st.columns(2)
    with c1: st.metric("Eje Económico (X)", f"{'Derecha' if x>0 else 'Izquierda'}", f"{int(abs(x))}%")
    with c2: st.metric("Eje Social (Y)", f"{'Autoritario' if y>0 else 'Libertario'}", f"{int(abs(y))}%")

    def get_b64(f):
        try:
            with open(f, "rb") as b: return base64.b64encode(b.read()).decode()
        except: return ""

    img_data = get_b64("chart.png")
    
    # Marcadores Líderes
    l_html = "".join([f'<div style="position:absolute; left:{50+(l["x"]*0.23)}%; top:{50-(l["y"]*0.23)}%; transform:translate(-50%,-50%); text-align:center;">'
                      f'<div style="width:12px; height:12px; background:{l["c"]}; border-radius:50%; border:2px solid white;"></div>'
                      f'<div style="font-size:10px; font-weight:bold; color:black; background:rgba(255,255,255,0.8); padding:1px 3px; border-radius:3px;">{l["n"]}</div></div>' for l in LEADERS])
    
    # MARCADOR TÚ (Alta visibilidad)
    ux, uy = max(5, min(95, 50 + (x * 0.23))), max(5, min(95, 50 - (y * 0.23)))
    
    st.markdown(f"""
        <div style="position:relative; width:500px; height:500px; margin:20px auto; border:5px solid #0D47A1; border-radius:10px; background:white;">
            <img src="data:image/png;base64,{img_data}" style="width:100%; height:100%;">
            {l_html}
            <div style="position:absolute; left:{ux}%; top:{uy}%; transform:translate(-50%,-50%); z-index:999;">
                <div style="width:30px; height:30px; background:#FF1744; border-radius:50%; border:4px solid white; box-shadow:0 0 15px rgba(255,0,0,0.8);"></div>
                <div style="font-size:16px; font-weight:900; color:white; background:#FF1744; padding:2px 8px; border-radius:5px; margin-top:5px; text-shadow:1px 1px 2px black;">TÚ</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # BOTONES FINALES SEPARADOS
    st.write("---")
    col_a, col_b, col_c = st.columns([1, 0.2, 1])
    with col_a:
        if st.button("🔄 REINICIAR TEST", use_container_width=True):
            st.session_state.update({'idx':0, 'x':0, 'y':0, 'hist':[]})
            st.rerun()
    with col_c:
        if st.button("🖨️ IMPRIMIR / GUARDAR PDF", use_container_width=True):
            st.components.v1.html("<script>window.print();</script>", height=0)

# --- PANTALLA DE PREGUNTAS ---
else:
    st.progress(st.session_state.idx / len(questions))
    st.markdown(f'<div class="question-box"><h2 style="color:#0D47A1;">{questions[st.session_state.idx]["t"]}</h2></div>', unsafe_allow_html=True)
    
    st.button("Totalmente de acuerdo", on_click=responder, args=(2,))
    st.button("De acuerdo", on_click=responder, args=(1,))
    st.button("No estoy seguro / Neutral", on_click=responder, args=(0,))
    st.button("En desacuerdo", on_click=responder, args=(-1,))
    st.button("Totalmente en desacuerdo", on_click=responder, args=(-2,))

    st.write("")
    if st.session_state.idx > 0:
        if st.button("⬅️ VOLVER A LA ANTERIOR"):
            px, py = st.session_state.hist.pop()
            st.session_state.x -= px; st.session_state.y -= py
            st.session_state.idx -= 1
            st.rerun()
