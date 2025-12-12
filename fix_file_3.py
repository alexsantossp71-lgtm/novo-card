import json
from services.image_service import ImageService
import os

def fix_file_3():
    filepath = "data/3_Hackeou_o_espaço_alemão_fez_o_que_a_NASA_não_conse.json"
    
    print(f"Fixing {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Manual override for better quality and removing hallucinations
    new_prompts = {
        "general_summary": "A cinematic graphic novel illustration of a square CubeSat satellite orbiting Earth, glowing with blue digital data streams representing a software hack.",
        "introduction": "A small BEESAT-1 nanosatellite floating in space with Earth in the background, toon style, high detail.",
        "development": "A determined university student sitting at a cluttered desk with multiple monitors displaying code and satellite telemetry, dark room, glowing screens.",
        "conclusion": "The satellite successfully transmitting a signal back to Earth, visualized as a beam of light connecting to a ground station in Berlin, triumphant atmosphere."
    }
    
    data['prompts'] = new_prompts
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("Prompts updated.")
    
    # Generate General Summary Image
    output_filename = "3_Hackeou_o_espaço_alemão_fez_o_que_a_NASA_não_conse_general_summary.png"
    output_path = os.path.join("data/images", output_filename)
    
    print(f"Generating image: {output_filename}")
    service = ImageService()
    service.generate_image(
        prompt=new_prompts['general_summary'],
        output_path=output_path
    )
    print("Done.")

if __name__ == "__main__":
    fix_file_3()
