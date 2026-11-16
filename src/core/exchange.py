from datetime import time as dt_time
from pathlib import Path
import yaml

class Exchange:
    def __init__(self, config_path: str | Path):
        with open(config_path, "r") as f:
            self.cfg = yaml.safe_load(f)
        self.exchange_id = self.cfg["exchange_id"]
        self._sessions = self.cfg["sessions"]
        self._auctions = self.cfg.get("auctions", {})

    def _parse(self, hhmm: str) -> dt_time:
        h, m = map(int, hhmm.split(":"))
        return dt_time(h, m)

    def session_at(self, t: dt_time) -> str:
        for name, window in self._sessions.items():
            if "start" in window and "end" in window:
                if self._parse(window["start"]) <= t < self._parse(window["end"]):
                    return name
            elif "cross_time" in window:
                if t == self._parse(window["cross_time"]):
                    return name
        return "closed"

    def is_continuous_trading(self, t: dt_time) -> bool:
        return self.session_at(t) == "regular"