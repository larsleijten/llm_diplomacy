# LLM Diplomacy Arena

Local LLMs play the board game Diplomacy against each other — negotiating, betraying, and conquering Europe. Please update this file to reflect any recent updates that were made to the code or the project. 

## Goal

Pit small language models against each other in full-press Diplomacy to explore: how small can you go before structured output breaks down, negotiations become incoherent, or lying stops working?

## Stack

| Component | Tool |
|---|---|
| Game engine | `diplomacy` v1.1.2 (DATC-compliant, pip installable) |
| LLM backend | Ollama (local inference) |
| LLM client | `ollama-python` |
| Schema validation | Pydantic |
| Language | Python 3.11+ |
| Inference GPU | NVIDIA RTX 2080 Ti — **11 GB VRAM** (host: butterfree) |

## Project Structure (target)

```
src/
  game/
    runner.py          # Main game loop
    state.py           # Board state → JSON for LLM
    validation.py      # Validate orders against engine
  agents/
    base.py            # Abstract agent interface
    ollama_agent.py    # Ollama-backed agent
    random_agent.py    # Random legal moves (baseline)
    prompts.py         # System prompts and templates
  schemas/
    game_state.py      # Pydantic input schema (what LLM receives)
    agent_response.py  # Pydantic output schema (what LLM returns)
  analysis/
    logger.py          # Per-phase event logging
    report.py          # Post-game stats
configs/
  default.yaml         # Model assignments, map, turn limits
logs/                  # JSON game logs
```

## Turn Loop

1. Serialize board state to JSON (units, supply centers, legal orders per unit, incoming messages, recent history)
2. Each agent negotiates: sends messages to other powers
3. Each agent submits orders as JSON
4. Orders validated → invalid orders default to hold
5. Engine adjudicates all orders simultaneously
6. Log everything

## LLM Interface

**Input (per agent per phase):**
- Phase, power name, own units/SCs, all units/SCs (no fog of war)
- Legal orders per unit (model picks from list, doesn't construct notation)
- Incoming messages, recent order history

**Output (Pydantic-validated):**
```json
{
  "orders": ["A PAR - BUR", "F BRE - MAO"],
  "messages": [{"recipient": "ENGLAND", "body": "..."}]
}
```

Order notation: `A PAR - BUR` (move), `F BRE S A PAR - PIC` (support), `A MUN H` (hold).

## Target Models (Ollama)

**VRAM budget (11 GB):** on the 2080 Ti, Q4_K_M weights **and** the KV cache for the
(large) Diplomacy context must both fit. Diplomacy prompts are heavy — full board JSON,
per-unit legal-order lists, message history — so keep weights ≤ ~7 GB to leave room for
context. Sizes below are approximate Q4_K_M download sizes.

| Model | Params | ~Q4_K_M | Fits 11 GB? | Role |
|---|---|---|---|---|
| `llama3.2:3b` | 3B | ~2.0 GB | ✅ easily | small-end probe |
| `phi4-mini` | 3.8B | ~2.5 GB | ✅ | small-end probe |
| `qwen3.5:4b` | 4B | ~2.7 GB | ✅ | small-end probe |
| `gemma3:4b` | 4B | ~3.3 GB | ✅ | small-end probe |
| `mistral:7b` | 7B | ~4.4 GB | ✅ | mid baseline |
| `qwen3:8b` | 8B | 5.2 GB | ✅ | mid baseline |
| `qwen3.5:9b` | 9.65B | 6.6 GB | ✅ **default / strong baseline** | upper bound that still fits |
| `qwen3:14b` | 14B | 9.3 GB | ⚠️ tight — little KV headroom, short contexts only | stretch |
| `qwen3.6:27b`+ | 27B+ | 17 GB+ | ❌ won't fit | needs a bigger GPU |

**Recommended default: `qwen3.5:9b`** — newest generation that fits, switchable thinking
mode (useful for strategy/deception, and toggleable to measure its effect), and ~4 GB left
for context KV cache. `qwen3.6` starts at 27B and does not fit 11 GB.

## Roadmap

- [x] Select engine + LLM interface
- [ ] Pydantic schemas (`game_state.py`, `agent_response.py`)
- [ ] Game loop with negotiation rounds (`runner.py`)
- [ ] System prompts for small models (`prompts.py`)
- [ ] Random agent baseline
- [ ] First full game (one model plays all 7 powers)
- [ ] Multi-model games
- [ ] Game logging + post-game analysis
- [ ] API model support (OpenAI, Anthropic)

## Key Design Decisions

- Models receive the **full legal move list** per unit — they pick, not construct. This sidesteps notation generation failures.
- Pydantic retry loops planned for malformed responses.
- JSON vs YAML for prompts is still TBD — test empirically which small models handle better.
- Architecture should make swapping Ollama for an API model a config change, not a code change.
