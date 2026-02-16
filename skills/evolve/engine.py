#!/usr/bin/env python3
"""Design evolution engine — genetic algorithm for design systems.

Deep module: simple CLI, complex internals. State persists in
.design-evolution/evolution.yaml. Phase 2 web app reads/writes
the same format.

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

def save(evo: Evolution):
    d = _dir(evo.repo_path)
    d.mkdir(parents=True, exist_ok=True)
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


def suggest_population(
    count: int, taste: dict, locked_axes: list = None,
    locked_values: dict = None, min_diversity: int = 3, attempts: int = 500,
) -> list:
    """Generate diverse DNA population, weighted by taste."""
    locked_axes = locked_axes or []
    locked_values = locked_values or {}
    pop = []

    for _ in range(attempts):
        if len(pop) >= count:
            break
        genes = {}
        for axis in AXIS_NAMES:
            if axis in locked_values:
                genes[axis] = locked_values[axis]
            elif axis in taste and taste[axis] and random.random() < 0.6:
                # Bias toward preferred values via softmax-ish weighting
                scores = taste[axis]
                options = AXES[axis]
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
                genes[axis] = random.choice(AXES[axis])
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


def select(evo: Evolution, winners: list, killed: list):
    gen = evo.current_gen()
    if not gen:
        raise ValueError("No current generation")
    for p in gen.proposals:
        if p.id in winners:
            p.status = "winner"
            _update_taste(evo.taste, p, +1)
        elif p.id in killed:
            p.status = "killed"
            _update_taste(evo.taste, p, -1)


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


def lock_proposal(evo: Evolution, pid: str):
    p = evo.find(pid)
    if not p:
        raise ValueError(f"Proposal {pid} not found")
    p.status = "locked"
    evo.locked = pid


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


def render_catalog(evo: Evolution) -> str:
    gen = evo.current_gen()
    if not gen:
        return "<html><body><p>No generations yet.</p></body></html>"

    cards = []
    for p in gen.proposals:
        sc = _STATUS_COLORS.get(p.status, "#6b7280")

        notes = ""
        if p.notes:
            items = "".join(f"<li>{n}</li>" for n in p.notes)
            notes = f'<div class="notes"><strong>Notes:</strong><ul>{items}</ul></div>'

        link = ""
        if p.artifacts.get("html"):
            link = f'<a href="{p.artifacts["html"]}" target="_blank" class="link">Open Preview</a>'

        origin = f'<span class="origin">{p.origin}'
        if p.parent:
            origin += f' from {p.parent}'
        origin += '</span>'

        pills = "".join(
            f'<span class="pill" style="border-left:2px solid {_AXIS_COLORS[a]}">'
            f'{getattr(p.dna, a)}</span>'
            for a in AXIS_NAMES
        )

        cards.append(f'''<div class="card {p.status}" data-id="{p.id}">
<div class="hdr"><span class="pid">{p.id}</span>
<span class="badge" style="background:{sc}">{p.status}</span></div>
<div class="dna">{pills}</div>
<div class="code">{p.dna.as_code()}</div>
{origin}{notes}{link}</div>''')

    gen_notes = ""
    if gen.general_notes:
        items = "".join(f"<li>{n}</li>" for n in gen.general_notes)
        gen_notes = f'<div class="section"><h3>General Notes</h3><ul>{items}</ul></div>'

    taste_html = ""
    ts = taste_summary(evo.taste)
    if ts:
        rows = []
        for axis, data in ts.items():
            pref = ", ".join(f"{v} (+{s})" for v, s in data.get("preferred", []))
            avoid = ", ".join(f"{v} ({s})" for v, s in data.get("avoided", []))
            rows.append(f"<tr><td>{axis}</td><td>{pref or '—'}</td><td>{avoid or '—'}</td></tr>")
        taste_html = f'''<div class="section"><h3>Taste Profile</h3>
<table><tr><th>Axis</th><th>Preferred</th><th>Avoided</th></tr>
{"".join(rows)}</table></div>'''

    return f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{evo.project} — Gen {gen.number}</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:"SF Mono","Cascadia Code","Fira Code",monospace;background:#0a0a0a;color:#e5e5e5;padding:2rem}}
h1{{font-size:1.4rem;margin-bottom:.25rem}}
.meta{{color:#737373;font-size:.75rem;margin-bottom:2rem}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:1.5rem}}
.card{{background:#171717;border:1px solid #262626;border-radius:8px;padding:1.25rem;transition:border-color .15s}}
.card:hover{{border-color:#404040}}
.card.winner{{border-color:#22c55e40}}
.card.killed{{opacity:.35}}
.card.locked{{border-color:#f59e0b80;box-shadow:0 0 24px #f59e0b10}}
.hdr{{display:flex;justify-content:space-between;align-items:center;margin-bottom:.75rem}}
.pid{{font-size:1.2rem;font-weight:700}}
.badge{{font-size:.65rem;padding:2px 8px;border-radius:99px;color:#fff;text-transform:uppercase;letter-spacing:.05em}}
.dna{{display:flex;flex-wrap:wrap;gap:.35rem;margin-bottom:.5rem}}
.pill{{font-size:.65rem;padding:2px 8px;background:#262626;border-radius:4px;color:#a3a3a3}}
.code{{font-size:.6rem;color:#525252;margin-bottom:.5rem;word-break:break-all}}
.origin{{font-size:.65rem;color:#525252;display:block;margin-bottom:.5rem}}
.notes{{margin-top:.75rem;padding-top:.75rem;border-top:1px solid #262626;font-size:.8rem}}
.notes ul{{padding-left:1.25rem;color:#a3a3a3}}
.notes li{{margin:.2rem 0}}
.link{{display:block;margin-top:.75rem;color:#3b82f6;text-decoration:none;font-size:.8rem}}
.link:hover{{text-decoration:underline}}
.section{{margin-top:2rem;padding:1.25rem;background:#171717;border:1px solid #262626;border-radius:8px}}
.section h3{{font-size:.85rem;margin-bottom:.75rem}}
.section ul{{padding-left:1.25rem;color:#a3a3a3;font-size:.8rem}}
.section li{{margin:.2rem 0}}
table{{width:100%;font-size:.75rem;border-collapse:collapse}}
th,td{{text-align:left;padding:.5rem;border-bottom:1px solid #262626}}
th{{color:#737373;font-weight:500}}
</style></head>
<body>
<h1>{evo.project}</h1>
<div class="meta">Generation {gen.number} · {len(gen.proposals)} proposals · \
scope: {evo.config.scope} · brand: {"adherent" if evo.config.brand_adherent else "free"} · \
{gen.timestamp[:10] if gen.timestamp else ""}</div>
<div class="grid">{"".join(cards)}</div>
{gen_notes}{taste_html}
</body></html>'''


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
    save(evo)
    print(f"Initialized: {_file(args.repo)}")
    print(f"  scope={cfg.scope} brand={cfg.brand_adherent} pop={cfg.population_size}")


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
    save(evo)
    print(f"Generation {gen.number}: {len(gen.proposals)} proposals")
    for p in gen.proposals:
        print(f"  {p.id}: {p.dna.as_code()}")


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

    args = p.parse_args()
    if not args.cmd:
        p.print_help()
        sys.exit(1)

    {
        "init": cmd_init, "suggest": cmd_suggest, "add": cmd_add,
        "select": cmd_select, "note": cmd_note, "advance": cmd_advance,
        "status": cmd_status, "catalog": cmd_catalog, "lock": cmd_lock,
        "taste": cmd_taste, "export": cmd_export,
    }[args.cmd](args)


if __name__ == "__main__":
    main()
