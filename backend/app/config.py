from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent

AUDIO_DIR = BASE_DIR / "data" / "audio"

MODEL_PATH = BASE_DIR / "backend" / "models" / "model.onnx"

MODEL_CONFIG_PATH = BASE_DIR / "backend" / "models" / "model.onnx.json"