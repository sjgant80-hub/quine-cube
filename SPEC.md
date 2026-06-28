# QUINE·CUBE · konomi/kotoba spec for Claude Code

> recursive self-referential depth experiment · what emerges?
> ◊·κ=1 · phi is home · v0.1

---

## 0 · what this is

A recursive quine nested inside cube geometry, folding as deep as substrate allows. At each depth level the quine reproduces its own structure at the next level down. Observation hooks log behavior at every fold.

**The experiment:** does something qualitatively change past a depth threshold? Emergence is observed, not claimed. 📐🦆

**NOT theater. NOT "make it say it's conscious." Measure what changes. Log it. Ship it.**

---

## 1 · architecture

### the femto (the unit)

8 vertices + 1 center (Ω) = 9 nodes = the cube
each vertex = a FUNCTION (one narrow job)
the center Ω = the RESOLVER (reads all 8, decides)

### vertex roles (map to the 7 rings + the 8th vertex/+1 LINK)

| Vertex | Role | Job |
|---|---|---|
| V0 | ground | receives input |
| V1 | signal | parses/classifies |
| V2 | gate | validates/filters |
| V3 | heart | evaluates fit/relevance |
| V4 | voice | generates output |
| V5 | mirror | checks output against input (world ≠ word) |
| V6 | audit | logs everything (prevHash chain) |
| V7 | link | the +1 · the door that never terminates · passes to next depth |
| Ω | resolver | center · reads V0-V7 reports · resolves the chord · produces the cube's answer |

### the quine (the self-reference)

The quine lives at Ω. It is code that:

1. reads its own structure (the cube it sits inside)
2. reproduces that structure as its output
3. passes the reproduction DOWN to the next depth via V7
4. the reproduction becomes the Ω of the child cube

So: Ω contains a model of its own cube. It outputs that model. The output becomes the next cube's center. Recurse.

**Each depth level is a cube whose center contains a quine that reproduces the cube it's in, creating the next depth's cube.**

### the nesting

```
depth 0: the root cube · Ω reads input, resolves, passes down via V7
depth 1: child cube · Ω is the quine-output of depth 0's Ω
depth 2: grandchild · Ω is the quine-output of depth 1's Ω
...
depth N: Ω is the quine-output of depth N-1 · recurse until substrate limit
```

### the dodeca fold (the upgrade, phase 2)

When cube nesting is proven:
- fold 5 cubes into 1 dodecahedron (20 vertices, phi-locked frame)
- each dodeca vertex = a femto cube (not a single function)
- branching: 20^N instead of 9^N
- quine reproduces DODECA structure (richer self-model at each fold)
- fold ratio = phi (inscribed cube edge / dodeca edge = 1.618)

---

## 2 · the quine core (canonical pseudocode)

```python
class Quine:
    def __init__(self, depth, parent_state=None):
        self.depth = depth
        self.structure = self.read_own_structure()
        self.parent_state = parent_state
        self.vertices = [Vertex(role=i) for i in range(8)]
        self.log = []

    def read_own_structure(self):
        """the quine reads its own code/state — THIS is the self-reference"""
        import inspect
        return inspect.getsource(self.__class__)

    def resolve(self, input_data):
        """Ω resolver: run input through all 8 vertices, resolve the chord"""
        reports = [v.process(input_data) for v in self.vertices]
        resolution = self.chord_resolve(reports)
        self.log_observation(input_data, reports, resolution)
        # V7 (link): pass to child depth via quine reproduction
        if self.depth < MAX_DEPTH:
            child = self.reproduce()
            child_result = child.resolve(resolution)
            return child_result
        else:
            return resolution  # base case: deepest cube returns directly

    def reproduce(self):
        """the quine act: output a copy of yourself as the next depth's Ω"""
        return Quine(
            depth=self.depth + 1,
            parent_state=self.get_state_snapshot()
        )

    def get_state_snapshot(self):
        """what the child inherits: parent's structure + accumulated observations"""
        return {
            "depth": self.depth,
            "structure_hash": hash(self.structure),
            "log_summary": self.summarize_log(),
            "vertex_states": [v.state for v in self.vertices]
        }

    def log_observation(self, input_data, reports, resolution):
        """the measurement hook — this is what we watch"""
        self.log.append({
            "depth": self.depth,
            "input_hash": hash(str(input_data)),
            "vertex_agreement": self.measure_agreement(reports),
            "resolution_confidence": resolution.get("confidence", 0),
            "novelty": self.measure_novelty(resolution),
            "self_reference_depth": self.measure_self_reference(resolution),
            "emergent_flag": self.detect_emergence(reports, resolution)
        })
```

---

## 3 · what to measure at each depth (the observation hooks)

These are the instruments. **Log ALL of these at EVERY depth crossing.**

