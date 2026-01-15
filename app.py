import streamlit as st
from PIL import Image, ImageChops

# Configuración de lienzo
canvas_w, canvas_h = 1400, 800

st.title("Normalizador Final de Logos")
uploaded_file = st.file_uploader("Sube el logo", type=["png", "jpg", "jpeg", "webp"])

if uploaded_file is not None:
    img = Image.open(uploaded_file).convert("RGBA")
    
    # 1. Recorte radical de bordes
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)

    ratio = img.width / img.height
    
    # 2. Lógica de escala agresiva
    if ratio < 1.3: # Logos verticales/cuadrados (como tu último Wayvant)
        new_h = 750 # Casi el total del lienzo (800)
        new_w = int(new_h * ratio)
    else: # Logos horizontales (como Cleafy)
        new_w = 1100 
        new_h = int(new_w / ratio)

    img_resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    # 3. Pegar en lienzo blanco
    final_canvas = Image.new("RGB", (canvas_w, canvas_h), (255, 255, 255))
    offset = ((canvas_w - new_w) // 2, (canvas_h - new_h) // 2)
    final_canvas.paste(img_resized, offset, img_resized)
    
    st.image(final_canvas)
    
    import io
    buf = io.BytesIO()
    final_canvas.save(buf, format="PNG")
    st.download_button("Descargar Logo", buf.getvalue(), "logo_final.png", "image/png")
