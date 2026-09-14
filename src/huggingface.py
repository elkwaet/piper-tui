import httpx
import json

class HuggingFaceAPI:
    BASE_URL = "https://huggingface.co/rhasspy/piper-voices/raw/main/voices.json"
    DOWNLOAD_URL = "https://huggingface.co/rhasspy/piper-voices/resolve/main/{}"

    @classmethod
    async def fetch_french_voices(cls):
        """Récupère dynamiquement toutes les voix françaises disponibles."""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(cls.BASE_URL)
                response.raise_for_status()
                data = response.json()
            except Exception as e:
                # Fallback on network error
                return []
        
        french_voices = []
        for voice_key, voice_data in data.items():
            lang = voice_data.get("language", {}).get("family")
            if lang == "fr":
                # Cherche le fichier ONNX
                onnx_file = next((f for f in voice_data.get("files", {}).keys() if f.endswith(".onnx")), None)
                if not onnx_file:
                    continue
                
                name = voice_data.get("name", "Inconnu").capitalize()
                quality = voice_data.get("quality", "inconnue")
                
                # Le taux d'échantillonnage dépend souvent de la qualité dans les modèles rhasspy, 
                # mais le plus sûr est de l'extraire du fichier JSON de config du modèle (souvent 22050 ou 16000).
                # Pour l'UI, on liste juste les options.
                
                french_voices.append({
                    "key": voice_key,
                    "name": f"{name} ({quality})",
                    "file_path": onnx_file,
                    "download_url": cls.DOWNLOAD_URL.format(onnx_file),
                    "json_url": cls.DOWNLOAD_URL.format(onnx_file + ".json")
                })
        return french_voices
