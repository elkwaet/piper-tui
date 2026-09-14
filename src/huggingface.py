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
        for voice_key, voice_data in data.items():
            lang = voice_data.get("language", {}).get("family")
            if lang in ["fr", "en"]:
                onnx_file = next((f for f in voice_data.get("files", {}).keys() if f.endswith(".onnx")), None)
                if not onnx_file:
                    continue
                
                name = voice_data.get("name", "Inconnu").capitalize()
                quality = voice_data.get("quality", "inconnue")
                code = voice_data.get("language", {}).get("code", lang).replace("_", "-").upper()
                
                catalog_voices.append({
                    "key": voice_key,
                    "name": f"[{code}] {name} ({quality})",
                    "file_path": onnx_file,
                    "download_url": cls.DOWNLOAD_URL.format(onnx_file),
                    "json_url": cls.DOWNLOAD_URL.format(onnx_file + ".json")
                })
                
        catalog_voices.sort(key=lambda x: x["name"])
        return catalog_voices
