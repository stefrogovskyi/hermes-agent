#!/usr/bin/env python3
"""Write fallback_providers into Hermes config.yaml as a REAL YAML list.

Why: `hermes config set fallback_providers '<json>'` stringifies the value as a
quoted JSON string, and Hermes reads it back as `str` (fallback silently empty).
`write_file`/`patch` on config.yaml are guardrailed. This script bypasses both by
importing atomic_yaml_write and writing the list directly.
"""
import os, sys
sys.path.insert(0, r"C:\Users\Stefan\AppData\Local\hermes\hermes-agent")
from utils import atomic_yaml_write
import yaml

CFG = os.path.expanduser(r"~/AppData/Local/hermes/config.yaml")

# Edit this list to change the chain. Keep existing nous entries first.
FALLBACK = [
    {"provider": "nous", "model": "poolside/laguna-s-2.1:free"},
    {"provider": "nous", "model": "stepfun/step-3.7-flash:free"},
    {"provider": "nous", "model": "poolside/laguna-xs-2.1:free"},
    {"provider": "openrouter", "model": "nvidia/nemotron-3-ultra-550b-a55b:free"},
    {"provider": "openrouter", "model": "nvidia/nemotron-3-super-120b-a12b:free"},
    {"provider": "openrouter", "model": "nvidia/nemotron-3-nano-30b-a3b:free"},
    {"provider": "openrouter", "model": "google/gemma-4-31b-it:free"},
    {"provider": "openrouter", "model": "google/gemma-4-26b-a4b-it:free"},
    {"provider": "openrouter", "model": "openai/gpt-oss-20b:free"},
    {"provider": "openrouter", "model": "inclusionai/ling-3.0-flash:free"},
    {"provider": "openrouter", "model": "cohere/north-mini-code:free"},
    {"provider": "openrouter", "model": "poolside/laguna-m.1:free"},
    {"provider": "openrouter", "model": "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free"},
    {"provider": "openrouter", "model": "openrouter/free"},
]

with open(CFG, encoding="utf-8") as f:
    cfg = yaml.safe_load(f) or {}

cfg["fallback_providers"] = FALLBACK
atomic_yaml_write(CFG, cfg, sort_keys=False)
print("OK: wrote %d fallback providers as YAML list" % len(FALLBACK))
