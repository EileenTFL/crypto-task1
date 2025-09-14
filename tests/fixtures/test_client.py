from src.etherscan_client import EtherscanClient

def test_fixture_loads_without_api_key(monkeypatch, tmp_path):
    monkeypatch.delenv("ETHERSCAN_API_KEY", raising=False)
    c = EtherscanClient(api_key=None, cache_dir=tmp_path)
    rows = c.txlist("0xde0B295669a9FD93d5F28D9Ec85E40f4cb697BAe")
    assert isinstance(rows, list)
    assert len(rows) > 0
