import streamlit as st
from PIL import Image, ImageChops

st.set_page_config(page_title="Normalizador de Logos Pro", layout="centered")

st.title("Normalizador Visual de Logos")
st.write("Versión Optimizada: Ajuste de escala por peso visual.")

uploaded_file = st.file_uploader("Sube el logo original", type=["png", "jpg", "jpeg", "webp"])

if uploaded_file is not None:
    img = Image.open(uploaded_file).convert("RGBA")
    
    # 1. Auto-crop agresivo
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)

    # --- NUEVA LÓGICA DE ESCALADO VISUAL ---
    canvas_w, canvas_h = 1400, 800
    
    # Definimos límites máximos de seguridad
    max_w = 1100 
    max_h = 450  # Aumentamos la altura permitida
    
    # Calculamos el factor de escala
    # Si el logo es muy ancho (como Wayvant), priorizamos que llene más espacio horizontal
    ratio = img.width / img.height
    
    if ratio > 2.5: # Logos muy horizontales
        new_w = 950 # Forzamos un ancho mayor para que la letra crezca
        new_h = int(new_w / ratio)
    else: # Logos más cuadrados o compactos
        new_h = 300
        new_w = int(new_h * ratio)

    # Verificamos que no se pase de los límites de seguridad
    if new_w > max_w:
        new_w = max_w
        new_h = int(new_w / ratio)
    if new_h > max_h:
        new_h = max_h
        new_w = int(new_h * ratio)

    img_resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    # 2. Crear lienzo blanco y centrar
    final_canvas = Image.new("RGB", (canvas_w, canvas_h), (255, 255, 255))
    offset = ((canvas_w - new_w) // 2, (canvas_h - new_h) // 2)
    
    final_canvas.paste(img_resized, offset, img_resized)
    
    # --- MOSTRAR Y DESCARGAR ---
    st.image(final_canvas, caption="Logo Normalizado")
    
    import io
    buf = io.BytesIO()
    final_canvas.save(buf, format="PNG")
    byte_im = buf.getvalue()
    
    st.download_button(
        label="Descargar Logo Final",
        data=byte_im,
        file_name="logo_unificado_v2.png",
        mime="image/png"
    )
