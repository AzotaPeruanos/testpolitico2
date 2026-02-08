import streamlit as st
import streamlit.components.v1 as components
import math

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Compás Político", layout="centered")

# 2. ESTILOS CSS (Preguntas Gigantes y Refinamiento Visual)
st.markdown("""
    <style>
    .stApp { background-color: #F8FAFC; }
    .main .block-container { max-width: 900px; display: flex; flex-direction: column; align-items: center; }
    
    /* Títulos */
    .main-title { font-size: 55px; font-weight: 950; color: #1E3A8A; text-align: center; width: 100%; margin-bottom: 10px; }
    .warning-box { background-color: #FFFBEB; border: 2px solid #F59E0B; border-radius: 15px; padding: 20px; text-align: center; color: #92400E; font-weight: 700; font-size: 18px; margin-bottom: 25px; width: 100%; }
    
    /* PREGUNTAS GIGANTES */
    .question-container { margin: 60px auto; width: 100%; text-align: center; min-height: 160px; display: flex; align-items: center; justify-content: center; }
    .question-text { font-size: 42px !important; font-weight: 800; color: #1E40AF; line-height: 1.1; letter-spacing: -1px; }
    
    /* RESULTADOS */
    .result-bubble { background-color: white; border-radius: 35px; padding: 50px; box-shadow: 0 20px 40px rgba(0,0,0,0.06); border: 3px solid #BFDBFE; text-align: center; margin: 30px auto; width: 100%; }
    .ideology-title { font-size: 42px !important; font-weight: 950; color: #2563EB; margin: 0; text-transform: uppercase; }
    .ideology-desc { font-size: 19px !important; color: #334155; margin-top: 25px; line-height: 1.7; text-align: justify; font-weight: 400; }

    /* BOTONES */
    div.stButton > button { width: 100% !important; max-width: 650px !important; height: 70px !important; border-radius: 18px !important; font-size: 24px !important; background-color: #DBEAFE !important; color: #1E40AF !important; border: 1px solid #BFDBFE !important; border-bottom: 5px solid #A5C9F8 !important; margin: 12px auto !important; display: block !important; font-weight: 700; }
    
    .leader-match { background: white; border: 1px solid #E2E8F0; border-radius: 12px; padding: 15px; margin: 8px 0; display: flex; justify-content: space-between; color: #1E293B; font-weight: 700; font-size: 18px; width: 100%; max-width: 600px; }
    </style>
    """, unsafe_allow_html=True)

