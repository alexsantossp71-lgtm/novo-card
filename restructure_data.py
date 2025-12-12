import os
import shutil
import glob

def restructure():
    # Base data dir
    data_dir = "data"
    
    # Get all JSON files in data/
    json_files = glob.glob(os.path.join(data_dir, "*.json"))
    
    print(f"Found {len(json_files)} JSON files to restructure.")
    
    for filepath in json_files:
        filename = os.path.basename(filepath)
        
        # Skip if it doesn't look like our standard "ID_Title.json" format
        # Check if first char is digit
        if not filename[0].isdigit():
            print(f"Skipping {filename} (doesn't start with digit)")
            continue
            
        # Create folder name same as filename without extension
        folder_name = filename.replace('.json', '')
        target_dir = os.path.join(data_dir, folder_name)
        
        # Create directory
        os.makedirs(target_dir, exist_ok=True)
        
        # Move JSON file
        target_path = os.path.join(target_dir, filename)
        shutil.move(filepath, target_path)
        print(f"Moved {filename} -> {target_dir}/")
        
    print("Restructure complete.")

if __name__ == "__main__":
    restructure()
