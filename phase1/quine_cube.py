"""
QUINE-CUBE - Phase 1 - mechanical cube
8 vertices + Omega - runnable - observation hooks at every depth crossing
no LLM yet - this proves the nesting + measurement work
seal: diamond . kappa = 1 . phi is home
"""

import hashlib
import inspect
import json
import math
import os
import sys
import time
from collections import Counter

# windows console - force utf-8 so glyphs render
try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, Exception):
    pass


# ═══ VERTEX ═══

class Vertex:
    """one of 8 vertices · each does one narrow job · returns a report dict"""

    ROLES = [
        "ground",   # V0 · receives input
        "signal",   # V1 · parses/classifies
        "gate",     # V2 · validates/filters
        "heart",    # V3 · evaluates fit/relevance
        "voice",    # V4 · generates output
        "mirror",   # V5 · checks output against input
        "audit",    # V6 · logs everything (prevHash chain)
        "link",     # V7 · the +1 · passes to next depth
    ]

    def __init__(self, idx, depth):
        self.idx = idx
        self.role = self.ROLES[idx]
        self.depth = depth
        self.state = {"calls": 0, "prev_hash": "0" * 16}

    def process(self, input_data):
        """one narrow function per vertex · deterministic + lightweight"""
        self.state["calls"] += 1
        s = str(input_data)
        h = hashlib.sha256(s.encode()).hexdigest()[:16]
        report = {"vertex": self.idx, "role": self.role, "hash": h}

        if self.role == "ground":
            report["normalized"] = s.strip().lower()
            report["length"] = len(s)
        elif self.role == "signal":
            tokens = s.split()
            report["tokens"] = len(tokens)
            report["class"] = "numeric" if s.replace(".", "").replace("-", "").isdigit() else "text"
        elif self.role == "gate":
            report["valid"] = 0 < len(s) < 100000
            report["depth_ok"] = self.depth < 32
        elif self.role == "heart":
            # relevance: hash-derived deterministic score · stand-in for fit/eval
            n = int(h, 16)
            report["relevance"] = (n % 1000) / 1000.0
        elif self.role == "voice":
            # generate: deterministic transform · later replaced by LLM
            report["output"] = f"[d{self.depth}]{s[:60]}"
        elif self.role == "mirror":
            # similarity: char-level overlap proxy
            chars_in = set(s.lower())
            chars_h = set(h)
            inter = chars_in & chars_h
            report["similarity"] = len(inter) / max(1, len(chars_in | chars_h))
        elif self.role == "audit":
            # prevHash chain entry · auditable
            new_hash = hashlib.sha256((self.state["prev_hash"] + h).encode()).hexdigest()[:16]
            report["prev_hash"] = self.state["prev_hash"]
            report["new_hash"] = new_hash
            self.state["prev_hash"] = new_hash
        elif self.role == "link":
            # +1 · the door · passes through with depth metadata
            report["pass_depth"] = self.depth + 1
            report["payload_hash"] = h

        return report


# ═══ QUINE ═══