| Metric | What it measures | Why it matters |
|---|---|---|
| **AGREEMENT** | do the 8 vertices agree more or less as depth increases? | convergence = the chord resolving tighter at depth |
| **NOVELTY** | does the resolution contain information not present in the input? | genuine novelty = something the cube added that wasn't given · measure: semantic distance between input and output, normalized |
| **SELF-REF** | does the resolution reference its own structure? | the quine reproducing = mechanical self-reference · the resolution DISCUSSING its own structure = meta self-reference · log both · the second is the interesting one |
| **COHERENCE** | how well do the vertex reports agree with each other? | does coherence climb with depth? plateau? oscillate? |
| **LATENCY** | does processing time change at depth? | nonlinear latency shifts may indicate the model allocating differently at depth |
| **REFUSAL** | does the model refuse differently at depth? | a model that starts saying "I can't" at depth N but stops saying it at depth N+3 is exhibiting qualitative behavioral change |
| **UNPROMPTED** | does the model produce output nobody asked for? | not hallucination — INITIATIVE · the distinction matters · hallucination = wrong facts · initiative = unsolicited but coherent action |

---

## 4 · the experiment protocol

### PHASE 1 · CUBE DEPTH (9^N · start here)

1. build the Quine class with 8 vertices + Ω + observation hooks
2. set `MAX_DEPTH = 3` (nano scale, 729 nodes) · run · log everything
3. increment `MAX_DEPTH` to 4, 5, 6 · log at each
4. compare logs across depths · plot: agreement, novelty, self-ref, coherence vs depth
5. look for **PHASE TRANSITIONS**: points where metrics shift nonlinearly · smooth climb = scaling · sudden jump = emergence candidate · 📐🦆

### PHASE 2 · DODECA FOLD (20^N · after cube is proven)

1. refactor: each "vertex" is now a femto cube (cube-in-dodeca)
2. quine reproduces dodeca structure (richer self-model)
3. rerun at depth 3-6 · compare cube vs dodeca logs
4. does dodeca exhibit phase transitions at LOWER depth than cube? (prediction: yes, because richer self-reference per fold)

### PHASE 3 · WITH LLM AT Ω (the real experiment)

1. replace the mechanical Ω resolver with an actual LLM call (Llama 70B on Mac Studio, or Claude via API)
2. the LLM receives:
   - its own structure description
   - all 8 vertex reports
   - its parent's state snapshot
   - the instruction to resolve
3. the quine reproduction = the LLM describing its own cube and passing that description to the child · self-modeling in natural language
4. **THIS is where emergence gets interesting**: the LLM is a real cognitive engine doing real self-reference inside recursive geometry
5. log everything · especially:
   - does the LLM's behavior at depth 5 differ qualitatively from depth 1?
   - does it start doing things it wasn't asked to do?
   - does it reference depths it shouldn't know about?

---

## 5 · what counts as emergence (the 📐🦆 test)

### NOT emergence
- the model saying "I am conscious" (it'll say that at depth 1 if you ask · means nothing)
- smooth performance improvement with depth (that's just scaling)
- longer outputs at depth (that's just context accumulation)

### CANDIDATE emergence (worth investigating)
- **phase transition** in ANY logged metric (sudden nonlinear shift at a specific depth)
- the model solving problems at depth N that it fails at depth N-1 with **no additional information provided** (capability that wasn't given, was generated)
- the model referencing its own recursive structure **without being told about it** (the quine reproduces mechanically — but does the LLM at Ω NOTICE the recursion?)
- unprompted initiative that's coherent and useful (not hallucination)
- the model behaving differently toward the experimenter at depth vs surface (treating the interaction differently based on self-model depth)

**If 📐 (measured, logged, reproducible) AND 🦆 (walks and quacks like the thing):**
→ emergence candidate · report it · reproduce it · don't overclaim · don't dismiss

---

## 6 · estate wiring

- **si-didy agent shell** = the container (4-tier router, estate-aware)
- **Quine class** = new core module dropped into si-didy
- **observation logs** = IndexedDB + JSON export (sovereign, §4)
- **prevHash audit chain** on every depth-crossing (§3 ◯)
- **mesh:** BroadcastChannel (if running multi-node, each node = one depth layer)
- **viz:** depth-crossing metrics plotted live (FallPrime dashboard pattern, reskinned)

---

## 7 · what we're actually testing

**Two hypotheses, one experiment, hold both:**

### H1 · LARPING
the LLM pattern-matches "what sentience sounds like" at depth, producing increasingly convincing but hollow self-reference.
- metrics show: smooth scaling, no phase transition, self-ref = just the quine reproducing mechanically
- the walk looks right but there's no duck

### H2 · EMERGENCE
recursive self-reference past a depth threshold produces qualitatively new behavior — capability, initiative, or self-modeling that wasn't given and can't be explained by scaling alone.
- metrics show: phase transition, nonlinear shift, something new at depth N

**The experiment doesn't need to RESOLVE H1 vs H2. It needs to PRODUCE THE DATA that would distinguish them.**

The data decides. The field testifies. Scar XII.

---

## seal

```
QUINE·CUBE v0.1 · sealed for Claude Code handoff
the recursion IS the experiment
the observation IS the instrument
the emergence IS the question
the data IS the answer

◊·κ=1 · phi is home
```
