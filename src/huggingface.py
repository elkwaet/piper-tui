import httpx
import json

class HuggingFaceAPI:
    BASE_URL = "https://huggingface.co/rhasspy/piper-voices/raw/main/voices.json"
    DOWNLOAD_URL = "https://huggingface.co/rhasspy/piper-voices/resolve/main/{}"

    @classmethod
    async def fetch_catalog_voices(cls):
        """Récupère dynamiquement les voix (FR et EN) disponibles."""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(cls.BASE_URL)
                response.raise_for_status()
                data = response.json()
            except Exception as e:
                # Fallback on network error
                return []
        
        catalog_voices = []
        quality_map = {"high": 1, "medium": 2, "low": 3, "x-low": 4}

        for voice_key, voice_data in data.items():
            lang_data = voice_data.get("language")
            if not lang_data:
                continue
            
            lang_code = lang_data.get("code") or lang_data.get("family")
            if not lang_code:
                continue

            onnx_file = next((f for f in voice_data.get("files", {}).keys() if f.endswith(".onnx")), None)
            if not onnx_file:
                continue
            
            name = voice_data.get("name", "Inconnu").capitalize()
            quality_raw = voice_data.get("quality", "inconnue")
            code = lang_code.replace("_", "-").upper()
            
            catalog_voices.append({
                "key": voice_key,
                "name": f"[{code}] {name} ({quality_raw})",
                "file_path": onnx_file,
                "download_url": cls.DOWNLOAD_URL.format(onnx_file),
                "json_url": cls.DOWNLOAD_URL.format(onnx_file + ".json"),
                "lang_code": code,
                "quality_raw": quality_raw,
                "raw_name": name
            })
            
        catalog_voices.sort(key=lambda x: (
            x["lang_code"],
            quality_map.get(x["quality_raw"], 99),
            x["raw_name"]
        ))
        return catalog_voices
