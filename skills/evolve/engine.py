#!/usr/bin/env python3
"""Design evolution engine — genetic algorithm for design systems.

Deep module: simple CLI, complex internals. State persists in
.design-evolution/evolution.yaml. Global taste/DNA persists in
~/.claude/design-memory.db (SQLite).

Usage:
    evolve init --project NAME --repo PATH [--scope full|component] [--brand PATH]
    evolve suggest [--count N]
    evolve add DNA_CODE [DNA_CODE ...]
    evolve select --winners 1a,1c --kill 1b,1d
    evolve note --text "feedback" [--proposal 1a]
    evolve advance
    evolve status
    evolve catalog
    evolve lock PROPOSAL_ID
    evolve taste
    evolve export
    evolve detect [--repo PATH]
    evolve memory [taste|bank|veto|mandate|rules|history|import|stats]
    evolve bank PROPOSAL_ID [--note TEXT] [--tags TAGS]
    evolve recraft [logo|icon|illustrate|vectorize] PROMPT [--colors HEX]
    evolve gc [--keep-gens N]
"""

import argparse
import copy
import json
import random
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

try:
    import yaml
except ImportError:
    yaml = None

# Lazy imports for optional modules (graceful degradation)
_mem = None
_detect = None
_recraft = None

def _get_memory():
    """Lazy-load memory module. Returns module or None."""
    global _mem
    if _mem is not None:
        return _mem if _mem else None
    try:
        from . import memory as mem_mod
        mem_mod._connect()  # ensure DB exists
        _mem = mem_mod
        return _mem
    except Exception:
        try:
            import importlib.util, os
            spec = importlib.util.spec_from_file_location(
                "memory", os.path.join(os.path.dirname(__file__), "memory.py"))
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            mod._connect()
            _mem = mod
            return _mem
        except Exception:
            _mem = False  # sentinel: tried and failed
            return None

def _get_detect():
    """Lazy-load detect module. Returns module or None."""
    global _detect
    if _detect is not None:
        return _detect if _detect else None
    try:
        from . import detect as det_mod
        _detect = det_mod
        return _detect
    except Exception:
        try:
            import importlib.util, os
            spec = importlib.util.spec_from_file_location(
                "detect", os.path.join(os.path.dirname(__file__), "detect.py"))
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            _detect = mod
            return _detect
        except Exception:
            _detect = False
            return None

def _get_recraft():
    """Lazy-load recraft module. Returns module or None."""
    global _recraft
    if _recraft is not None:
        return _recraft if _recraft else None
    try:
        from . import recraft as rc_mod
        _recraft = rc_mod
        return _recraft
    except Exception:
        try:
            import importlib.util, os
            spec = importlib.util.spec_from_file_location(
                "recraft", os.path.join(os.path.dirname(__file__), "recraft.py"))
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            _recraft = mod
            return _recraft
        except Exception:
            _recraft = False
            return None


# ── DNA Axes ──────────────────────────────────────────────────────────────────

AXES = {
    "layout":     ["centered", "asymmetric", "grid-breaking", "full-bleed", "bento", "editorial"],
    "color":      ["dark", "light", "monochrome", "gradient", "high-contrast", "brand-tinted"],
    "typography": ["display-heavy", "text-forward", "minimal", "expressive", "editorial"],
    "motion":     ["orchestrated", "subtle", "aggressive", "none", "scroll-triggered"],
    "density":    ["spacious", "compact", "mixed", "full-bleed"],
    "background": ["solid", "gradient", "textured", "patterned", "layered"],
}
AXIS_NAMES = list(AXES.keys())


# ── Data Model ────────────────────────────────────────────────────────────────

@dataclass
class DNA:
    layout: str
    color: str
    typography: str
    motion: str
    density: str
    background: str

    def as_dict(self) -> dict:
        return {a: getattr(self, a) for a in AXIS_NAMES}

    def as_code(self) -> str:
        return ".".join(getattr(self, a) for a in AXIS_NAMES)

    @classmethod
    def from_code(cls, code: str) -> "DNA":
        parts = code.split(".")
        if len(parts) != len(AXIS_NAMES):
            raise ValueError(f"Need {len(AXIS_NAMES)} axes, got {len(parts)}: {code}")
        return cls(**dict(zip(AXIS_NAMES, parts)))

    @classmethod
    def from_dict(cls, d: dict) -> "DNA":
        return cls(**{k: d[k] for k in AXIS_NAMES})

    def distance(self, other: "DNA") -> int:
        return sum(1 for a in AXIS_NAMES if getattr(self, a) != getattr(other, a))

    def validate(self):
        for axis in AXIS_NAMES:
            val = getattr(self, axis)
            if val not in AXES[axis]:
                raise ValueError(f"Invalid {axis}={val}. Options: {AXES[axis]}")