# 3. BASE DE DATOS LÍDERES
LEADERS = [
    {"n": "Stalin", "x": -9, "y": 9, "c": "#C53030"}, {"n": "Hitler", "x": 8, "y": 9.5, "c": "#2D3748"},
    {"n": "Mao", "x": -9.5, "y": 8.5, "c": "#E53E3E"}, {"n": "Gandhi", "x": -6.5, "y": -7.5, "c": "#48BB78"},
    {"n": "Thatcher", "x": 7.5, "y": 6.5, "c": "#3182CE"}, {"n": "Milei", "x": 9.2, "y": -8.8, "c": "#D69E2E"},
    {"n": "Castro", "x": -8.5, "y": 7, "c": "#2F855A"}, {"n": "Friedman", "x": 8.5, "y": -6, "c": "#ECC94B"},
    {"n": "Sanders", "x": -5.5, "y": -2, "c": "#4299E1"}, {"n": "Pinochet", "x": 8.8, "y": 8, "c": "#1A202C"},
    {"n": "Chomsky", "x": -8.5, "y": -8.5, "c": "#38A169"}, {"n": "Rothbard", "x": 10, "y": -10, "c": "#F6E05E"},
    {"n": "Obama", "x": 2.5, "y": 1.5, "c": "#2B6CB0"}, {"n": "Mandela", "x": -3, "y": -3, "c": "#48BB78"},
    {"n": "Churchill", "x": 6, "y": 5, "c": "#2C5282"}, {"n": "Lenin", "x": -8.5, "y": 8, "c": "#C53030"}, 
    {"n": "Trump", "x": 6.5, "y": 5.5, "c": "#E53E3E"}, {"n": "Biden", "x": 3, "y": 2, "c": "#3182CE"}, 
    {"n": "Merkel", "x": 2.5, "y": 3, "c": "#4A5568"}, {"n": "Bukele", "x": 5, "y": 7, "c": "#2D3748"}, 
    {"n": "Putin", "x": 7, "y": 8.5, "c": "#2B6CB0"}, {"n": "Sánchez", "x": -2.5, "y": 1, "c": "#F56565"}, 
    {"n": "Abascal", "x": 7.5, "y": 7.5, "c": "#38A169"}, {"n": "Díaz", "x": -6, "y": -2, "c": "#ED64A6"}, 
    {"n": "Bolsonaro", "x": 8, "y": 6.5, "c": "#48BB78"}, {"n": "Lula", "x": -4.5, "y": 1.5, "c": "#E53E3E"}, 
    {"n": "Jefferson", "x": 4, "y": -7.5, "c": "#D69E2E"}, {"n": "Robespierre", "x": -4, "y": 9, "c": "#C53030"}, 
    {"n": "Mussolini", "x": 7.5, "y": 9.5, "c": "#1A202C"}, {"n": "Keynes", "x": -3, "y": 2, "c": "#63B3ED"}, 
    {"n": "Hayek", "x": 9, "y": -7, "c": "#F6E05E"}, {"n": "Che Guevara", "x": -9, "y": 6, "c": "#2F855A"}, 
    {"n": "Franco", "x": 7, "y": 9, "c": "#2D3748"}, {"n": "Kropotkin", "x": -10, "y": -10, "c": "#000000"}, 
    {"n": "Malatesta", "x": -9, "y": -9.5, "c": "#4A5568"}, {"n": "Rousseau", "x": -5, "y": 4, "c": "#4299E1"}, 
    {"n": "Voltaire", "x": 5, "y": -3, "c": "#ECC94B"}, {"n": "Locke", "x": 6, "y": -5, "c": "#3182CE"}, 
    {"n": "Rand", "x": 9.5, "y": -8, "c": "#718096"}, {"n": "Gaddafi", "x": -2, "y": 8, "c": "#38A169"}, 
    {"n": "Kim Jong-un", "x": -9.5, "y": 10, "c": "#E53E3E"}, {"n": "Macron", "x": 4, "y": 3, "c": "#3182CE"}, 
    {"n": "Trudeau", "x": -1.5, "y": -1.5, "c": "#ED64A6"}, {"n": "Meloni", "x": 7, "y": 6, "c": "#2C5282"}, 
    {"n": "Mujica", "x": -7, "y": -4, "c": "#48BB78"}
]

# 4. LAS 85 PREGUNTAS
questions = [
    # ECONÓMICAS
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
    
    # SOCIALES
    {"t": "La disciplina y la obediencia son lo más importante en la educación.", "a": "y", "v": 1},
    {"t": "La libertad de expresión debe ser total, aunque alguien se ofenda.", "a": "y", "v": -1},
    {"t": "Hace falta mucha más policía en las calles.", "a": "y", "v": 1},
    {"t": "El aborto debe ser una decisión libre de la mujer.", "a": "y", "v": -1},
    {"t": "Un país necesita un líder fuerte que tome decisiones rápidas.", "a": "y", "v": 1},
    {"t": "La religión no tiene sitio en la política moderna.", "a": "y", "v": -1},
    {"t": "Gastar más dinero en el ejército es necesario.", "a": "y", "v": 1},
    {"t": "Ayudar a morir a un enfermo terminal debe ser legal.", "a": "y", "v": -1},
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
    {"t": "La policía debería poder registrar a sospechosos sin orden judicial.", "a": "y", "v": 1},
    {"t": "La educación sexual no debe darse en los colegios.", "a": "y", "v": 1},
    {"t": "Blasfemar debe estar castigado.", "a": "y", "v": 1},
    {"t": "La globalización destruye la identidad de nuestro país.", "a": "y", "v": 1},
    {"t": "La experimentación con células madre debe ser libre.", "a": "y", "v": -1},
    {"t": "La autoridad de un profesor nunca debe cuestionarse.", "a": "y", "v": 1},
    {"t": "El arte moderno es a veces una falta de respeto.", "a": "y", "v": 1},
    {"t": "Las cárceles deben ser lugares de castigo duro.", "a": "y", "v": 1},
    {"t": "Prohibiría el tabaco si pudiera.", "a": "y", "v": 1},
    {"t": "La unidad del país es más importante que el derecho a decidir.", "a": "y", "v": 1},
    {"t": "El gobierno debe premiar a quienes tengan muchos hijos.", "a": "y", "v": 1},
    {"t": "Las redes sociales nos están volviendo maleducados.", "a": "y", "v": 1},
    {"t": "Tener un arma en casa para defensa debería ser un derecho.", "a": "y", "v": -1},
    {"t": "Los antepasados y la patria son sagrados.", "a": "y", "v": 1},
    {"t": "Un buen ciudadano siempre obedece la ley sin preguntar.", "a": "y", "v": 1}
]

