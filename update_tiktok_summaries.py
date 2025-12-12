from services.summarizer import OllamaSummarizer
import json
import glob
import os

def update_files():
    summarizer = OllamaSummarizer(model="llama3.2:3b")
    files = glob.glob('data/*.json')
    
    print(f"Found {len(files)} files to check...")
    
    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Check if needs update
            current_summary = data.get('summary', {})
            if 'tiktok_summary' in current_summary:
                print(f"Skipping {file_path} (already has tiktok_summary)")
                continue
                
            print(f"Updating {file_path}...")
            content = data.get('content')
            if not content:
                print(f"  Skipping {file_path} (no content)")
                continue

            # Re-generate summary to get the new field
            new_summary = summarizer.summarize(content)
            
            # Preserve existing fields if generation fails in a weird way, 
            # but usually we want the new structure.
            # Append Link to TikTok summary
            url = data.get('url', '')
            if 'tiktok_summary' in new_summary:
                new_summary['tiktok_summary'] += f"\n\n🔗 {url}"
            else:
                 # Fallback if model didn't output it
                 new_summary['tiktok_summary'] = f"Confira a notícia completa no link!\n\n🔗 {url}"

            data['summary'] = new_summary
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"  Updated!")

        except Exception as e:
            print(f"Error processing {file_path}: {e}")

if __name__ == "__main__":
    update_files()
