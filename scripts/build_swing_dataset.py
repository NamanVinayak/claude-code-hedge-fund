#!/usr/bin/env python3
"""
Merge all swing-mode trade predictions from three sources into one dataset:
  1. scripts/routine_raw_results_v2.json   (cloud routine runs, Apr 17-27)
  2. runs/*/decisions.json filtered to mode=swing (local runs, mostly pre-Apr 17)
  3. tracker/swing_predictions.json        (hand-curated)

Dedupe key: (rec_date, ticker, direction)
Priority on conflict: routine_v2 > local_run > manual_predictions
Conflicts logged to scripts/build_swing_dataset.log.

Output: scripts/all_swing_predictions.json
"""

import json
import glob
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
OUT = SCRIPTS / "all_swing_predictions.json"
LOG = SCRIPTS / "build_swing_dataset.log"

CRYPTO_RE = re.compile(r"-(USD|USDT)$")


def is_crypto_ticker(ticker: str) -> bool:
    return bool(CRYPTO_RE.search(ticker.upper()))


def normalize_action(action: str | None) -> str | None:
    if not action:
        return None
    a = action.lower()
    if a in ("buy", "long", "cover"):
        return "long"
    if a in ("sell", "short"):
        return "short"
    return None  # hold / neutral / no_trade / unknown


def to_float(v) -> float | None:
    if v is None or v == "":
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def get_first(d: dict, *keys, default=None):
    for k in keys:
        if k in d and d[k] not in (None, ""):
            return d[k]
    return default


def normalize_prediction(*, source: str, source_id: str, rec_dt_utc: str, rec_date: str,
                         ticker: str, decision: dict, is_crypto: bool | None = None,
                         status_detail: str = "") -> dict | None:
    direction = normalize_action(decision.get("action") or decision.get("direction"))
    if direction is None:
        return None  # skip holds

    entry = to_float(get_first(decision, "entry", "entry_price"))
    target = to_float(get_first(decision, "target", "target_price", "target_1"))
    if target is None and isinstance(decision.get("targets"), list) and decision["targets"]:
        target = to_float(decision["targets"][0])
    stop = to_float(get_first(decision, "stop", "stop_loss"))

    if not (entry and target and stop):
        return None
    if entry <= 0:
        return None

    if is_crypto is None:
        is_crypto = is_crypto_ticker(ticker)

    return {
        "source": source,
        "source_id": source_id,
        "rec_date": rec_date,
        "rec_time_utc": rec_dt_utc,
        "ticker": ticker,
        "direction": direction,
        "entry": entry,
        "target": target,
        "stop": stop,
        "confidence": decision.get("confidence"),
        "timeframe": decision.get("timeframe", ""),
        "is_crypto": bool(is_crypto),
        "status_detail": status_detail,
    }


def load_routine_v2() -> list[dict]:
    path = SCRIPTS / "routine_raw_results_v2.json"
    data = json.loads(path.read_text())
    out = []
    for run in data["runs"]:
        if not run.get("decisions"):
            continue
        rec_dt = run["created_at"]
        rec_date = rec_dt[:10]
        is_crypto = "Crypto" in run["batch"]
        for ticker, decision in run["decisions"].items():
            rec = normalize_prediction(
                source="routine_v2",
                source_id=f"{run['batch']}::{run['session_id']}",
                rec_dt_utc=rec_dt,
                rec_date=rec_date,
                ticker=ticker,
                decision=decision,
                is_crypto=is_crypto,
                status_detail=run.get("status_detail", ""),
            )
            if rec:
                out.append(rec)
    return out


def parse_run_id_to_dt(run_id: str) -> str | None:
    """`20260424_183538` -> `2026-04-24T18:35:38Z`"""
    m = re.match(r"(\d{4})(\d{2})(\d{2})_(\d{2})(\d{2})(\d{2})$", run_id)
    if not m:
        return None
    y, mo, d, h, mi, s = m.groups()
    return f"{y}-{mo}-{d}T{h}:{mi}:{s}Z"


