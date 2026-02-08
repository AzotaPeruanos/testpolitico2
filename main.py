import streamlit as st
import streamlit.components.v1 as components

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Compás Político Pro", layout="centered")

# 2. ESTILOS CSS
st.markdown("""
    <style>
    .stApp { background-color: #F0F8FF; }
    
    .main-title { text-align: center; font-size: 45px; font-weight: 800; color: #1E3A8A; margin-bottom: 10px; }
    .question-text { text-align: center; font-size: 28px !important; font-weight: 700; color: #1E3A8A; margin: 40px 0px; min-height: 100px; }
    .ideology-title { text-align: center; font-size: 48px !important; font-weight: 900; color: #2B6CB0; margin-top: 10px; text-transform: uppercase; }
    .ideology-desc { text-align: center; font-size: 20px; color: #4A5568; margin-bottom: 30px; line-height: 1.4; }

    /* Advertencia inicial */
    .warning-box { background-color: #FFFBEB; border-left: 5px solid #F59E0B; padding: 20px; margin-bottom: 20px; border-radius: 8px; color: #92400E; text-align: center; font-weight: 600; }

    /* Botones de respuesta */
    div.stButton > button {
        width: 100% !important; max-width: 550px !important; height: 60px !important;
        border-radius: 15px !important; font-size: 18px !important;
        background-color: #BEE3F8 !important; color: #2C5282 !important;
        border: 2px solid #90CDF4 !important; margin: 5px auto !important;
        display: block !important; transition: 0.3s; font-weight: 600;
    }
    div.stButton > button:hover { background-color: #90CDF4 !important; transform: scale(1.02); }

    /* Separador */
    .custom-hr { border: 0; height: 1px; background-image: linear-gradient(to right, transparent, #CBD5E1, transparent); margin: 40px 0; }

    /* Botones de acción final */
    .action-btn > div.stButton > button { background-color: #2D3748 !important; color: white !important; width: 300px !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. BASE DE DATOS AMPLIADA
LEADERS = [
    {"n": "Milei", "x": 9, "y": -9, "c": "#F6AD55"}, {"n": "Stalin", "x": -9, "y": 9, "c": "#F56565"},
    {"n": "Hitler", "x": 8, "y": 9.5, "c": "#4A5568"}, {"n": "Mao", "x": -9.5, "y": 8.5, "c": "#E53E3E"},
    {"n": "Gandhi", "x": -6.5, "y": -7.5, "c": "#68D391"}, {"n": "Thatcher", "x": 7.5, "y": 6.5, "c": "#4299E1"},
    {"n": "Castro", "x": -8.5, "y": 7, "c": "#38A169"}, {"n": "Friedman", "x": 8, "y": -5, "c": "#ECC94B"},
    {"n": "Sanders", "x": -5, "y": -3, "c": "#63B3ED"}, {"n": "Churchill", "x": 6, "y": 5, "c": "#2B6CB0"},
    {"n": "Obama", "x": 2.5, "y": 2, "c": "#3182CE"}, {"n": "Merkel", "x": 3, "y": 3, "c": "#3182CE"},
    {"n": "Kim Jong-un", "x": -9, "y": 9.5, "c": "#C0392B"}, {"n": "Rothbard", "x": 10, "y": -10, "c": "#D69E2E"},
    {"n": "Chomsky", "x": -8, "y": -8, "c": "#48BB78"}, {"n": "Pinochet", "x": 8.5, "y": 8, "c": "#2D3748"},
    {"n": "Lula", "x": -4, "y": 1, "c": "#E53E3E"}, {"n": "Mandela", "x": -2, "y": -3, "c": "#48BB78"},
    {"n": "Macron", "x": 3.5, "y": 1.5, "c": "#3182CE"}, {"n": "Franco", "x": 6, "y": 8.5, "c": "#2D3748"},
    {"n": "Mussolini", "x": 7, "y": 9, "c": "#2D3748"}, {"n": "Jefferson", "x": 5, "y": -6, "c": "#D69E2E"},
    {"n": "Bakunin", "x": -9, "y": -9.5, "c": "#1A202C"}, {"n": "Hayek", "x": 8, "y": -4, "c": "#D69E2E"}
]

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
    # SOCIALES (Y)
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
    {"t": "Las cuotas de género son injustas.", "a": "y", "v": 1},
    {"t": "El servicio militar debería volver a ser obligatorio.", "a": "y", "v": 1},
    {"t": "La policía debería poder registrar a sospechosos sin orden.", "a": "y", "v": 1},
    {"t": "La educación sexual no debe darse en los colegios.", "a": "y", "v": 1},
    {"t": "Blasfemar debe estar castigado.", "a": "y", "v": 1},
    {"t": "La globalización destruye la identidad de nuestro país.", "a": "y", "v": 1},
    {"t": "La experimentación con células madre debe ser libre.", "a": "y", "v": -1},
    {"t": "La autoridad de un profesor nunca debe cuestionarse.", "a": "y", "v": 1},
    {"t": "El arte moderno es a veces una falta de respeto.", "a": "y", "v": 1},
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
    st.markdown('<div class="main-title">📍 Resultado Final</div>', unsafe_allow_html=True)
    x, y = st.session_state.x, st.session_state.y

    # LÓGICA DE 30 IDEOLOGÍAS (Simplificada)
    if y > 6:
        if x < -6: id_nom, desc = "Totalitarismo", "Crees en un control estatal absoluto sobre la economía y la vida social."
        elif x > 6: id_nom, desc = "Fascismo / Nacionalismo", "Priorizas la nación y el orden social con un mercado dirigido o corporativo."
        else: id_nom, desc = "Autoritarismo Radical", "Estado omnipresente para garantizar el orden y la moralidad."
    elif y < -6:
        if x < -6: id_nom, desc = "Anarco-Comunismo", "Buscas la abolición de toda autoridad y la propiedad comunal total."
        elif x > 6: id_nom, desc = "Anarco-Capitalismo", "Defiendes la libertad individual absoluta y la eliminación total del Estado."
        else: id_nom, desc = "Libertarismo Radical", "Oposición frontal a cualquier interferencia gubernamental."
    elif abs(x) < 2 and abs(y) < 2:
        id_nom, desc = "Centrismo Puro", "Postura equilibrada que busca el pragmatismo y el consenso social."
    elif x < -5:
        id_nom, desc = "Socialismo de Estado", "Igualdad económica mediante una fuerte regulación y servicios públicos."
    elif x > 5:
        id_nom, desc = "Liberalismo Clásico", "Derechos individuales y libre mercado como motores de la sociedad."
    else:
        id_nom, desc = "Social-Liberalismo", "Equilibrio entre las libertades civiles y la justicia social."

    st.markdown(f'<div class="ideology-title">{id_nom}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="ideology-desc">{desc}</div>', unsafe_allow_html=True)

    # GRÁFICO CORREGIDO
    leaders_js = "".join([f"""
        <div class="dot" style="left:{50 + (l['x']*4.5)}%; top:{50 - (l['y']*4.5)}%; background:{l['c']};"></div>
        <div class="label" style="left:{50 + (l['x']*4.5)}%; top:{50 - (l['y']*4.5)}%;">{l['n']}</div>
    """ for l in LEADERS])

    user_x = max(5, min(95, 50 + (x * 4.5)))
    user_y = max(5, min(95, 50 - (y * 4.5)))

    compass_html = f"""
    <style>
        .map {{ position: relative; width: 500px; height: 500px; margin: auto; background: white; border: 3px solid #333; }}
        .axis-h {{ position: absolute; width: 100%; height: 2px; background: #333; top: 50%; }}
        .axis-v {{ position: absolute; width: 2px; height: 100%; background: #333; left: 50%; }}
        .q-label {{ position: absolute; font-size: 11px; font-weight: bold; color: #333; z-index: 5; }}
        .dot {{ position: absolute; width: 10px; height: 10px; border-radius: 50%; transform: translate(-50%, -50%); border: 1px solid #000; z-index: 2; }}
        .label {{ position: absolute; font-size: 9px; font-weight: bold; transform: translate(-50%, 8px); width: 60px; text-align: center; z-index: 2; }}
        .user-dot {{ position: absolute; width: 22px; height: 22px; background: red; border-radius: 50%; transform: translate(-50%, -50%); border: 3px solid white; box-shadow: 0 0 10px red; z-index: 10; }}
        .user-label {{ position: absolute; font-size: 16px; font-weight: 900; color: red; transform: translate(-50%, -30px); z-index: 11; text-shadow: 1px 1px white; }}
        .quadrant {{ position: absolute; width: 50%; height: 50%; opacity: 0.15; }}
    </style>
    <div class="map">
        <div class="quadrant" style="top:0; left:0; background: #ff7f7f;"></div>
        <div class="quadrant" style="top:0; right:0; background: #7f7fff;"></div>
        <div class="quadrant" style="bottom:0; left:0; background: #7fff7f;"></div>
        <div class="quadrant" style="bottom:0; right:0; background: #ffff7f;"></div>
        <div class="axis-h"></div><div class="axis-v"></div>
        <div class="q-label" style="top:5px; left:41%;">AUTORITARIO</div>
        <div class="q-label" style="bottom:5px; left:42%;">LIBERTARIO</div>
        <div class="q-label" style="top:48%; left:5px;">IZQUIERDA</div>
        <div class="q-label" style="top:48%; right:5px;">DERECHA</div>
        {leaders_js}
        <div class="user-dot" style="left:{user_x}%; top:{user_y}%;"></div>
        <div class="user-label" style="left:{user_x}%; top:{user_y}%;">TÚ</div>
    </div>
    """
    components.html(compass_html, height=530)

    st.markdown('<div class="action-btn">', unsafe_allow_html=True)
    if st.button("🖨️ IMPRIMIR / GUARDAR PDF"):
        components.html("<script>window.print();</script>", height=0)
    
    resumen = f"RESULTADO: {id_nom}\nEconómico: {x:.2f}\nSocial: {y:.2f}"
    st.download_button("📄 DESCARGAR RESULTADOS (.TXT)", resumen, file_name="resultado.txt")
    
    if st.button("🔄 REPETIR TEST"):
        st.session_state.update({'idx': 0, 'x': 0.0, 'y': 0.0, 'hist': []})
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- PANTALLA DE PREGUNTAS ---
else:
    st.markdown('<div class="main-title">Compás Político</div>', unsafe_allow_html=True)
    
    if st.session_state.idx == 0:
        st.markdown('<div class="warning-box">⚠️ ATENCIÓN: Responde con sinceridad. No hay respuestas correctas, solo perfiles distintos.</div>', unsafe_allow_html=True)
    
    st.progress(st.session_state.idx / len(questions))
    st.write(f"<p style='text-align:center;'>Pregunta {st.session_state.idx + 1} de {len(questions)}</p>", unsafe_allow_html=True)
    st.markdown(f'<div class="question-text">{questions[st.session_state.idx]["t"]}</div>', unsafe_allow_html=True)
    
    st.button("✅ Totalmente de acuerdo", on_click=responder, args=(2,))
    st.button("👍 De acuerdo", on_click=responder, args=(1,))
    st.button("😐 Neutral / No lo sé", on_click=responder, args=(0,))
    st.button("👎 En desacuerdo", on_click=responder, args=(-1,))
    st.button("❌ Totalmente en desacuerdo", on_click=responder, args=(-2,))

    if st.session_state.idx > 0:
        st.markdown('<div class="custom-hr"></div>', unsafe_allow_html=True)
        if st.button("⬅️ VOLVER A LA PREGUNTA ANTERIOR"):
            px, py = st.session_state.hist.pop()
            st.session_state.x -= px
            st.session_state.y -= py
            st.session_state.idx -= 1
            st.rerun()
