import os
import shutil
import json
from services.workflow_manager import WorkflowManager

def fix_recent_files():
    # Helper to utilize the new generate method
    manager = WorkflowManager()
    
    files_to_fix = [
        "7_O_dízimo_é_o_milagre_econômico_de_Jesus_que_salva_.json",
        "8_Senhores_do_Supremo_tenham_juízo.json",
        "9_O_Brasil_vive_um_estado_de_coisas_golpistas.json"
    ]
    
    print("Fixing files 7, 8, 9...")
    
    for filename in files_to_fix:
        src_path = os.path.join("data", filename)
        if not os.path.exists(src_path):
            print(f"File {filename} not found in root (maybe already moved?). Checking if folder exists...")
            # Check if it's already in a folder?
            base_name = filename.replace('.json', '')
            folder_path = os.path.join("data", base_name)
            target_path = os.path.join(folder_path, filename)
            
            if os.path.exists(target_path):
                 print(f"  Found in folder {folder_path}. Proceeding to generate images.")
                 src_path = target_path # Use this as source for reading data
            else:
                 print(f"  Could not find {filename} anywhere. Skipping.")
                 continue
        else:
            # Move it
            base_name = filename.replace('.json', '')
            folder_path = os.path.join("data", base_name)
            os.makedirs(folder_path, exist_ok=True)
            target_path = os.path.join(folder_path, filename)
            
            shutil.move(src_path, target_path)
            print(f"  Moved to {folder_path}")
            src_path = target_path

        # Now Generate Images
        try:
            with open(src_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            print(f"  Generating images for {base_name}...")
            manager.generate_images_for_article(src_path, data, progress_callback=lambda m: print(f"    {m}"))
            
        except Exception as e:
            print(f"  Error processing {filename}: {e}")

if __name__ == "__main__":
    fix_recent_files()