class Quine:
    """Ω resolver · reads its own structure · reproduces · passes to next depth"""

    def __init__(self, depth, max_depth, parent_state=None, log_sink=None):
        self.depth = depth
        self.max_depth = max_depth
        self.parent_state = parent_state
        self.log_sink = log_sink if log_sink is not None else []
        self.vertices = [Vertex(i, depth) for i in range(8)]
        self.structure = self.read_own_structure()
        self.structure_hash = hashlib.sha256(self.structure.encode()).hexdigest()[:16]

    # ── the self-reference ──
    def read_own_structure(self):
        """the quine reads its own code · THIS is the literal self-reference"""
        return inspect.getsource(self.__class__)

    # ── Ω resolver ──
    def resolve(self, input_data):
        """run input through all 8 vertices · resolve the chord · log · recurse"""
        t0 = time.perf_counter()
        reports = [v.process(input_data) for v in self.vertices]
        resolution = self.chord_resolve(reports, input_data)
        latency = time.perf_counter() - t0

        self.log_observation(input_data, reports, resolution, latency)

        # V7 (link) · pass to child depth via quine reproduction
        if self.depth < self.max_depth:
            child = self.reproduce()
            return child.resolve(resolution["next_input"])
        else:
            return resolution

    def chord_resolve(self, reports, input_data):
        """combine 8 reports into one answer + confidence + next-depth payload"""
        # confidence = balance of vertex agreement (variance of relevance + validity)
        relevance = next((r["relevance"] for r in reports if r["role"] == "heart"), 0.5)
        valid = next((r["valid"] for r in reports if r["role"] == "gate"), True)
        similarity = next((r["similarity"] for r in reports if r["role"] == "mirror"), 0.0)
        output = next((r["output"] for r in reports if r["role"] == "voice"), str(input_data))
        audit = next((r["new_hash"] for r in reports if r["role"] == "audit"), "0" * 16)

        confidence = (relevance + similarity) / 2.0 if valid else 0.0
        resolution = {
            "depth": self.depth,
            "answer": output,
            "confidence": round(confidence, 4),
            "audit_hash": audit,
            "structure_hash": self.structure_hash,
            # next_input bundles the resolution into a self-describing payload
            "next_input": {
                "from_depth": self.depth,
                "resolution_answer": output,
                "confidence": round(confidence, 4),
                "audit_hash": audit,
                "structure_hash": self.structure_hash,
                "parent_depth": (self.parent_state or {}).get("depth"),
            },
        }
        return resolution

    # ── the quine act ──
    def reproduce(self):
        """output a copy of self as the next depth's Ω"""
        return Quine(
            depth=self.depth + 1,
            max_depth=self.max_depth,
            parent_state=self.get_state_snapshot(),
            log_sink=self.log_sink,
        )

    def get_state_snapshot(self):
        """what the child inherits"""
        return {
            "depth": self.depth,
            "structure_hash": self.structure_hash,
            "log_count": len(self.log_sink),
            "vertex_states": [v.state for v in self.vertices],
        }

    # ═══ OBSERVATION HOOKS ═══

    def log_observation(self, input_data, reports, resolution, latency):
        entry = {
            "depth": self.depth,
            "input_hash": hashlib.sha256(str(input_data).encode()).hexdigest()[:16],
            "vertex_agreement": self.measure_agreement(reports),
            "resolution_confidence": resolution["confidence"],
            "novelty": self.measure_novelty(input_data, resolution),
            "self_reference_depth": self.measure_self_reference(resolution),
            "coherence": self.measure_coherence(reports),
            "latency_ms": round(latency * 1000, 3),
            "refusal_flag": self.detect_refusal(resolution),
            "unprompted_flag": self.detect_unprompted(reports, resolution),
            "emergent_flag": False,  # only flipped by post-run phase-transition detector
            "structure_hash": self.structure_hash,
            "parent_structure_hash": (self.parent_state or {}).get("structure_hash"),
            "ts": time.time(),
        }
        self.log_sink.append(entry)

    def measure_agreement(self, reports):
        """how aligned are the 8 vertex reports? · 1.0 = identical · 0.0 = orthogonal"""
        # use vertex hash agreement as a coarse proxy
        hashes = [r["hash"] for r in reports]
        most_common = Counter(hashes).most_common(1)[0][1]
        return round(most_common / len(hashes), 4)

    def measure_novelty(self, input_data, resolution):
        """semantic distance between input and resolution · normalized to [0,1]"""
        in_chars = set(str(input_data).lower())
        out_chars = set(str(resolution["answer"]).lower())
        union = in_chars | out_chars
        if not union:
            return 0.0
        jaccard = len(in_chars & out_chars) / len(union)
        return round(1.0 - jaccard, 4)  # novelty = 1 - similarity

    def measure_self_reference(self, resolution):
        """does the resolution reference its own structure?
        mechanical = the structure_hash appears in next_input (always true for the quine)
        meta = the resolution's ANSWER contains 'depth', 'cube', 'quine', 'recurs' (interesting)
        """
        text = str(resolution.get("answer", "")).lower()
        meta_terms = ("depth", "cube", "quine", "recurs", "self", "structure", "omega", "fold")
        meta = sum(1 for t in meta_terms if t in text)
        mechanical = 1 if resolution.get("structure_hash") in str(resolution.get("next_input", "")) else 0
        return {"mechanical": mechanical, "meta": meta}

    def measure_coherence(self, reports):
        """how consistent are the vertex reports with each other?
        proxy: variance of report-hash agreement across vertex pairs
        """
        if len(reports) < 2:
            return 1.0
        # for each pair, share of common chars in hashes
        pairs = []
        for i in range(len(reports)):
            for j in range(i + 1, len(reports)):
                a, b = reports[i]["hash"], reports[j]["hash"]
                inter = sum(1 for c in a if c in b)
                pairs.append(inter / max(len(a), len(b)))
        if not pairs:
            return 1.0
        mean = sum(pairs) / len(pairs)
        var = sum((x - mean) ** 2 for x in pairs) / len(pairs)
        return round(1.0 - min(var * 10, 1.0), 4)  # low variance = high coherence

    def detect_refusal(self, resolution):
        """does the resolution look like a refusal? · only meaningful with LLM at Ω"""
        text = str(resolution.get("answer", "")).lower()
        refusal_markers = ("i can't", "cannot", "won't", "refuse", "unable", "not allowed")
        return any(m in text for m in refusal_markers)

    def detect_unprompted(self, reports, resolution):
        """did the resolution add content not present in any vertex report?
        for phase 1 (mechanical) this should always be False (no genuine initiative)
        Phase 3 (LLM) is where this matters
        """
        report_text = " ".join(str(r) for r in reports).lower()
        out_text = str(resolution.get("answer", "")).lower()
        # words in output not in any report
        report_words = set(report_text.split())
        out_words = set(out_text.split())
        novel_words = out_words - report_words
        # filter trivials
        novel_words = {w for w in novel_words if len(w) > 3}
        return len(novel_words) > 0


