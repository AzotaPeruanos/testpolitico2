import streamlit as st
import streamlit.components.v1 as components

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Compás Político Educativo", layout="centered")

# 2. ESTILOS CSS (Burbujas, Botones y Centrado)
st.markdown("""
    <style>
    .stApp { background-color: #F8FAFC; }
    .main-title { text-align: center; font-size: 42px; font-weight: 800; color: #1E3A8A; margin-bottom: 5px; }
    .question-text { text-align: center; font-size: 26px !important; font-weight: 700; color: #1E3A8A; margin: 30px 0px; min-height: 90px; }
    
    /* Advertencia */
    .warning-box { 
        background-color: #FFFBEB; border-left: 5px solid #F59E0B; 
        padding: 20px; margin-bottom: 25px; border-radius: 12px; 
        color: #92400E; text-align: center; font-weight: 600; font-size: 17px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }

    /* Burbuja de Ideología */
    .result-bubble {
        background-color: white; border-radius: 25px; padding: 40px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1); border: 2px solid #E2E8F0;
        text-align: center; margin-bottom: 40px;
    }
    .ideology-title { font-size: 38px !important; font-weight: 900; color: #2563EB; text-transform: uppercase; margin: 0; }
    .ideology-desc { font-size: 18px; color: #475569; margin-top: 15px; line-height: 1.6; }

    /* Botones de respuesta uniformes */
    div.stButton > button {
        width: 100% !important; max-width: 600px !important; height: 58px !important;
        border-radius: 12px !important; font-size: 18px !important;
        background-color: #DBEAFE !important; color: #1E40AF !important;
        border: 2px solid #BFDBFE !important; margin: 10px auto !important;
        display: block !important; transition: 0.2s ease; font-weight: 600;
    }
    div.stButton > button:hover { background-color: #BFDBFE !important; border-color: #3B82F6 !important; }

    /* Separador y retroceso */
    .custom-hr { border: 0; height: 1px; background: #CBD5E1; margin: 40px 0; }
    .back-btn-container { text-align: center; }
    .back-btn-container div.stButton > button { 
        background-color: #F1F5F9 !important; color: #64748B !important; 
        width: 320px !important; border: 1px solid #E2E8F0 !important; font-size: 15px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. BASE DE DATOS: LÍDERES
LEADERS = [
    {"n": "Stalin", "x": -9, "y": 9, "c": "#C53030"}, {"n": "Hitler", "x": 8, "y": 9.5, "c": "#2D3748"},
    {"n": "Mao", "x": -9.5, "y": 8.5, "c": "#E53E3E"}, {"n": "Gandhi", "x": -6.5, "y": -7.5, "c": "#48BB78"},
    {"n": "Thatcher", "x": 7.5, "y": 6.5, "c": "#3182CE"}, {"n": "Milei", "x": 9.2, "y": -8.8, "c": "#D69E2E"},
    {"n": "Castro", "x": -8.5, "y": 7, "c": "#2F855A"}, {"n": "Friedman", "x": 8.5, "y": -6, "c": "#ECC94B"},
    {"n": "Sanders", "x": -5.5, "y": -2, "c": "#4299E1"}, {"n": "Pinochet", "x": 8.8, "y": 8, "c": "#1A202C"},
    {"n": "Chomsky", "x": -8.5, "y": -8.5, "c": "#38A169"}, {"n": "Rothbard", "x": 10, "y": -10, "c": "#F6E05E"},
    {"n": "Obama", "x": 2.5, "y": 1.5, "c": "#2B6CB0"}, {"n": "Mandela", "x": -3, "y": -3, "c": "#48BB78"},
    {"n": "Churchill", "x": 6, "y": 5, "c": "#2C5282"}
]

# 85 PREGUNTAS (Simplificadas para 4º ESO)
questions = [
    # ECONÓMICAS (X) - 42 preguntas aprox
    {"t": "El gobierno no debería decir a las empresas cuánto pagar.", "a": "x", "v": 1},
    {"t": "La sanidad debería ser gratis y pagada con impuestos.", "a": "x", "v": -1},
    {"t": "El Estado debería ser dueño de las eléctricas.", "a": "x", "v": -1},
    {"t": "Los colegios privados ayudan a que haya mejor educación.", "a": "x", "v": 1},
    {"t": "Los ricos deben pagar un porcentaje mucho mayor de impuestos.", "a": "x", "v": -1},
    {"t": "Poner un límite al precio del alquiler es una buena idea.", "a": "x", "v": -1},
    {"t": "Si una empresa quiebra por mala gestión, el Estado no debe salvarla.", "a": "x", "v": 1},
    {"t": "Deberíamos consumir solo productos nacionales para ayudar al país.", "a": "x", "v": -1},
    {"t": "Hacerse rico es mérito propio y el Estado no debe quitarte nada.", "a": "x", "v": 1},
    {"t": "El transporte público debe ser financiado 100% por el Estado.", "a": "x", "v": -1},
    {"t": "El capitalismo es el sistema que mejor saca a la gente de la pobreza.", "a": "x", "v": 1},
    {"t": "La propiedad privada debe estar por encima del interés común.", "a": "x", "v": 1},
    {"t": "El Estado debería dar una paga básica a todo ciudadano.", "a": "x", "v": -1},
    {"t": "Los sindicatos hoy en día solo sirven para frenar el progreso.", "a": "x", "v": 1},
    {"t": "Las grandes empresas tienen demasiada influencia en la política.", "a": "x", "v": -1},
    {"t": "Es injusto que existan los paraísos fiscales.", "a": "x", "v": -1},
    {"t": "Bajar impuestos a las empresas crea más puestos de trabajo.", "a": "x", "v": 1},
    {"t": "La competencia siempre es buena para el consumidor.", "a": "x", "v": 1},
    {"t": "Las herencias deberían estar libres de impuestos.", "a": "x", "v": 1},
    {"t": "El agua debe ser un bien público y nunca privado.", "a": "x", "v": -1},
    {"t": "El desempleo es a veces culpa de la falta de esfuerzo individual.", "a": "x", "v": 1},
    {"t": "Las multinacionales deberían pagar más impuestos que las PYMES.", "a": "x", "v": -1},
    {"t": "Es mejor privatizar empresas públicas que pierden dinero.", "a": "x", "v": 1},
    {"t": "La globalización económica perjudica al trabajador local.", "a": "x", "v": -1},
    {"t": "El ahorro individual es más importante que el gasto público.", "a": "x", "v": 1},
    {"t": "Los bancos deberían estar más vigilados por el gobierno.", "a": "x", "v": -1},
    {"t": "El libre comercio entre países ayuda a todos.", "a": "x", "v": 1},
    {"t": "Los servicios públicos son menos eficientes que los privados.", "a": "x", "v": 1},
    {"t": "Pagar impuestos es un deber moral de todo ciudadano.", "a": "x", "v": -1},
    {"t": "El Estado no debe intervenir en el precio del pan o la leche.", "a": "x", "v": 1},
    {"t": "La deuda pública de un país es un robo a las futuras generaciones.", "a": "x", "v": 1},
    {"t": "El gobierno debe garantizar que nadie pase hambre.", "a": "x", "v": -1},
    {"t": "Las subvenciones a la cultura suelen ser dinero malgastado.", "a": "x", "v": 1},
    {"t": "Es justo que un CEO gane 100 veces más que un empleado.", "a": "x", "v": 1},
    {"t": "La vivienda es un derecho, no un negocio.", "a": "x", "v": -1},
    {"t": "El Estado gasta demasiado dinero en políticos.", "a": "x", "v": 1},
    {"t": "Debería ser legal comprar y vender cualquier cosa.", "a": "x", "v": 1},
    {"t": "El medio ambiente no puede ser excusa para frenar empresas.", "a": "x", "v": 1},
    {"t": "Si el mercado lo pide, el sueldo mínimo debería poder bajar.", "a": "x", "v": 1},
    {"t": "La justicia social requiere quitar a unos para dar a otros.", "a": "x", "v": -1},
    {"t": "No debería haber fronteras para el dinero ni las mercancías.", "a": "x", "v": 1},
    {"t": "El Estado debería controlar los sueldos de los futbolistas.", "a": "x", "v": -1},
    {"t": "El dinero físico debería desaparecer para evitar fraude.", "a": "x", "v": -1},

    # SOCIALES (Y) - 43 preguntas aprox
    {"t": "La obediencia a la autoridad es una virtud fundamental.", "a": "y", "v": 1},
    {"t": "Cada uno debe poder decir lo que quiera, aunque ofenda.", "a": "y", "v": -1},
    {"t": "Necesitamos leyes más duras contra la delincuencia.", "a": "y", "v": 1},
    {"t": "El aborto debe ser legal y gratuito.", "a": "y", "v": -1},
    {"t": "Un líder fuerte es mejor que una democracia lenta.", "a": "y", "v": 1},
    {"t": "La religión debería quedarse fuera de las escuelas.", "a": "y", "v": -1},
    {"t": "Es necesario aumentar el presupuesto militar.", "a": "y", "v": 1},
    {"t": "La eutanasia es un derecho humano básico.", "a": "y", "v": -1},
    {"t": "El gobierno debería censurar noticias falsas en internet.", "a": "y", "v": 1},
    {"t": "Nuestra cultura está amenazada por la inmigración masiva.", "a": "y", "v": 1},
    {"t": "La familia tradicional es la base de la sociedad.", "a": "y", "v": 1},
    {"t": "El consumo de drogas blandas debería ser legal.", "a": "y", "v": -1},
    {"t": "La bandera y el himno son sagrados.", "a": "y", "v": 1},
    {"t": "El Estado debe proteger la moral pública.", "a": "y", "v": 1},
    {"t": "Cortar una calle para protestar debería ser ilegal.", "a": "y", "v": 1},
    {"t": "La cadena perpetua es necesaria para asesinos.", "a": "y", "v": 1},
    {"t": "El porno hace daño a los jóvenes y debe controlarse.", "a": "y", "v": 1},
    {"t": "El servicio militar obligatorio ayuda a formar a los jóvenes.", "a": "y", "v": 1},
    {"t": "La policía debería poder registrar a sospechosos sin orden.", "a": "y", "v": 1},
    {"t": "Las tradiciones son lo que mantiene unido a un país.", "a": "y", "v": 1},
    {"t": "El matrimonio solo debe ser entre hombre y mujer.", "a": "y", "v": 1},
    {"t": "La experimentación con animales debería estar prohibida.", "a": "y", "v": -1},
    {"t": "Un profesor debe tener autoridad absoluta en su clase.", "a": "y", "v": 1},
    {"t": "La globalización borra la identidad de los pueblos.", "a": "y", "v": 1},
    {"t": "Cualquier persona debería poder vivir donde quiera.", "a": "y", "v": -1},
    {"t": "La justicia es demasiado blanda con los okupas.", "a": "y", "v": 1},
    {"t": "Quemar una bandera es libertad de expresión.", "a": "y", "v": -1},
    {"t": "La pornografía debería estar prohibida.", "a": "y", "v": 1},
    {"t": "Es mejor la seguridad que la libertad total.", "a": "y", "v": 1},
    {"t": "Los hijos son de los padres y no del Estado.", "a": "y", "v": 1},
    {"t": "La prostitución debería ser legal y regulada.", "a": "y", "v": -1},
    {"t": "La religión da valores positivos que la política no da.", "a": "y", "v": 1},
    {"t": "El patriotismo es necesario para que el país funcione.", "a": "y", "v": 1},
    {"t": "La policía necesita armas taser y cámaras.", "a": "y", "v": 1},
    {"t": "Se debería prohibir el lenguaje inclusivo por ley.", "a": "y", "v": 1},
    {"t": "La educación sexual en el cole debe ser obligatoria.", "a": "y", "v": -1},
    {"t": "Cualquier forma de arte es respetable.", "a": "y", "v": -1},
    {"t": "Hay que limitar el poder de los jueces.", "a": "y", "v": 1},
    {"t": "La vigilancia masiva con cámaras evita delitos.", "a": "y", "v": 1},
    {"t": "El Estado debería fomentar tener más hijos.", "a": "y", "v": 1},
    {"t": "Tener un arma para defender tu casa debe ser legal.", "a": "y", "v": -1},
    {"t": "La pena de muerte es aceptable en algunos casos.", "a": "y", "v": 1}
]

# 4. LÓGICA DE ESTADO
if 'idx' not in st.session_state:
    st.session_state.update({'idx': 0, 'x': 0.0, 'y': 0.0, 'hist': []})

def responder(puntos):
    q = questions[st.session_state.idx]
    # Normalización basada en 42/43 preguntas por eje
    total_eje = len([qu for qu in questions if qu["a"] == q["a"]])
    # Valor máximo teórico por eje es total_eje * 2 (si responde siempre extremo)
    # Queremos que eso resulte en 10 puntos. Factor = 10 / (total_eje * 1) aprox.
    val = (puntos / 2) * (10 / (total_eje / 2)) * q["v"]
    
    if q["a"] == "x": st.session_state.x += val
    else: st.session_state.y += val
    st.session_state.hist.append((val if q["a"]=="x" else 0, val if q["a"]=="y" else 0))
    st.session_state.idx += 1

# --- PANTALLA DE RESULTADOS ---
if st.session_state.idx >= len(questions):
    st.markdown('<div class="main-title">Análisis de Perfil Político</div>', unsafe_allow_html=True)
    x, y = st.session_state.x, st.session_state.y

    # Lógica de 30 Ideologías (Subdivisión de cuadrantes)
    if y > 6:
        if x < -6: id_nom, desc = "Marxismo-Leninismo", "Crees en la abolición del capitalismo mediante un Estado centralizado y poderoso."
        elif x > 6: id_nom, desc = "Nacional-Socialismo / Fascismo", "Estado totalitario con economía dirigida y fuerte enfoque nacionalista."
        elif x < -2: id_nom, desc = "Socialismo Autoritario", "Igualdad económica garantizada por un control gubernamental estricto."
        elif x > 2: id_nom, desc = "Conservadurismo Autoritario", "Estado policial enfocado en la moral tradicional y el orden."
        else: id_nom, desc = "Totalitarismo", "Control total del Estado sobre todos los aspectos de la vida ciudadana."
    elif y < -6:
        if x < -6: id_nom, desc = "Anarco-Comunismo", "Sociedad sin clases ni Estado, basada en la cooperación voluntaria."
        elif x > 6: id_nom, desc = "Anarco-Capitalismo", "Propiedad privada absoluta y eliminación total de cualquier gobierno."
        elif x < -2: id_nom, desc = "Mutualismo", "Economía de mercado basada en cooperativas sin jerarquías estatales."
        elif x > 2: id_nom, desc = "Minarquismo", "El Estado solo debe existir para proteger la propiedad y la vida (policía y justicia)."
        else: id_nom, desc = "Libertarismo Radical", "Oposición frontal a cualquier regulación estatal sobre el individuo."
    elif y > 2:
        if x < -5: id_nom, desc = "Socialismo de Estado", "Gestión pública de los recursos con regulaciones sociales firmes."
        elif x > 5: id_nom, desc = "Derecha Conservadora", "Libre mercado combinado con la defensa de valores tradicionales."
        elif x < -1: id_nom, desc = "Estatismo de Izquierda", "Prioridad al gasto público y al control social moderado."
        elif x > 1: id_nom, desc = "Democracia Cristiana", "Economía social de mercado con enfoque en la familia y el orden."
        else: id_nom, desc = "Populismo", "Liderazgo fuerte que apela al pueblo contra las élites."
    elif y < -2:
        if x < -5: id_nom, desc = "Socialismo Libertario", "Búsqueda de la igualdad social rechazando las estructuras de mando."
        elif x > 5: id_nom, desc = "Liberalismo Radical", "Libertad económica extrema y libertades civiles totales."
        elif x < -1: id_nom, desc = "Progresismo", "Enfoque en derechos de minorías y justicia social redistributiva."
        elif x > 1: id_nom, desc = "Liberalismo Progresista", "Libertades individuales con un Estado que corrige desigualdades."
        else: id_nom, desc = "Individualismo", "La libertad personal es la máxima prioridad."
    else:
        if x < -5: id_nom, desc = "Socialismo Democrático", "Cambio hacia la igualdad mediante el sistema parlamentario."
        elif x > 5: id_nom, desc = "Liberalismo Clásico", "Libre mercado, propiedad privada y libertades civiles limitadas."
        elif x < -2: id_nom, desc = "Socialdemocracia", "Capitalismo regulado con un fuerte Estado del bienestar."
        elif x > 2: id_nom, desc = "Neoliberalismo", "Reducción del gasto público y privatización de servicios."
        elif abs(x) < 1.5: id_nom, desc = "Centrismo Pragmático", "Buscas soluciones técnicas evitando los extremos ideológicos."
        else: id_nom, desc = "Centro-Derecha / Centro-Izquierda", "Postura moderada según el contexto económico."

    # BURBUJA
    st.markdown(f"""
        <div class="result-bubble">
            <p class="ideology-title">{id_nom}</p>
            <p class="ideology-desc">{desc}</p>
        </div>
    """, unsafe_allow_html=True)

    # GRÁFICO (600px)
    leaders_html = "".join([f"""
        <div style="position:absolute; width:10px; height:10px; background:{l['c']}; border-radius:50%; left:{50 + (l['x']*4.5)}%; top:{50 - (l['y']*4.5)}%; transform:translate(-50%,-50%); border:1px solid #000; z-index:2;"></div>
        <div style="position:absolute; font-size:10px; font-weight:bold; left:{50 + (l['x']*4.5)}%; top:{50 - (l['y']*4.5)}%; transform:translate(-50%, 8px); color:#334155; z-index:2; white-space:nowrap;">{l['n']}</div>
    """ for l in LEADERS])

    user_x = max(2, min(98, 50 + (x * 4.5)))
    user_y = max(2, min(98, 50 - (y * 4.5)))

    compass_code = f"""
    <div style="position:relative; width:600px; height:600px; margin:auto; background:white; border:3px solid #1e293b; overflow:hidden;">
        <div style="position:absolute; width:50%; height:50%; top:0; left:0; background:rgba(239,68,68,0.15);"></div>
        <div style="position:absolute; width:50%; height:50%; top:0; right:0; background:rgba(59,130,246,0.15);"></div>
        <div style="position:absolute; width:50%; height:50%; bottom:0; left:0; background:rgba(34,197,94,0.15);"></div>
        <div style="position:absolute; width:50%; height:50%; bottom:0; right:0; background:rgba(234,179,8,0.15);"></div>
        <div style="position:absolute; width:100%; height:2px; background:#1e293b; top:50%;"></div>
        <div style="position:absolute; width:2px; height:100%; background:#1e293b; left:50%;"></div>
        <div style="position:absolute; top:8px; width:100%; text-align:center; font-weight:900; font-family:sans-serif; font-size:14px; color:#1e293b;">AUTORITARIO</div>
        <div style="position:absolute; bottom:8px; width:100%; text-align:center; font-weight:900; font-family:sans-serif; font-size:14px; color:#1e293b;">LIBERTARIO</div>
        <div style="position:absolute; top:48%; left:8px; font-weight:900; font-family:sans-serif; font-size:14px; color:#1e293b;">IZQUIERDA</div>
        <div style="position:absolute; top:48%; right:8px; font-weight:900; font-family:sans-serif; font-size:14px; color:#1e293b;">DERECHA</div>
        {leaders_html}
        <div style="position:absolute; width:16px; height:16px; background:red; border:3px solid white; border-radius:50%; left:{user_x}%; top:{user_y}%; transform:translate(-50%,-50%); z-index:10; box-shadow:0 0 10px red;"></div>
        <div style="position:absolute; color:red; font-weight:900; font-size:16px; left:{user_x}%; top:{user_y}%; transform:translate(-50%, -28px); z-index:11; font-family:sans-serif; text-shadow:1px 1px white;">TÚ</div>
    </div>
    """
    components.html(compass_code, height=640)

    # BOTONES FINALES
    st.markdown('<div style="display:flex; flex-direction:column; align-items:center; margin-top:30px;">', unsafe_allow_html=True)
    if st.button("🖨️ IMPRIMIR / GUARDAR COMO PDF"):
        components.html("<script>window.print();</script>", height=0)
    
    if st.button("🔄 REPETIR TEST"):
        st.session_state.update({'idx': 0, 'x': 0.0, 'y': 0.0, 'hist': []})
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- PANTALLA DE PREGUNTAS ---
else:
    st.markdown('<div class="main-title">Compás Político</div>', unsafe_allow_html=True)
    
    if st.session_state.idx == 0:
        st.markdown("""
            <div class="warning-box">
                ⚠️ <b>AVISO PARA ALUMNOS:</b> Responde con total libertad. 
                Si no entiendes el significado de una pregunta, selecciona la opción 
                <b>'Neutral / No lo sé'</b> para no alterar el resultado.
            </div>
        """, unsafe_allow_html=True)
    
    st.progress(st.session_state.idx / len(questions))
    st.write(f"<p style='text-align:center; color:#64748B;'>Pregunta {st.session_state.idx + 1} de {len(questions)}</p>", unsafe_allow_html=True)
    st.markdown(f'<div class="question-text">{questions[st.session_state.idx]["t"]}</div>', unsafe_allow_html=True)
    
    # Botones centrados
    col1, col2, col3 = st.columns([1, 8, 1])
    with col2:
        st.button("✅ Totalmente de acuerdo", on_click=responder, args=(2,))
        st.button("👍 De acuerdo", on_click=responder, args=(1,))
        st.button("😐 Neutral / No lo sé", on_click=responder, args=(0,))
        st.button("👎 En desacuerdo", on_click=responder, args=(-1,))
        st.button("❌ Totalmente en desacuerdo", on_click=responder, args=(-2,))

    if st.session_state.idx > 0:
        st.markdown('<div class="custom-hr"></div>', unsafe_allow_html=True)
        st.markdown('<div class="back-btn-container">', unsafe_allow_html=True)
        if st.button("⬅️ VOLVER A LA PREGUNTA ANTERIOR"):
            px, py = st.session_state.hist.pop()
            st.session_state.x -= px
            st.session_state.y -= py
            st.session_state.idx -= 1
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
