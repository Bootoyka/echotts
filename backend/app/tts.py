import subprocess
from backend.app.config import settings

AUDIO_DIR = settings.AUDIO_DIR
AUDIO_DIR.mkdir(parents=True, exist_ok=True)


def generate_audio(text: str, job_id: str) -> str:
    output_path = AUDIO_DIR / f"{job_id}.wav"

    cmd = [
        "piper",
        "--model", settings.MODEL_PATH,
        "--config", settings.CONFIG_PATH,
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