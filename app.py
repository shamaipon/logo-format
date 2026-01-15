import streamlit as st
from PIL import Image, ImageChops

st.set_page_config(page_title="Normalizador de Logos Pro", layout="centered")

st.title("Normalizador Visual de Logos")
st.write("Ajuste de escala agresivo para logos verticales.")

uploaded_file = st.file_uploader("Sube el logo original", type=["png", "jpg", "jpeg", "webp"])

if uploaded_file is not None:
    img = Image.open(uploaded_file).convert("RGBA")
    
    # 1. Auto-crop total para medir desde el primer píxel visible
    bg = Image.new(img.mode, img.size, img.getpixel((0,0)))
    diff = ImageChops.difference(img, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        img = img.crop(bbox)

    # --- LÓGICA DE EXPANSIÓN MÁXIMA ---
    canvas_w, canvas_h = 1400, 800
    ratio = img.width / img.height
    
    # Si el logo es vertical/cuadrado (ratio < 1.5), forzamos que sea MUY grande
    if ratio < 1.5:
        # Forzamos una altura de 700px (el lienzo mide 800px, solo dejamos 50px de margen arriba y abajo)
        new_h = 700 
        new_w = int(new_h * ratio)
        # Si al hacerlo tan alto se vuelve demasiado ancho, lo limitamos
        if new_w > 1200:
            new_w = 1200
            new_h = int(new_w / ratio)
    else:
        # Para logos horizontales tipo Cleafy
        new_w = 1000
        new_h = int(new_w / ratio)
        # Límite de altura para horizontales para que no se vean gigantes
        if new_h > 400:
            new_h = 400
            new_w = int(new_h * ratio)

    img_resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    # 2. Crear lienzo blanco y centrar
    final_canvas = Image.new("RGB", (canvas_w, canvas_h), (255, 255, 255))
    offset = ((canvas_w - new_w) // 2, (canvas_h - new_h) // 2)
    final_canvas.paste(img_resized, offset, img_resized)
    
    # --- VISTA PREVIA Y DESCARGA ---
    st.image(final_canvas)
    
    import io
    buf = io.BytesIO()
    final_canvas.save(buf, format="PNG")
    byte_im = buf.getvalue()
    
    st.download_button("Descargar Logo Final", byte_im, "logo_unificado.png", "image/png")