# 5. LÓGICA DE ESTADO
if 'idx' not in st.session_state:
    st.session_state.update({'idx': 0, 'x': 0.0, 'y': 0.0, 'hist': []})

def responder(puntos):
    q = questions[st.session_state.idx]
    factor = 10 / (43 if q["a"] == "x" else 42)
    val = puntos * factor * q["v"]
    if q["a"] == "x": st.session_state.x += val
    else: st.session_state.y += val
    st.session_state.hist.append((val if q["a"]=="x" else 0, val if q["a"]=="y" else 0))
    st.session_state.idx += 1

# 6. DESCRIPIÓN LARGA DE IDEOLOGÍAS
def get_long_desc(x, y):
    if y > 6:
        if x < -6: return "Marxismo-Leninismo", "Usted aboga por una sociedad donde el Estado controla totalmente los medios de producción para eliminar las clases sociales. Cree en una disciplina revolucionaria estricta y en la planificación económica centralizada como única vía para la justicia proletaria."
        if -6 <= x < -2: return "Nacionalbolchevismo", "Una posición inusual que combina una economía socialista radical con un nacionalismo extremo. Usted valora la soberanía nacional y la identidad tradicional tanto como la redistribución de la riqueza bajo un mando central fuerte."
        if -2 <= x <= 2: return "Totalitarismo", "Para usted, el Estado es el eje absoluto de la existencia humana. Cree que los derechos individuales deben sacrificarse por completo en favor de la seguridad, el orden y el cumplimiento de un objetivo nacional o ideológico superior."
        if 2 < x <= 6: return "Fascismo Clásico", "Usted defiende un Estado fuerte y corporativo que unifique a la nación por encima de las divisiones de clase. Cree en la jerarquía natural, el heroísmo y la importancia de la unidad nacional bajo una autoridad incuestionable."
        return "Estatismo de Extrema Derecha", "Su visión se basa en una jerarquía rígida y valores tradicionales infranqueables, protegidos por un mercado que sirve a los intereses de la nación y un Estado que mantiene el orden moral y civil mediante el uso de la fuerza."
    elif 2 < y <= 6:
        if x < -6: return "Socialismo de Estado", "Cree que el Estado debe gestionar la mayoría de los recursos para garantizar la igualdad, limitando algunas libertades individuales para prevenir la explotación. El bienestar colectivo es su prioridad sobre la autonomía privada."
        if -6 <= x < -2: return "Populismo de Izquierda", "Su ideología se centra en la lucha contra las élites. Defiende un Estado fuerte que proteja a los trabajadores y redistribuya la riqueza, apoyándose en la voluntad popular para transformar las estructuras económicas."
        if -2 <= x <= 2: return "Dirigismo / Estatismo", "Usted cree que el capitalismo solo funciona si el Estado actúa como guía. Defiende la propiedad privada pero exige que el gobierno intervenga constantemente para estabilizar la economía y mantener la cohesión social."
        if 2 < x <= 6: return "Conservadurismo", "Valora la estabilidad, la tradición y las instituciones históricas. Cree en el libre mercado pero considera que el Estado debe actuar para preservar la moral pública y la ley frente a cambios sociales radicales."
        return "Derecha Autoritaria", "Su postura favorece un mercado muy libre y una mínima intervención económica estatal, pero exige un control social firme, fuerzas de seguridad potentes y leyes estrictas para mantener la estructura de la sociedad."
    elif -2 <= y <= 2:
        if x < -6: return "Socialismo Democrático", "Busca una transformación del sistema económico hacia la propiedad común mediante procesos democráticos. Rechaza el autoritarismo pero insiste en que la economía debe servir a la humanidad y no al beneficio privado."
        if -6 <= x < -2: return "Socialdemocracia", "Usted es el defensor del Estado del Bienestar. Cree en una economía de mercado pero con impuestos progresivos altos para financiar salud, educación y pensiones universales, buscando el equilibrio humano."
        if -2 <= x <= 2: return "Centrismo", "Usted evita los extremos. Cree en soluciones pragmáticas que combinen la eficiencia del mercado con redes de seguridad social moderadas, protegiendo tanto las libertades civiles como el orden público."
        if 2 < x <= 6: return "Liberalismo Moderno", "Su prioridad es la libertad individual. Defiende una economía de mercado dinámica y libertades sociales amplias, considerando que el Estado solo debe intervenir para corregir fallos evidentes o proteger derechos básicos."
        return "Liberalismo Clásico", "Usted es heredero de la Ilustración. Cree que el mercado se regula solo y que el Estado debe limitarse a proteger la vida, la libertad y la propiedad privada, interfiriendo lo mínimo posible en la vida de los ciudadanos."
    elif -6 < y <= -2:
        if x < -6: return "Anarcosindicalismo", "Su visión es una sociedad organizada a través de sindicatos y federaciones de trabajadores. Cree en la abolición del Estado pero insiste en la propiedad colectiva voluntaria para evitar nuevas formas de jerarquía."
        if -6 <= x < -2: return "Socialismo Libertario", "Combina un profundo deseo de igualdad económica con un rechazo visceral a la autoridad. Cree en comunidades autogestionadas donde los recursos se comparten libremente sin necesidad de un gobierno central."
        if -2 <= x <= 2: return "Libertarismo Progresista", "Usted quiere libertad total en lo social (legalización, autonomía corporal) pero acepta que el Estado mantenga una pequeña red de seguridad o servicios comunes para garantizar la igualdad de oportunidades inicial."
        if 2 < x <= 6: return "Minarquismo", "Usted cree en un 'Estado Vigilante Nocturno'. El gobierno debe existir únicamente para proteger a los individuos de la agresión y el fraude; cualquier otra función estatal se considera una violación de la libertad."
        return "Paleolibertarismo", "Combina una economía de mercado radicalmente libre con valores culturales tradicionales. Usted cree que el Estado debe desaparecer, pero que la sociedad debe guiarse por normas morales naturales o religiosas."
    else:
        if x < -6: return "Anarcocomunismo", "Usted sueña con la abolición total del Estado, el dinero y la propiedad privada. Cree en una sociedad de abundancia basada en el lema 'de cada cual según su capacidad, a cada cual según su necesidad'."
        if -6 <= x < -2: return "Mutualismo", "Propone un sistema de mercado sin Estado basado en el intercambio recíproco. Cree que la propiedad solo es legítima mientras se use, y aboga por cooperativas y bancos de crédito gratuito."
        if -2 <= x <= 2: return "Anarquismo Individualista", "Para usted, el individuo es la unidad suprema. Rechaza cualquier contrato o institución que limite su voluntad, defendiendo una autonomía radical donde nadie tenga poder sobre nadie."
        if 2 < x <= 6: return "Voluntarismo", "Usted cree que toda interacción humana debe ser estrictamente voluntaria. Rechaza el Estado por ser intrínsecamente coercitivo y defiende la libertad de asociación como el pilar fundamental de la civilización."
        return "Anarcocapitalismo", "Usted cree que el Estado es un robo. Defiende la privatización de absolutamente todo, desde las carreteras hasta la justicia, confiando en que el derecho de propiedad y el mercado libre generen un orden natural óptimo."

