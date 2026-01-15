import streamlit as st
from PIL import Image, ImageChops

st.set_page_config(page_title="Normalizador de Logos Pro", layout="centered")

st.title("Normalizador Visual de Logos")
st.write("Unificación de tamaño basada en peso visual de tipografía.")

uploaded_file = st.file_uploader("Sube el logo original", type=["png", "jpg", "jpeg", "webp"])

if uploaded_file is not None:
    img = Image.open(uploaded_file).convert("RGBA")
    
    # 1. Auto-crop para medir el logo real sin aire
    bg = Image.new(img.mode, img.size, img.getpixel((0,0)))
    diff = ImageChops.difference(img, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        img = img.crop(bbox)

    # --- LÓGICA DE UNIFICACIÓN POR PESO VISUAL ---
    canvas_w, canvas_h = 1400, 800
    ratio = img.width / img.height
    
    # Ajustamos el tamaño según la forma del logo
    if ratio > 3.0: 
        # Logos muy horizontales (ej. Wayvant alargado)
        new_w = 950
        new_h = int(new_w / ratio)
    elif ratio < 1.2:
        # Logos verticales o cuadrados (ej. Wayvant con símbolo arriba)
        # Les damos mucha más altura para que la letra de abajo sea grande
        new_h = 500 
        new_w = int(new_h * ratio)
    else:
        # Logos intermedios (ej. Cleafy)
        new_h = 320
        new_w = int(new_h * ratio)

    # Margen de seguridad final para que nunca toque los bordes
    if new_w > 1100:
        new_w = 1100
        new_h = int(new_w / ratio)
    if new_h > 600:
        new_h = 600
        new_w = int(new_h * ratio)

    img_resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    # 2. Crear lienzo blanco y centrar
    final_canvas = Image.new("RGB", (canvas_w, canvas_h), (255, 255, 255))
    offset = ((canvas_w - new_w) // 2, (canvas_h - new_h) // 2)
    final_canvas.paste(img_resized, offset, img_resized)
    
    # --- MOSTRAR Y DESCARGAR ---
    st.image(final_canvas, caption="Resultado: Peso visual unificado")
    
    import io
    buf = io.BytesIO()
    final_canvas.save(buf, format="PNG")
    byte_im = buf.getvalue()
    
    st.download_button(
        label="Descargar Logo Unificado",
        data=byte_im,
        file_name="logo_unificado_final.png",
        mime="image/png"
    )
