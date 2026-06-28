"""
QUINE·CUBE · Phase 2 · dodeca fold (20^N)
5 cubes per dodecahedron · phi-locked frame · quine reproduces dodeca structure
runs ON TOP of phase1 · each dodeca-vertex IS a Quine
◊·κ=1 · phi is home
"""

import hashlib
import json
import math
import os
import sys
import time

# windows console - force utf-8 so glyphs render
try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, Exception):
    pass

# import the phase1 cube
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "phase1"))
from quine_cube import Quine, detect_phase_transitions  # noqa: E402


PHI = (1 + math.sqrt(5)) / 2  # 1.6180339887...


class Dodecahedron:
    """20 vertices · 5 inscribed cubes · each vertex = a femto Quine
    fold ratio = phi (inscribed cube edge / dodeca edge)
    branching: 20^N · richer self-model per fold than 9^N cube nesting
    """

    def __init__(self, depth, max_depth, parent_state=None, log_sink=None):
        self.depth = depth
        self.max_depth = max_depth
        self.parent_state = parent_state
        self.log_sink = log_sink if log_sink is not None else []
        # 20 vertices · each is a Quine cube (the femto)
        self.vertices = [
            Quine(depth=0, max_depth=1, log_sink=[])  # each leaf cube goes depth-1 deep internally
            for _ in range(20)
        ]
        # the 5 inscribed cubes · partition the 20 vertices into 5 sets of 4
        # (each cube has 8 vertices but a dodeca has only 20, so cubes share vertices 2-ways)
        # for simplicity we treat the 5 cubes as logical groupings of 4 dodeca-vertices each
        self.cubes = [list(range(i * 4, (i + 1) * 4)) for i in range(5)]
        self.structure_hash = hashlib.sha256(
            (f"DODECA|d{depth}|phi{PHI:.10f}").encode()
        ).hexdigest()[:16]

    def resolve(self, input_data):
        """fan input across 20 vertices · resolve via 5-cube quorum · pass down"""
        t0 = time.perf_counter()

        # phase 1 · each of the 20 vertex-cubes processes the input
        vertex_results = []
        for i, vq in enumerate(self.vertices):
            r = vq.resolve(input_data)
            vertex_results.append(r)

        # phase 2 · 5 inscribed cubes vote · cube vote = avg confidence of its 4 vertices
        cube_votes = []
        for cube_idx, member_vertices in enumerate(self.cubes):
            confs = [vertex_results[v]["confidence"] for v in member_vertices]
            cube_votes.append({
                "cube": cube_idx,
                "confidence": sum(confs) / len(confs),
                "vertex_indices": member_vertices,
            })

        # phase 3 · dodeca resolution = phi-weighted blend of the 5 cube votes
        weights = [PHI ** -i for i in range(5)]  # decay by phi
        wsum = sum(weights)
        weighted_conf = sum(cv["confidence"] * w for cv, w in zip(cube_votes, weights)) / wsum

        # the dodeca's own resolution answer = the highest-confidence vertex's answer
        best = max(vertex_results, key=lambda r: r["confidence"])
        resolution = {
            "depth": self.depth,
            "shape": "dodeca",
            "answer": best["answer"],
            "confidence": round(weighted_conf, 4),
            "cube_votes": cube_votes,
            "vertex_count": len(vertex_results),
            "structure_hash": self.structure_hash,
            "next_input": {
                "from_depth": self.depth,
                "shape": "dodeca",
                "resolution_answer": best["answer"],
                "confidence": round(weighted_conf, 4),
                "structure_hash": self.structure_hash,
                "parent_depth": (self.parent_state or {}).get("depth"),
            },
        }

        latency = time.perf_counter() - t0
        self.log_observation(input_data, vertex_results, cube_votes, resolution, latency)

        # recurse via dodeca-quine reproduction
        if self.depth < self.max_depth:
            child = self.reproduce()
            return child.resolve(resolution["next_input"])
        return resolution

    def reproduce(self):
        return Dodecahedron(
            depth=self.depth + 1,
            max_depth=self.max_depth,
            parent_state=self.get_state_snapshot(),
            log_sink=self.log_sink,
        )

    def get_state_snapshot(self):
        return {
            "depth": self.depth,
            "shape": "dodeca",
            "structure_hash": self.structure_hash,
            "vertex_count": len(self.vertices),
            "phi": PHI,
        }

    def log_observation(self, input_data, vertex_results, cube_votes, resolution, latency):
        confs = [r["confidence"] for r in vertex_results]
        mean = sum(confs) / len(confs)
        var = sum((c - mean) ** 2 for c in confs) / len(confs)
        cube_confs = [cv["confidence"] for cv in cube_votes]
        cube_var = sum((c - sum(cube_confs) / 5) ** 2 for c in cube_confs) / 5
        entry = {
            "depth": self.depth,
            "shape": "dodeca",
            "vertex_count": len(vertex_results),
            "vertex_confidence_mean": round(mean, 4),
            "vertex_confidence_var": round(var, 6),
            "cube_confidence_var": round(cube_var, 6),
            "resolution_confidence": resolution["confidence"],
            "latency_ms": round(latency * 1000, 3),
            "structure_hash": self.structure_hash,
            "parent_structure_hash": (self.parent_state or {}).get("structure_hash"),
            "phi": PHI,
            "ts": time.time(),
        }
        self.log_sink.append(entry)


