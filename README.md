# GGUF Modelfile Maker

A Python tool to catalog all `.gguf` files in a folder, save their locations to a CSV, and generate Ollama-compatible `.Modelfile` stubs for each model. The typical usecase would be when you use BOTH LMStudio and Ollama, and want to catalog all your .ggufs for use in Ollama. I prefer this approach to Ollama managing the models because it is easier to manage models by name and size than Ollama's default method of blobs and manifests. It's also easier to set up custom parameters.

## Features
- Recursively scans a folder for `.gguf` files and catalogs them with normalized parent folder names.
- Saves a CSV catalog (`latest_GGUF_catalog.csv`) of all found models.
- Generates `.Modelfile` stubs for each model, compatible with Ollama, using a customizable template.
- Fully interactive: prompts for all paths, but supports environment variable overrides and sensible defaults.

## Requirements
- Python 3.8+
- See `requirements.txt` for required packages.

## Installation
```bash
pip install -r requirements.txt
```

## Usage
1. Run the script:
   ```bash
   python gguf-modelfile-maker.py
   ```
2. When prompted, enter the folder containing your `.gguf` files (or press Enter to use the default).
3. Enter the folder where `.Modelfile` stubs should be saved (or press Enter to use the default).
4. The script will:
    - Catalog all `.gguf` files and save a CSV.
    - Optionally let you select a different CSV for modelfile generation.
    - Generate `.Modelfile` stubs for each model in the chosen output directory.

## Environment Variables (`.env`)
- `MODELFILE_LOCATION`: Default directory to save `.Modelfile` stubs.
- `MODELFILE_DEFAULTS`: Default content to append to each `.Modelfile` (e.g., context length, prompt, etc).

Example `.env`:
```
MODELFILE_LOCATION=/your/modelfile/output/dir
MODELFILE_DEFAULTS=PARAM1=value1\nPARAM2=value2
```

## Output
- `latest_GGUF_catalog.csv`: Catalog of all found `.gguf` files.
- `.Modelfile` stubs: One per model, named after the normalized parent folder.

## License
MIT

---
Contributions and issues welcome!
