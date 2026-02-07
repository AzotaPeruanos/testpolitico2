import flet as ft
import os
import sys

def main(page: ft.Page):
    # --- Configuración Estética ---
    page.title = "Brújula Política Profesional"
    page.bgcolor = "#e3f2fd"  # Fondo azul claro
    page.scroll = "adaptive"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 30
    page.clean()

    # --- Localizador de Archivos para Modo Local (Mac/IDLE) ---
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    # Esta ruta solo se usará si NO estamos en la web
    local_image_path = os.path.join(base_path, "assets", "chart.png")

    # --- Estado del Test ---
    state = {
        "idx": 0, 
        "x": 0.0, 
        "y": 0.0,
        "history": [] 
    }

    # Banco de 65 preguntas
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

    def get_ideology(x, y):
        if x > 5 and y > 5: return "Derecha Autoritaria"
        if x < -5 and y > 5: return "Izquierda Autoritaria"
        if x > 5 and y < -5: return "Derecha Libertaria"
        if x < -5 and y < -5: return "Izquierda Libertaria"
        if abs(x) <= 5 and abs(y) <= 5: return "Centrismo"
        return "Tendencia Moderada"

    def update_ui():
        if state["idx"] < len(questions):
            q_text.value = questions[state["idx"]]["t"]
            p_bar.value = state["idx"] / len(questions)
            counter.value = f"Pregunta {state['idx'] + 1} de {len(questions)}"
            btn_prev.visible = True if state["idx"] > 0 else False
            page.update()
        else:
            show_results()

    def on_answer(multiplier):
        q = questions[state["idx"]]
        points = multiplier * q["v"]
        state["history"].append((points if q["a"] == "x" else 0, points if q["a"] == "y" else 0))
        if q["a"] == "x": state["x"] += points
        else: state["y"] += points
        state["idx"] += 1
        update_ui()

    def go_back(e):
        if state["idx"] > 0:
            state["idx"] -= 1
            px, py = state["history"].pop()
            state["x"] -= px
            state["y"] -= py
            update_ui()

    def show_results():
        page.clean()
        ideology = get_ideology(state["x"], state["y"])
        
        # --- LÓGICA DE IMAGEN HÍBRIDA ---
        # En la web, Flet busca en la carpeta 'assets' automáticamente.
        # En local, necesitamos la ruta absoluta.
        final_src = "chart.png" if page.web else local_image_path
        
        pos_left = 200 + (state["x"] * 2.8) - 7
        pos_top = 200 - (state["y"] * 2.8) - 7
        
        page.add(
            ft.Column([
                ft.Text("Tu Perfil Político", size=32, weight="bold", color="#0d47a1"),
                ft.Container(
                    content=ft.Text(ideology, size=24, color="white", weight="bold"),
                    bgcolor="#1e88e5", padding=15, border_radius=10
                ),
                ft.Stack([
                    ft.Image(src=final_src, width=400, height=400),
                    ft.Container(
                        bgcolor="red", width=14, height=14, 
                        border_radius=7, left=pos_left, top=pos_top,
                        border=ft.border.all(1, "white")
                    )
                ]),
                ft.Text(f"Coordenadas: X={round(state['x'],1)}, Y={round(state['y'],1)}", size=16),
                ft.ElevatedButton("Repetir el Test", on_click=lambda _: main(page))
            ], horizontal_alignment="center", spacing=20)
        )

    # --- UI Elements ---
    q_text = ft.Text(value=questions[0]["t"], size=22, weight="bold", text_align="center", color="#1565c0")
    p_bar = ft.ProgressBar(value=0, width=450, color="#1e88e5", bgcolor="#bbdefb")
    counter = ft.Text(value=f"Pregunta 1 de {len(questions)}", color="#546e7a")
    btn_prev = ft.TextButton("← Volver", on_click=go_back, visible=False)
    
    responses = ft.Column([
        ft.ElevatedButton("Totalmente de acuerdo", width=380, bgcolor="#2e7d32", color="white", on_click=lambda _: on_answer(2)),
        ft.ElevatedButton("De acuerdo", width=380, bgcolor="#66bb6a", color="white", on_click=lambda _: on_answer(1)),
        ft.ElevatedButton("Neutral / No sé", width=380, bgcolor="#90a4ae", color="white", on_click=lambda _: on_answer(0)),
        ft.ElevatedButton("En desacuerdo", width=380, bgcolor="#ef5350", color="white", on_click=lambda _: on_answer(-1)),
        ft.ElevatedButton("Totalmente en desacuerdo", width=380, bgcolor="#c62828", color="white", on_click=lambda _: on_answer(-2)),
        ft.Container(height=10),
        btn_prev
    ], horizontal_alignment="center", spacing=10)

    page.add(
        ft.Container(height=20),
        p_bar,
        counter,
        ft.Container(content=q_text, padding=40, width=600),
        responses
    )

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
