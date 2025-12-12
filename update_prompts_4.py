from services.prompt_generator import OllamaPromptGenerator
import json
import glob
import os

def update_files():
    generator = OllamaPromptGenerator(model="llama3.2:3b")
    files = glob.glob('data/*.json')
    
    print(f"Found {len(files)} files to check...")
    
    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            summary = data.get('summary', {})
            prompts = data.get('prompts', {})
            
            # Check if needs update
            if 'general_summary' in prompts:
                print(f"Skipping {file_path} (already has general_summary)")
                continue
                
            print(f"Updating prompts for {file_path}...")
            
            # Re-generate ALL prompts to ensure consistency
            new_prompts = generator.generate_prompts(summary)
            
            data['prompts'] = new_prompts
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"  Updated!")

        except Exception as e:
            print(f"Error processing {file_path}: {e}")

if __name__ == "__main__":
    update_files()
