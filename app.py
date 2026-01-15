import streamlit as st
from PIL import Image, ImageOps

st.title("Normalizador de Logotipos Web")
st.write("Sube tu logo para centrarlo y unificarlo a 1400x800px")

uploaded_file = st.file_uploader("Elige un logo...", type=["png", "jpg", "jpeg", "webp"])

if uploaded_file is not None:
    # Procesamiento técnico
    img = Image.open(uploaded_file).convert("RGBA")
    
    # 1. Quitar márgenes originales (Crop)
    bbox = img.getbbox()
    img = img.crop(bbox)
    
    # 2. Definir dimensiones
    canvas_w, canvas_h = 1400, 800
    max_logo_w, max_logo_h = 900, 300 # El "área de peso visual"
    
    # 3. Escalar proporcionalmente
    img.thumbnail((max_logo_w, max_logo_h), Image.Resampling.LANCZOS)
    
    # 4. Crear lienzo blanco y pegar
    final_canvas = Image.new("RGB", (canvas_w, canvas_h), (255, 255, 255))
    offset = ((canvas_w - img.width) // 2, (canvas_h - img.height) // 2)
    final_canvas.paste(img, offset, img)
    
    st.image(final_canvas, caption="Vista previa del logo normalizado")
    
    # Botón de descarga
    final_canvas.save("logo_normalizado.png")
    with open("logo_normalizado.png", "rb") as file:
        st.download_button("Descargar Logo", file, "logo_web.png", "image/png")