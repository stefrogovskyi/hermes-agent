import json
import os
import re
import sys

def main():
    base_dir = os.getcwd()
    auth_path = os.path.join(base_dir, "auth.json")
    env_path = os.path.join(base_dir, ".env")
    
    if not os.path.exists(auth_path):
        home_auth = os.path.expanduser("~/.hermes/auth.json")
        if os.path.exists(home_auth):
            auth_path = home_auth

    if not os.path.exists(auth_path):
        print(f"Error: auth.json not found at {auth_path}", file=sys.stderr)
        sys.exit(1)
        
    try:
        with open(auth_path, "r", encoding="utf-8") as f:
            auth_data = json.load(f)
    except Exception as e:
        print(f"Error reading auth.json: {e}", file=sys.stderr)
        sys.exit(1)
        
    access_token = None
    providers = auth_data.get("providers", {})
    nous_info = providers.get("nous", {})
    if isinstance(nous_info, dict):
        access_token = nous_info.get("access_token")
        
    if not access_token and "access_token" in auth_data:
        access_token = auth_data["access_token"]
        
    if not access_token:
        if os.path.exists(env_path):
            with open(env_path, "r", encoding="utf-8") as f:
                content = f.read()
            if "NOUS_API_KEY=" in content:
                print("NOUS_API_KEY already present in .env, no new access_token in auth.json")
                sys.exit(0)
        print("Error: No access_token found in auth.json and NOUS_API_KEY not set in .env", file=sys.stderr)
        sys.exit(1)
        
    if not os.path.exists(env_path):
        print(f"Error: .env not found at {env_path}", file=sys.stderr)
        sys.exit(1)
        
    with open(env_path, "r", encoding="utf-8") as f:
        env_content = f.read()
        
    if "NOUS_API_KEY=" in env_content:
        env_content = re.sub(r'NOUS_API_KEY=.*', f'NOUS_API_KEY={access_token}', env_content)
    else:
        env_content += f"\nNOUS_API_KEY={access_token}\n"
        
    with open(env_path, "w", encoding="utf-8") as f:
        f.write(env_content)
        
    print("Successfully refreshed NOUS_API_KEY in .env")

if __name__ == "__main__":
    main()
