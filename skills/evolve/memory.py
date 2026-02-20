#!/usr/bin/env python3
"""Design memory — persistent cross-project taste and DNA bank.

SQLite database at ~/.claude/design-memory.db. Auto-created on first access.
All functions are safe to call when DB doesn't exist yet (auto-initializes).

Standalone test: python3 memory.py
"""

import json
import sqlite3
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

DB_PATH = Path.home() / ".claude" / "design-memory.db"

SCHEMA_VERSION = 2

_SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS schema_version (
    version INTEGER PRIMARY KEY,
    applied_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))
);

CREATE TABLE IF NOT EXISTS taste (
    axis    TEXT NOT NULL,
    value   TEXT NOT NULL,
    score   INTEGER NOT NULL DEFAULT 0,
    updated_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
    PRIMARY KEY (axis, value)
);

CREATE TABLE IF NOT EXISTS contextual_taste (
    context TEXT NOT NULL,
    axis    TEXT NOT NULL,
    value   TEXT NOT NULL,
    score   INTEGER NOT NULL DEFAULT 0,
    updated_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
    PRIMARY KEY (context, axis, value)
);

CREATE TABLE IF NOT EXISTS hard_preferences (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    type    TEXT NOT NULL CHECK (type IN ('veto', 'mandate')),
    axis    TEXT NOT NULL,
    value   TEXT NOT NULL,
    context TEXT,
    reason  TEXT,
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
    UNIQUE (type, axis, value, context)
);

CREATE TABLE IF NOT EXISTS dna_bank (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    dna_code        TEXT NOT NULL,
    layout          TEXT NOT NULL,
    color           TEXT NOT NULL,
    typography      TEXT NOT NULL,
    motion          TEXT NOT NULL,
    density         TEXT NOT NULL,
    background      TEXT NOT NULL,
    source_project  TEXT,
    source_proposal TEXT,
    source_status   TEXT,
    tags            TEXT NOT NULL DEFAULT '[]',
    note            TEXT,
    banked_at       TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
    UNIQUE (dna_code)
);

CREATE TABLE IF NOT EXISTS projects (
    project     TEXT PRIMARY KEY,
    repo_path   TEXT NOT NULL,
    scope       TEXT NOT NULL DEFAULT 'full',
    contexts    TEXT NOT NULL DEFAULT '[]',
    brand_state TEXT NOT NULL DEFAULT '{}',
    generations INTEGER NOT NULL DEFAULT 0,
    proposals_evaluated INTEGER NOT NULL DEFAULT 0,
    locked_dna  TEXT,
    first_run   TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
    last_run    TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))
);

CREATE TABLE IF NOT EXISTS feedback_log (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    project     TEXT NOT NULL,
    generation  INTEGER NOT NULL,
    proposal_id TEXT NOT NULL,
    dna_code    TEXT NOT NULL,
    action      TEXT NOT NULL CHECK (action IN ('winner', 'killed', 'banked', 'noted', 'locked')),
    note        TEXT,
    contexts    TEXT NOT NULL DEFAULT '[]',
    timestamp   TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))
);

