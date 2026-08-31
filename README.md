<div align="center"><pre>
   _______             __  __                   ______                   __  __                     
|       \           |  \|  \                 /      \                 |  \|  \                    
| $$$$$$$\  ______   \$$| $$ __    __       |  $$$$$$\  ______    ____| $$ \$$ _______    ______  
| $$  | $$ |      \ |  \| $$|  \  |  \      | $$   \$$ /      \  /      $$|  \|       \  /      \ 
| $$  | $$  \$$$$$$\| $$| $$| $$  | $$      | $$      |  $$$$$$\|  $$$$$$$| $$| $$$$$$$\|  $$$$$$\
| $$  | $$ /      $$| $$| $$| $$  | $$      | $$   __ | $$  | $$| $$  | $$| $$| $$  | $$| $$  | $$
| $$__/ $$|  $$$$$$$| $$| $$| $$__/ $$      | $$__/  \| $$__/ $$| $$__| $$| $$| $$  | $$| $$__| $$
| $$    $$ \$$    $$| $$| $$ \$$    $$       \$$    $$ \$$    $$ \$$    $$| $$| $$  | $$ \$$    $$
 \$$$$$$$   \$$$$$$$ \$$ \$$ _\$$$$$$$        \$$$$$$   \$$$$$$   \$$$$$$$ \$$ \$$   \$$ _\$$$$$$$
                            |  \__| $$                                                  |  \__| $$
                             \$$    $$                                                   \$$    $$
                              \$$$$$$                                                     \$$$$$$ 
</pre>

Daily Python practice — one small program a day, working from fundamentals up toward building my own Small Language Model (SLM).

</div>

## Goal

Consistency over intensity. Every day, write and commit one Python program. Start simple, gradually increase complexity, and use this repo as a running log of progress — from basic scripts to (eventually) implementing core ML/NLP concepts from scratch.

## Structure

Each day gets its own folder, numbered sequentially:

```
daily-coding/
├── day-001-calculator/
│   ├── calculator.py
│   └── README.md
├── day-002-.../
│   └── ...
└── README.md
```

Each day's folder contains:
- The program itself
- A short `README.md` explaining what it does, what was learned, and any challenges hit

## Progress Log

| Day | Project | Concepts Practiced |
|-----|---------|---------------------|
| 001 | Calculator | Functions, input handling, control flow, error handling |

*(updated daily)*

## Roadmap (loose, evolving)

- **Phase 1 — Fundamentals:** small CLI tools, data structures, file I/O, OOP basics
- **Phase 2 — Applied Python:** APIs, scripting, automation, testing
- **Phase 3 — Math & ML foundations:** linear algebra, probability, NumPy/PyTorch basics
- **Phase 4 — NLP building blocks:** tokenization, embeddings, attention, mini transformer components
- **Phase 5 — SLM:** train a small language model from scratch

## Rules

1. Code every day. Even a small, ugly program counts.
2. No skipping days without a note explaining why (life happens).
3. Prefer understanding over copy-pasting — write it, break it, fix it.
4. Refactor old days occasionally as skills improve.

## Setup

```bash
git clone https://github.com/<your-username>/daily-coding.git
cd daily-coding
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt  # once dependencies exist
```
