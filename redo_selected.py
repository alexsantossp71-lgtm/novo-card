import json
import os
from services.prompt_generator import OllamaPromptGenerator
from services.image_service import ImageService
import time

def redo_selected():
    files = [
        "data/2_A_Geração_Z_está_perdendo_uma_habilidade_milenar_d.json",
        "data/4_Trump_diz_que_assinará_decreto_para_restringir_lei.json"
    ]

    print("Initializing Services for Redo...")
    # Increase timeout for prompt gen in case Ollama is slow
    prompt_gen = OllamaPromptGenerator(model="llama3.2:3b")
    image_service = ImageService()
    
    os.makedirs("data/images", exist_ok=True)

    for i, filepath in enumerate(files):
        print(f"\n[{i+1}/{len(files)}] Redoing {filepath}...")
        
        if not os.path.exists(filepath):
            print(f"  File not found: {filepath}")
            continue

        try:
            # 1. Load JSON
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 2. Regenerate Prompts
            print("  Regenerating prompts...")
            summary = data.get('summary', {})
            # Retry mechanism for prompts
            new_prompts = prompt_gen.generate_prompts(summary)
            
            # Check for error
            if new_prompts.get('general_summary') == "Error":
                print("  Failed to generate prompts (Ollama Error). Retrying once...")
                time.sleep(2)
                new_prompts = prompt_gen.generate_prompts(summary)
            
            # Update data
            data['prompts'] = new_prompts
            
            # Save updated JSON
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print("  JSON updated with new prompts.")
            
            # 3. Generate Image
            prompt = new_prompts.get('general_summary')
            if not prompt or prompt == "Error":
                print(f"  Skipping image generation due to invalid prompt: {prompt}")
                continue
                
            basename = os.path.basename(filepath).replace('.json', '')
            output_filename = f"{basename}_general_summary.png"
            output_path = os.path.join("data/images", output_filename)
            
            print(f"  Generating image: {output_filename}")
            print(f"  Base Prompt: {prompt}")
            
            start_t = time.time()
            image_service.generate_image(
                prompt=prompt,
                output_path=output_path
            )
            print(f"  Image generated in {time.time() - start_t:.2f}s")
            
        except Exception as e:
            print(f"  Error processing {filepath}: {e}")

if __name__ == "__main__":
    redo_selected()
