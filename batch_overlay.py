from PIL import Image, ImageDraw, ImageFont
import json
import os
import glob
from datetime import datetime
import textwrap

def add_text_overlay(image_path, json_path, output_path):
    print(f"Overlaying {image_path}...")
    
    try:
        img = Image.open(image_path).convert("RGBA")
    except Exception as e:
        print(f"Error loading image: {e}")
        return

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading JSON: {e}")
        return

    title_text = data.get('title', 'No Title')
    url = data.get('url', '')
    date_str = data.get('date', '')

    if "terra.com.br" in url:
        source_text = "Terra"
    elif "brasil247.com" in url:
        source_text = "Brasil 247"
    else:
        source_text = "Fonte"

    try:
        dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        formatted_date = dt.strftime("%d/%m/%Y")
    except:
        formatted_date = date_str

    draw = ImageDraw.Draw(img)
    width, height = img.size
    
    # Fonts
    font_path = "arialbd.ttf"
    try:
        title_font_size = int(width * 0.08)
        meta_font_size = int(width * 0.05)
        title_font = ImageFont.truetype(font_path, title_font_size)
        meta_font = ImageFont.truetype(font_path, meta_font_size)
    except:
        title_font = ImageFont.load_default()
        meta_font = ImageFont.load_default()

    # Draw Title
    avg_char_width = title_font_size * 0.5
    chars_per_line = int(width * 0.8 / avg_char_width)
    lines = textwrap.wrap(title_text, width=chars_per_line)
    
    line_height = title_font_size * 1.2
    total_title_height = len(lines) * line_height
    start_y = (height - total_title_height) / 2
    
    text_color = "white"
    stroke_color = "black"
    stroke_width = int(title_font_size * 0.05)
    orange_color = (255, 165, 0)
    
    current_y = start_y
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=title_font)
        text_w = bbox[2] - bbox[0]
        x = (width - text_w) / 2
        draw.text((x, current_y), line, font=title_font, fill=text_color, 
                  stroke_width=stroke_width, stroke_fill=stroke_color)
        current_y += line_height

    # Draw Source
    current_y += line_height * 0.5
    bbox = draw.textbbox((0, 0), source_text, font=meta_font)
    text_w = bbox[2] - bbox[0]
    x = (width - text_w) / 2
    draw.text((x, current_y), source_text, font=meta_font, fill=orange_color,
              stroke_width=int(meta_font_size*0.03), stroke_fill="black") # added stroke to source too for consistency? User didn't specify stroke for source, but "com um espaçamento do title". Test had stroke? 
    # Logic in test_overlay.py HAD stroke for source ("stroke_fill='black'"). I will keep it.
    
    current_y += meta_font_size * 1.2

    # Draw Date
    bbox = draw.textbbox((0, 0), formatted_date, font=meta_font)
    text_w = bbox[2] - bbox[0]
    x = (width - text_w) / 2
    draw.text((x, current_y), formatted_date, font=meta_font, fill=orange_color,
              stroke_width=int(meta_font_size*0.03), stroke_fill="black")

    img.save(output_path)
    print(f"Saved {output_path}")

def process_batch_overlay():
    data_dir = "data"
    subdirs = [os.path.join(data_dir, d) for d in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, d))]
    
    print(f"Scanning {len(subdirs)} folders...")
    
    for subdir in subdirs:
        # Find JSON
        json_files = glob.glob(os.path.join(subdir, "*.json"))
        if not json_files:
            continue
        json_path = json_files[0]
        
        # Target Image
        img_path = os.path.join(subdir, "general_summary.png")
        if not os.path.exists(img_path):
            print(f"Skipping {subdir} (no general_summary.png)")
            continue
            
        # Add Overlay
        add_text_overlay(img_path, json_path, img_path) # Overwrite

if __name__ == "__main__":
    process_batch_overlay()
