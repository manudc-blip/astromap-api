
import os, yaml

def load_config():
    here = os.getcwd()
    for fname in ("config.yaml", "config.yml"):
        fp = os.path.join(here, fname)
        if os.path.exists(fp):
            with open(fp, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
    example = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "config.example.yaml")
    example = os.path.abspath(example)
    if os.path.exists(example):
        with open(example, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    return {}
