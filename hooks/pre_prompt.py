import sys
import subprocess

def is_thing_installed(thing: str):
    try:
        subprocess.run([thing, "--version"], capture_output=True, check=True)
        print(f'SUCCESS: {thing} is installed')
    except Exception:
        print(f"ERROR: {thing} is not installed.")
        sys.exit(1)

if __name__ == "__main__":
    is_thing_installed('docker')
    is_thing_installed('uv')
    is_thing_installed('node')
    is_thing_installed('git')