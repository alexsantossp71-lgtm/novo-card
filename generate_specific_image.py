from services.image_service import ImageService
import os

def generate():
    service = ImageService()
    
    prompt = "Image of a formal Supreme Court session with judges in robes, including Flávio Dino and Alexandre de Moraes, in a virtual plenarium."
    negative_prompt = "blurry, low quality, ugly, watermark, text"
    
    # Target Path based on convention
    output_dir = "data/images"
    os.makedirs(output_dir, exist_ok=True)
    filename = "5_STF_marca_sessão_para_confirmar_a_decisão_que_ence_general_summary.png"
    output_path = os.path.join(output_dir, filename)
    
    print(f"Starting generation for: {output_path}")
    print(f"Prompt: {prompt}")
    
    service.generate_image(prompt, output_path, negative_prompt=negative_prompt)
    
    if os.path.exists(output_path):
        print(f"Success! Image saved to {output_path}")
    else:
        print("Failed to save image.")

if __name__ == "__main__":
    generate()