def load_local_runs() -> list[dict]:
    out = []
    for md_path in sorted(glob.glob(str(ROOT / "runs/*/metadata.json"))):
        md = json.loads(Path(md_path).read_text())
        if md.get("mode") != "swing":
            continue
        run_dir = os.path.dirname(md_path)
        run_name = os.path.basename(run_dir)
        if run_name.startswith(("test", "smoke", "news_check")):
            continue
        dec_path = os.path.join(run_dir, "decisions.json")
        if not os.path.exists(dec_path):
            continue

        # extract timestamp portion (handles both "20260409_030346" and "swing_20260411_211655")
        ts = run_name.split("_", 1)[-1] if run_name.startswith("swing_") else run_name
        rec_dt = parse_run_id_to_dt(ts) or md.get("date") or ""
        rec_date = rec_dt[:10] if rec_dt else (md.get("date", "")[:10])

        is_crypto_run = (md.get("asset_type") == "crypto")
        decisions = json.loads(Path(dec_path).read_text()).get("decisions", {})
        for ticker, decision in decisions.items():
            rec = normalize_prediction(
                source="local_run",
                source_id=run_name,
                rec_dt_utc=rec_dt,
                rec_date=rec_date,
                ticker=ticker,
                decision=decision,
                is_crypto=is_crypto_run or is_crypto_ticker(ticker),
            )
            if rec:
                out.append(rec)
    return out


def load_manual() -> list[dict]:
    path = ROOT / "tracker" / "swing_predictions.json"
    data = json.loads(path.read_text())
    out = []
    for entry in data:
        decision = {
            "action": entry["direction"],
            "entry": entry["entry"],
            "target": entry["target"],
            "stop": entry["stop"],
            "confidence": entry.get("confidence"),
        }
        rec = normalize_prediction(
            source="manual_predictions",
            source_id=entry.get("run_id", "manual"),
            rec_dt_utc=f"{entry['start_date']}T00:00:00Z",
            rec_date=entry["start_date"],
            ticker=entry["ticker"],
            decision=decision,
            is_crypto=entry.get("is_crypto"),
        )
        if rec:
            out.append(rec)
    return out


def merge_with_priority(*sources: list[dict]) -> tuple[list[dict], list[str]]:
    """sources is in priority order (highest first)."""
    seen: dict[tuple, dict] = {}
    conflicts: list[str] = []

    for source_list in sources:
        for rec in source_list:
            key = (rec["rec_date"], rec["ticker"], rec["direction"])
            if key in seen:
                existing = seen[key]
                if (rec["entry"], rec["target"], rec["stop"]) != \
                        (existing["entry"], existing["target"], existing["stop"]):
                    conflicts.append(
                        f"{key} kept={existing['source']}({existing['source_id']}) "
                        f"E={existing['entry']} T={existing['target']} S={existing['stop']} "
                        f"vs dropped={rec['source']}({rec['source_id']}) "
                        f"E={rec['entry']} T={rec['target']} S={rec['stop']}"
                    )
            else:
                seen[key] = rec
    return list(seen.values()), conflicts


def main() -> None:
    routine = load_routine_v2()
    local = load_local_runs()
    manual = load_manual()

    print(f"  routine_v2:     {len(routine)} predictions")
    print(f"  local_run:      {len(local)} predictions")
    print(f"  manual:         {len(manual)} predictions")
    print(f"  raw total:      {len(routine) + len(local) + len(manual)}")

    merged, conflicts = merge_with_priority(routine, local, manual)
    merged.sort(key=lambda r: (r["rec_date"], r["ticker"], r["direction"]))

    print(f"  merged unique:  {len(merged)}")
    print(f"  conflicts:      {len(conflicts)}")

    src_count = Counter(r["source"] for r in merged)
    crypto_count = Counter(r["is_crypto"] for r in merged)
    print(f"  by source:      {dict(src_count)}")
    print(f"  by asset:       stock={crypto_count[False]} crypto={crypto_count[True]}")

    OUT.write_text(json.dumps(merged, indent=2))
    print(f"  wrote {OUT}")

    LOG.write_text("\n".join(conflicts) + "\n" if conflicts else "no conflicts\n")
    print(f"  wrote {LOG}")


if __name__ == "__main__":
    main()
