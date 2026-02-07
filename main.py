import streamlit as st
import base64

# 1. Configuración de página y Estética Avanzada
st.set_page_config(page_title="Brújula Política v3.0", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #e3f2fd; }
    
    /* Centrado total de la App */
    .main .block-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding-top: 2rem;
    }

    /* Botones idénticos y elegantes */
    div.stButton > button {
        width: 100% !important;
        max-width: 500px;
        margin: 8px auto !important;
        border-radius: 15px;
        height: 4em;
        font-weight: bold;
        font-size: 16px;
        background-color: white;
        border: 2px solid #1565c0;
        color: #1565c0;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.05);
    }
    
    div.stButton > button:hover {
        background-color: #e1f5fe;
        border-color: #0d47a1;
        transform: scale(1.01);
    }

    /* Caja de Ideología */
    .ideologia-box {
        background-color: #90caf9;
        color: #0d47a1;
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        border: 2px solid #1565c0;
        margin-bottom: 20px;
        width: 100%;
        max-width: 600px;
    }

    /* Mapa de resultados */
    .map-wrapper {
        position: relative;
        width: 450px;
        height: 450px;
        margin: 20px auto;
        border: 5px solid white;
        border-radius: 15px;
        box-shadow: 0px 10px 20px rgba(0,0,0,0.1);
        background-color: white;
    }
    .chart-img { width: 100%; height: 100%; border-radius: 10px; }
    .red-dot {
        position: absolute;
        width: 20px;
        height: 20px;
        background-color: #ff0000;
        border-radius: 50%;
        border: 3px solid white;
        transform: translate(-50%, -50%);
        z-index: 100;
        box-shadow: 0px 0px 10px rgba(0,0,0,0.5);
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Inicialización de estado
if 'idx' not in st.session_state:
    st.session_state.idx, st.session_state.x, st.session_state.y = 0, 0.0, 0.0
    st.session_state.history = []

# 3. El Banco de 85 Preguntas
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
    {"t": "65. La disciplina escolar debe ser estricta.", "a": "y", "v": 1},
    {"t": "66. La IA debe ser regulada por el estado.", "a": "y", "v": 1},
    {"t": "67. La energía nuclear es una solución necesaria.", "a": "x", "v": 1},
    {"t": "68. Los animales deben tener derechos legales.", "a": "y", "v": -1},
    {"t": "69. El espacio debe ser colonizado por privados.", "a": "x", "v": 1},
    {"t": "70. La libertad de expresión incluye ofender.", "a": "y", "v": -1},
    {"t": "71. El estado debe financiar las artes.", "a": "x", "v": -1},
    {"t": "72. La globalización destruye identidades.", "a": "y", "v": 1},
    {"t": "73. El capitalismo es insostenible.", "a": "x", "v": -1},
    {"t": "74. Votar directamente todas las leyes.", "a": "y", "v": -1},
    {"t": "75. Prisiones para rehabilitación.", "a": "y", "v": -1},
    {"t": "76. La riqueza es esfuerzo personal.", "a": "x", "v": 1},
    {"t": "77. Internet debe ser un derecho público.", "a": "x", "v": -1},
    {"t": "78. Religión en escuelas públicas.", "a": "y", "v": 1},
    {"t": "79. Intervención militar por DD.HH.", "a": "y", "v": 1},
    {"t": "80. Criptomonedas vs Moneda estatal.", "a": "x", "v": 1},
    {"t": "81. La meritocracia justifica salarios.", "a": "x", "v": 1},
    {"t": "82. El estado debe prohibir comida basura.", "a": "y", "v": 1},
    {"t": "83. La diversidad es nuestra mayor fuerza.", "a": "y", "v": -1},
    {"t": "84. Las huelgas dañan más de lo que ayudan.", "a": "x", "v": 1},
    {"t": "85. La tecnología nos hace menos libres.", "a": "y", "v": 1}
]

def responder(m):
    q = questions[st.session_state.idx]
    p = m * q["v"]
    st.session_state.history.append((p if q["a"]=="x" else 0, p if q["a"]=="y" else 0))
    if q["a"]=="x": st.session_state.x += p
    else: st.session_state.y += p
    st.session_state.idx += 1

