import json
import os
import glob
from services.prompt_generator import OllamaPromptGenerator
from services.image_service import ImageService
import time

def generate_all():
    # Base data dir
    data_dir = "data"
    
    # Get all subdirectories
    subdirs = [os.path.join(data_dir, d) for d in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, d)) and d != "images" and d != "outputs"]
    
    print(f"Found {len(subdirs)} news folders.")
    
    prompt_gen = OllamaPromptGenerator(model="llama3.2:3b")
    image_service = ImageService()
    
    total_images = len(subdirs) * 4
    current_image = 0
    
    for subdir in subdirs:
        # Find JSON file
        json_files = glob.glob(os.path.join(subdir, "*.json"))
        if not json_files:
            print(f"No JSON in {subdir}, skipping.")
            continue
            
        json_path = json_files[0]
        print(f"\nProcessing {json_path}...")
        
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Check prompts
            prompts = data.get('prompts', {})
            needs_update = False
            
            # If any prompt is missing or Error, regenerate ALL to be safe/consistent
            keys = ['general_summary', 'introduction', 'development', 'conclusion']
            if any(prompts.get(k, "") == "Error" or not prompts.get(k) for k in keys):
                print("  Found invalid prompts. Regenerating...")
                summary = data.get('summary', {})
                new_prompts = prompt_gen.generate_prompts(summary)
                
                # Retry if error
                if new_prompts.get('general_summary') == "Error":
                    print("  Retry prompt generation...")
                    time.sleep(2)
                    new_prompts = prompt_gen.generate_prompts(summary)
                
                data['prompts'] = new_prompts
                prompts = new_prompts
                needs_update = True
                
            if needs_update:
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print("  JSON updated.")
                
            # Generate Images
            for key in keys:
                prompt_text = prompts.get(key)
                if not prompt_text or prompt_text == "Error":
                    print(f"  Skipping {key} (invalid prompt)")
                    continue
                    
                output_filename = f"{key}.png"
                output_path = os.path.join(subdir, output_filename)
                
                # We overwrite as requested "gera todas as imagens"
                print(f"  [{current_image+1}/{total_images}] Generating: {output_filename}")
                # print(f"    Prompt: {prompt_text[:50]}...")
                
                start_t = time.time()
                image_service.generate_image(
                    prompt=prompt_text,
                    output_path=output_path
                )
                print(f"    Done in {time.time() - start_t:.2f}s")
                current_image += 1
                
        except Exception as e:
            print(f"  Error processing {subdir}: {e}")

if __name__ == "__main__":
    generate_all()
