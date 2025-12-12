import os
import json
import glob
import shutil
import zipfile

DOCS_DIR = 'docs'
ASSETS_DIR = os.path.join(DOCS_DIR, 'assets')
DATA_DIR = 'data'

def build_site():
    print("Building Static Site...")
    
    # 1. Clean/Create Dirs
    if os.path.exists(DOCS_DIR):
        # Don't delete verify files (html/css/js) if they exist, but clear assets? 
        # Actually safer to just ensure structure.
        pass
    
    os.makedirs(ASSETS_DIR, exist_ok=True)
    
    news_items = []
    
    # 2. Scan Data
    # Get all subfolders in data/
    subdirs = [os.path.join(DATA_DIR, d) for d in os.listdir(DATA_DIR) if os.path.isdir(os.path.join(DATA_DIR, d))]
    # Sort by name (which starts with index) or modification time? 
    # Filenames start with index, so sorting by name is good enough for now.
    # To be numerically correct, let's sort by the integer prefix.
    
    def get_sort_key(path):
        name = os.path.basename(path)
        try:
            return int(name.split('_')[0])
        except:
            return 0
            
    subdirs.sort(key=get_sort_key, reverse=True) # Newest first
    
    print(f"Found {len(subdirs)} news items.")
    
    for subdir in subdirs:
        folder_name = os.path.basename(subdir)
        json_files = glob.glob(os.path.join(subdir, "*.json"))
        if not json_files: continue
        
        json_path = json_files[0]
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except:
            print(f"Error reading {json_path}")
            continue
            
        # Target Asset Folder
        item_assets_dir = os.path.join(ASSETS_DIR, folder_name)
        os.makedirs(item_assets_dir, exist_ok=True)
        
        # Images to handle
        images = ['general_summary.png', 'introduction.png', 'development.png', 'conclusion.png']
        valid_images = []
        
        # Copy Images
        for img_name in images:
            src_img = os.path.join(subdir, img_name)
            if os.path.exists(src_img):
                shutil.copy2(src_img, os.path.join(item_assets_dir, img_name))
                valid_images.append(img_name)
        
        # Create ZIP
        zip_path = os.path.join(item_assets_dir, 'images.zip')
        with zipfile.ZipFile(zip_path, 'w') as zf:
            for img_name in valid_images:
                zf.write(os.path.join(item_assets_dir, img_name), arcname=img_name)
                
        # Build Data Object
        summary = data.get('summary', {})
        prompts = data.get('prompts', {})
        
        item_data = {
            "id": folder_name,
            "title": data.get('title'),
            "date": data.get('date'),
            "url": data.get('url'),
            "assets_path": f"assets/{folder_name}",
            "zip_path": f"assets/{folder_name}/images.zip",
            "content": {
                "introduction": {
                    "text": summary.get('introduction', ''),
                    "image": "introduction.png",
                    "prompt": prompts.get('introduction', '')
                },
                "development": {
                    "text": summary.get('development', ''),
                    "image": "development.png",
                    "prompt": prompts.get('development', '')
                },
                "conclusion": {
                    "text": summary.get('conclusion', ''),
                    "image": "conclusion.png",
                    "prompt": prompts.get('conclusion', '')
                },
                "general_summary": {
                    "image": "general_summary.png",
                    "prompt": prompts.get('general_summary', '')
                },
                "tiktok_summary": summary.get('tiktok_summary', '')
            }
        }
        news_items.append(item_data)
        print(f"Processed {folder_name}")

    # 3. Write data.js
    js_content = f"const newsData = {json.dumps(news_items, ensure_ascii=False, indent=2)};"
    with open(os.path.join(DOCS_DIR, 'data.js'), 'w', encoding='utf-8') as f:
        f.write(js_content)
        
    print(f"Site built! Data saved to {os.path.join(DOCS_DIR, 'data.js')}")

if __name__ == "__main__":
    build_site()
