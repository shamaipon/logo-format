import streamlit as st
from PIL import Image, ImageChops

st.set_page_config(page_title="Normalizador de Logos Pro", layout="centered")

st.title("Normalizador Visual de Logos")
st.write("Ajuste de escala inteligente para unificar tipografías.")

uploaded_file = st.file_uploader("Sube el logo original", type=["png", "jpg", "jpeg", "webp"])

if uploaded_file is not None:
    img = Image.open(uploaded_file).convert("RGBA")
    
    # 1. Auto-crop: Eliminamos cualquier margen invisible para medir el logo real
    bg = Image.new(img.mode, img.size, img.getpixel((0,0)))
    diff = ImageChops.difference(img, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        img = img.crop(bbox)

    # --- LÓGICA DE ESCALADO POR PESO VISUAL ---
    canvas_w, canvas_h = 1400, 800
    ratio = img.width / img.height
    
    # Si el logo es vertical o cuadrado (ratio cerca de 1 o menor), 
    # necesitamos que sea mucho más alto para que la letra de abajo sea grande.
    if ratio < 1.5: 
        # Caso Wayvant con símbolo arriba: permitimos una altura muy generosa
        new_h = 580 
        new_w = int(new_h * ratio)
    elif ratio > 3.5:
        # Caso logos muy alargados: priorizamos ancho
        new_w = 1000
        new_h = int(new_w / ratio)
    else:
        # Caso estándar (ej. Cleafy): equilibrio medio
        new_h = 350
        new_w = int(new_h * ratio)

    # Seguridad: Evitar que el logo toque los bordes del lienzo
    if new_w > 1200:
        new_w = 1200
        new_h = int(new_w / ratio)
    if new_h > 650:
        new_h = 650
        new_w = int(new_h * ratio)

    img_resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    # 2. Crear lienzo blanco y centrar
    final_canvas = Image.new("RGB", (canvas_w, canvas_h), (255, 255, 255))
    offset = ((canvas_w - new_w) // 2, (canvas_h - new_h) // 2)
    final_canvas.paste(img_resized, offset, img_resized)
    
    # --- VISTA PREVIA Y DESCARGA ---
    st.image(final_canvas, caption="Logo normalizado: La tipografía ahora tiene el peso correcto.")
    
    import io
    buf = io.BytesIO()
    final_canvas.save(buf, format="PNG")
    byte_im = buf.getvalue()
    
    st.download_button(
        label="Descargar Logo Final",
        data=byte_im,
        file_name="logo_unificado_perfecto.png",
        mime="image/png"
    )
