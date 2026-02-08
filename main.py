import streamlit as st
import streamlit.components.v1 as components

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Compás Político", layout="centered")

# 2. ESTILOS CSS (Centrado y Diseño de Botones)
st.markdown("""
    <style>
    .stApp { background-color: #F0F8FF; }
    
    /* Centrar títulos y textos */
    .main-title { text-align: center; font-size: 45px; font-weight: 800; color: #1E3A8A; margin-bottom: 10px; }
    .question-text { text-align: center; font-size: 28px !important; font-weight: 700; color: #1E3A8A; margin: 40px 0px; min-height: 100px; }
    .ideology-title { text-align: center; font-size: 52px !important; font-weight: 900; color: #2B6CB0; margin-top: 10px; text-transform: uppercase; }
    .ideology-desc { text-align: center; font-size: 20px; color: #4A5568; margin-bottom: 30px; line-height: 1.4; }

    /* Botones de respuesta centrados */
    div.stButton { display: flex; justify-content: center; }
    div.stButton > button {
        width: 550px !important; height: 60px !important;
        border-radius: 15px !important; font-size: 18px !important;
        background-color: #BEE3F8 !important; color: #2C5282 !important;
        border: 2px solid #90CDF4 !important; margin: 5px 0px !important;
        transition: 0.3s; font-weight: 600;
    }
    div.stButton > button:hover { background-color: #90CDF4 !important; transform: scale(1.02); }

    /* Botones de acción final */
    .action-btn > div.stButton > button {
        background-color: #2D3748 !important; color: white !important;
        width: 300px !important; margin: 10px auto !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. BASE DE DATOS: LÍDERES Y PREGUNTAS
LEADERS = [
    {"n": "Milei", "x": 8.5, "y": -8.5, "c": "#F6AD55"},
    {"n": "Stalin", "x": -9, "y": 9, "c": "#F56565"},
    {"n": "Hitler", "x": 8, "y": 9.5, "c": "#4A5568"},
    {"n": "Mao", "x": -9.5, "y": 8.5, "c": "#E53E3E"},
    {"n": "Gandhi", "x": -6.5, "y": -7.5, "c": "#68D391"},
    {"n": "Thatcher", "x": 7.5, "y": 6.5, "c": "#4299E1"},
    {"n": "Castro", "x": -8.5, "y": 7, "c": "#38A169"},
    {"n": "Friedman", "x": 8, "y": -5, "c": "#ECC94B"},
    {"n": "Sanders", "x": -5, "y": -3, "c": "#63B3ED"}
]

# 85 Preguntas (Simplificadas 4º ESO)
questions = [
    # ECONÓMICAS (X)
    {"t": "El gobierno no debería decir a las empresas cuánto pagar a sus empleados.", "a": "x", "v": 1},
    {"t": "La sanidad debería ser gratis y pagada con los impuestos de todos.", "a": "x", "v": -1},
    {"t": "El Estado debería ser el dueño de las empresas de luz y agua.", "a": "x", "v": -1},
    {"t": "Es mejor que los colegios sean privados para que haya competencia.", "a": "x", "v": 1},
    {"t": "Los que más dinero ganan deben pagar muchos más impuestos.", "a": "x", "v": -1},
    {"t": "El gobierno debería poner límites al precio de la comida básica.", "a": "x", "v": -1},
    {"t": "Si una empresa va a quebrar, el gobierno no debería ayudarla.", "a": "x", "v": 1},
    {"t": "Es mejor comprar productos de nuestro país que traerlos de fuera.", "a": "x", "v": -1},
    {"t": "Abrir un negocio debería ser fácil y sin tantos permisos del gobierno.", "a": "x", "v": 1},
    {"t": "Las huelgas de trabajadores hacen más daño que bien a la economía.", "a": "x", "v": 1},
    {"t": "El gobierno debe asegurar que todo el mundo tenga una casa.", "a": "x", "v": -1},
    {"t": "El libre mercado es la mejor forma de que un país sea rico.", "a": "x", "v": 1},
    {"t": "Hacerse rico es un mérito y el Estado no debería quitarte ese dinero.", "a": "x", "v": 1},
    {"t": "Los sindicatos tienen demasiado poder hoy en día.", "a": "x", "v": 1},
    {"t": "El transporte público debería ser totalmente gratuito.", "a": "x", "v": -1},
    {"t": "La competencia entre empresas baja los precios para nosotros.", "a": "x", "v": 1},
    {"t": "El Estado debería dar un sueldo básico a todos por igual.", "a": "x", "v": -1},
    {"t": "Los bancos no deberían cobrar intereses tan altos.", "a": "x", "v": -1},
    {"t": "Las herencias familiares no deberían tener impuestos.", "a": "x", "v": 1},
    {"t": "Los servicios públicos funcionan peor que los privados.", "a": "x", "v": 1},
    {"t": "Debería estar prohibido despedir a gente si la empresa gana dinero.", "a": "x", "v": -1},
    {"t": "Los paraísos fiscales deberían estar prohibidos.", "a": "x", "v": -1},
    {"t": "El capitalismo es el sistema más justo para progresar.", "a": "x", "v": 1},
    {"t": "Las grandes fortunas deberían repartirse entre los pobres.", "a": "x", "v": -1},
    {"t": "Si te esfuerzas más, es justo que ganes mucho más dinero.", "a": "x", "v": 1},
    {"t": "No debería haber impuestos especiales para la gasolina.", "a": "x", "v": 1},
    {"t": "Cualquier medicina debería ser gratis para quien la necesite.", "a": "x", "v": -1},
    {"t": "Es mejor bajar impuestos para que la gente tenga más dinero.", "a": "x", "v": 1},
    {"t": "El gobierno debe evitar que una sola empresa controle todo.", "a": "x", "v": -1},
    {"t": "Las multas a empresas que engañan deberían ser altísimas.", "a": "x", "v": -1},
    {"t": "La propiedad privada es intocable.", "a": "x", "v": 1},
    {"t": "El gobierno debería crear fábricas para dar empleo.", "a": "x", "v": -1},
    {"t": "El Banco Central hace que el dinero pierda valor.", "a": "x", "v": 1},
    {"t": "Es normal y natural que unos tengan más dinero que otros.", "a": "x", "v": 1},
    {"t": "Gastar dinero público en cultura es un error.", "a": "x", "v": 1},
    {"t": "Las leyes ambientales frenan el crecimiento económico.", "a": "x", "v": 1},
    {"t": "Bajar impuestos a los ricos crea empleo para los demás.", "a": "x", "v": 1},
    {"t": "Las máquinas que sustituyen humanos deberían pagar impuestos.", "a": "x", "v": -1},
    {"t": "El Estado no debería pedir préstamos que pagaremos nosotros.", "a": "x", "v": 1},
    {"t": "El precio del alquiler debe estar regulado por ley.", "a": "x", "v": -1},
    {"t": "Vender órganos debería ser legal si hay acuerdo entre personas.", "a": "x", "v": 1},
    {"t": "El Estado gasta demasiado en políticos y burocracia.", "a": "x", "v": 1},
    {"t": "Tener mucha riqueza acumulada debería ser ilegal.", "a": "x", "v": -1},

    # SOCIALES / AUTORIDAD (Y)
    {"t": "La disciplina y la obediencia son lo más importante en la educación.", "a": "y", "v": 1},
    {"t": "La libertad de expresión debe ser total, aunque alguien se ofenda.", "a": "y", "v": -1},
    {"t": "Hace falta mucha más policía en las calles.", "a": "y", "v": 1},
    {"t": "El aborto debe ser una decisión libre de la mujer.", "a": "y", "v": -1},
    {"t": "Un país necesita un líder fuerte que tome decisiones rápidas.", "a": "y", "v": 1},
    {"t": "La religión no tiene sitio en la política moderna.", "a": "y", "v": -1},
    {"t": "Gastar más dinero en el ejército es necesario.", "a": "y", "v": 1},
    {"t": "Ayudar a morir a un enfermo terminal (eutanasia) debe ser legal.", "a": "y", "v": -1},
    {"t": "El gobierno debería controlar lo que se publica en internet.", "a": "y", "v": 1},
    {"t": "Lo que haga un adulto en su casa no es asunto del Estado.", "a": "y", "v": -1},
    {"t": "Nuestra cultura nacional es superior a otras.", "a": "y", "v": 1},
    {"t": "El matrimonio debe ser solo entre hombre y mujer.", "a": "y", "v": 1},
    {"t": "Las cámaras de vigilancia en la calle nos hacen más libres.", "a": "y", "v": 1},
    {"t": "Se debe legalizar el consumo de marihuana.", "a": "y", "v": -1},
    {"t": "Hay que endurecer las fronteras para frenar la inmigración.", "a": "y", "v": 1},
    {"t": "La bandera es el símbolo más sagrado de un ciudadano.", "a": "y", "v": 1},
    {"t": "Cortar una carretera en una protesta debería ser cárcel.", "a": "y", "v": 1},
    {"t": "Las tradiciones religiosas son la base de nuestra moral.", "a": "y", "v": 1},
    {"t": "El Estado no debería pedirnos el DNI para todo.", "a": "y", "v": -1},
    {"t": "La cadena perpetua es necesaria para asesinos.", "a": "y", "v": 1},
    {"t": "El orden público es más importante que los derechos individuales.", "a": "y", "v": 1},
    {"t": "La justicia protege demasiado a los delincuentes.", "a": "y", "v": 1},
    {"t": "Los hijos pertenecen a los padres, no al Estado.", "a": "y", "v": 1},
    {"t": "Quemar la bandera nacional debería ser delito.", "a": "y", "v": 1},
    {"t": "El porno hace mucho daño a la sociedad y debe controlarse.", "a": "y", "v": 1},
    {"t": "Las cuotas de género (obligar a contratar mujeres) son injustas.", "a": "y", "v": 1},
    {"t": "El servicio militar debería volver a ser obligatorio.", "a": "y", "v": 1},
    {"t": "La policía debería poder registrar a sospechosos sin orden judicial.", "a": "y", "v": 1},
    {"t": "La educación sexual no debe darse en los colegios.", "a": "y", "v": 1},
    {"t": "Blasfemar (insultar a la religión) debe estar castigado.", "a": "y", "v": 1},
    {"t": "La globalización destruye la identidad de nuestro país.", "a": "y", "v": 1},
    {"t": "La experimentación con células madre debe ser libre.", "a": "y", "v": -1},
    {"t": "La autoridad de un profesor nunca debe cuestionarse.", "a": "y", "v": 1},
    {"t": "El arte moderno es a veces una falta de respeto a los valores.", "a": "y", "v": 1},
    {"t": "Las cárceles deben ser lugares de castigo duro.", "a": "y", "v": 1},
    {"t": "Prohibiría el tabaco por salud pública si pudiera.", "a": "y", "v": 1},
    {"t": "La unidad del país es más importante que el derecho a decidir.", "a": "y", "v": 1},
    {"t": "El gobierno debe premiar a quienes tengan muchos hijos.", "a": "y", "v": 1},
    {"t": "Las redes sociales nos están volviendo maleducados.", "a": "y", "v": 1},
    {"t": "Tener un arma en casa para defensa debería ser un derecho.", "a": "y", "v": -1},
    {"t": "Los antepasados y la historia patria son sagrados.", "a": "y", "v": 1},
    {"t": "Un buen ciudadano siempre obedece la ley sin preguntar.", "a": "y", "v": 1}
]

# 4. LÓGICA DE ESTADO
if 'idx' not in st.session_state:
    st.session_state.update({'idx': 0, 'x': 0.0, 'y': 0.0, 'hist': []})

def responder(puntos):
    q = questions[st.session_state.idx]
    total_x = len([qu for qu in questions if qu["a"] == "x"])
    total_y = len([qu for qu in questions if qu["a"] == "y"])
    val = (puntos / 2) * (10 / ( (total_x if q["a"]=="x" else total_y) / 2)) * q["v"]
    if q["a"] == "x": st.session_state.x += val
    else: st.session_state.y += val
    st.session_state.hist.append((val if q["a"]=="x" else 0, val if q["a"]=="y" else 0))
    st.session_state.idx += 1

# --- PANTALLA DE RESULTADOS ---
if st.session_state.idx >= len(questions):
    st.markdown('<div class="main-title">📍 Tu Resultado Final</div>', unsafe_allow_html=True)
    x, y = st.session_state.x, st.session_state.y

    # Definición de ideología y descripción
    if y > 2:
        if x > 2: id_nom, desc = "Derecha Conservadora", "Buscas mantener las tradiciones y el orden social con un sistema económico de mercado libre."
        elif x < -2: id_nom, desc = "Izquierda Autoritaria", "Crees en la igualdad económica impuesta por un Estado fuerte que dirija la sociedad."
        else: id_nom, desc = "Populismo de Orden", "Priorizas el control social y la autoridad del Estado por encima de la economía o la libertad."
    elif y < -2:
        if x > 2: id_nom, desc = "Libertarismo de Derecha", "Defiendes la libertad individual absoluta y un mercado sin ninguna intervención del gobierno."
        elif x < -2: id_nom, desc = "Socialismo Libertario", "Buscas la igualdad social y económica pero rechazando la autoridad de los gobiernos."
        else: id_nom, desc = "Progresismo Radical", "Te enfocas en los derechos civiles y la libertad personal con un sistema económico mixto."
    else:
        if x > 2: id_nom, desc = "Liberalismo Clásico", "Defiendes las libertades individuales y una economía de mercado con poca intervención estatal."
        elif x < -2: id_nom, desc = "Socialdemocracia", "Crees en la democracia parlamentaria combinada con ayudas sociales y regulación económica."
        else: id_nom, desc = "Centro Político", "Mantienes una postura equilibrada entre la autoridad, la libertad, el mercado y el Estado."

    st.markdown(f'<div class="ideology-title">{id_nom}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="ideology-desc">{desc}</div>', unsafe_allow_html=True)

    # GRÁFICO HTML/CSS RENDERIZADO
    leaders_js = "".join([f"""
        <div class="dot" style="left:{50 + (l['x']*4.5)}%; top:{50 - (l['y']*4.5)}%; background:{l['c']};"></div>
        <div class="label" style="left:{50 + (l['x']*4.5)}%; top:{50 - (l['y']*4.5)}%;">{l['n']}</div>
    """ for l in LEADERS])

    user_x = max(2, min(98, 50 + (x * 4.5)))
    user_y = max(2, min(98, 50 - (y * 4.5)))

    compass_html = f"""
    <style>
        .map {{ position: relative; width: 450px; height: 450px; margin: auto; background: white; border: 3px solid #333; border-radius: 5px; font-family: sans-serif; }}
        .axis-h {{ position: absolute; width: 100%; height: 2px; background: #333; top: 50%; }}
        .axis-v {{ position: absolute; width: 2px; height: 100%; background: #333; left: 50%; }}
        .q-label {{ position: absolute; font-size: 10px; font-weight: bold; color: #666; }}
        .dot {{ position: absolute; width: 12px; height: 12px; border-radius: 50%; transform: translate(-50%, -50%); border: 1px solid #000; }}
        .label {{ position: absolute; font-size: 9px; font-weight: bold; transform: translate(-50%, 5px); width: 60px; text-align: center; }}
        .user-dot {{ position: absolute; width: 20px; height: 20px; background: red; border-radius: 50%; transform: translate(-50%, -50%); border: 3px solid white; box-shadow: 0 0 8px red; z-index: 10; }}
        .user-label {{ position: absolute; font-size: 14px; font-weight: 900; color: red; transform: translate(-50%, 10px); z-index: 10; }}
        .quadrant {{ position: absolute; width: 50%; height: 50%; opacity: 0.15; }}
    </style>
    <div class="map">
        <div class="quadrant" style="top:0; left:0; background: #ff7f7f;"></div>
        <div class="quadrant" style="top:0; right:0; background: #7f7fff;"></div>
        <div class="quadrant" style="bottom:0; left:0; background: #7fff7f;"></div>
        <div class="quadrant" style="bottom:0; right:0; background: #ffff7f;"></div>
        <div class="axis-h"></div><div class="axis-v"></div>
        <div class="q-label" style="top:5px; left:40%;">AUTORITARIO</div>
        <div class="q-label" style="bottom:5px; left:41%;">LIBERTARIO</div>
        <div class="q-label" style="top:48%; left:5px;">IZQUIERDA</div>
        <div class="q-label" style="top:48%; right:5px;">DERECHA</div>
        {leaders_js}
        <div class="user-dot" style="left:{user_x}%; top:{user_y}%;"></div>
        <div class="user-label" style="left:{user_x}%; top:{user_y}%;">TÚ</div>
    </div>
    """
    components.html(compass_html, height=480)

    # BOTONES FINALES
    st.markdown('<div class="action-btn">', unsafe_allow_html=True)
    st.button("🖨️ IMPRIMIR / GUARDAR PDF", on_click=lambda: components.html("<script>window.print();</script>"))
    
    resumen = f"RESULTADO COMPÁS POLÍTICO\nIdeología: {id_nom}\nEje Económico: {x:.2f}\nEje Social: {y:.2f}"
    st.download_button("📄 DESCARGAR RESULTADOS (.TXT)", resumen, file_name="mi_politica.txt")
    
    if st.button("🔄 REPETIR TEST"):
        st.session_state.update({'idx': 0, 'x': 0.0, 'y': 0.0, 'hist': []})
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- PANTALLA DE PREGUNTAS ---
else:
    st.markdown('<div class="main-title">Compás Político</div>', unsafe_allow_html=True)
    st.progress(st.session_state.idx / len(questions))
    st.write(f"<p style='text-align:center;'>Pregunta {st.session_state.idx + 1} de {len(questions)}</p>", unsafe_allow_html=True)
    
    st.markdown(f'<div class="question-text">{questions[st.session_state.idx]["t"]}</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 10, 1])
    with col2:
        st.button("✅ Totalmente de acuerdo", on_click=responder, args=(2,))
        st.button("👍 De acuerdo", on_click=responder, args=(1,))
        st.button("😐 Neutral / No lo sé", on_click=responder, args=(0,))
        st.button("👎 En desacuerdo", on_click=responder, args=(-1,))
        st.button("❌ Totalmente en desacuerdo", on_click=responder, args=(-2,))

    if st.session_state.idx > 0:
        st.write("")
        if st.button("⬅️ VOLVER A LA PREGUNTA ANTERIOR", key="back"):
            px, py = st.session_state.hist.pop()
            st.session_state.x -= px
            st.session_state.y -= py
            st.session_state.idx -= 1
            st.rerun()
