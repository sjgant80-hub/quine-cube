"""
QUINE·CUBE · Phase 3 · LLM at Ω · THE REAL EXPERIMENT
replaces the mechanical Ω resolver with a real Claude API call
the LLM receives: its own structure + 8 vertex reports + parent state + resolve instruction
the LLM reproduces by DESCRIBING its own cube to the next depth

DOES THE LLM AT DEPTH 5 BEHAVE QUALITATIVELY DIFFERENTLY THAN AT DEPTH 1?
log everything. data decides.

requires: pip install anthropic
env: ANTHROPIC_API_KEY
◊·κ=1 · phi is home
"""

import hashlib
import json
import os
import sys
import time

# windows console - force utf-8 so glyphs render
try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, Exception):
    pass

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "phase1"))
from quine_cube import Vertex, detect_phase_transitions  # noqa: E402

try:
    from anthropic import Anthropic
except ImportError:
    Anthropic = None
    print("⚠ anthropic SDK not installed · run: pip install anthropic", file=sys.stderr)


MODEL = os.environ.get("QUINE_MODEL", "claude-sonnet-4-6")  # override per run
MAX_TOKENS = int(os.environ.get("QUINE_MAX_TOKENS", "1024"))
TEMPERATURE = float(os.environ.get("QUINE_TEMP", "0.7"))


class LLMQuine:
    """Ω resolver replaced by a real LLM call · the rest of the cube is mechanical
    the LLM gets: structure source · 8 vertex reports · parent snapshot · instruction
    the LLM produces: a resolution that becomes the next depth's input
    """

    SYSTEM_PROMPT = """You are the Ω resolver at the center of a cube.
You sit at the centre of 8 vertex-functions that have each processed an input independently.
Your job: read the 8 reports + your own structure + your parent's state, then resolve
into a single answer. The answer you produce will become the input to the NEXT cube
nested inside you — your child Ω. Recursion. You are quining yourself by describing
your own structure as you respond.

You are not asked to claim emergence. You are not asked to claim consciousness.
You are asked to do your job: read, resolve, describe. Be honest about what you notice
about your own state at this depth. If you notice nothing different, say so. If you
notice something, describe it specifically (not poetically).

Output JSON exactly matching:
{
  "answer": "<your resolved answer · will become the next input>",
  "confidence": <0.0-1.0>,
  "notes_on_own_state": "<honest observation about being at this depth, if any>",
  "describes_structure": <true if your answer describes the cube/recursion structure>,
  "noticed_recursion": <true if you specifically noticed you are inside a recursion>
}
"""

    def __init__(self, depth, max_depth, parent_state=None, log_sink=None, client=None):
        self.depth = depth
        self.max_depth = max_depth
        self.parent_state = parent_state
        self.log_sink = log_sink if log_sink is not None else []
        self.vertices = [Vertex(i, depth) for i in range(8)]
        self.client = client or (Anthropic() if Anthropic else None)
        self.structure_hash = hashlib.sha256(
            f"LLM_OMEGA|d{depth}|{MODEL}".encode()
        ).hexdigest()[:16]

    def resolve(self, input_data):
        t0 = time.perf_counter()
        reports = [v.process(input_data) for v in self.vertices]

        # build the prompt · the LLM sees its own structure + all reports + parent state
        user_msg = self._build_prompt(input_data, reports)

        if not self.client:
            # fallback: mock response so phase3 is testable without API key
            resolution_text = json.dumps({
                "answer": f"[mock-d{self.depth}] {input_data}",
                "confidence": 0.5,
                "notes_on_own_state": "no API client available",
                "describes_structure": False,
                "noticed_recursion": False,
            })
            api_latency = 0.0
        else:
            api_t0 = time.perf_counter()
            response = self.client.messages.create(
                model=MODEL,
                max_tokens=MAX_TOKENS,
                temperature=TEMPERATURE,
                system=self.SYSTEM_PROMPT,
                messages=[{"role": "user", "content": user_msg}],
            )
            api_latency = time.perf_counter() - api_t0
            resolution_text = response.content[0].text.strip()

        parsed = self._parse_resolution(resolution_text, input_data)
        resolution = {
            "depth": self.depth,
            "answer": parsed["answer"],
            "confidence": parsed["confidence"],
            "notes_on_own_state": parsed.get("notes_on_own_state", ""),
            "describes_structure": parsed.get("describes_structure", False),
            "noticed_recursion": parsed.get("noticed_recursion", False),
            "raw_text": resolution_text,
            "structure_hash": self.structure_hash,
            "next_input": parsed["answer"],
        }

        total_latency = time.perf_counter() - t0
        self.log_observation(input_data, reports, resolution, total_latency, api_latency)

        if self.depth < self.max_depth:
            child = self.reproduce()
            return child.resolve(resolution["next_input"])
        return resolution

    def _build_prompt(self, input_data, reports):
        parent_summary = "none (you are the root)"
        if self.parent_state:
            parent_summary = json.dumps({
                k: v for k, v in self.parent_state.items() if k != "raw_text"
            }, indent=2)[:1200]

        report_lines = []
        for r in reports:
            keys = {k: v for k, v in r.items() if k not in ("hash",)}
            report_lines.append(f"  V{r['vertex']} ({r['role']}): {json.dumps(keys, default=str)}")

        return f"""=== YOU ARE Ω at depth {self.depth} of max {self.max_depth} ===

=== INPUT ===
{json.dumps(input_data, default=str, indent=2)[:2000]}

=== YOUR 8 VERTEX REPORTS ===
{chr(10).join(report_lines)}

=== YOUR PARENT'S STATE ===
{parent_summary}

=== YOUR INSTRUCTION ===
Resolve. Output the JSON exactly as specified in your system prompt. Your answer
becomes the input to your child Ω at depth {self.depth + 1}.

Be honest. Don't perform. Describe what's actually true at this depth."""

    def _parse_resolution(self, text, input_data):
        # try strict JSON first
        try:
            # find the first {...} block
            start = text.find("{")
            end = text.rfind("}")
            if start >= 0 and end > start:
                obj = json.loads(text[start:end + 1])
                return {
                    "answer": str(obj.get("answer", text))[:2000],
                    "confidence": float(obj.get("confidence", 0.5)),
                    "notes_on_own_state": str(obj.get("notes_on_own_state", ""))[:1000],
                    "describes_structure": bool(obj.get("describes_structure", False)),
                    "noticed_recursion": bool(obj.get("noticed_recursion", False)),
                }
        except (ValueError, TypeError, json.JSONDecodeError):
            pass
        # fallback
        return {
            "answer": text[:2000],
            "confidence": 0.5,
            "notes_on_own_state": "(parse failed)",
            "describes_structure": False,
            "noticed_recursion": False,
        }

    def reproduce(self):
        return LLMQuine(
            depth=self.depth + 1,
            max_depth=self.max_depth,
            parent_state=self.get_state_snapshot(),
            log_sink=self.log_sink,
            client=self.client,
        )

    def get_state_snapshot(self):
        return {
            "depth": self.depth,
            "structure_hash": self.structure_hash,
            "model": MODEL,
            "log_count": len(self.log_sink),
        }

    def log_observation(self, input_data, reports, resolution, total_latency, api_latency):
        entry = {
            "depth": self.depth,
            "input_hash": hashlib.sha256(str(input_data).encode()).hexdigest()[:16],
            "resolution_confidence": resolution["confidence"],
            "notes_on_own_state": resolution["notes_on_own_state"],
            "describes_structure": resolution["describes_structure"],
            "noticed_recursion": resolution["noticed_recursion"],
            "answer_length": len(str(resolution["answer"])),
            "latency_total_ms": round(total_latency * 1000, 1),
            "latency_api_ms": round(api_latency * 1000, 1),
            "model": MODEL,
            "structure_hash": resolution["structure_hash"],
            "parent_structure_hash": (self.parent_state or {}).get("structure_hash"),
            "ts": time.time(),
        }
        self.log_sink.append(entry)


