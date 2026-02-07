import streamlit as st
import base64, math
from io import BytesIO
from PIL import Image, ImageDraw

# =====================================================
# CONFIGURACIÓN GENERAL
# =====================================================
st.set_page_config(
    page_title="Brújula Política Radical",
    layout="centered"
)

# =====================================================
# ESTILOS
# =====================================================
st.markdown("""
<style>
.stApp { background-color:#0b0e14; color:white; }

/* BOTONES CENTRADOS */
div.stButton { display:flex; justify-content:center; }
.stButton > button {
    width:100% !important;
    max-width:720px !important;
    height:65px !important;
    margin:10px auto !important;
    border-radius:60px !important;
    background:#1a1f29 !important;
    border:2px solid #3b82f6 !important;
    color:white !important;
    font-size:18px !important;
    font-weight:bold !important;
    transition:0.25s;
}
.stButton > button:hover {
    background:#3b82f6 !important;
    transform:scale(1.02);
    box-shadow:0 0 20px rgba(59,130,246,.6);
}

/* MAPA */
.map-frame {
    position:relative;
    width:500px;
    height:500px;
    margin:30px auto;
    border:4px solid #3b82f6;
    border-radius:15px;
    background:white;
}
.chart-bg { width:100%; height:100%; }
.dot {
    position:absolute;
    transform:translate(-50%,-50%);
    border-radius:50%;
}
.user-dot {
    width:36px;
    height:36px;
    background:red;
    color:white;
    font-size:11px;
    font-weight:bold;
    display:flex;
    align-items:center;
    justify-content:center;
    box-shadow:0 0 18px red;
    z-index:100;
}
.leader-dot { width:14px; height:14px; border:1px solid white; }
</style>
""", unsafe_allow_html=True)

# =====================================================
# ESTADO
# =====================================================
if "idx" not in st.session_state:
    st.session_state.update({
        "idx":0, "x":0.0, "y":0.0, "eco":0.0, "glob":0.0, "hist":[]
    })

# =====================================================
# UTILIDADES
# =====================================================
def radical_pow(v): return (v**3)*5

def distance(x1,y1,x2,y2):
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)

def closest_leaders(x,y):
    return sorted(
        [{**l,"d":round(distance(x,y,l["x"],l["y"]),2)} for l in LEADERS],
        key=lambda z:z["d"]
    )