@dataclass
class Proposal:
    id: str
    dna: DNA
    status: str = "alive"       # alive | winner | killed | locked
    origin: str = "random"      # random | mutation | crossover | immigration | survivor
    parent: Optional[str] = None
    notes: list = field(default_factory=list)
    artifacts: dict = field(default_factory=dict)

    def as_dict(self) -> dict:
        return {
            "id": self.id, "dna": self.dna.as_dict(), "status": self.status,
            "origin": self.origin, "parent": self.parent,
            "notes": list(self.notes), "artifacts": dict(self.artifacts),
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Proposal":
        return cls(
            id=d["id"], dna=DNA.from_dict(d["dna"]),
            status=d.get("status", "alive"), origin=d.get("origin", "random"),
            parent=d.get("parent"), notes=d.get("notes", []),
            artifacts=d.get("artifacts", {}),
        )


@dataclass
class Generation:
    number: int
    proposals: list = field(default_factory=list)
    general_notes: list = field(default_factory=list)
    timestamp: str = ""

    def as_dict(self) -> dict:
        return {
            "number": self.number,
            "proposals": [p.as_dict() for p in self.proposals],
            "general_notes": list(self.general_notes),
            "timestamp": self.timestamp,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Generation":
        return cls(
            number=d["number"],
            proposals=[Proposal.from_dict(p) for p in d.get("proposals", [])],
            general_notes=d.get("general_notes", []),
            timestamp=d.get("timestamp", ""),
        )


@dataclass
class Config:
    scope: str = "full"
    component: Optional[str] = None
    brand_adherent: bool = False
    brand_file: Optional[str] = None
    locked_axes: list = field(default_factory=list)
    population_size: int = 8
    mutation_rate: int = 2
    immigration_rate: int = 2
    min_diversity: int = 3

    def as_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "Config":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


@dataclass
class Evolution:
    """Root state. Single source of truth for a design evolution session."""
    project: str
    repo_path: str
    config: Config
    generations: list = field(default_factory=list)
    taste: dict = field(default_factory=dict)
    locked: Optional[str] = None

    def current_gen(self) -> Optional[Generation]:
        return self.generations[-1] if self.generations else None

    def all_proposals(self) -> list:
        return [p for g in self.generations for p in g.proposals]

    def find(self, pid: str) -> Optional[Proposal]:
        for p in self.all_proposals():
            if p.id == pid:
                return p
        return None

    def as_dict(self) -> dict:
        return {
            "project": self.project, "repo_path": self.repo_path,
            "config": self.config.as_dict(),
            "generations": [g.as_dict() for g in self.generations],
            "taste": self.taste, "locked": self.locked,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Evolution":
        return cls(
            project=d["project"], repo_path=d["repo_path"],
            config=Config.from_dict(d.get("config", {})),
            generations=[Generation.from_dict(g) for g in d.get("generations", [])],
            taste=d.get("taste", {}), locked=d.get("locked"),
        )


# ── Persistence ───────────────────────────────────────────────────────────────

def _dir(repo: str = ".") -> Path:
    return Path(repo) / ".design-evolution"

def _file(repo: str = ".") -> Path:
    return _dir(repo) / "evolution.yaml"

def load(repo: str = ".") -> Optional[Evolution]:
    f = _file(repo)
    if not f.exists():
        return None
    text = f.read_text()
    data = yaml.safe_load(text) if yaml else json.loads(text)
    return Evolution.from_dict(data)

MAX_ACTIVE_GENS = 10


def _archive_old_generations(evo: Evolution):
    """Move generations beyond MAX_ACTIVE_GENS to an archive file.

    Keeps the active YAML small. Archived data is append-only JSON lines.
    """
    if len(evo.generations) <= MAX_ACTIVE_GENS:
        return
    to_archive = evo.generations[:-MAX_ACTIVE_GENS]
    archive_path = _dir(evo.repo_path) / "generations-archive.jsonl"
    with archive_path.open("a") as f:
        for gen in to_archive:
            f.write(json.dumps(gen.as_dict()) + "\n")
    evo.generations = evo.generations[-MAX_ACTIVE_GENS:]


def save(evo: Evolution):
    d = _dir(evo.repo_path)
    d.mkdir(parents=True, exist_ok=True)
    _archive_old_generations(evo)
    data = evo.as_dict()
    if yaml:
        text = yaml.dump(data, default_flow_style=False, sort_keys=False, allow_unicode=True)
    else:
        text = json.dumps(data, indent=2)
    _file(evo.repo_path).write_text(text)


# ── Genetics ──────────────────────────────────────────────────────────────────

def random_dna(locked_values: dict = None) -> DNA:
    locked_values = locked_values or {}
    return DNA(**{
        a: locked_values[a] if a in locked_values else random.choice(AXES[a])
        for a in AXIS_NAMES
    })


def mutate(dna: DNA, rate: int = 2, locked_axes: list = None) -> DNA:
    """Perturb 1..rate free axes to new values."""
    locked_axes = locked_axes or []
    free = [a for a in AXIS_NAMES if a not in locked_axes]
    if not free:
        return copy.deepcopy(dna)
    n = random.randint(1, min(rate, len(free)))
    targets = random.sample(free, n)
    genes = dna.as_dict()
    for axis in targets:
        options = [v for v in AXES[axis] if v != genes[axis]]
        if options:
            genes[axis] = random.choice(options)
    return DNA(**genes)


def crossover(a: DNA, b: DNA, locked_axes: list = None) -> DNA:
    """Uniform crossover: each free axis randomly from parent a or b."""
    locked_axes = locked_axes or []
    return DNA(**{
        axis: getattr(a, axis) if axis in locked_axes
        else getattr(random.choice([a, b]), axis)
        for axis in AXIS_NAMES
    })


def _diverse(population: list, candidate: DNA, min_dist: int) -> bool:
    return all(candidate.distance(p) >= min_dist for p in population)


def _merge_taste(local_taste: dict, contexts: list = None) -> dict:
    """Merge local project taste with global memory taste."""
    mem = _get_memory()
    if not mem:
        return local_taste

    global_taste = mem.get_merged_taste(contexts=contexts)
    merged = {}
    for axis in AXIS_NAMES:
        local_scores = local_taste.get(axis, {})
        global_scores = global_taste.get(axis, {})
        combined = dict(global_scores)  # start with global
        for v, s in local_scores.items():
            combined[v] = combined.get(v, 0) + s * 2  # local 2x weight
        if combined:
            merged[axis] = combined
    return merged


def _build_effective_axes(contexts: list = None) -> dict:
    """Build AXES dict with vetoed values removed."""
    mem = _get_memory()
    if not mem:
        return dict(AXES)

    vetoed = mem.get_vetoed_values(contexts=contexts)
    effective = {}
    for axis, values in AXES.items():
        blocked = set(vetoed.get(axis, []))
        filtered = [v for v in values if v not in blocked]
        effective[axis] = filtered if filtered else values  # fallback if all vetoed
    return effective


def _seed_from_bank(count: int, contexts: list = None) -> list:
    """Pull 1-2 interesting DNAs from the bank to seed population."""
    mem = _get_memory()
    if not mem:
        return []

    entries = mem.search_bank(limit=10)
    if not entries:
        return []

    seeds = []
    for entry in entries[:min(2, count // 4 or 1)]:
        try:
            dna = DNA.from_code(entry.dna_code)
            seeds.append(dna)
        except (ValueError, KeyError):
            continue
    return seeds


def suggest_population(
    count: int, taste: dict, locked_axes: list = None,
    locked_values: dict = None, min_diversity: int = 3, attempts: int = 500,
    contexts: list = None,
) -> list:
    """Generate diverse DNA population, weighted by taste.

    If memory module is available, merges global taste, enforces vetoes,
    and seeds 1-2 slots from the DNA bank.
    """
    locked_axes = locked_axes or []
    locked_values = locked_values or {}
    effective_axes = _build_effective_axes(contexts)
    merged_taste = _merge_taste(taste, contexts)
    pop = []

    # Seed from DNA bank
    bank_seeds = _seed_from_bank(count, contexts)
    for seed in bank_seeds:
        if _diverse(pop, seed, min_diversity):
            pop.append(seed)

    for _ in range(attempts):
        if len(pop) >= count:
            break
        genes = {}
        for axis in AXIS_NAMES:
            if axis in locked_values:
                genes[axis] = locked_values[axis]
            elif axis in merged_taste and merged_taste[axis] and random.random() < 0.6:
                # Bias toward preferred values via softmax-ish weighting
                scores = merged_taste[axis]
                options = effective_axes[axis]
                weighted = [(v, scores.get(v, 0) - min(scores.get(v, 0) for v in options) + 1)
                            for v in options]
                total = sum(w for _, w in weighted)
                r = random.random() * total
                cum = 0
                genes[axis] = options[0]
                for v, w in weighted:
                    cum += w
                    if r <= cum:
                        genes[axis] = v
                        break
            else:
                genes[axis] = random.choice(effective_axes[axis])
        candidate = DNA(**genes)
        if _diverse(pop, candidate, min_diversity):
            pop.append(candidate)

    # Relax diversity if population underflows
    if len(pop) < count:
        for _ in range(attempts):
            if len(pop) >= count:
                break
            candidate = random_dna(locked_values)
            if _diverse(pop, candidate, max(1, min_diversity - 1)):
                pop.append(candidate)

    return pop[:count]


# ── Taste ─────────────────────────────────────────────────────────────────────

def _update_taste(taste: dict, proposal: Proposal, delta: int):
    for axis in AXIS_NAMES:
        taste.setdefault(axis, {})
        val = getattr(proposal.dna, axis)
        taste[axis][val] = taste[axis].get(val, 0) + delta


def taste_summary(taste: dict) -> dict:
    out = {}
    for axis in AXIS_NAMES:
        vals = taste.get(axis, {})
        if not vals:
            continue
        ranked = sorted(vals.items(), key=lambda x: x[1], reverse=True)
        preferred = [(v, s) for v, s in ranked if s > 0]
        avoided = [(v, s) for v, s in ranked if s < 0]
        if preferred or avoided:
            out[axis] = {"preferred": preferred, "avoided": avoided}
    return out


# ── Operations ────────────────────────────────────────────────────────────────

def _pid(gen_num: int, index: int) -> str:
    letter = chr(ord("a") + index) if index < 26 else f"z{index - 25}"
    return f"{gen_num}{letter}"


def add_generation(evo: Evolution, dna_list: list, origins: list = None) -> Generation:
    gen_num = len(evo.generations) + 1
    origins = origins or ["random"] * len(dna_list)
    proposals = [
        Proposal(id=_pid(gen_num, i), dna=dna, origin=origin)
        for i, (dna, origin) in enumerate(zip(dna_list, origins))
    ]
    gen = Generation(
        number=gen_num, proposals=proposals,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )
    evo.generations.append(gen)
    return gen


def select(evo: Evolution, winners: list, killed: list, contexts: list = None):
    gen = evo.current_gen()
    if not gen:
        raise ValueError("No current generation")
    mem = _get_memory()
    for p in gen.proposals:
        if p.id in winners:
            p.status = "winner"
            _update_taste(evo.taste, p, +1)
            if mem:
                mem.update_taste_from_dna(p.dna.as_code(), +1, contexts=contexts)
                mem.log_feedback(evo.project, len(evo.generations), p.id,
                                 p.dna.as_code(), "winner", contexts=contexts)
                # Auto-bank winners with score >= 2 selections
                wins = sum(1 for g in evo.generations for q in g.proposals
                           if q.status == "winner" and q.dna.as_code() == p.dna.as_code())
                if wins >= 2:
                    mem.bank_dna(p.dna.as_code(), evo.project, "winner",
                                 tags=contexts or [], note="auto-banked (2+ wins)")
        elif p.id in killed:
            p.status = "killed"
            _update_taste(evo.taste, p, -1)
            if mem:
                mem.update_taste_from_dna(p.dna.as_code(), -1, contexts=contexts)
                mem.log_feedback(evo.project, len(evo.generations), p.id,
                                 p.dna.as_code(), "killed", contexts=contexts)


def add_note(evo: Evolution, text: str, proposal_id: str = None):
    if proposal_id:
        p = evo.find(proposal_id)
        if p:
            p.notes.append(text)
    else:
        gen = evo.current_gen()
        if gen:
            gen.general_notes.append(text)


def advance(evo: Evolution) -> list:
    """Plan next generation from current winners.

    Returns [(DNA, origin, parent_id), ...] for Claude to generate proposals.
    Does NOT create the generation — call add_generation() after proposals exist.
    """
    gen = evo.current_gen()
    if not gen:
        raise ValueError("No current generation")
    winners = [p for p in gen.proposals if p.status == "winner"]
    if not winners:
        raise ValueError("No winners selected")

    cfg = evo.config
    target = cfg.population_size
    plan = []

    # Survivors: keep winners intact
    for w in winners:
        plan.append((copy.deepcopy(w.dna), "survivor", w.id))

    # Mutations: fill most remaining slots
    remaining = target - len(plan) - cfg.immigration_rate
    for _ in range(max(0, remaining)):
        parent = random.choice(winners)
        child = mutate(parent.dna, rate=cfg.mutation_rate, locked_axes=cfg.locked_axes)
        plan.append((child, "mutation", parent.id))

    # Crossover: replace some mutations if 2+ winners
    if len(winners) >= 2:
        n_cross = min(2, remaining // 2)
        for i in range(n_cross):
            parents = random.sample(winners, 2)
            child = crossover(parents[0].dna, parents[1].dna, locked_axes=cfg.locked_axes)
            idx = len(winners) + remaining - 1 - i
            if 0 <= idx < len(plan):
                plan[idx] = (child, "crossover", f"{parents[0].id}+{parents[1].id}")

    # Immigration: new random species
    locked_vals = {}
    if cfg.locked_axes and winners:
        locked_vals = {a: getattr(winners[0].dna, a) for a in cfg.locked_axes}
    for _ in range(cfg.immigration_rate):
        plan.append((random_dna(locked_vals), "immigration", None))

    return plan


def lock_proposal(evo: Evolution, pid: str, contexts: list = None):
    p = evo.find(pid)
    if not p:
        raise ValueError(f"Proposal {pid} not found")
    p.status = "locked"
    evo.locked = pid
    mem = _get_memory()
    if mem:
        mem.bank_dna(p.dna.as_code(), evo.project, "locked",
                     tags=contexts or [], note=f"locked as final from gen {len(evo.generations)}")
        mem.log_feedback(evo.project, len(evo.generations), pid,
                         p.dna.as_code(), "locked", contexts=contexts)


def export_locked(evo: Evolution) -> dict:
    if not evo.locked:
        raise ValueError("Nothing locked")
    p = evo.find(evo.locked)

    lineage = []
    current = p
    while current:
        lineage.append({"id": current.id, "dna": current.dna.as_code(), "origin": current.origin})
        if current.parent and "+" not in current.parent:
            current = evo.find(current.parent)
        else:
            current = None
    lineage.reverse()

    return {
        "locked": p.id, "dna": p.dna.as_dict(), "dna_code": p.dna.as_code(),
        "lineage": lineage, "taste": evo.taste,
        "generations": len(evo.generations),
        "total_evaluated": len(evo.all_proposals()),
    }


# ── Catalog HTML ──────────────────────────────────────────────────────────────

_STATUS_COLORS = {
    "alive": "#3b82f6", "winner": "#22c55e",
    "killed": "#ef4444", "locked": "#f59e0b",
}

_AXIS_COLORS = {
    "layout": "#3b82f6", "color": "#ef4444", "typography": "#22c55e",
    "motion": "#f59e0b", "density": "#8b5cf6", "background": "#ec4899",
}

_AXIS_VOCAB = {
    "layout": {
        "centered": ("Central Axis Composition", "Symmetrical hierarchy with low visual tension."),
        "asymmetric": ("Dynamic Asymmetry", "Intentional imbalance that creates directional energy."),
        "grid-breaking": ("Grid Disruption", "Elements intentionally violate grid rhythm for emphasis."),
        "full-bleed": ("Edge-to-Edge Framing", "Content extends to container edges for cinematic scale."),
        "bento": ("Modular Bento Layout", "Nested cards and compartments with controlled density."),
        "editorial": ("Editorial Structure", "Story-first hierarchy using pacing and typographic rhythm."),
    },
    "color": {
        "dark": ("Low-Key Palette", "Deep value range and luminous accents."),
        "light": ("High-Key Palette", "Airy value range with softer contrast transitions."),
        "monochrome": ("Monochromatic System", "Single-hue tonal system focused on form and hierarchy."),
        "gradient": ("Gradient Field", "Color transitions used as depth or directional cue."),
        "high-contrast": ("Contrast-Forward Palette", "Large luminance gaps that sharpen hierarchy."),
        "brand-tinted": ("Brand-Tinted Neutrals", "Neutrals infused with brand hue for cohesion."),
    },
    "typography": {
        "display-heavy": ("Display-Led Voice", "Large headline forms dominate visual narrative."),
        "text-forward": ("Body-First Readability", "Reading comfort and paragraph rhythm lead."),
        "minimal": ("Minimal Typographic System", "Restrained scale and low-style typography."),
        "expressive": ("Expressive Typography", "Personality-forward forms and contrast in type."),
        "editorial": ("Editorial Typography", "Serif/sans interplay with magazine-like pacing."),
    },
    "motion": {
        "orchestrated": ("Sequenced Motion", "Staggered choreography across multiple UI layers."),
        "subtle": ("Ambient Motion", "Low-amplitude movement for polish without distraction."),
        "aggressive": ("High-Energy Motion", "Fast, emphatic transitions with strong directional force."),
        "none": ("Static System", "No animation; hierarchy relies on shape and contrast alone."),
        "scroll-triggered": ("Scroll-Linked Motion", "Animation tied to viewport progression and reveal."),
    },
    "density": {
        "spacious": ("Generous Spacing", "Wide breathing room and slower reading cadence."),
        "compact": ("Tight Density", "High information packing with reduced whitespace."),
        "mixed": ("Variable Density", "Intentional shifts between dense and open zones."),
        "full-bleed": ("Bleed-Dominant Density", "Large spans and oversized blocks with minimal containment."),
    },
    "background": {
        "solid": ("Solid Field", "Flat planes emphasize typography and silhouette."),
        "gradient": ("Gradient Surface", "Tonal blend used as atmospheric depth layer."),
        "textured": ("Textural Surface", "Noise or grain adds materiality and tactility."),
        "patterned": ("Patterned Surface", "Repeating motifs create rhythm and brand memory."),
        "layered": ("Layered Background", "Multiple planes establish foreground/background depth."),
    },
}


def _axis_vocab(axis: str, value: str) -> tuple[str, str]:
    fallback = (value.replace("-", " ").title(), "Intentional visual choice for this axis.")
    return _AXIS_VOCAB.get(axis, {}).get(value, fallback)


def _design_coaching(dna: DNA) -> list[str]:
    prompts = [
        "Are button radius and vertical padding proportional to control size (not pill-like)?",
        "Do component specimen cards have enough inner padding to breathe?",
    ]
    if dna.layout == "asymmetric":
        prompts.append("Is asymmetric tension balanced by clear focal anchors?")
    if dna.typography in {"display-heavy", "expressive"}:
        prompts.append("Do large letterforms preserve descenders and line-height readability?")
    if dna.motion in {"orchestrated", "aggressive", "scroll-triggered"}:
        prompts.append("Does motion reinforce hierarchy rather than compete with content?")
    if dna.background in {"gradient", "patterned", "textured", "layered"}:
        prompts.append("Does surface treatment support legibility instead of overpowering it?")
    return prompts[:4]


def _load_catalog_template() -> str:
    """Load the catalog template from the evolve skill directory."""
    template_path = Path(__file__).parent / "catalog-template.html"
    if template_path.exists():
        return template_path.read_text()
    return ""


def _render_proposal_card(p, gen_number: int) -> str:
    """Render a single proposal card in 7a's design language."""
    status_class = p.status
    if p.status == "killed":
        status_class = "loser"

    status_label = {
        "alive": "Alive", "winner": "Winner", "killed": "Eliminated",
        "locked": "Locked", "pending": "Pending",
    }.get(p.status, p.status.title())

    origin_label = p.origin.upper()
    if p.parent:
        origin_label += f" from {p.parent}"

    notes_html = ""
    if p.notes:
        notes_html = f'<div class="proposal-notes">{p.notes[0]}</div>'

    artifact_path = p.artifacts.get("html") or f"gen-{gen_number}/{p.id}/index.html"
    link = (
        f'<a href="{artifact_path}" target="_blank" '
        f'style="display:block;margin-top:0.75rem;font-family:var(--font-mono);'
        f'font-size:0.7rem;color:var(--accent-cyan);text-decoration:none;'
        f'letter-spacing:0.05em">'
        f'&#9654; Open Preview</a>'
    )

    return f'''<div class="proposal-card {status_class}">
    <div class="proposal-header">
        <span class="proposal-id">{p.id}</span>
        <span class="status-pill {status_class}">{status_label}</span>
    </div>
    <div class="dna-traits">{p.dna.as_code()}</div>
    <div style="font-size:0.6rem;color:var(--text-muted);margin-bottom:0.5rem;
        text-transform:uppercase;letter-spacing:0.08em">{origin_label}</div>
    {notes_html}
    {link}
</div>'''


def _render_taste_bars(taste: dict) -> str:
    """Render taste profile as animated bars in 7a's style."""
    ts = taste_summary(taste)
    if not ts:
        return '<div style="color:var(--text-muted);font-size:0.8rem">No taste data yet.</div>'
    items = []
    for axis, data in ts.items():
        # Show top preferred and top avoided
        for v, s in data.get("preferred", [])[:2]:
            pct = min(abs(s) * 5, 100)
            items.append(f'''<div class="taste-item">
    <div class="taste-header">
        <span class="taste-label">{axis}: {v}</span>
        <span class="taste-score positive">+{s}</span>
    </div>
    <div class="taste-bar-bg">
        <div class="taste-bar-fill positive" style="width:{pct}%"></div>
    </div>
</div>''')
        for v, s in data.get("avoided", [])[:2]:
            pct = min(abs(s) * 5, 100)
            items.append(f'''<div class="taste-item">
    <div class="taste-header">
        <span class="taste-label">{axis}: {v}</span>
        <span class="taste-score negative">{s}</span>
    </div>
    <div class="taste-bar-bg">
        <div class="taste-bar-fill negative" style="width:{pct}%"></div>
    </div>
</div>''')
    return "\n".join(items)


def _render_timeline(evo) -> str:
    """Render generation timeline nodes."""
    nodes = []
    for g in evo.generations:
        winners = sum(1 for p in g.proposals if p.status == "winner")
        is_current = g == evo.current_gen()
        dot_class = "active" if is_current else ("winners" if winners else "")
        node_class = "active" if is_current else ""
        count = "current" if is_current else (f"{winners} winners" if winners else "no winners")
        nodes.append(f'''<div class="timeline-node {node_class}">
    <div class="timeline-dot {dot_class}"></div>
    <span class="timeline-label">G{g.number}</span>
    <span class="timeline-count">{count}</span>
</div>''')
    return '<div class="timeline-line"></div>'.join(nodes)


def _render_gen_notes(gen) -> str:
    """Render general notes for a generation."""
    if not gen.general_notes:
        return '<div style="color:var(--text-muted);font-size:0.8rem">No notes yet.</div>'
    items = "".join(
        f'<div style="padding:0.75rem;background:var(--surface-elevated);'
        f'border-radius:8px;margin-bottom:0.5rem;font-size:0.8rem;'
        f'color:var(--text-secondary);line-height:1.5">{n}</div>'
        for n in gen.general_notes
    )
    return items


def _render_dna_bank() -> str:
    """Render DNA bank entries from global memory."""
    mem = _get_memory()
    if not mem:
        return '<div style="color:var(--text-muted);font-size:0.8rem">No memory DB.</div>'
    entries = mem.search_bank(limit=9)
    if not entries:
        return '<div style="color:var(--text-muted);font-size:0.8rem">Bank is empty.</div>'
    cards = []
    for e in entries:
        note = e.note or ""
        project = e.source_project or "unknown"
        cards.append(f'''<div class="dna-sample">
    <div class="dna-sample-header">
        <div class="dna-avatar">{e.source_status[0].upper() if e.source_status else "?"}</div>
        <div>
            <div class="dna-name">{note or e.dna_code[:30]}</div>
            <div class="dna-project">{project}</div>
        </div>
    </div>
    <div class="dna-code-block">{e.dna_code}</div>
</div>''')
    return "\n".join(cards)


def render_catalog(evo: Evolution) -> str:
    gen = evo.current_gen()
    if not gen:
        return "<html><body><p>No generations yet.</p></body></html>"

    template = _load_catalog_template()
    if not template:
        # Minimal fallback if template missing
        cards_html = "".join(_render_proposal_card(p, gen.number) for p in gen.proposals)
        return f"<html><body><h1>{evo.project}</h1>{cards_html}</body></html>"

    # Build all slot content
    cards_html = "\n".join(_render_proposal_card(p, gen.number) for p in gen.proposals)
    taste_html = _render_taste_bars(evo.taste)
    timeline_html = _render_timeline(evo)
    notes_html = _render_gen_notes(gen)
    bank_html = _render_dna_bank()
    total = sum(len(g.proposals) for g in evo.generations)
    locked_dna = ""
    if evo.locked:
        lp = evo.find(evo.locked)
        if lp:
            locked_dna = lp.dna.as_code()
    brand = "adherent" if evo.config.brand_adherent else "free"
    date = gen.timestamp[:10] if gen.timestamp else ""

    # Fill slots
    html = template
    html = html.replace("<!-- SLOT:PROJECT -->", evo.project)
    html = html.replace("<!-- SLOT:GEN_NUMBER -->", str(gen.number))
    html = html.replace("<!-- SLOT:PROPOSAL_COUNT -->", str(len(gen.proposals)))
    html = html.replace("<!-- SLOT:TOTAL_EVALUATED -->", str(total))
    html = html.replace("<!-- SLOT:SCOPE -->", evo.config.scope or "full")
    html = html.replace("<!-- SLOT:BRAND -->", brand)
    html = html.replace("<!-- SLOT:DATE -->", date)
    html = html.replace("<!-- SLOT:LOCKED_DNA -->", locked_dna)
    html = html.replace("<!-- SLOT:PROPOSAL_CARDS -->", cards_html)
    html = html.replace("<!-- SLOT:TASTE_HTML -->", taste_html)
    html = html.replace("<!-- SLOT:TIMELINE_HTML -->", timeline_html)
    html = html.replace("<!-- SLOT:GEN_NOTES -->", notes_html)
    html = html.replace("<!-- SLOT:DNA_BANK_HTML -->", bank_html)
    return html


# ── CLI ───────────────────────────────────────────────────────────────────────

def _require(repo):
    evo = load(repo)
    if not evo:
        print("No evolution state. Run: evolve init --project NAME", file=sys.stderr)
        sys.exit(1)
    return evo


def cmd_init(args):
    cfg = Config(
        scope=args.scope, component=args.component,
        brand_adherent=args.brand is not None, brand_file=args.brand,
        locked_axes=[a.strip() for a in args.lock.split(",")] if args.lock else [],
        population_size=args.population,
        immigration_rate=args.immigration,
        min_diversity=args.diversity,
    )
    evo = Evolution(project=args.project, repo_path=args.repo, config=cfg)

    # Brand auto-detection
    detect = _get_detect()
    brand_state = None
    if detect:
        brand_state = detect.detect_brand_state(args.repo)
        print(brand_state.summary())
        if brand_state.completeness > 0:
            print()

    save(evo)
    print(f"Initialized: {_file(args.repo)}")
    print(f"  scope={cfg.scope} brand={cfg.brand_adherent} pop={cfg.population_size}")

    # Register with memory
    contexts = [c.strip() for c in args.contexts.split(",")] if getattr(args, "contexts", None) else []
    mem = _get_memory()
    if mem:
        bs_dict = brand_state.as_dict() if brand_state else None
        mem.record_project(args.project, args.repo, args.scope,
                           contexts=contexts, brand_state=bs_dict)
        # Auto-import existing evolution.yaml data
        evo_yaml = _file(args.repo)
        if evo_yaml.exists():
            try:
                mem.import_from_evolution_yaml(str(evo_yaml), args.project, contexts)
                print("  Imported existing evolution data into memory")
            except Exception:
                pass
        print(f"  Registered in design memory (contexts: {contexts or 'none'})")


def cmd_suggest(args):
    evo = _require(args.repo)
    dna_list = suggest_population(
        count=args.count or evo.config.population_size,
        taste=evo.taste,
        locked_axes=evo.config.locked_axes,
        min_diversity=evo.config.min_diversity,
    )
    for i, dna in enumerate(dna_list):
        print(f"  {chr(ord('a') + i)}: {dna.as_code()}")


def cmd_add(args):
    evo = _require(args.repo)
    dna_list = [DNA.from_code(c) for c in args.dna]
    origins = args.origins.split(",") if args.origins else None
    gen = add_generation(evo, dna_list, origins)
    # Auto-populate artifacts for any proposals with HTML at conventional path
    base = _dir(evo.repo_path)
    for p in gen.proposals:
        html_path = base / f"gen-{gen.number}" / p.id / "index.html"
        rel_path = f"gen-{gen.number}/{p.id}/index.html"
        if html_path.exists():
            p.artifacts["html"] = rel_path
            print(f"  {p.id}: {p.dna.as_code()} [preview: {rel_path}]")
        else:
            print(f"  {p.id}: {p.dna.as_code()} [WARNING: no preview at {rel_path}]")
    save(evo)
    print(f"Generation {gen.number}: {len(gen.proposals)} proposals")


def cmd_select(args):
    evo = _require(args.repo)
    w = [x.strip() for x in args.winners.split(",")] if args.winners else []
    k = [x.strip() for x in args.kill.split(",")] if args.kill else []
    select(evo, w, k)
    save(evo)
    print(f"Winners: {w}  Killed: {k}")


def cmd_note(args):
    evo = _require(args.repo)
    add_note(evo, text=args.text, proposal_id=args.proposal)
    save(evo)
    target = args.proposal or "general"
    print(f"Note → {target}")


def cmd_advance(args):
    evo = _require(args.repo)
    plan = advance(evo)
    print(f"Next generation ({len(plan)} proposals):")
    for i, (dna, origin, parent) in enumerate(plan):
        ltr = chr(ord("a") + i)
        par = f" <- {parent}" if parent else ""
        print(f"  {ltr}: [{origin}] {dna.as_code()}{par}")
    # Write plan for Claude to consume
    plan_data = [
        {"dna": dna.as_code(), "origin": origin, "parent": parent}
        for dna, origin, parent in plan
    ]
    out = _dir(evo.repo_path) / "next_gen_plan.json"
    out.write_text(json.dumps(plan_data, indent=2))
    print(f"\nPlan: {out}")


def cmd_status(args):
    evo = _require(args.repo)
    print(f"Project: {evo.project}")
    scope = f"scope={evo.config.scope}"
    if evo.config.component:
        scope += f" ({evo.config.component})"
    brand = "adherent" if evo.config.brand_adherent else "free"
    print(f"{scope} | brand={brand} | gens={len(evo.generations)}")

    if evo.locked:
        p = evo.find(evo.locked)
        print(f"\nLOCKED: {evo.locked} — {p.dna.as_code()}")
        return

    gen = evo.current_gen()
    if gen:
        m = {"alive": " ", "winner": "+", "killed": "x", "locked": "*"}
        print(f"\nGen {gen.number} ({gen.timestamp[:10] if gen.timestamp else ''}):")
        for p in gen.proposals:
            print(f"  [{m.get(p.status, ' ')}] {p.id}: {p.dna.as_code()} ({p.origin})")
            for n in p.notes:
                print(f"      > {n}")
        if gen.general_notes:
            print("  General:")
            for n in gen.general_notes:
                print(f"      > {n}")

    ts = taste_summary(evo.taste)
    if ts:
        print("\nTaste:")
        for axis, data in ts.items():
            parts = []
            pref = [f"{v}(+{s})" for v, s in data.get("preferred", [])]
            avoid = [f"{v}({s})" for v, s in data.get("avoided", [])]
            if pref:
                parts.append(f"like: {', '.join(pref)}")
            if avoid:
                parts.append(f"dislike: {', '.join(avoid)}")
            print(f"  {axis}: {' | '.join(parts)}")


def cmd_catalog(args):
    evo = _require(args.repo)
    html = render_catalog(evo)
    out = _dir(evo.repo_path) / "catalog.html"
    out.write_text(html)
    print(f"Catalog: {out}")


def cmd_lock(args):
    evo = _require(args.repo)
    lock_proposal(evo, args.proposal)
    save(evo)
    p = evo.find(args.proposal)
    print(f"Locked {args.proposal}: {p.dna.as_code()}")


def cmd_taste(args):
    evo = _require(args.repo)
    ts = taste_summary(evo.taste)
    if not ts:
        print("No taste data. Select winners/losers first.")
        return
    print("Taste Profile:")
    for axis, data in ts.items():
        print(f"\n  {axis}:")
        for v, s in data.get("preferred", []):
            print(f"    +{s} {'█' * s} {v}")
        for v, s in data.get("avoided", []):
            print(f"    {s} {'░' * abs(s)} {v}")


def cmd_export(args):
    evo = _require(args.repo)
    data = export_locked(evo)
    out = _dir(evo.repo_path) / "export.json"
    out.write_text(json.dumps(data, indent=2))
    print(json.dumps(data, indent=2))


def cmd_serve(args):
    """Start HTTP server on a project-specific port (hash-based, no collisions)."""
    evo = _require(args.repo)
    base_dir = _dir(evo.repo_path)
    port = _project_port(evo.project)
    import os, signal, subprocess
    # Kill any existing server on this port
    try:
        result = subprocess.run(["lsof", "-ti", f":{port}"], capture_output=True, text=True)
        if result.stdout.strip():
            for pid in result.stdout.strip().split("\n"):
                os.kill(int(pid), signal.SIGTERM)
            import time; time.sleep(0.5)
    except Exception:
        pass
    print(f"Serving {evo.project} at http://localhost:{port}")
    print(f"  Catalog: http://localhost:{port}/catalog.html")
    os.chdir(str(base_dir))
    import http.server, socketserver
    with socketserver.TCPServer(("", port), http.server.SimpleHTTPRequestHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass


def cmd_port(args):
    """Print the project-specific port without starting a server."""
    evo = _require(args.repo)
    port = _project_port(evo.project)
    print(f"{port}")


# ── New v2 commands ──────────────────────────────────────────────────────────

def cmd_detect(args):
    """Show brand state for a repo."""
    detect = _get_detect()
    if not detect:
        print("detect.py not available", file=sys.stderr)
        sys.exit(1)
    state = detect.detect_brand_state(args.repo)
    print(state.summary())
    if args.json:
        print(json.dumps(state.as_dict(), indent=2))


def cmd_memory(args):
    """Memory subcommands: stats, taste, bank, veto, mandate, rules, history, import."""
    mem = _get_memory()
    if not mem:
        print("memory.py not available", file=sys.stderr)
        sys.exit(1)

    sub = args.memory_cmd

    if not sub or sub == "stats":
        s = mem.stats()
        print("Design Memory Stats:")
        for k, v in s.items():
            print(f"  {k}: {v}")

    elif sub == "taste":
        contexts = [c.strip() for c in args.context.split(",")] if getattr(args, "context", None) else None
        print(mem.taste_summary_text(contexts))

    elif sub == "bank":
        search = getattr(args, "search", None)
        if search:
            entries = mem.search_bank(axis_filters={"_query": search}, limit=20)
        else:
            entries = mem.search_bank(limit=20)
        if not entries:
            print("DNA bank is empty.")
            return
        print(f"DNA Bank ({len(entries)} entries):")
        for e in entries:
            tags = ", ".join(e.tags) if e.tags else ""
            note = e.note or ""
            print(f"  {e.dna_code}  [{e.source_status or ''}] "
                  f"from {e.source_project or '?'}"
                  f"{' #' + tags if tags else ''}"
                  f"{' — ' + note if note else ''}")

    elif sub == "veto":
        if not args.axis or not args.value:
            print("Usage: evolve memory veto AXIS VALUE [--reason R] [--context C]")
            return
        ctx = args.context if getattr(args, "context", None) else None
        reason = getattr(args, "reason", None)
        mem.add_hard_preference("veto", args.axis, args.value, context=ctx, reason=reason)
        print(f"Vetoed: {args.axis}={args.value}" + (f" (context: {ctx})" if ctx else ""))

    elif sub == "mandate":
        if not args.axis or not args.value:
            print("Usage: evolve memory mandate AXIS VALUE [--reason R] [--context C]")
            return
        ctx = args.context if getattr(args, "context", None) else None
        reason = getattr(args, "reason", None)
        mem.add_hard_preference("mandate", args.axis, args.value, context=ctx, reason=reason)
        print(f"Mandated: {args.axis}={args.value}" + (f" (context: {ctx})" if ctx else ""))

    elif sub == "rules":
        remove_id = getattr(args, "remove", None)
        if remove_id:
            # Find rule details first, then remove by type/axis/value
            prefs = mem.list_hard_preferences()
            target = next((p for p in prefs if str(p.get("id")) == str(remove_id)), None)
            if target:
                mem.remove_hard_preference(target["type"], target["axis"],
                                            target["value"], target.get("context"))
                print(f"Removed rule {remove_id}")
            else:
                print(f"Rule {remove_id} not found", file=sys.stderr)
            return
        prefs = mem.list_hard_preferences()
        if not prefs:
            print("No hard preferences set.")
            return
        print("Hard Preferences:")
        for p in prefs:
            ctx = f" (context: {p['context']})" if p.get("context") else ""
            reason = f" — {p['reason']}" if p.get("reason") else ""
            print(f"  [{p['id']}] {p['type'].upper()} {p['axis']}={p['value']}{ctx}{reason}")

    elif sub == "history":
        project = getattr(args, "project", None)
        entries = mem.get_feedback_history(project=project, limit=50)
        if not entries:
            print("No feedback history.")
            return
        print(f"Feedback History ({len(entries)} entries):")
        for e in entries:
            print(f"  {e.get('timestamp', '?')[:16]}  {e.get('action', '?'):8s} "
                  f"{e.get('dna_code', '?')}  [{e.get('project', '?')}]")

    elif sub == "import":
        path = args.path
        project = getattr(args, "project", None) or "imported"
        contexts = [c.strip() for c in args.context.split(",")] if getattr(args, "context", None) else []
        count = mem.import_from_evolution_yaml(path, project, contexts)
        print(f"Imported {count} feedback entries from {path}")

    else:
        print(f"Unknown memory command: {sub}")


def cmd_bank(args):
    """Bank a proposal from current generation."""
    evo = _require(args.repo)
    mem = _get_memory()
    if not mem:
        print("memory.py not available", file=sys.stderr)
        sys.exit(1)

    p = evo.find(args.proposal)
    if not p:
        print(f"Proposal {args.proposal} not found", file=sys.stderr)
        sys.exit(1)

    tags = [t.strip() for t in args.tags.split(",")] if getattr(args, "tags", None) else []
    note = getattr(args, "note", None) or ""
    mem.bank_dna(p.dna.as_code(), evo.project, p.status, tags=tags, note=note)
    print(f"Banked {args.proposal}: {p.dna.as_code()}"
          f"{' #' + ','.join(tags) if tags else ''}"
          f"{' — ' + note if note else ''}")


def cmd_recraft(args):
    """Recraft AI image generation commands."""
    rc = _get_recraft()
    if not rc:
        print("recraft.py not available", file=sys.stderr)
        sys.exit(1)

    sub = args.recraft_cmd

    if sub == "logo":
        colors = rc.parse_color_arg(args.colors) if getattr(args, "colors", None) else None
        n = getattr(args, "n", 4) or 4
        images = rc.generate_logo(args.prompt, brand_colors=colors,
                                  substyle=getattr(args, "substyle", None), n=n)
        out = Path(getattr(args, "out", ".") or ".")
        saved = rc.download_and_save(images, out, "logo")
        for s in saved:
            print(f"  Saved: {s}")

    elif sub == "icon":
        colors = rc.parse_color_arg(args.colors) if getattr(args, "colors", None) else None
        n = getattr(args, "n", 4) or 4
        images = rc.generate_icon(args.prompt, brand_colors=colors, n=n)
        out = Path(getattr(args, "out", ".") or ".")
        saved = rc.download_and_save(images, out, "icon")
        for s in saved:
            print(f"  Saved: {s}")

    elif sub == "illustrate":
        colors = rc.parse_color_arg(args.colors) if getattr(args, "colors", None) else None
        n = getattr(args, "n", 4) or 4
        style = getattr(args, "style", "digital_illustration") or "digital_illustration"
        images = rc.generate_illustration(args.prompt, style=style, brand_colors=colors, n=n)
        out = Path(getattr(args, "out", ".") or ".")
        saved = rc.download_and_save(images, out, "illustration")
        for s in saved:
            print(f"  Saved: {s}")

    elif sub == "vectorize":
        url = rc.vectorize(args.image_url)
        print(f"  Vectorized: {url}")

    elif sub == "test":
        print("Testing Recraft API connectivity...")
        try:
            images = rc.generate_logo("simple geometric circle logo", n=1)
            print(f"  Generated {len(images)} image(s)")
            print("  API test passed.")
        except Exception as e:
            print(f"  API test failed: {e}", file=sys.stderr)
            sys.exit(1)

    else:
        print(f"Unknown recraft command: {sub}")


DEFAULT_KEEP_GENS = 3


def _gc_html_previews(repo: str, keep_gens: int = DEFAULT_KEEP_GENS) -> dict:
    """Remove old generation HTML previews, keeping only the latest N.

    Returns dict with cleanup stats.
    """
    base = _dir(repo)
    if not base.exists():
        return {"html_dirs_removed": 0, "bytes_freed": 0}

    # Find all gen-N directories
    gen_dirs = sorted(
        [d for d in base.iterdir() if d.is_dir() and d.name.startswith("gen-")],
        key=lambda d: int(d.name.split("-")[1]) if d.name.split("-")[1].isdigit() else 0,
    )

    if len(gen_dirs) <= keep_gens:
        return {"html_dirs_removed": 0, "bytes_freed": 0}

    to_remove = gen_dirs[:-keep_gens]
    removed = 0
    freed = 0
    import shutil
    for d in to_remove:
        # Sum file sizes before removal
        for f in d.rglob("*"):
            if f.is_file():
                freed += f.stat().st_size
        shutil.rmtree(d)
        removed += 1

    return {"html_dirs_removed": removed, "bytes_freed": freed}


def cmd_gc(args):
    """Garbage collection: prune memory DB + clean old HTML previews."""
    keep = getattr(args, "keep_gens", DEFAULT_KEEP_GENS) or DEFAULT_KEEP_GENS

    # 1. Memory DB maintenance
    mem = _get_memory()
    if mem:
        result = mem.gc()
        print("Memory DB:")
        print(f"  Taste scores clamped to ±{mem.TASTE_SCORE_CAP}")
        if result["bank_pruned"]:
            print(f"  DNA bank pruned: {result['bank_pruned']} entries removed")
        else:
            print(f"  DNA bank: within limit ({mem.MAX_BANK_SIZE})")
        if result["feedback_pruned"]:
            print(f"  Feedback pruned: {result['feedback_pruned']} entries removed")
        else:
            print(f"  Feedback: within limit ({mem.MAX_FEEDBACK_PER_PROJECT}/project)")
        print("  WAL checkpoint: done")
    else:
        print("Memory DB: not available (skipped)")

    # 2. HTML preview cleanup for current repo
    html = _gc_html_previews(args.repo, keep)
    if html["html_dirs_removed"]:
        mb = html["bytes_freed"] / (1024 * 1024)
        print(f"\nHTML previews:")
        print(f"  Removed {html['html_dirs_removed']} old generation(s), freed {mb:.1f}MB")
        print(f"  Keeping last {keep} generation(s)")
    else:
        print(f"\nHTML previews: nothing to clean (≤{keep} generations)")


def _project_port(project_name: str) -> int:
    """Deterministic port from project name. Range 8800-9799 (1000 slots)."""
    h = sum(ord(c) * (i + 1) for i, c in enumerate(project_name))
    return 8800 + (h % 1000)


def main():
    p = argparse.ArgumentParser(prog="evolve", description="Design evolution engine")
    p.add_argument("--repo", default=".", help="Repository root (default: .)")
    sub = p.add_subparsers(dest="cmd")

    s = sub.add_parser("init")
    s.add_argument("--project", required=True)
    s.add_argument("--scope", choices=["full", "component"], default="full")
    s.add_argument("--component")
    s.add_argument("--brand", help="Path to brand.yaml")
    s.add_argument("--lock", help="Comma-separated axes to lock")
    s.add_argument("--contexts", help="Comma-separated context tags (saas, landing, dashboard)")
    s.add_argument("--population", type=int, default=8)
    s.add_argument("--immigration", type=int, default=2)
    s.add_argument("--diversity", type=int, default=3)

    s = sub.add_parser("suggest")
    s.add_argument("--count", type=int)

    s = sub.add_parser("add")
    s.add_argument("dna", nargs="+")
    s.add_argument("--origins")

    s = sub.add_parser("select")
    s.add_argument("--winners")
    s.add_argument("--kill")

    s = sub.add_parser("note")
    s.add_argument("--proposal")
    s.add_argument("--text", required=True)

    sub.add_parser("advance")
    sub.add_parser("status")
    sub.add_parser("catalog")

    s = sub.add_parser("lock")
    s.add_argument("proposal")

    sub.add_parser("taste")
    sub.add_parser("export")
    sub.add_parser("serve")
    sub.add_parser("port")

    # v2: detect
    s = sub.add_parser("detect", help="Auto-detect brand infrastructure")
    s.add_argument("--json", action="store_true", help="Output as JSON")

    # v2: memory
    s = sub.add_parser("memory", help="Design memory management")
    s.add_argument("memory_cmd", nargs="?", default="stats",
                   choices=["stats", "taste", "bank", "veto", "mandate", "rules", "history", "import"])
    s.add_argument("axis", nargs="?", help="Axis name (for veto/mandate)")
    s.add_argument("value", nargs="?", help="Value (for veto/mandate)")
    s.add_argument("--context", help="Context tag")
    s.add_argument("--reason", help="Reason for veto/mandate")
    s.add_argument("--search", help="Search DNA bank")
    s.add_argument("--remove", help="Remove rule by ID")
    s.add_argument("--project", help="Filter by project")
    s.add_argument("--path", help="Path for import command")

    # v2: bank
    s = sub.add_parser("bank", help="Bank a proposal into DNA bank")
    s.add_argument("proposal", help="Proposal ID to bank")
    s.add_argument("--note", help="Note for banked DNA")
    s.add_argument("--tags", help="Comma-separated tags")

    # v2: recraft
    s = sub.add_parser("recraft", help="Recraft AI image generation")
    rsub = s.add_subparsers(dest="recraft_cmd")

    rs = rsub.add_parser("logo", help="Generate vector logos")
    rs.add_argument("prompt", help="Logo description")
    rs.add_argument("--colors", help="Brand colors as hex: '#1a1a2e,#e94560'")
    rs.add_argument("--substyle", help="Vector substyle")
    rs.add_argument("--n", type=int, default=4)
    rs.add_argument("--out", default=".", help="Output directory")

    rs = rsub.add_parser("icon", help="Generate UI icons")
    rs.add_argument("prompt", help="Icon description")
    rs.add_argument("--colors", help="Brand colors as hex")
    rs.add_argument("--n", type=int, default=4)
    rs.add_argument("--out", default=".", help="Output directory")

    rs = rsub.add_parser("illustrate", help="Generate illustrations")
    rs.add_argument("prompt", help="Illustration description")
    rs.add_argument("--style", default="digital_illustration",
                    choices=["digital_illustration", "realistic_image"])
    rs.add_argument("--colors", help="Brand colors as hex")
    rs.add_argument("--n", type=int, default=4)
    rs.add_argument("--out", default=".", help="Output directory")

    rs = rsub.add_parser("vectorize", help="Convert raster to SVG")
    rs.add_argument("image_url", help="URL of image to vectorize")

    rsub.add_parser("test", help="Quick API connectivity test")

    # v2: gc
    s = sub.add_parser("gc", help="Garbage collection: prune DB + clean HTML")
    s.add_argument("--keep-gens", type=int, default=DEFAULT_KEEP_GENS,
                   help=f"Keep last N generations' HTML (default: {DEFAULT_KEEP_GENS})")

    args = p.parse_args()
    if not args.cmd:
        p.print_help()
        sys.exit(1)

    {
        "init": cmd_init, "suggest": cmd_suggest, "add": cmd_add,
        "select": cmd_select, "note": cmd_note, "advance": cmd_advance,
        "status": cmd_status, "catalog": cmd_catalog, "lock": cmd_lock,
        "taste": cmd_taste, "export": cmd_export,
        "serve": cmd_serve, "port": cmd_port,
        "detect": cmd_detect, "memory": cmd_memory,
        "bank": cmd_bank, "recraft": cmd_recraft, "gc": cmd_gc,
    }[args.cmd](args)


if __name__ == "__main__":
    main()
