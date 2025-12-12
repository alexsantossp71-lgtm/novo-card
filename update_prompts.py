import os
import json
import glob
from services.prompt_generator import OllamaPromptGenerator

def main():
    data_dir = os.path.join(os.getcwd(), 'data')
    json_files = glob.glob(os.path.join(data_dir, '*.json'))
    
    if not json_files:
        print("No JSON files found in data/ directory.")
        return

    generator = OllamaPromptGenerator(model="llama3.2:3b")
    
    print(f"Found {len(json_files)} files to update.")
    
    for filepath in json_files:
        print(f"Processing {os.path.basename(filepath)}...")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                print(f"  Error reading JSON. Skipping.")
                continue
        
        if 'summary' not in data:
            print("  No summary found. Skipping.")
            continue
            
        # skip if already has prompts (optional, but good for idempotency)
        # if 'prompts' in data:
        #    print("  Prompts already exist. Skipping.")
        #    continue

        print("  Generating image prompts...")
        prompts = generator.generate_prompts(data['summary'])
        
        data['prompts'] = prompts
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        print("  Updated and saved.")

if __name__ == "__main__":
    main()