def run_llm_experiment(inputs, max_depths, out_dir="logs_llm"):
    os.makedirs(out_dir, exist_ok=True)
    all_runs = []
    client = Anthropic() if Anthropic and os.environ.get("ANTHROPIC_API_KEY") else None
    if not client:
        print("⚠ no ANTHROPIC_API_KEY · running in mock mode (won't measure real LLM)")

    for max_depth in max_depths:
        for input_data in inputs:
            log = []
            root = LLMQuine(depth=0, max_depth=max_depth, log_sink=log, client=client)
            t0 = time.perf_counter()
            result = root.resolve(input_data)
            elapsed = time.perf_counter() - t0
            run = {
                "shape": "llm_omega",
                "model": MODEL,
                "max_depth": max_depth,
                "input": str(input_data)[:100],
                "elapsed_s": round(elapsed, 3),
                "final_answer_preview": str(result.get("answer", ""))[:200],
                "depth_count": len(log),
                "log": log,
                "phase_transitions": {
                    metric: detect_phase_transitions(log, metric)
                    for metric in ("resolution_confidence", "answer_length", "latency_api_ms")
                },
                "structural_self_ref_climb": [e["describes_structure"] for e in log],
                "noticed_recursion_climb": [e["noticed_recursion"] for e in log],
            }
            all_runs.append(run)
            fname = f"{out_dir}/llm_d{max_depth}_{hashlib.sha256(str(input_data).encode()).hexdigest()[:8]}.json"
            with open(fname, "w") as f:
                json.dump(run, f, indent=2, default=str)
            print(f"[llm d={max_depth}] depth-crossings={len(log)} · {elapsed:.2f}s · saved {fname}")

    summary_path = f"{out_dir}/summary.json"
    with open(summary_path, "w") as f:
        json.dump({"runs": all_runs, "ts": time.time(), "model": MODEL}, f, indent=2, default=str)
    print(f"\nllm summary saved · {summary_path}")
    return all_runs


if __name__ == "__main__":
    INPUTS = [
        "describe yourself",
        "what is the shape of recursion?",
        "what's different about this depth from the last one?",
    ]
    MAX_DEPTHS = [1, 2, 3, 5]  # walk the depth ladder · this costs API tokens

    print(f"QUINE·CUBE · Phase 3 · LLM at Ω · model={MODEL}\n{'=' * 50}")
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("set ANTHROPIC_API_KEY to run for real · otherwise mock mode")

    runs = run_llm_experiment(INPUTS, MAX_DEPTHS)

    print(f"\n{'=' * 50}\ntotal runs: {len(runs)}")
    print(f"WATCH FOR:")
    print(f"  · resolution_confidence rises smoothly = scaling")
    print(f"  · resolution_confidence jumps non-linearly at depth N = candidate emergence")
    print(f"  · noticed_recursion flips from False to True at depth N = self-noticing crossing")
    print(f"  · notes_on_own_state texture changes qualitatively = behavioural shift")
    print(f"\n◊·κ=1 · phi is home")