def get_full_analysis(x, y):
    if x > 30 and y > 30: 
        return "Autoritarismo Nacional", "Priorizas el orden estatal y la jerarquía económica. Crees en una nación fuerte y un mercado regulado por el interés nacional."
    if x > 30 and y < -30: 
        return "Anarcocapitalismo", "Abogas por la libertad individual extrema y la eliminación del Estado en favor del mercado libre absoluto."
    if x < -30 and y > 30: 
        return "Socialismo de Estado", "Crees en el control estatal de los medios de producción y una fuerte autoridad para garantizar la igualdad social."
    if x < -30 and y < -30: 
        return "Anarcomunismo", "Buscas una sociedad sin clases ni Estado, basada en la cooperación voluntaria y la propiedad colectiva."
    if abs(x) <= 20 and abs(y) <= 20: 
        return "Centrismo Moderado", "Tus posiciones son equilibradas. Prefieres cambios graduales y soluciones pragmáticas que no se van a los extremos."
    if x > 30: return "Derecha Conservadora", "Valoras las libertades de mercado y la tradición, con un Estado que protege la propiedad."
    if x < -30: return "Socialdemocracia Progresista", "Apoyas un sistema redistributivo fuerte dentro de un marco democrático y libertades civiles."
    if y > 30: return "Conservadurismo Social", "Crees que el Estado debe proteger los valores morales y la cohesión social tradicional."
    if y < -30: return "Libertarismo Civil", "Tu prioridad es que el Estado no se meta en la vida privada de las personas, independientemente de la economía."
    return "Tendencia Mixta", "Tus opiniones combinan elementos de varios cuadrantes de forma ecléctica."

# --- INTERFAZ ---
if st.session_state.idx >= len(questions):
    st.markdown("<h1>📊 Tu Perfil Político</h1>", unsafe_allow_html=True)
    
    nombre_id, desc_id = get_full_analysis(st.session_state.x, st.session_state.y)
    
    st.markdown(f"""
        <div class='ideologia-box'>
            <h2 style='margin:0;'>{nombre_id}</h2>
            <hr style='border: 1px solid #1565c0;'>
            <p style='font-size: 18px;'>{desc_id}</p>
        </div>
    """, unsafe_allow_html=True)

    # Cálculo visual (Rango máximo aprox +/- 170. Factor 0.25 para el mapa de 450px)
    left_p = 50 + (st.session_state.x * 0.28) 
    top_p = 50 - (st.session_state.y * 0.28)

    def get_base64_img(file):
        with open(file, "rb") as f:
            return base64.b64encode(f.read()).decode()

    try:
        bin_str = get_base64_img("chart.png")
        st.markdown(f"""
            <div class="map-wrapper">
                <img src="data:image/png;base64,{bin_str}" class="chart-img">
                <div class="red-dot" style="left: {left_p}%; top: {top_p}%;"></div>
            </div>
        """, unsafe_allow_html=True)
    except:
        st.error("Error al cargar la imagen. Sube chart.png a GitHub.")

    st.write("")
    if st.button("🔄 Volver a realizar el test"):
        st.session_state.idx, st.session_state.x, st.session_state.y = 0, 0.0, 0.0
        st.session_state.history = []
        st.rerun()

else:
    st.markdown(f"<p style='color: #546e7a;'>Pregunta {st.session_state.idx + 1} de {len(questions)}</p>", unsafe_allow_html=True)
    st.progress(st.session_state.idx / len(questions))
    
    st.markdown(f"<h2 style='color: #1565c0; padding: 20px;'>{questions[st.session_state.idx]['t']}</h2>", unsafe_allow_html=True)
    
    # Botones centrados
    if st.button("✨ Totalmente de acuerdo"): responder(2); st.rerun()
    if st.button("👍 De acuerdo"): responder(1); st.rerun()
    if st.button("⚪ Neutral / No sé"): responder(0); st.rerun()
    if st.button("👎 En desacuerdo"): responder(-1); st.rerun()
    if st.button("🔥 Totalmente en desacuerdo"): responder(-2); st.rerun()
    
    if st.session_state.idx > 0:
        st.write("")
        if st.button("⬅️ Pregunta anterior"):
            st.session_state.idx -= 1
            px, py = st.session_state.history.pop()
            st.session_state.x -= px; st.session_state.y -= py
            st.rerun()