# --- PANTALLA RESULTADOS ---
if st.session_state.idx >= len(questions):
    st.markdown('<h1 class="main-title">Compás Político</h1>', unsafe_allow_html=True)
    x, y = max(min(st.session_state.x, 10), -10), max(min(st.session_state.y, 10), -10)
    id_nom, id_desc = get_long_desc(x, y)
    
    st.markdown(f'<div class="result-bubble"><p class="ideology-title">{id_nom}</p><p class="ideology-desc">{id_desc}</p></div>', unsafe_allow_html=True)

    # GRÁFICO (Refinado)
    leaders_html = "".join([f"""
        <div style="position:absolute; width:10px; height:10px; background:{l['c']}; border-radius:50%; left:{50 + (l['x']*4.6)}%; top:{50 - (l['y']*4.6)}%; transform:translate(-50%,-50%); border:1px solid black; z-index:5;"></div>
        <div style="position:absolute; font-size:11px; font-weight:900; left:{50 + (l['x']*4.6)}%; top:{50 - (l['y']*4.6)}%; transform:translate(-50%, 8px); color:#1E293B; z-index:6; white-space:nowrap; text-shadow: 1px 1px white;">{l['n']}</div>
    """ for l in LEADERS])

    compass_code = f"""
    <div style="position:relative; width:650px; height:650px; margin:20px auto; background:white; border:4px solid #1e293b; overflow:hidden; border-radius:15px; font-family: sans-serif;">
        <div style="position:absolute; width:50%; height:50%; top:0; left:0; background:rgba(239,68,68,0.25);"></div>
        <div style="position:absolute; width:50%; height:50%; top:0; right:0; background:rgba(59,130,246,0.25);"></div>
        <div style="position:absolute; width:50%; height:50%; bottom:0; left:0; background:rgba(34,197,94,0.25);"></div>
        <div style="position:absolute; width:50%; height:50%; bottom:0; right:0; background:rgba(234,179,8,0.25);"></div>
        <div style="position:absolute; width:100%; height:3px; background:#1e293b; top:50%;"></div>
        <div style="position:absolute; width:3px; height:100%; background:#1e293b; left:50%;"></div>
        {leaders_html}
        <div style="position:absolute; width:18px; height:18px; background:red; border:3px solid white; border-radius:50%; left:{50+(x*4.6)}%; top:{50-(y*4.6)}%; transform:translate(-50%,-50%); z-index:100; box-shadow:0 0 10px rgba(255,0,0,0.5);"></div>
        <div style="position:absolute; color:red; font-weight:1000; font-size:20px; left:{50+(x*4.6)}%; top:{50-(y*4.6)}%; transform:translate(-50%, {"-35px" if y < -8 else "18px"}); z-index:101; text-shadow:2px 2px white, -2px -2px white;">TÚ</div>
    </div>
    """
    components.html(compass_code, height=680)

    # AFINIDAD
    st.markdown("<h2 style='text-align:center;'>Afinidad con Líderes</h2>", unsafe_allow_html=True)
    for l in LEADERS: l['match'] = max(0, 100 - (math.sqrt((x-l['x'])**2 + (y-l['y'])**2) * 5.5))
    for l in sorted(LEADERS, key=lambda k: k['match'], reverse=True)[:3]:
        st.markdown(f'<div class="leader-match"><span>{l["n"]}</span><span>{l["match"]:.1f}%</span></div>', unsafe_allow_html=True)

    if st.button("🖨️ GUARDAR RESULTADOS"): components.html("<script>window.print();</script>", height=0)
    if st.button("🔄 REINICIAR"): st.session_state.update({'idx': 0, 'x': 0.0, 'y': 0.0, 'hist': []}); st.rerun()

# --- PANTALLA PREGUNTAS ---
else:
    st.markdown('<h1 class="main-title">Compás Político</h1>', unsafe_allow_html=True)
    if st.session_state.idx == 0:
        st.markdown('<div class="warning-box">Responda con total sinceridad. La opción "Neutral" es válida pero menos precisa.</div>', unsafe_allow_html=True)
    
    st.progress(st.session_state.idx / len(questions))
    st.markdown(f'<div class="question-container"><span class="question-text">{questions[st.session_state.idx]["t"]}</span></div>', unsafe_allow_html=True)
    
    st.button("✅ Totalmente de acuerdo", on_click=responder, args=(2,))
    st.button("👍 De acuerdo", on_click=responder, args=(1,))
    st.button("😐 Neutral / No lo sé", on_click=responder, args=(0,))
    st.button("👎 En desacuerdo", on_click=responder, args=(-1,))
    st.button("❌ Totalmente en desacuerdo", on_click=responder, args=(-2,))

    if st.session_state.idx > 0:
        if st.button("⬅️ PREGUNTA ANTERIOR"):
            px, py = st.session_state.hist.pop()
            st.session_state.x -= px; st.session_state.y -= py
            st.session_state.idx -= 1; st.rerun()