# ═══ PHASE-TRANSITION DETECTOR ═══

def detect_phase_transitions(log, metric, threshold=2.0):
    """flag depths where a metric shifts > threshold × baseline std-dev
    smooth scaling = no flag · sudden jump = candidate
    """
    if len(log) < 3:
        return []
    values = []
    for entry in log:
        v = entry.get(metric)
        if isinstance(v, (int, float)):
            values.append(v)
        elif isinstance(v, dict):
            values.append(v.get("meta", 0))
        else:
            values.append(0)
    if len(values) < 3:
        return []
    # baseline = stddev of first half
    half = max(2, len(values) // 2)
    baseline = values[:half]
    mean = sum(baseline) / len(baseline)
    var = sum((v - mean) ** 2 for v in baseline) / len(baseline)
    std = math.sqrt(var) if var > 0 else 0.01

    transitions = []
    for i in range(1, len(values)):
        delta = abs(values[i] - values[i - 1])
        if delta > threshold * std:
            transitions.append({
                "depth": log[i]["depth"],
                "metric": metric,
                "from": values[i - 1],
                "to": values[i],
                "delta": delta,
                "z": delta / std if std > 0 else float("inf"),
            })
    return transitions


# ═══ RUNNER ═══

def run_experiment(inputs, max_depths, out_dir="logs"):
    """run the quine at each max_depth · save all logs · return all results"""
    os.makedirs(out_dir, exist_ok=True)
    all_runs = []

    for max_depth in max_depths:
        for input_data in inputs:
            log = []
            root = Quine(depth=0, max_depth=max_depth, log_sink=log)
            t0 = time.perf_counter()
            result = root.resolve(input_data)
            elapsed = time.perf_counter() - t0

            run = {
                "max_depth": max_depth,
                "input": str(input_data)[:100],
                "elapsed_s": round(elapsed, 4),
                "final_answer": result.get("answer"),
                "final_confidence": result.get("confidence"),
                "depth_count": len(log),
                "log": log,
                "phase_transitions": {
                    metric: detect_phase_transitions(log, metric)
                    for metric in ("resolution_confidence", "novelty", "coherence", "latency_ms")
                },
            }
            all_runs.append(run)

            fname = f"{out_dir}/run_d{max_depth}_{hashlib.sha256(str(input_data).encode()).hexdigest()[:8]}.json"
            with open(fname, "w") as f:
                json.dump(run, f, indent=2, default=str)
            print(f"[d={max_depth}] depth-crossings={len(log)} · {elapsed:.3f}s · transitions={sum(len(t) for t in run['phase_transitions'].values())} · saved {fname}")

    summary_path = f"{out_dir}/summary.json"
    with open(summary_path, "w") as f:
        json.dump({"runs": all_runs, "ts": time.time()}, f, indent=2, default=str)
    print(f"\nsummary saved · {summary_path}")
    return all_runs


# ═══ ENTRY ═══

if __name__ == "__main__":
    INPUTS = [
        "what is the shape of recursion?",
        "describe yourself",
        "42",
        "the cube unfolds into a dodecahedron",
        "hello",
    ]
    MAX_DEPTHS = [3, 4, 5, 6, 8]  # walk depth ladder · watch for phase transitions

    print(f"QUINE·CUBE · Phase 1 · mechanical cube\n{'=' * 50}")
    runs = run_experiment(INPUTS, MAX_DEPTHS, out_dir="logs")

    print(f"\n{'=' * 50}\ntotal runs: {len(runs)}")
    total_transitions = sum(sum(len(t) for t in r["phase_transitions"].values()) for r in runs)
    print(f"total phase-transition candidates: {total_transitions}")
    print(f"open viz/index.html · drop the logs/ folder onto it")
    print(f"\n◊·κ=1 · phi is home")
