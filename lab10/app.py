import os
import yaml
import hvac

def get_secret_from_env():
    return os.environ["APP_SECRET"]

def get_secret_from_file():
    with open("config.yaml", "r") as f:
        data = yaml.safe_load(f)
    return data["app"]["secret"]

def get_secret_from_vault():
    vault_addr = os.environ["VAULT_ADDR"]
    vault_token = os.environ["VAULT_TOKEN"]

    client = hvac.Client(url=vault_addr, token=vault_token)
    resp = client.secrets.kv.v2.read_secret_version(path="app")
    return resp["data"]["data"]["APP_SECRET"]

if __name__ == "__main__":
    mode = os.getenv("MODE", "env")  # env / file / vault

    if mode == "env":
        secret = get_secret_from_env()
        print(f"[ENV] Secret = {secret}")

    elif mode == "file":
        secret = get_secret_from_file()
        print(f"[FILE] Secret = {secret}")

    elif mode == "vault":
        secret = get_secret_from_vault()
        print(f"[VAULT] Secret = {secret}")

    else:
        raise ValueError("Unknown MODE. Use env / file / vault")

