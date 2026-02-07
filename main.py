import streamlit as st

# 1. Configuración de página y Estética (Parecido a Flet)
st.set_page_config(page_title="Brújula Política", layout="centered")

st.markdown("""
    <style>
    /* Fondo azul claro como en Flet */
    .stApp {
        background-color: #e3f2fd;
    }
    /* Estilo para los botones */
    div.stButton > button {
        width: 100%;
        border-radius: 12px;
        height: 3.5em;
        font-weight: bold;
        font-size: 18px;
        border: none;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
        transition: 0.3s;
    }
    /* Colores específicos para botones */
    .stButton>button:hover {
        transform: translateY(-2px);
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Inicializar estado del test
if 'idx' not in st.session_state:
    st.session_state.idx = 0
    st.session_state.x = 0.0
    st.session_state.y = 0.0
    st.session_state.history = []

# Banco de 65 preguntas (Asegúrate de que estén todas aquí)
questions = [
    {"t": "1. El mercado libre beneficia a todos a largo plazo.", "a": "x", "v": 1},
    {"t": "2. La sanidad debe ser 100% pública y gratuita.", "a": "x", "v": -1},
    {"t": "3. El estado debe regular los precios del alquiler.", "a": "x", "v": -1},
    {"t": "4. La privatización de empresas eléctricas es positiva.", "a": "x", "v": 1},
    {"t": "5. Los impuestos a las grandes fortunas deben subir.", "a": "x", "v": -1},
    {"t": "6. El proteccionismo protege el empleo local.", "a": "x", "v": -1},
    {"t": "7. El salario mínimo debería eliminarse.", "a": "x", "v": 1},
    {"t": "8. El medio ambiente es más importante que el PIB.", "a": "x", "v": -1},
    {"t": "9. Las subvenciones a empresas deben desaparecer.", "a": "x", "v": 1},
    {"t": "10. La herencia es un derecho familiar intocable.", "a": "x", "v": 1},
    {"t": "11. La educación universitaria debe ser gratuita.", "a": "x", "v": -1},
    {"t": "12. La competencia siempre mejora la calidad.", "a": "x", "v": 1},
    {"t": "13. El estado debe garantizar un trabajo a todos.", "a": "x", "v": -1},
    {"t": "14. La propiedad privada debe ser absoluta.", "a": "x", "v": 1},
    {"t": "15. Los bancos centrales no deberían existir.", "a": "x", "v": 1},
    {"t": "16. La infraestructura debe ser estatal.", "a": "x", "v": -1},
    {"t": "17. El comercio global reduce la pobreza.", "a": "x", "v": 1},
    {"t": "18. La especulación financiera debe prohibirse.", "a": "x", "v": -1},
    {"t": "19. El gasto público excesivo daña la economía.", "a": "x", "v": 1},
    {"t": "20. La caridad es mejor que el bienestar estatal.", "a": "x", "v": 1},
    {"t": "21. Los paraísos fiscales son legítimos.", "a": "x", "v": 1},
    {"t": "22. El estado debe rescatar sectores clave.", "a": "x", "v": -1},
    {"t": "23. La austeridad es necesaria en crisis.", "a": "x", "v": 1},
    {"t": "24. La desigualdad es natural en el progreso.", "a": "x", "v": 1},
    {"t": "25. El sindicato tiene demasiado poder.", "a": "x", "v": 1},
    {"t": "26. La moneda debe estar ligada al oro.", "a": "x", "v": 1},
    {"t": "27. La automatización requiere renta básica.", "a": "x", "v": -1},
    {"t": "28. Las patentes frenan el progreso humano.", "a": "x", "v": -1},
    {"t": "29. El consumo es el motor de la felicidad.", "a": "x", "v": 1},
    {"t": "30. La jornada laboral debe ser de 30 horas.", "a": "x", "v": -1},
    {"t": "31. La meritocracia es real en el capitalismo.", "a": "x", "v": 1},
    {"t": "32. Los monopolios naturales deben ser públicos.", "a": "x", "v": -1},
    {"t": "33. El FMI ayuda a las naciones pobres.", "a": "x", "v": 1},
    {"t": "34. La obediencia a la autoridad es una virtud.", "a": "y", "v": 1},
    {"t": "35. El aborto debe ser legal y seguro.", "a": "y", "v": -1},
    {"t": "36. La religión no debe influir en la política.", "a": "y", "v": -1},
    {"t": "37. Se necesita un líder fuerte para la nación.", "a": "y", "v": 1},
    {"t": "38. La marihuana debería ser legalizada.", "a": "y", "v": -1},
    {"t": "39. La cadena perpetua es necesaria.", "a": "y", "v": 1},
    {"t": "40. Las fronteras deben estar controladas.", "a": "y", "v": 1},
    {"t": "41. El feminismo actual es necesario.", "a": "y", "v": -1},
    {"t": "42. La vigilancia masiva evita el terrorismo.", "a": "y", "v": 1},
    {"t": "43. La libertad individual es absoluta.", "a": "y", "v": -1},
    {"t": "44. La eutanasia debe ser un derecho legal.", "a": "y", "v": -1},
    {"t": "45. El servicio militar debería ser obligatorio.", "a": "y", "v": 1},
    {"t": "46. La familia tradicional es el pilar social.", "a": "y", "v": 1},
    {"t": "47. La pornografía debería ser ilegal.", "a": "y", "v": 1},
    {"t": "48. El arte no debe ser censurado nunca.", "a": "y", "v": -1},
    {"t": "49. La pena de muerte es justa a veces.", "a": "y", "v": 1},
    {"t": "50. La inmigración descontrolada es un peligro.", "a": "y", "v": 1},
    {"t": "51. El matrimonio es solo hombre y mujer.", "a": "y", "v": 1},
    {"t": "52. La protesta callejera debe ser regulada.", "a": "y", "v": 1},
    {"t": "53. La identidad de género es una elección.", "a": "y", "v": -1},
    {"t": "54. La monarquía debe ser abolida.", "a": "y", "v": -1},
    {"t": "55. La policía necesita más poderes.", "a": "y", "v": 1},
    {"t": "56. La educación sexual debe ser obligatoria.", "a": "y", "v": -1},
    {"t": "57. La blasfemia no debería ser delito.", "a": "y", "v": -1},
    {"t": "58. Mi bandera es el símbolo más importante.", "a": "y", "v": 1},
    {"t": "59. La clonación humana debe permitirse.", "a": "y", "v": -1},
    {"t": "60. La corrección política limita la libertad.", "a": "y", "v": 1},
    {"t": "61. El multiculturalismo ha fallado.", "a": "y", "v": 1},
    {"t": "62. La experimentación con animales es necesaria.", "a": "y", "v": 1},
    {"t": "63. El estado debe promover la natalidad.", "a": "y", "v": 1},
    {"t": "64. La piratería digital no es un crimen real.", "a": "y", "v": -1},
    {"t": "65. La disciplina escolar debe ser estricta.", "a": "y", "v": 1}
]

def responder(m):
    # Solo procesamos si hay preguntas pendientes
    if st.session_state.idx < len(questions):
        q = questions[st.session_state.idx]
        p = m * q["v"]
        st.session_state.history.append((p if q["a"]=="x" else 0, p if q["a"]=="y" else 0))
        if q["a"]=="x": st.session_state.x += p
        else: st.session_state.y += p
        st.session_state.idx += 1

def go_back():
    if st.session_state.idx > 0:
        st.session_state.idx -= 1
        px, py = st.session_state.history.pop()
        st.session_state.x -= px
        st.session_state.y -= py

# --- Pantalla de Resultados ---
if st.session_state.idx >= len(questions):
    st.markdown("<h1 style='text-align: center; color: #0d47a1;'>Tu Perfil Político</h1>", unsafe_allow_html=True)
    
    # Mostrar el mapa (chart.png)
    st.image("chart.png", use_container_width=True)
    
    st.markdown(f"""
        <div style='background-color: #1e88e5; padding: 20px; border-radius: 10px; color: white; text-align: center;'>
            <h3>Coordenadas Finales</h3>
            <p style='font-size: 24px;'>Eje Económico (X): {round(st.session_state.x, 2)}</p>
            <p style='font-size: 24px;'>Eje Social (Y): {round(st.session_state.y, 2)}</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("Repetir el Test"):
        st.session_state.idx = 0
        st.session_state.x = 0.0
        st.session_state.y = 0.0
        st.session_state.history = []
        st.rerun()

# --- Pantalla de Preguntas ---
else:
    st.markdown(f"<p style='text-align: center; color: #546e7a;'>Pregunta {st.session_state.idx + 1} de {len(questions)}</p>", unsafe_allow_html=True)
    st.progress(st.session_state.idx / len(questions))
    
    st.markdown(f"<h2 style='text-align: center; color: #1565c0; padding: 20px;'>{questions[st.session_state.idx]['t']}</h2>", unsafe_allow_html=True)
    
    # Botones con colores
    if st.button("✅ Totalmente de acuerdo"): responder(2); st.rerun()
    if st.button("👍 De acuerdo"): responder(1); st.rerun()
    if st.button("⚪ Neutral / No sé"): responder(0); st.rerun()
    if st.button("👎 En desacuerdo"): responder(-1); st.rerun()
    if st.button("❌ Totalmente en desacuerdo"): responder(-2); st.rerun()
    
    st.write("") # Espacio
    if st.session_state.idx > 0:
        if st.button("← Volver a la pregunta anterior"):
            go_back()
            st.rerun()
