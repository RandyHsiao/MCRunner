from __future__ import annotations
from datetime import datetime
from typing import List
from .bar import Bar


def _parse_datetime(date_str: str, time_str: str | None) -> datetime:
    patterns = ["%Y/%m/%d", "%Y-%m-%d", "%Y%m%d"]
    if time_str is not None:
        time_patterns = ["%H:%M", "%H:%M:%S"]
        for dp in patterns:
            for tp in time_patterns:
                try:
                    return datetime.strptime(f"{date_str} {time_str}", f"{dp} {tp}")
                except ValueError:
                    continue
    else:
        for dp in patterns:
            try:
                return datetime.strptime(date_str, dp)
            except ValueError:
                continue
    return datetime.now()


def load_bars_from_file(path: str) -> List[Bar]:
    bars: List[Bar] = []
    with open(path, "r", encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if not line or any(c.isalpha() for c in line.split(',')[0]):
                # skip header or invalid line
                continue
            parts = [p.strip() for p in line.replace('\t', ',').split(',') if p.strip()]
            if len(parts) < 5:
                continue
            if len(parts) >= 7:
                date_str, time_str = parts[0], parts[1]
                idx = 2
            else:
                date_str, time_str = parts[0], None
                idx = 1
            dt = _parse_datetime(date_str, time_str)
            try:
                open_p = float(parts[idx]); idx += 1
                high_p = float(parts[idx]); idx += 1
                low_p = float(parts[idx]); idx += 1
                close_p = float(parts[idx]); idx += 1
            except (ValueError, IndexError):
                continue
            volume = float(parts[idx]) if len(parts) > idx else 0.0
            bars.append(Bar(Time=dt, Open=open_p, High=high_p, Low=low_p, Close=close_p, Volume=volume))
    return bars
