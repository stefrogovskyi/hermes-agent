---
name: afterquery-skyrl
description: Use when exploring reinforcement learning (RL) post-training, PPO/GRPO optimization, and reasoning alignment using AfterQuery SkyRL.
category: research/afterquery
---

# AfterQuery SkyRL (Reinforcement Learning & Reasoning Engine)

SkyRL is a high-performance framework for reinforcement learning (RL) post-training, enabling language models to develop advanced step-by-step reasoning (similar to DeepSeek-R1 and OpenAI o1 architectures).

## Key Capabilities
- Asynchronous RL training pipelines with Ray and vLLM integration.
- SFT and RL rollout collection for fine-tuning custom domain models.
- Support for Llama 3, Qwen 2.5 / 3, and DeepSeek model families.

## Repository Location
`/opt/hermes/profiles/alistair/repos/afterquery/SkyRL`

## Quick Start & Verification
```bash
cd /opt/hermes/profiles/alistair/repos/afterquery/SkyRL
python3 -c "import os; print('SkyRL modules:', os.listdir('.'))"
```
