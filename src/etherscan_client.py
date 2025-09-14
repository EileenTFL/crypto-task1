import os
import json
from pathlib import Path
from typing import Dict, Any, List, Optional

import requests
from dotenv import load_dotenv

load_dotenv()
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")


class EtherscanClient:
    """Thin wrapper for Etherscan account.txlist. Falls back to fixture if no API key."""
    def __init__(self, api_key: Optional[str] = None, cache_dir: str = "data/raw"):
        self.api_key = api_key or ETHERSCAN_API_KEY
        self.base = "https://api.etherscan.io/api"
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _cache_path(self, address: str) -> Path:
        return self.cache_dir / f"txlist_{address.lower()}.json"

    def txlist(self, address: str, *, sort: str = "desc", page: int = 1, offset: int = 100) -> List[Dict[str, Any]]:
        if not self.api_key:
            # Use cached or fixture so it runs without a key
            p = self._cache_path(address)
            if p.exists():
                return json.loads(p.read_text())
            fixture = Path(__file__).resolve().parent.parent / "tests/fixtures/sample_txlist.json"
            if fixture.exists():
                return json.loads(fixture.read_text())
            raise RuntimeError("No ETHERSCAN_API_KEY and no fixture available.")
        params = {
            "module": "account", "action": "txlist", "address": address,
            "startblock": 0, "endblock": 99999999, "page": page, "offset": offset,
            "sort": sort, "apikey": self.api_key,
        }
        r = requests.get(self.base, params=params, timeout=30)
        r.raise_for_status()
        data = r.json()
        result = data.get("result", [])
        self._cache_path(address).write_text(json.dumps(result, indent=2))
        return result
