import subprocess
import json

def run_wpscan_docker(target_url, api_token):
    try:
        # Docker command to run WPScan
        cmd = [
            "docker", "run", "--rm",
            "wpscanteam/wpscan",
            "--url", target_url,
            "--format", "json",
            "--api-token", api_token
        ]

        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode != 0:
            print("[!] WPScan Docker Error:")
            print(result.stderr)
            return None

        # Parse the JSON output
        output_json = json.loads(result.stdout)
        return output_json

    except Exception as e:
        print(f"[!] Exception: {e}")
        return None


# ======= Test script ========
if __name__ == "__main__":
    url = input("Nhập URL website WordPress: ").strip() or 'https://vi.wordpress.org/'
    api_key = input("Nhập WPScan API token: ").strip() or 'Ee8c58nlO0483oCZj0Ih4PJUUJW5N6VHA0eztvTZFAE'

    result = run_wpscan_docker(url, api_key)

    if result:
        print(json.dumps(result, indent=2))
    else:
        print("Không có kết quả.")
