import streamlit as st
from PIL import Image, ImageChops
import io

# Configuración de lienzo original
canvas_w, canvas_h = 1400, 800

st.title("Normalizador Final de Logos (Doble Formato)")
uploaded_file = st.file_uploader("Sube el logo", type=["png", "jpg", "jpeg", "webp"])

if uploaded_file is not None:
    img = Image.open(uploaded_file).convert("RGBA")
    
    # 1. Recorte radical de bordes para medir el logo real
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)

    ratio = img.width / img.height
    
    # 2. Lógica de escala agresiva (Peso visual)
    if ratio < 1.3: # Logos verticales/cuadrados
        new_h = 750 
        new_w = int(new_h * ratio)
    else: # Logos horizontales
        new_w = 1100 
        new_h = int(new_w / ratio)

    img_resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    # 3. Crear lienzo blanco de 1400x800 y centrar
    final_canvas_1400 = Image.new("RGB", (canvas_w, canvas_h), (255, 255, 255))
    offset = ((canvas_w - new_w) // 2, (canvas_h - new_h) // 2)
    final_canvas_1400.paste(img_resized, offset, img_resized)
    
    # 4. Crear la versión de 700x400 (Redimensionando el lienzo final)
    final_canvas_700 = final_canvas_1400.resize((700, 400), Image.Resampling.LANCZOS)
    
    # --- VISTA PREVIA ---
    st.image(final_canvas_1400, caption="Vista previa (Tamaño original 1400x800)")
    
    # --- BOTONES DE DESCARGA ---
    col1, col2 = st.columns(2)
    
    # Preparar buffer para 1400x800
    buf_1400 = io.BytesIO()
    final_canvas_1400.save(buf_1400, format="PNG")
    
    with col1:
        st.download_button(
            label="Descargar PNG (1400x800)",
            data=buf_1400.getvalue(),
            file_name="logo_1400x800.png",
            mime="image/png"
        )
        
    # Preparar buffer para 700x400
    buf_700 = io.BytesIO()
    final_canvas_700.save(buf_700, format="PNG")
    
    with col2:
        st.download_button(
            label="Descargar PNG (700x400)",
            data=buf_700.getvalue(),
            file_name="logo_700x400.png",
            mime="image/png"
        )