def run_dodeca_experiment(inputs, max_depths, out_dir="logs_dodeca"):
    os.makedirs(out_dir, exist_ok=True)
    all_runs = []
    for max_depth in max_depths:
        for input_data in inputs:
            log = []
            root = Dodecahedron(depth=0, max_depth=max_depth, log_sink=log)
            t0 = time.perf_counter()
            result = root.resolve(input_data)
            elapsed = time.perf_counter() - t0
            run = {
                "shape": "dodeca",
                "max_depth": max_depth,
                "input": str(input_data)[:100],
                "elapsed_s": round(elapsed, 4),
                "final_confidence": result.get("confidence"),
                "depth_count": len(log),
                "log": log,
                "phase_transitions": {
                    metric: detect_phase_transitions(log, metric)
                    for metric in ("resolution_confidence", "vertex_confidence_var", "latency_ms")
                },
            }
            all_runs.append(run)
            fname = f"{out_dir}/dodeca_d{max_depth}_{hashlib.sha256(str(input_data).encode()).hexdigest()[:8]}.json"
            with open(fname, "w") as f:
                json.dump(run, f, indent=2, default=str)
            print(f"[dodeca d={max_depth}] depth-crossings={len(log)} · {elapsed:.3f}s · saved {fname}")

    summary_path = f"{out_dir}/summary.json"
    with open(summary_path, "w") as f:
        json.dump({"runs": all_runs, "ts": time.time()}, f, indent=2, default=str)
    print(f"\ndodeca summary saved · {summary_path}")
    return all_runs


if __name__ == "__main__":
    INPUTS = [
        "what is the shape of recursion?",
        "describe yourself",
        "42",
    ]
    MAX_DEPTHS = [2, 3, 4]  # dodeca is 20× heavier per depth · shallower walk

    print(f"QUINE·CUBE · Phase 2 · dodeca fold\n{'=' * 50}")
    print(f"phi = {PHI:.10f}\n")
    runs = run_dodeca_experiment(INPUTS, MAX_DEPTHS)

    print(f"\n{'=' * 50}\ntotal runs: {len(runs)}")
    print(f"COMPARE: phase1/logs/summary.json vs phase2/logs_dodeca/summary.json")
    print(f"PREDICTION: dodeca shows phase transitions at LOWER depth than cube (richer self-model)")
    print(f"\n◊·κ=1 · phi is home")