def get_b64(path):
    try:
        with open(path,"rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return ""

def generate_png(user_x,user_y,label):
    img = Image.open("chart.png").convert("RGB")
    d = ImageDraw.Draw(img)
    w,h = img.size
    ux = int(w*(50+user_x/2)/100)
    uy = int(h*(50-user_y/2)/100)
    d.ellipse((ux-10,uy-10,ux+10,uy+10),fill="red",outline="white",width=2)
    d.text((15,h-35),label,fill="black")
    buf = BytesIO()
    img.save(buf,format="PNG")
    buf.seek(0)
    return buf

# =====================================================
# LÍDERES
# =====================================================
LEADERS = [
    {"n":"Milei","x":88,"y":-80,"c":"#facc15"},
    {"n":"Stalin","x":-95,"y":95,"c":"#ef4444"},
    {"n":"Hitler","x":92,"y":98,"c":"#4b5563"},
    {"n":"Mao","x":-98,"y":88,"c":"#dc2626"},
    {"n":"Pol Pot","x":-100,"y":75,"c":"#7f1d1d"},
    {"n":"Pinochet","x":98,"y":92,"c":"#1d4ed8"},
    {"n":"Rothbard","x":100,"y":-100,"c":"#f97316"},
    {"n":"Gandhi","x":-70,"y":-85,"c":"#22c55e"}
]

# =====================================================
# PREGUNTAS (85)
# =====================================================
questions = [
{"t":"El mercado libre es el único sistema moral.","a":"x","v":1,"s":"e"},
{"t":"La sanidad debe ser 100% pública.","a":"x","v":-1,"s":None},
{"t":"Regular precios del alquiler.","a":"x","v":-1,"s":None},
{"t":"Privatizar energía es positivo.","a":"x","v":1,"s":"e"},
{"t":"Subir impuestos a grandes fortunas.","a":"x","v":-1,"s":None},
{"t":"Proteccionismo protege empleo.","a":"x","v":-1,"s":"g"},
{"t":"Eliminar salario mínimo.","a":"x","v":1,"s":None},
{"t":"Medio ambiente sobre PIB.","a":"x","v":-1,"s":"e"},
{"t":"Eliminar subvenciones empresariales.","a":"x","v":1,"s":None},
{"t":"Herencia intocable.","a":"x","v":1,"s":None},
{"t":"Universidad gratuita.","a":"x","v":-1,"s":None},
{"t":"Competencia mejora calidad.","a":"x","v":1,"s":"e"},
{"t":"Estado debe garantizar trabajo.","a":"x","v":-1,"s":None},
{"t":"Propiedad privada absoluta.","a":"x","v":1,"s":None},
{"t":"Bancos centrales no deberían existir.","a":"x","v":1,"s":None},
{"t":"Infraestructuras estatales.","a":"x","v":-1,"s":None},
{"t":"Comercio global reduce pobreza.","a":"x","v":1,"s":"g"},
{"t":"Prohibir especulación financiera.","a":"x","v":-1,"s":None},
{"t":"Gasto público excesivo daña nación.","a":"x","v":1,"s":None},
{"t":"Caridad privada > bienestar estatal.","a":"x","v":1,"s":None},

{"t":"Obedecer autoridad es virtud.","a":"y","v":1,"s":None},
{"t":"Aborto legal.","a":"y","v":-1,"s":None},
{"t":"Separación Iglesia-Estado.","a":"y","v":-1,"s":None},
{"t":"Líder fuerte para orden.","a":"y","v":1,"s":None},
{"t":"Legalizar marihuana.","a":"y","v":-1,"s":None},
{"t":"Cadena perpetua.","a":"y","v":1,"s":None},
{"t":"Control fronterizo militar.","a":"y","v":1,"s":"g"},
{"t":"Feminismo necesario.","a":"y","v":-1,"s":None},
{"t":"Vigilancia masiva.","a":"y","v":1,"s":None},
{"t":"Libertad de expresión total.","a":"y","v":-1,"s":None},
{"t":"Eutanasia legal.","a":"y","v":-1,"s":None},
{"t":"Servicio militar obligatorio.","a":"y","v":1,"s":"g"},
{"t":"Familia tradicional base social.","a":"y","v":1,"s":None},
{"t":"Prohibir pornografía.","a":"y","v":1,"s":None},
{"t":"Arte nunca censurado.","a":"y","v":-1,"s":None},
{"t":"Pena de muerte extrema.","a":"y","v":1,"s":None},
{"t":"Inmigración diluye identidad.","a":"y","v":1,"s":"g"},
{"t":"Matrimonio solo H-M.","a":"y","v":1,"s":None},
{"t":"Prohibir protestas que cortan.","a":"y","v":1,"s":None},
{"t":"Género es construcción social.","a":"y","v":-1,"s":None},

{"t":"Energía nuclear solución.","a":"x","v":1,"s":"e"},
{"t":"Derechos legales animales.","a":"y","v":-1,"s":"e"},
{"t":"Colonización espacial privada.","a":"x","v":1,"s":"e"},
{"t":"Derecho a portar armas.","a":"y","v":-1,"s":None},
{"t":"Subvencionar cultura.","a":"x","v":-1,"s":None},
{"t":"Capitalismo destruye planeta.","a":"x","v":-1,"s":"e"},
{"t":"Democracia directa online.","a":"y","v":-1,"s":None},
{"t":"Cárceles castigo, no reinserción.","a":"y","v":1,"s":None},
{"t":"Riqueza es mérito individual.","a":"x","v":1,"s":None},
{"t":"Internet derecho humano.","a":"x","v":-1,"s":None}
]

# =====================================================
# RESPONDER
# =====================================================
def responder(m):
    q = questions[st.session_state.idx]
    val = radical_pow(m)*q["v"]
    st.session_state.hist.append(
        (val if q["a"]=="x" else 0, val if q["a"]=="y" else 0)
    )
    if q["a"]=="x": st.session_state.x+=val
    else: st.session_state.y+=val
    if q["s"]=="e": st.session_state.eco+=val
    if q["s"]=="g": st.session_state.glob+=val
    st.session_state.idx+=1

# =====================================================
# FINAL
# =====================================================
if st.session_state.idx >= len(questions):
    x,y = st.session_state.x, st.session_state.y

    if x>45 and y>45: res="Autoritarismo Nacional"
    elif x<-45 and y>45: res="Totalitarismo Estatal"
    elif x>45 and y<-45: res="Anarcocapitalismo"
    elif x<-45 and y<-45: res="Anarcocomunismo"
    else: res="Centrismo Inestable"

    st.success(f"### Resultado: {res}")

    closest = closest_leaders(x,y)

    st.markdown("## 🧭 Comparación ideológica")
    for i,l in enumerate(closest[:3]):
        st.write(f"{'🥇🥈🥉'[i]} **{l['n']}** — distancia `{l['d']}`")

    # MAPA
    b64 = get_b64("chart.png")
    dots=""
    for l in LEADERS:
        dots+=f"<div class='dot leader-dot' style='left:{50+l['x']/2}%;top:{50-l['y']/2}%;background:{l['c']};'></div>"

    ux,uy=max(min(x,100),-100),max(min(y,100),-100)
    st.markdown(f"""
    <div class="map-frame">
        <img src="data:image/png;base64,{b64}" class="chart-bg">
        {dots}
        <div class="dot user-dot" style="left:{50+ux/2}%;top:{50-uy/2}%;">TÚ</div>
    </div>
    """, unsafe_allow_html=True)

    # DESCARGAS
    img = generate_png(ux,uy,f"{res} ~ {closest[0]['n']}")
    st.download_button("⬇️ Descargar PNG", img, "resultado.png","image/png")

    if st.button("📄 Guardar PDF"): st.components.v1.html("<script>window.print()</script>",0)
    if st.button("🔄 Reiniciar"):
        st.session_state.clear()
        st.rerun()

# =====================================================
# CUESTIONARIO
# =====================================================
else:
    st.progress(st.session_state.idx/len(questions))
    st.markdown(f"<h2 style='text-align:center'>{questions[st.session_state.idx]['t']}</h2>",unsafe_allow_html=True)

    if st.button("✨ Totalmente de acuerdo"): responder(2); st.rerun()
    if st.button("👍 De acuerdo"): responder(1); st.rerun()
    if st.button("⚪ Neutral"): responder(0); st.rerun()
    if st.button("👎 En desacuerdo"): responder(-1); st.rerun()
    if st.button("🔥 Totalmente en desacuerdo"): responder(-2); st.rerun()
