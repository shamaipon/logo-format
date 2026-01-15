import streamlit as st
from PIL import Image, ImageChops

st.set_page_config(page_title="Normalizador de Logos", layout="centered")

st.title("Normalizador Técnico de Logos")
st.write("Ajuste automático para máxima visibilidad de tipografía.")

uploaded_file = st.file_uploader("Sube el logo original", type=["png", "jpg", "jpeg", "webp"])

if uploaded_file is not None:
    img = Image.open(uploaded_file).convert("RGBA")
    
    # 1. Recorte exacto para eliminar aire alrededor del logo
    bg = Image.new(img.mode, img.size, img.getpixel((0,0)))
    diff = ImageChops.difference(img, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        img = img.crop(bbox)

    # --- LÓGICA DE TAMAÑO MÁXIMO ---
    canvas_w, canvas_h = 1400, 800
    
    # Queremos que el logo sea GRANDE. 
    # Forzamos a que ocupe casi todo el ancho disponible si es horizontal.
    target_width = 1100 
    target_height = 450 # Mucho más alto para que la letra no sufra
    
    ratio = img.width / img.height
    
    # Calculamos el tamaño intentando llenar el ancho de 1100px
    new_w = target_width
    new_h = int(new_w / ratio)
    
    # Si al hacerlo tan ancho se pasa de alto, lo limitamos por altura
    if new_h > target_height:
        new_h = target_height
        new_w = int(new_h * ratio)

    img_resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    # 2. Crear lienzo blanco y centrar exactamente
    final_canvas = Image.new("RGB", (canvas_w, canvas_h), (255, 255, 255))
    offset = ((canvas_w - new_w) // 2, (canvas_h - new_h) // 2
