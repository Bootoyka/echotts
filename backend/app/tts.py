import subprocess
from pathlib import Path

MODEL_PATH = "models/model.onnx"
CONFIG_PATH = "models/model.onnx.json"

AUDIO_DIR = Path("data/audio")
AUDIO_DIR.mkdir(parents=True, exist_ok=True)


def generate_audio(text: str, job_id: str) -> str:
    output_path = AUDIO_DIR / f"{job_id}.wav"

    cmd = [
        "piper",
        "--model", MODEL_PATH,
        "--config", CONFIG_PATH,
        "--output_file", str(output_path),
    ]

    result = subprocess.run(
        cmd,
        input=text,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"Piper failed:\nSTDERR:\n{result.stderr}"
        )

    return str(output_path)