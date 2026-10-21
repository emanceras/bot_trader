"""Run the real browser check with isolated synthetic state and owned child processes."""

import argparse
import os
import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--state-dir", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    state = args.state_dir.resolve()
    state.mkdir(parents=True, exist_ok=True, mode=0o700)
    python = root / ".venv/bin/python"
    command = [str(python), "-m", "bot_trader.cli", "--state-dir", str(state)]
    try:
        urllib.request.urlopen("http://127.0.0.1:8000/api/health", timeout=1)
    except urllib.error.URLError:
        pass
    else:
        raise RuntimeError("Port 8000 is occupied; stop your own development server first.")
    subprocess.run([*command, "init"], cwd=root, check=True, capture_output=True)
    subprocess.run([*command, "credential", "viewer"], cwd=root, check=True, capture_output=True)
    print("Initialized isolated synthetic browser state; starting API and worker.", flush=True)
    children = []
    with (state / "api.log").open("w") as api_log, (state / "worker.log").open("w") as worker_log:
        try:
            children.append(subprocess.Popen([*command, "serve"], cwd=root,
                                             stdout=api_log, stderr=subprocess.STDOUT))
            children.append(subprocess.Popen([*command, "worker", "--watch"], cwd=root,
                                             stdout=worker_log, stderr=subprocess.STDOUT))
            deadline = time.monotonic() + 60
            while True:
                if any(child.poll() is not None for child in children):
                    raise RuntimeError("A child process stopped; inspect the private test-state logs.")
                try:
                    with urllib.request.urlopen("http://127.0.0.1:8000/", timeout=1) as response:
                        if response.status == 200:
                            break
                except urllib.error.URLError:
                    pass
                if time.monotonic() >= deadline:
                    raise RuntimeError("Built web/API readiness timed out.")
                time.sleep(1)
            print("Built frontend and backend ready; running Chromium integration.", flush=True)
            environment = dict(os.environ)
            environment["BOT_TRADER_E2E_STATE"] = str(state)
            environment.setdefault("NPM_CONFIG_CACHE", str(state / "npm-cache"))
            subprocess.run(["npm", "run", "test:e2e"], cwd=root / "web", env=environment,
                           check=True, timeout=240)
        finally:
            for child in children:
                child.terminate()
            for child in children:
                try:
                    child.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    child.kill()
                    child.wait()
    print(f"Browser verification completed. Non-secret screenshots and private state: {state}")


if __name__ == "__main__":
    main()
