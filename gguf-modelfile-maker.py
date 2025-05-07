########### PYTHON
# Script Title: GGUF Catalog and Modelfile Generator
# Script Description: Catalogs .gguf files in a folder, saves CSV, and generates Modelfile stubs for each model.
# Script Author: myPyAI + Naveen Srivatsav
# Last Updated: 20250507
###########

import os
import pandas as pd
from datetime import datetime
from pathlib import Path
import csv
import dotenv


def prompt_for_folder(user_input, default_path, must_exist=True):
    """
    Takes user_input and default_path. If user_input is empty, uses default_path.
    Validates the resulting path (if must_exist). Returns Path object.
    """
    folder_str = user_input.strip() if user_input else str(default_path)
    folder = Path(folder_str).expanduser().resolve()
    if must_exist and not folder.is_dir():
        print(f"Provided path '{folder}' is not a valid directory.")
        return None
    return folder


def collect_gguf_files(root_folder):
    """
    Recursively traverses root_folder for .gguf files.
    Returns list of (normalized_parent_folder, absolute_file_path).
    """
    records = []
    for dirpath, _, filenames in os.walk(root_folder):
        for fname in filenames:
            if fname.lower().endswith('.gguf'):
                abs_path = Path(dirpath) / fname
                parent_name = abs_path.parent.name
                if parent_name.lower().endswith('-gguf'):
                    parent_name = parent_name[:-5]
                normalized = f"lmstudio-{parent_name}".lower()
                records.append((normalized, str(abs_path)))
    return records


def save_catalog(records, output_dir):
    """
    Save records to a timestamped CSV in output_dir. Returns Path to CSV.
    """
    #now = datetime.now().strftime('%Y%m%d%H%M%S')
    out_name = "latest_GGUF_catalog.csv"
    df = pd.DataFrame(records, columns=["ParentFolder", "AbsoluteGGUFPath"])
    out_path = Path(output_dir) / out_name
    df.to_csv(out_path, index=False)
    return out_path


def load_gguf_paths_from_csv(csv_path):
    """
    Loads a CSV of ParentFolder,AbsoluteGGUFPath and returns a dict.
    """
    gguf_paths = {}
    with open(csv_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            gguf_paths[row['ParentFolder']] = row['AbsoluteGGUFPath']
    return gguf_paths


def generate_modelfiles(gguf_paths, modelfile_dir, modelfile_defaults):
    """
    For each model, create a .Modelfile in modelfile_dir with FROM and defaults.
    """
    modelfile_dir = Path(modelfile_dir)
    modelfile_dir.mkdir(parents=True, exist_ok=True)
    for model_name, path in gguf_paths.items():
        modelfile_path = modelfile_dir / f"{model_name}.Modelfile"
        with open(modelfile_path, mode='w') as modelfile:
            modelfile.write(f"FROM {path}\n")
            if modelfile_defaults:
                modelfile.write(f"{modelfile_defaults}\n")
        print(f"Wrote: {modelfile_path}")


def main():
    dotenv.load_dotenv()
    dotenv.load_dotenv(override=True)
    print("--- GGUF Catalog and Modelfile Generator ---")

    default_modelfile_dir = Path("/Users/sumergoconicio/Documents/Code/Models/modelfiles")
    default_gguf_dir = Path("/Volumes/somatique/AImodels")
    modelpath_input = input(f"Enter desired folder path here or leave blank to use default value [{default_gguf_dir}]: ")
    modelfilepath_input = input(f"Enter folder to save .Modelfile stubs or leave blank to use default [{default_modelfile_dir}]: ")
    
    # Step 0: Prompt for folder paths   
    modelpath = prompt_for_folder(modelpath_input, default_gguf_dir, must_exist=True)
    if modelpath is None:
        return
    modelfilepath = prompt_for_folder(modelfilepath_input, default_modelfile_dir, must_exist=False) 
    if modelfilepath is None:
        return

    # Step 1: Catalog GGUF files
    gguf_records = collect_gguf_files(modelpath)
    if not gguf_records:
        print("No .gguf files found in the specified folder.")
        return
    
    output_csv = save_catalog(gguf_records, modelfilepath)
    print(f"Catalog saved: {output_csv}")

    # Step 2: Load GGUF paths from CSV (user can override path)
    use_csv = input(f"Use generated CSV ({output_csv})? [Y/n]: ").strip().lower()
    if use_csv in ('', 'y', 'yes'):
        ggufs_csv = output_csv
    else:
        user_csv_input = input(f"Enter desired GGUF catalog CSV path or leave blank to use default [{output_csv}]: ")
        ggufs_csv = prompt_for_folder(user_csv_input, output_csv, must_exist=True)
        if ggufs_csv is None:
            return
    gguf_paths = load_gguf_paths_from_csv(ggufs_csv)
    print(f"Loaded {len(gguf_paths)} GGUF paths from CSV.")

    # Step 3: Generate Modelfiles
    modelfile_defaults = os.getenv("MODELFILE_DEFAULTS") or ""
    generate_modelfiles(gguf_paths, modelfilepath, modelfile_defaults)
    print("All Modelfiles generated.")


if __name__ == "__main__":
    main()