CREATE INDEX IF NOT EXISTS idx_feedback_timestamp ON feedback_log(timestamp);
CREATE INDEX IF NOT EXISTS idx_feedback_project ON feedback_log(project);
"""

# DNA axis names — must match engine.py AXIS_NAMES
_AXIS_NAMES = ["layout", "color", "typography", "motion", "density", "background"]


# ── Connection ───────────────────────────────────────────────────────────────

_conn_cache = None
_schema_done = False


def _migrate_v1_to_v2(conn: sqlite3.Connection):
    """Allow 'locked' in feedback action CHECK constraint."""
    row = conn.execute(
        "SELECT sql FROM sqlite_master WHERE type='table' AND name='feedback_log'"
    ).fetchone()
    if not row:
        return
    sql = (row["sql"] or "").lower()
    if "'locked'" in sql:
        return

    conn.executescript(
        """
        CREATE TABLE feedback_log_new (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            project     TEXT NOT NULL,
            generation  INTEGER NOT NULL,
            proposal_id TEXT NOT NULL,
            dna_code    TEXT NOT NULL,
            action      TEXT NOT NULL CHECK (action IN ('winner', 'killed', 'banked', 'noted', 'locked')),
            note        TEXT,
            contexts    TEXT NOT NULL DEFAULT '[]',
            timestamp   TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))
        );
        INSERT INTO feedback_log_new (id, project, generation, proposal_id, dna_code, action, note, contexts, timestamp)
        SELECT id, project, generation, proposal_id, dna_code, action, note, contexts, timestamp
        FROM feedback_log;
        DROP TABLE feedback_log;
        ALTER TABLE feedback_log_new RENAME TO feedback_log;
        CREATE INDEX IF NOT EXISTS idx_feedback_timestamp ON feedback_log(timestamp);
        CREATE INDEX IF NOT EXISTS idx_feedback_project ON feedback_log(project);
        """
    )
    conn.execute("INSERT INTO schema_version (version) VALUES (?)", (2,))

def _connect() -> sqlite3.Connection:
    """Open DB, create schema if needed. Uses WAL for concurrent access.

    Caches connection for the process lifetime. Schema check runs once.
    """
    global _conn_cache, _schema_done
    if _conn_cache is not None:
        try:
            _conn_cache.execute("SELECT 1")
            return _conn_cache
        except Exception:
            _conn_cache = None

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH), timeout=5)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.row_factory = sqlite3.Row

    if not _schema_done:
        conn.executescript(_SCHEMA_SQL)
        cur = conn.execute("SELECT version FROM schema_version ORDER BY version DESC LIMIT 1")
        row = cur.fetchone()
        if not row:
            conn.execute("INSERT INTO schema_version (version) VALUES (?)", (SCHEMA_VERSION,))
        elif row["version"] < 2:
            _migrate_v1_to_v2(conn)
        conn.commit()
        _schema_done = True

    _conn_cache = conn
    return conn


# ── Taste ────────────────────────────────────────────────────────────────────

def update_taste(axis: str, value: str, delta: int,
                 contexts: list = None):
    """Increment global taste score. Also updates contextual_taste for each context."""
    conn = _connect()
    now = datetime.now(timezone.utc).isoformat()
    cap = TASTE_SCORE_CAP
    clamped = max(-cap, min(cap, delta))
    conn.execute(
        "INSERT INTO taste (axis, value, score, updated_at) VALUES (?, ?, ?, ?) "
        "ON CONFLICT(axis, value) DO UPDATE SET "
        "score = MAX(-?, MIN(?, score + ?)), updated_at = ?",
        (axis, value, clamped, now, cap, cap, delta, now),
    )
    for ctx in (contexts or []):
        conn.execute(
            "INSERT INTO contextual_taste (context, axis, value, score, updated_at) "
            "VALUES (?, ?, ?, ?, ?) "
            "ON CONFLICT(context, axis, value) DO UPDATE SET "
            "score = MAX(-?, MIN(?, score + ?)), updated_at = ?",
            (ctx, axis, value, clamped, now, cap, cap, delta, now),
        )
    conn.commit()



def update_taste_from_dna(dna_code: str, delta: int, contexts: list = None):
    """Update taste for all axes of a DNA code string (dot-separated)."""
    parts = dna_code.split(".")
    if len(parts) != len(_AXIS_NAMES):
        return
    for axis, value in zip(_AXIS_NAMES, parts):
        update_taste(axis, value, delta, contexts)


def get_merged_taste(contexts: list = None) -> dict:
    """Return taste dict compatible with engine's suggest_population(taste=...).

    Merge: global scores + contextual (1.5x weight) + hard preferences (-999/+999).
    """
    conn = _connect()
    result = {}

    # 1. Global taste
    for row in conn.execute("SELECT axis, value, score FROM taste WHERE score != 0"):
        result.setdefault(row["axis"], {})[row["value"]] = row["score"]

    # 2. Contextual overlay (1.5x weight)
    if contexts:
        ph = ",".join("?" * len(contexts))
        for row in conn.execute(
            f"SELECT axis, value, SUM(score) as total FROM contextual_taste "
            f"WHERE context IN ({ph}) GROUP BY axis, value",
            contexts,
        ):
            result.setdefault(row["axis"], {})
            result[row["axis"]][row["value"]] = (
                result[row["axis"]].get(row["value"], 0) + int(row["total"] * 1.5)
            )

    # 3. Hard preferences — absolute override
    for row in conn.execute(
        "SELECT type, axis, value, context FROM hard_preferences"
    ):
        # Apply if global (context IS NULL) or matching context
        if row["context"] is None or (contexts and row["context"] in contexts):
            result.setdefault(row["axis"], {})
            if row["type"] == "veto":
                result[row["axis"]][row["value"]] = -999
            elif row["type"] == "mandate":
                result[row["axis"]][row["value"]] = 999


    return result


def get_vetoed_values(contexts: list = None) -> dict:
    """Return {axis: [vetoed_values]}."""
    conn = _connect()
    result = {}
    for row in conn.execute(
        "SELECT axis, value, context FROM hard_preferences WHERE type = 'veto'"
    ):
        if row["context"] is None or (contexts and row["context"] in contexts):
            result.setdefault(row["axis"], []).append(row["value"])

    return result


def get_mandated_values(contexts: list = None) -> dict:
    """Return {axis: [mandated_values]}."""
    conn = _connect()
    result = {}
    for row in conn.execute(
        "SELECT axis, value, context FROM hard_preferences WHERE type = 'mandate'"
    ):
        if row["context"] is None or (contexts and row["context"] in contexts):
            result.setdefault(row["axis"], []).append(row["value"])

    return result


# ── Hard Preferences ─────────────────────────────────────────────────────────

def add_hard_preference(pref_type: str, axis: str, value: str,
                        context: str = None, reason: str = None):
    """Add a veto or mandate. Idempotent (upserts reason if exists)."""
    conn = _connect()
    conn.execute(
        "INSERT INTO hard_preferences (type, axis, value, context, reason) "
        "VALUES (?, ?, ?, ?, ?) "
        "ON CONFLICT(type, axis, value, context) DO UPDATE SET reason = ?",
        (pref_type, axis, value, context, reason, reason),
    )
    conn.commit()



def remove_hard_preference(pref_type: str = None, axis: str = None,
                           value: str = None, context: str = None,
                           pref_id: int = None):
    """Remove hard preference by ID or by (type, axis, value, context)."""
    conn = _connect()
    if pref_id is not None:
        conn.execute("DELETE FROM hard_preferences WHERE id = ?", (pref_id,))
    else:
        conn.execute(
            "DELETE FROM hard_preferences WHERE type = ? AND axis = ? AND value = ? "
            "AND context IS ?",
            (pref_type, axis, value, context),
        )
    conn.commit()



def list_hard_preferences(context: str = None) -> list:
    """List all hard preferences, optionally filtered by context."""
    conn = _connect()
    if context:
        rows = conn.execute(
            "SELECT * FROM hard_preferences WHERE context IS NULL OR context = ? "
            "ORDER BY created_at",
            (context,),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM hard_preferences ORDER BY created_at"
        ).fetchall()

    return [dict(r) for r in rows]


# ── DNA Bank ─────────────────────────────────────────────────────────────────

@dataclass
class BankedDNA:
    id: int
    dna_code: str
    axes: dict
    source_project: Optional[str]
    source_proposal: Optional[str]
    source_status: Optional[str]
    tags: list
    note: Optional[str]
    banked_at: str


def bank_dna(dna_code: str, source_project: str = None,
             source_proposal: str = None, source_status: str = None,
             tags: list = None, note: str = None) -> Optional[int]:
    """Save a DNA to the bank. Returns row id. Skips exact duplicates."""
    parts = dna_code.split(".")
    if len(parts) != len(_AXIS_NAMES):
        return None
    axes = dict(zip(_AXIS_NAMES, parts))
    conn = _connect()
    try:
        cur = conn.execute(
            "INSERT INTO dna_bank (dna_code, layout, color, typography, motion, "
            "density, background, source_project, source_proposal, source_status, tags, note) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (dna_code, *parts, source_project, source_proposal, source_status,
             json.dumps(tags or []), note),
        )
        conn.commit()
        row_id = cur.lastrowid
    except sqlite3.IntegrityError:
        # Duplicate — update note/tags if provided
        if note or tags:
            conn.execute(
                "UPDATE dna_bank SET note = COALESCE(?, note), "
                "tags = COALESCE(?, tags) WHERE dna_code = ?",
                (note, json.dumps(tags) if tags else None, dna_code),
            )
            conn.commit()
        row_id = None

    return row_id


def search_bank(axis_filters: dict = None, tags: list = None,
                project: str = None, limit: int = 20) -> list:
    """Search the DNA bank. Returns list of BankedDNA."""
    conn = _connect()
    clauses = []
    params = []

    if axis_filters:
        for axis, value in axis_filters.items():
            if axis in _AXIS_NAMES:
                clauses.append(f"{axis} = ?")
                params.append(value)

    if project:
        clauses.append("source_project = ?")
        params.append(project)

    if tags:
        # Match any tag via JSON
        tag_clauses = []
        for tag in tags:
            tag_clauses.append("tags LIKE ?")
            params.append(f'%"{tag}"%')
        clauses.append(f"({' OR '.join(tag_clauses)})")

    where = f" WHERE {' AND '.join(clauses)}" if clauses else ""
    params.append(limit)

    rows = conn.execute(
        f"SELECT * FROM dna_bank{where} ORDER BY banked_at DESC LIMIT ?",
        params,
    ).fetchall()


    result = []
    for r in rows:
        result.append(BankedDNA(
            id=r["id"], dna_code=r["dna_code"],
            axes={a: r[a] for a in _AXIS_NAMES},
            source_project=r["source_project"],
            source_proposal=r["source_proposal"],
            source_status=r["source_status"],
            tags=json.loads(r["tags"]) if r["tags"] else [],
            note=r["note"], banked_at=r["banked_at"],
        ))
    return result


def remove_from_bank(dna_code: str):
    """Remove a design from the bank."""
    conn = _connect()
    conn.execute("DELETE FROM dna_bank WHERE dna_code = ?", (dna_code,))
    conn.commit()



# ── Project History ──────────────────────────────────────────────────────────

def record_project(project: str, repo_path: str, scope: str = "full",
                   contexts: list = None, brand_state: dict = None):
    """Upsert a project record."""
    conn = _connect()
    now = datetime.now(timezone.utc).isoformat()
    conn.execute(
        "INSERT INTO projects (project, repo_path, scope, contexts, brand_state, first_run, last_run) "
        "VALUES (?, ?, ?, ?, ?, ?, ?) "
        "ON CONFLICT(project) DO UPDATE SET "
        "last_run = ?, contexts = COALESCE(?, contexts), brand_state = COALESCE(?, brand_state)",
        (project, repo_path, scope,
         json.dumps(contexts or []), json.dumps(brand_state or {}),
         now, now,
         now, json.dumps(contexts) if contexts else None,
         json.dumps(brand_state) if brand_state else None),
    )
    conn.commit()



def update_project_stats(project: str, generations: int = None,
                         proposals_evaluated: int = None,
                         locked_dna: str = None):
    """Update stats after generation completes."""
    conn = _connect()
    now = datetime.now(timezone.utc).isoformat()
    sets = ["last_run = ?"]
    params = [now]
    if generations is not None:
        sets.append("generations = ?")
        params.append(generations)
    if proposals_evaluated is not None:
        sets.append("proposals_evaluated = ?")
        params.append(proposals_evaluated)
    if locked_dna is not None:
        sets.append("locked_dna = ?")
        params.append(locked_dna)
    params.append(project)
    conn.execute(f"UPDATE projects SET {', '.join(sets)} WHERE project = ?", params)
    conn.commit()



def get_project(project: str) -> Optional[dict]:
    """Get project record."""
    conn = _connect()
    row = conn.execute(
        "SELECT * FROM projects WHERE project = ?", (project,)
    ).fetchone()

    return dict(row) if row else None


def list_projects() -> list:
    """List all known projects."""
    conn = _connect()
    rows = conn.execute(
        "SELECT * FROM projects ORDER BY last_run DESC"
    ).fetchall()

    return [dict(r) for r in rows]


# ── Feedback Log ─────────────────────────────────────────────────────────────

def log_feedback(project: str, generation: int, proposal_id: str,
                 dna_code: str, action: str, note: str = None,
                 contexts: list = None):
    """Append to the immutable feedback log."""
    conn = _connect()
    conn.execute(
        "INSERT INTO feedback_log (project, generation, proposal_id, dna_code, "
        "action, note, contexts) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (project, generation, proposal_id, dna_code, action, note,
         json.dumps(contexts or [])),
    )
    conn.commit()



def get_feedback_history(project: str = None, limit: int = 50) -> list:
    """Query feedback log."""
    conn = _connect()
    if project:
        rows = conn.execute(
            "SELECT * FROM feedback_log WHERE project = ? ORDER BY timestamp DESC LIMIT ?",
            (project, limit),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM feedback_log ORDER BY timestamp DESC LIMIT ?",
            (limit,),
        ).fetchall()

    return [dict(r) for r in rows]


# ── Migration ────────────────────────────────────────────────────────────────

def import_from_evolution_yaml(yaml_path: str, project: str = None,
                               contexts: list = None):
    """Bootstrap memory from an existing evolution.yaml.

    Imports taste, logs feedback, banks winners/locked, records project.
    """
    path = Path(yaml_path)
    if not path.exists():
        raise FileNotFoundError(yaml_path)

    text = path.read_text()
    try:
        import yaml as _yaml
        data = _yaml.safe_load(text)
    except ImportError:
        data = json.loads(text)

    if not data:
        return

    proj_name = project or data.get("project", path.parent.parent.name)
    repo_path = data.get("repo_path", str(path.parent.parent))
    scope = data.get("config", {}).get("scope", "full")

    # Record project
    record_project(proj_name, repo_path, scope, contexts)

    # Import taste scores
    taste = data.get("taste", {})
    for axis, values in taste.items():
        if not isinstance(values, dict):
            continue
        for value, score in values.items():
            if score != 0:
                update_taste(axis, value, score, contexts)

    # Walk all proposals
    generations = data.get("generations", [])
    total_proposals = 0
    for gen in generations:
        gen_num = gen.get("number", 0)
        for p in gen.get("proposals", []):
            total_proposals += 1
            pid = p.get("id", "")
            dna = p.get("dna", {})
            status = p.get("status", "alive")

            # Build DNA code from dict
            parts = [dna.get(a, "") for a in _AXIS_NAMES]
            dna_code = ".".join(parts)

            if status in ("winner", "killed"):
                log_feedback(proj_name, gen_num, pid, dna_code,
                             status, contexts=contexts)

            if status in ("winner", "locked"):
                bank_dna(dna_code, source_project=proj_name,
                         source_proposal=pid, source_status=status,
                         tags=["imported", status])

    # Update stats
    locked = data.get("locked")
    locked_dna = None
    if locked:
        for gen in generations:
            for p in gen.get("proposals", []):
                if p.get("id") == locked:
                    parts = [p.get("dna", {}).get(a, "") for a in _AXIS_NAMES]
                    locked_dna = ".".join(parts)
                    break

    update_project_stats(proj_name, generations=len(generations),
                         proposals_evaluated=total_proposals,
                         locked_dna=locked_dna)

    return {
        "project": proj_name,
        "generations": len(generations),
        "proposals": total_proposals,
        "taste_axes": len(taste),
    }


# ── Diagnostics ──────────────────────────────────────────────────────────────

def stats() -> dict:
    """Aggregate stats."""
    conn = _connect()
    result = {
        "projects": conn.execute("SELECT COUNT(*) FROM projects").fetchone()[0],
        "designs_banked": conn.execute("SELECT COUNT(*) FROM dna_bank").fetchone()[0],
        "feedback_events": conn.execute("SELECT COUNT(*) FROM feedback_log").fetchone()[0],
        "hard_preferences": conn.execute("SELECT COUNT(*) FROM hard_preferences").fetchone()[0],
        "taste_entries": conn.execute("SELECT COUNT(*) FROM taste WHERE score != 0").fetchone()[0],
    }

    return result


def taste_summary_text(contexts: list = None) -> str:
    """Human-readable taste summary."""
    taste = get_merged_taste(contexts)
    if not taste:
        return "No taste data in memory."

    lines = ["Global Design Memory — Taste Profile:"]
    if contexts:
        lines[0] += f" (contexts: {', '.join(contexts)})"

    for axis in _AXIS_NAMES:
        vals = taste.get(axis, {})
        if not vals:
            continue
        ranked = sorted(vals.items(), key=lambda x: x[1], reverse=True)
        preferred = [(v, s) for v, s in ranked if s > 0 and s != 999]
        mandated = [(v, s) for v, s in ranked if s == 999]
        vetoed = [(v, s) for v, s in ranked if s == -999]
        avoided = [(v, s) for v, s in ranked if s < 0 and s != -999]

        parts = []
        if mandated:
            parts.append("MUST: " + ", ".join(v for v, _ in mandated))
        if preferred:
            parts.append("like: " + ", ".join(f"{v}(+{s})" for v, s in preferred))
        if avoided:
            parts.append("dislike: " + ", ".join(f"{v}({s})" for v, s in avoided))
        if vetoed:
            parts.append("NEVER: " + ", ".join(v for v, _ in vetoed))

        if parts:
            lines.append(f"  {axis}: {' | '.join(parts)}")

    return "\n".join(lines)


# ── Maintenance ─────────────────────────────────────────────────────────────

MAX_BANK_SIZE = 200
MAX_FEEDBACK_PER_PROJECT = 500
TASTE_SCORE_CAP = 20


def decay_taste(factor: float = 0.8):
    """Decay all taste scores toward zero. Prevents runaway accumulation.

    Call periodically (e.g., every N projects or on `evolve gc`).
    Scores are rounded — values that decay to 0 are deleted.
    """
    conn = _connect()
    for table in ("taste", "contextual_taste"):
        conn.execute(f"UPDATE {table} SET score = CAST(score * ? AS INTEGER)", (factor,))
        conn.execute(f"DELETE FROM {table} WHERE score = 0")
    conn.commit()


def clamp_taste():
    """Clamp all scores to [-TASTE_SCORE_CAP, +TASTE_SCORE_CAP].

    Prevents indefinite accumulation. Called automatically during gc().
    """
    conn = _connect()
    cap = TASTE_SCORE_CAP
    for table in ("taste", "contextual_taste"):
        conn.execute(
            f"UPDATE {table} SET score = {cap} WHERE score > {cap}")
        conn.execute(
            f"UPDATE {table} SET score = -{cap} WHERE score < -{cap}")
    conn.commit()


def prune_bank(max_size: int = MAX_BANK_SIZE):
    """Keep only the most recent max_size entries in the DNA bank.

    Locked designs are never pruned.
    """
    conn = _connect()
    count = conn.execute("SELECT COUNT(*) FROM dna_bank").fetchone()[0]
    if count <= max_size:
        return 0
    excess = count - max_size
    # Delete oldest non-locked entries
    conn.execute(
        "DELETE FROM dna_bank WHERE id IN ("
        "  SELECT id FROM dna_bank WHERE source_status != 'locked' "
        "  ORDER BY banked_at ASC LIMIT ?"
        ")", (excess,))
    conn.commit()
    return excess


def prune_feedback(max_per_project: int = MAX_FEEDBACK_PER_PROJECT):
    """Keep only recent feedback per project. Oldest entries are deleted."""
    conn = _connect()
    projects = conn.execute(
        "SELECT DISTINCT project FROM feedback_log"
    ).fetchall()
    pruned = 0
    for row in projects:
        proj = row[0]
        count = conn.execute(
            "SELECT COUNT(*) FROM feedback_log WHERE project = ?", (proj,)
        ).fetchone()[0]
        if count > max_per_project:
            excess = count - max_per_project
            conn.execute(
                "DELETE FROM feedback_log WHERE id IN ("
                "  SELECT id FROM feedback_log WHERE project = ? "
                "  ORDER BY timestamp ASC LIMIT ?"
                ")", (proj, excess))
            pruned += excess
    conn.commit()
    return pruned


def gc():
    """Full garbage collection: clamp taste, prune bank, prune feedback, vacuum.

    Safe to run anytime. Idempotent.
    """
    clamp_taste()
    bank_pruned = prune_bank()
    feedback_pruned = prune_feedback()
    conn = _connect()
    conn.execute("PRAGMA wal_checkpoint(TRUNCATE)")
    # VACUUM needs to run outside WAL transaction
    # We'll just do the checkpoint which reclaims WAL space
    conn.commit()
    return {
        "taste_clamped": True,
        "bank_pruned": bank_pruned,
        "feedback_pruned": feedback_pruned,
    }


# ── Self-test ────────────────────────────────────────────────────────────────

def _self_test():
    """Quick smoke test. Creates test DB, exercises all functions."""
    global DB_PATH
    import tempfile
    DB_PATH = Path(tempfile.mkdtemp()) / "test-memory.db"
    print(f"Test DB: {DB_PATH}")

    # Stats on empty DB
    s = stats()
    assert s["projects"] == 0
    assert s["designs_banked"] == 0
    print(f"  Empty stats: OK")

    # Taste
    update_taste("color", "dark", +2, contexts=["saas"])
    update_taste("color", "light", -1)
    update_taste("typography", "editorial", +3, contexts=["saas", "landing"])
    taste = get_merged_taste()
    assert taste["color"]["dark"] == 2
    assert taste["color"]["light"] == -1
    print(f"  Global taste: OK")

    taste_ctx = get_merged_taste(contexts=["saas"])
    assert taste_ctx["color"]["dark"] > taste["color"]["dark"]  # 1.5x contextual
    print(f"  Contextual taste: OK")

    # Hard preferences
    add_hard_preference("veto", "typography", "minimal", reason="boring")
    add_hard_preference("mandate", "color", "brand-tinted", context="saas")
    prefs = list_hard_preferences()
    assert len(prefs) == 2
    vetoed = get_vetoed_values()
    assert "minimal" in vetoed.get("typography", [])
    print(f"  Hard preferences: OK")

    taste_hp = get_merged_taste()
    assert taste_hp["typography"]["minimal"] == -999
    print(f"  Veto in merged taste: OK")

    taste_ctx_hp = get_merged_taste(contexts=["saas"])
    assert taste_ctx_hp["color"]["brand-tinted"] == 999
    print(f"  Context mandate in merged taste: OK")

    # DNA bank
    bank_dna("editorial.dark.display-heavy.orchestrated.spacious.textured",
             source_project="test", source_proposal="1a", source_status="winner",
             tags=["favorite"], note="great vibes")
    bank_dna("bento.light.expressive.subtle.compact.layered",
             source_project="test", source_proposal="1b", source_status="winner")
    results = search_bank()
    assert len(results) == 2
    results = search_bank(axis_filters={"layout": "editorial"})
    assert len(results) == 1
    assert results[0].note == "great vibes"
    results = search_bank(tags=["favorite"])
    assert len(results) == 1
    print(f"  DNA bank: OK")

    # Project history
    record_project("test-proj", "/tmp/test", "full", contexts=["saas"])
    proj = get_project("test-proj")
    assert proj["project"] == "test-proj"
    print(f"  Project history: OK")

    # Feedback log
    log_feedback("test-proj", 1, "1a", "editorial.dark.display-heavy.orchestrated.spacious.textured",
                 "winner", contexts=["saas"])
    log_feedback("test-proj", 1, "1b", "bento.light.expressive.subtle.compact.layered",
                 "killed")
    history = get_feedback_history(project="test-proj")
    assert len(history) == 2
    print(f"  Feedback log: OK")

    # Remove hard preference
    remove_hard_preference(pref_id=prefs[0]["id"])
    assert len(list_hard_preferences()) == 1
    print(f"  Remove preference: OK")

    # Stats
    s = stats()
    assert s["projects"] == 1
    assert s["designs_banked"] == 2
    assert s["feedback_events"] == 2
    assert s["hard_preferences"] == 1
    print(f"  Final stats: {s}")

    # Summary text
    print(f"\n{taste_summary_text(contexts=['saas'])}")

    print(f"\nAll tests passed.")

    # Cleanup
    import shutil
    shutil.rmtree(DB_PATH.parent, ignore_errors=True)


if __name__ == "__main__":
    if "--test" in sys.argv:
        _self_test()
    else:
        # Show stats for real DB
        print(f"Design Memory: {DB_PATH}")
        s = stats()
        for k, v in s.items():
            print(f"  {k}: {v}")
        print()
        print(taste_summary_text())
