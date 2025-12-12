from services.image_service import ImageService
import time
import os

def generate_request():
    print("Initializing ImageService...")
    service = ImageService()
    
    # Prompt Parameters from user
    prompt = "woman cheyenne, detailed, sharp, HD, HDR, best quality, best resolution, 2D, colored Graphic Novel illustration, By Gibrat, hatching, lineart, sketch, hyper illustration, vibrant, saturated"
    negative_prompt = "simple background"
    seed = 3694963653
    steps = 30
    cfg = 3.5
    width = 832
    height = 1216
    
    # Output file
    output_dir = "data/outputs"
    os.makedirs(output_dir, exist_ok=True)
    timestamp = int(time.time())
    output_path = f"{output_dir}/cheyenne_req_{timestamp}.png"
    
    print(f"Starting generation...")
    print(f"Prompt: {prompt}")
    print(f"Seed: {seed}, Size: {width}x{height}, Steps: {steps}, CFG: {cfg}")
    
    start_time = time.time()
    
    service.generate_image(
        prompt=prompt,
        output_path=output_path,
        negative_prompt=negative_prompt,
        steps=steps,
        seed=seed,
        guidance_scale=cfg,
        width=width,
        height=height,
        upscale=False # Skipping hires fix for now to ensure base generation works on 6GB
    )
    
    elapsed = time.time() - start_time
    print(f"Generation complete in {elapsed:.2f}s")
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    generate_request()
