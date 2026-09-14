import os
import httpx
import subprocess
import tarfile
from pathlib import Path

# Paths
HOME_DIR = Path.home()
PIPER_DIR = HOME_DIR / ".piper"
VOICES_DIR = PIPER_DIR / "voices"
CONFIG_DIR = HOME_DIR / ".config" / "piper-tui"
CONFIG_FILE = CONFIG_DIR / "config.env"
READ_SCRIPT = PIPER_DIR / "read-selection.sh"
ENGINE_BIN = PIPER_DIR / "piper" / "piper"

def init_directories():
    PIPER_DIR.mkdir(parents=True, exist_ok=True)
    VOICES_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

def is_engine_installed():
    return ENGINE_BIN.exists()

async def download_engine(progress_callback=None):
    init_directories()
    url = "https://github.com/rhasspy/piper/releases/latest/download/piper_linux_x86_64.tar.gz"
    tar_path = PIPER_DIR / "piper_linux_x86_64.tar.gz"
    
    async with httpx.AsyncClient() as client:
        async with client.stream("GET", url, follow_redirects=True) as response:
            response.raise_for_status()
            total = int(response.headers.get("Content-Length", 0))
            downloaded = 0
            with open(tar_path, "wb") as f:
                async for chunk in response.aiter_bytes(chunk_size=65536):
                    f.write(chunk)
                    downloaded += len(chunk)
                    if progress_callback and total:
                        progress_callback(downloaded, total)
                        
    # Signal extraction start
    if progress_callback:
        progress_callback(-1, -1) 
        
    with tarfile.open(tar_path, "r:gz") as tar:
        tar.extractall(path=PIPER_DIR)
    tar_path.unlink()

async def download_voice(voice_data, progress_callback=None):
    init_directories()
    onnx_url = voice_data["download_url"]
    json_url = voice_data["json_url"]
    
    filename_base = voice_data["file_path"].split('/')[-1]
    onnx_path = VOICES_DIR / filename_base
    json_path = VOICES_DIR / (filename_base + ".json")
    
    async with httpx.AsyncClient() as client:
        # 1. Download JSON config
        json_resp = await client.get(json_url, follow_redirects=True)
        json_resp.raise_for_status()
        with open(json_path, "wb") as f:
            f.write(json_resp.content)
            
        # 2. Download ONNX binary with progress
        async with client.stream("GET", onnx_url, follow_redirects=True) as response:
            response.raise_for_status()
            total = int(response.headers.get("Content-Length", 0))
            downloaded = 0
            with open(onnx_path, "wb") as f:
                async for chunk in response.aiter_bytes(chunk_size=65536):
                    f.write(chunk)
                    downloaded += len(chunk)
                    if progress_callback and total:
                        progress_callback(downloaded, total)
                        
    # 3. Save as active voice config
    save_active_voice(voice_data["name"], str(onnx_path))

def save_active_voice(voice_name, voice_file_path):
    # Determine sample rate. Usually 22050 for medium/high quality, 16000 for low.
    sample_rate = 16000
    if "high" in voice_name.lower() or "medium" in voice_name.lower():
        sample_rate = 22050
        
    config_content = f"""ACTIVE_VOICE="{voice_name}"
VOICE_FILE="{voice_file_path}"
SAMPLE_RATE={sample_rate}
"""
    with open(CONFIG_FILE, "w") as f:
        f.write(config_content)
        
    update_read_script(voice_file_path, sample_rate)

def get_installed_voices():
    """Retourne la liste des noms de fichiers (sans l'extension) des voix installées."""
    if not VOICES_DIR.exists():
        return []
    installed = []
    for f in VOICES_DIR.iterdir():
        if f.suffix == ".onnx":
            installed.append(f.name)
    return installed

def delete_voice(filename: str):
    """Supprime les fichiers (.onnx et .json) d'une voix installée."""
    onnx = VOICES_DIR / filename
    json_f = VOICES_DIR / (filename + ".json")
    if onnx.exists():
        onnx.unlink()
    if json_f.exists():
        json_f.unlink()

def update_read_script(voice_file_path, sample_rate):
    import os
    from pathlib import Path
    app_dir = Path(__file__).resolve().parent.parent
    widget_path = app_dir / "src" / "widget.py"
    
    script_content = f"""#!/bin/bash
if [ "$XDG_SESSION_TYPE" = "wayland" ]; then
    TEXT=$(wl-paste --primary)
else
    TEXT=$(xsel -o)
fi

if [ ! -z "$TEXT" ]; then
    if pkill -x piper ; then
        pkill -f "[w]idget.py" || true
        exit 0
    fi
    echo "$TEXT" | {ENGINE_BIN} \
        --model "{voice_file_path}" \
        --output_raw | aplay -r {sample_rate} -f S16_LE -t raw &
        
    VENV_PYTHON="$HOME/.config/piper-tui/venv/bin/python"
    WIDGET_PATH="{widget_path}"
    if [ -f "$VENV_PYTHON" ] && [ -f "$WIDGET_PATH" ]; then
        "$VENV_PYTHON" "$WIDGET_PATH" &
    fi
fi
"""
    with open(READ_SCRIPT, "w") as f:
        f.write(script_content)
    os.chmod(READ_SCRIPT, 0o755)

def get_current_config():
    if not CONFIG_FILE.exists():
        return {"ACTIVE_VOICE": "Aucune", "VOICE_FILE": "", "SAMPLE_RATE": "16000"}
        
    conf = {}
    with open(CONFIG_FILE, "r") as f:
        for line in f:
            if "=" in line:
                k, v = line.strip().split("=", 1)
                conf[k] = v.strip('"')
    return conf
