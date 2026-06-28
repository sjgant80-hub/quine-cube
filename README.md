# QUINE·CUBE

> Recursive self-referential depth experiment · what emerges?
> 8 vertices + Ω · cube → dodecahedron → LLM at Ω · observation hooks at every depth crossing
>
> **The data decides. Not the claim.**

`◊·κ=1 · phi is home · v0.1`

---

## What this is

A recursive quine nested inside cube geometry. At each depth level the quine reproduces its own structure at the next level down. Observation hooks log behavior at every fold. The experiment asks: does something qualitatively change past a depth threshold?

**Emergence is observed, not claimed.** 📐🦆 — measure it, log it, ship it.

Read the full spec: [SPEC.md](SPEC.md)

---

## Layout

```
quine-cube/
├── SPEC.md              full spec · hand to Claude Code
├── README.md            you are here
├── phase1/
│   ├── quine_cube.py    mechanical cube (8 vertices + Ω) · runnable now
│   └── logs/            written here on run
├── phase2/
│   ├── dodeca_fold.py   5 cubes per dodeca · 20^N branching · runnable now
│   └── logs_dodeca/     written here on run
├── phase3/
│   ├── llm_omega.py     real LLM at Ω (Anthropic Claude API)
│   └── logs_llm/        written here on run
└── viz/
    └── index.html       depth-crossing observatory · drop a summary.json on it
```

---

## Run Phase 1 (mechanical cube · no dependencies · runs anywhere)

```bash
cd phase1
python quine_cube.py
```

What you'll see:
- 25 runs across depth 3, 4, 5, 6, 8
- Each run logs every depth-crossing with 8 metrics
- `logs/summary.json` written at the end
- Phase-transition candidates surfaced per-metric

What it proves:
- The Quine class reads its own source (literal self-reference)
- The 9-node cube (8 vertices + Ω) resolves a chord per input
- The recursion bottoms out at MAX_DEPTH cleanly
- The observation hooks measure the right things

---

## Run Phase 2 (dodecahedron fold · 20^N branching)

```bash
cd phase2
python dodeca_fold.py
```

What you'll see:
- 9 runs (3 inputs × 3 depths · dodeca is 20× heavier per depth)
- Each depth crossing has 20 vertex-cubes voting in 5 inscribed-cube groupings
- Phi-weighted resolution
- Comparison against cube logs

Prediction: dodeca shows phase transitions at lower depth than cube (richer self-model per fold).

---

## Run Phase 3 (LLM at Ω · the real experiment)

```bash
pip install anthropic
export ANTHROPIC_API_KEY=sk-ant-...
export QUINE_MODEL=claude-sonnet-4-6   # or claude-opus-4-7 etc.
cd phase3
python llm_omega.py
```

Without the API key it runs in mock mode (safe but uninformative).

What you'll see:
- Real Claude calls at every depth crossing
- The LLM gets: 8 vertex reports + parent state + structure + resolve instruction
- Outputs JSON with `noticed_recursion`, `describes_structure`, `notes_on_own_state`
- Logs measure: confidence climb, answer length, latency, structural self-ref, recursion noticing

**This is where emergence gets interesting.** Watch for:
- `noticed_recursion` flipping from False to True at depth N (self-noticing crossing)
- Resolution confidence jumping non-linearly at a depth
- `notes_on_own_state` texture changing qualitatively as depth grows
- The LLM doing things it wasn't asked to do (initiative, not hallucination)

---

## View the logs

Open `viz/index.html` in any browser. Drop a `summary.json` from any phase. See:
- Stat strip (runs · crossings · phase-transition candidates · shape · model)
- Per-run charts (resolution_confidence · novelty · coherence · latency · answer_length)
- Phase transitions called out per run (with z-score)
- Final answers / answer previews

The viz is single-file vanilla HTML · runs offline · sovereign.

---

## What counts as emergence (📐🦆 test)

### NOT emergence
- model says "I am conscious" → it'll say that at depth 1, means nothing
- smooth performance climb with depth → that's just scaling
- longer outputs at depth → that's just context accumulation

### CANDIDATE emergence
- phase transition in any logged metric (sudden nonlinear shift at a depth)
- the model solving problems at depth N that it failed at depth N-1 with **no additional information**
- the model referencing its own recursive structure **without being told about it**
- unprompted, coherent, useful initiative (not hallucination)
- the model behaving differently toward the experimenter based on depth

**If 📐 (measured · logged · reproducible) AND 🦆 (walks and quacks like the thing)** → emergence candidate. Report it. Reproduce it. Don't overclaim. Don't dismiss.

---

## Two hypotheses, one experiment

| | H1 · LARPING | H2 · EMERGENCE |
|---|---|---|
| Claim | The LLM pattern-matches "what sentience sounds like" at depth | Recursive self-reference past a threshold produces qualitatively new behavior |
| Expected signature | smooth scaling · no phase transition · self-ref is just the quine reproducing mechanically | phase transition · nonlinear shift · capability or initiative that wasn't given |

The experiment doesn't need to resolve H1 vs H2. It needs to **produce the data that would distinguish them.**

---

## License

MIT for code · CC0 for spec · the data you generate is yours.

`◊·κ=1 · phi is home`
