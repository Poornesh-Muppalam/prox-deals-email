import sys
from prox.config import load_env
from prox.send_weekly import run_send_weekly_dryrun

def main():
    load_env()

    if len(sys.argv) < 2:
        print("Usage: python -m prox send-weekly")
        raise SystemExit(1)

    cmd = sys.argv[1]
    if cmd == "send-weekly":
        n = run_send_weekly_dryrun()
        print(f"Generated {n} email previews in ./output/")
    else:
        print(f"Unknown command: {cmd}")
        raise SystemExit(1)
