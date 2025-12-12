import json
import os
from services.prompt_generator import OllamaPromptGenerator
from services.image_service import ImageService
import time

def process_batch():
    files = [
        "data/1_Lula_afirma_ter_dito_a_Trump_que_não_quer_guerra_n.json",
        "data/2_A_Geração_Z_está_perdendo_uma_habilidade_milenar_d.json",
        "data/3_Hackeou_o_espaço_alemão_fez_o_que_a_NASA_não_conse.json",
        "data/4_Trump_diz_que_assinará_decreto_para_restringir_lei.json",
        "data/5_STF_marca_sessão_para_confirmar_a_decisão_que_ence.json",
        "data/6_PL_da_dosimetria_é_uma_meia_anistia_aos_bolsonaris.json"
    ]

    print("Initializing Services...")
    prompt_gen = OllamaPromptGenerator(model="llama3.2:3b")
    image_service = ImageService()
    
    # Ensure images directory exists
    os.makedirs("data/images", exist_ok=True)

    for i, filepath in enumerate(files):
        print(f"\n[{i+1}/{len(files)}] Processing {filepath}...")
        
        if not os.path.exists(filepath):
            print(f"  File not found: {filepath}")
            continue

        try:
            # 1. Load JSON
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 2. Regenerate Prompts (fixing the prompts)
            print("  Regenerating prompts with new rules...")
            summary = data.get('summary', {})
            new_prompts = prompt_gen.generate_prompts(summary)
            
            # Update data
            data['prompts'] = new_prompts
            
            # Save updated JSON
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print("  JSON updated.")

            # 3. Generate Image for general_summary
            prompt = new_prompts.get('general_summary')
            if not prompt:
                print("  No general_summary prompt found.")
                continue
                
            # Define output filename
            # Use the numeric prefix + safe title + _gen.png
            basename = os.path.basename(filepath).replace('.json', '')
            output_filename = f"{basename}_general_summary.png"
            output_path = os.path.join("data/images", output_filename)
            
            print(f"  Generating image: {output_filename}")
            print(f"  Prompt: {prompt}")
            
            start_t = time.time()
            image_service.generate_image(
                prompt=prompt,
                output_path=output_path
                # defaults (30 steps, 3.5 CFG, etc) and style suffix handled by service
            )
            print(f"  Image generated in {time.time() - start_t:.2f}s")
            
        except Exception as e:
            print(f"  Error processing {filepath}: {e}")

if __name__ == "__main__":
    process_batch()
