import subprocess
import os

def separate_audio(file_path: str):
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)

    subprocess.run([
        "spleeter", "separate",
        "-p", "spleeter:4stems",
        "-o", output_dir,
        file_path
    ])

    return output_dir
