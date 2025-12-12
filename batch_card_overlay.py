from PIL import Image, ImageDraw, ImageFont
import json
import os
import glob
import textwrap

def add_card_overlay(image_path, text, output_path):
    print(f"Overlaying {image_path}...")
    
    try:
        img = Image.open(image_path).convert("RGBA")
    except Exception as e:
        print(f"Error loading image: {e}")
        return

    width, height = img.size
    draw = ImageDraw.Draw(img)
    
    # Layout Config
    # User requested top margin 40% smaller than 15% -> ~9%
    top_margin = int(height * 0.09)
    
    # Text Box Settings
    box_width = int(width * 0.9) # 90% width
    
    # Font Settings
    font_path = "arialbd.ttf"
    max_lines = 4
    
    # Dynamic Font Sizing
    font_size = 80 # Initial guess
    min_font_size = 20
    final_font = None
    final_lines = []
    
    # Iteratively find best font size
    current_size = font_size
    while current_size >= min_font_size:
        try:
            font = ImageFont.truetype(font_path, current_size)
        except:
            font = ImageFont.load_default()
            break
            
        avg_char_width = current_size * 0.5
        chars_per_line = int(box_width / avg_char_width)
        lines = textwrap.wrap(text, width=chars_per_line)
        
        if len(lines) <= max_lines:
            final_font = font
            final_lines = lines
            break
        
        current_size -= 2
        
    if final_font is None:
        # Fallback if text is huge
        print(f"  Warning: Text too long for {image_path}, truncating.")
        final_font = ImageFont.truetype(font_path, min_font_size)
        final_lines = textwrap.wrap(text, width=int(box_width / (min_font_size*0.5)))[:4]

    # Draw Text
    line_height = current_size * 1.2
    current_y = top_margin
    
    text_color = "white"
    stroke_color = "black"
    stroke_width = int(current_size * 0.08)
    
    for line in final_lines:
        bbox = draw.textbbox((0, 0), line, font=final_font)
        text_w = bbox[2] - bbox[0]
        x = (width - text_w) / 2
        
        draw.text((x, current_y), line, font=final_font, fill=text_color,
                  stroke_width=stroke_width, stroke_fill=stroke_color)
        current_y += line_height

    img.save(output_path)
    # print(f"Saved {output_path}")

def process_all_cards():
    data_dir = "data"
    subdirs = [os.path.join(data_dir, d) for d in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, d))]
    
    print(f"Scanning {len(subdirs)} folders...")
    
    card_types = ['introduction', 'development', 'conclusion']
    
    for subdir in subdirs:
        # Find JSON
        json_files = glob.glob(os.path.join(subdir, "*.json"))
        if not json_files: continue
        json_path = json_files[0]
        
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            summary = data.get('summary', {})
            
            for key in card_types:
                text = summary.get(key)
                if not text: continue
                
                img_path = os.path.join(subdir, f"{key}.png")
                if not os.path.exists(img_path):
                    continue
                    
                # Overwrite the image with overlay
                add_card_overlay(img_path, text, img_path)
                
        except Exception as e:
            print(f"Error processing {subdir}: {e}")

if __name__ == "__main__":
    process_all_cards()
