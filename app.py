import streamlit as st
from PIL import Image, ImageChops

st.set_page_config(page_title="Normalizador de Logos Pro", layout="centered")

st.title("Normalizador Visual de Logos")
st.write("Unifica el tamaño de la tipografía automáticamente.")

uploaded_file = st.file_uploader("Sube el logo original", type=["png", "jpg", "jpeg", "webp"])

if uploaded_file is not None:
    # 1. Cargar imagen
    img = Image.open(uploaded_file).convert("RGBA")
    
    # 2. Auto-crop: Quitar espacios vacíos alrededor
    bg = Image.new(img.mode, img.size, img.getpixel((0,0)))
    diff = ImageChops.difference(img, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        img = img.crop(bbox)

    # --- LÓGICA DE UNIFICACIÓN VISUAL ---
    canvas_w, canvas_h = 1400, 800
    
    # Queremos que la tipografía tenga una presencia constante.
    # Ajustamos el tamaño basándonos en una altura fija para el cuerpo del logo.
    target_height = 220 # Esta es la altura "maestra" para que todos se vean iguales
    
    aspect_ratio = img.width / img.height
    new_h = target_height
    new_w = int(new_h * aspect_ratio)
    
    # Si el logo es extremadamente largo, limitamos el ancho para que no se salga
    if new_w > 1100:
        new_w = 1100
        new_h = int(new_w / aspect_ratio)

    img_resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    # 3. Crear lienzo blanco y centrar
    final_canvas = Image.new("RGB", (canvas_w, canvas_h), (255, 255, 255))
    offset = ((canvas_w - new_w) // 2, (canvas_h - new_h) // 2)
    
    # Pegar usando el canal alfa como máscara
    final_canvas.paste(img_resized, offset, img_resized)
    
    # --- RESULTADO ---
    st.image(final_canvas, caption="Logo Normalizado (Tamaño de fuente unificado)")
    
    # Preparar descarga
    import io
    buf = io.BytesIO()
    final_canvas.save(buf, format="PNG")
    byte_im = buf.getvalue()
    
    st.download_button(
        label="Descargar Logo Final",
        data=byte_im,
        file_name="logo_web_unificado.png",
        mime="image/png"
    )
