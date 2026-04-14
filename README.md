# LLM Diplomacy Arena
 
Small language models play the board game [Diplomacy](https://en.wikipedia.org/wiki/Diplomacy_(game)) against each other — negotiating alliances, coordinating attacks, and inevitably betraying each other — all through structured JSON.
 
Diplomacy is a 7-player strategy game set in pre-WWI Europe with no dice and no hidden information. The only way to win is through negotiation. This makes it one of the hardest games for AI: you can't brute-force your way to victory, you have to talk your way there.
 
We use [Ollama](https://ollama.com) to run small open-weight models (3B–7B parameters) locally, and the [`diplomacy`](https://github.com/diplomacy/diplomacy) Python engine to handle the game rules. Each model receives the board state as JSON, sends messages to other players, and submits its military orders. A Pydantic validation layer ensures the models speak the right language — and when they don't, we log exactly how they fail.
 
## Quick Start
 
```bash
# Prerequisites: Python 3.11+, Ollama running locally
ollama pull qwen3:4b
 
git clone https://github.com/yourname/llm-diplomacy-arena.git
cd llm-diplomacy-arena
pip install -e .
python -m src.game.runner
```
 
## What's Interesting
 
- **How small can you go?** At what model size do negotiations become incoherent and orders become illegal?
- **Who lies better?** Some model families produce more deceptive agents than others.
- **Does talking help?** We can toggle negotiation on and off and measure the difference.
- **Emergent alliances** — Do models coordinate? Do they betray at the right moment?
 
## License
 
MIT