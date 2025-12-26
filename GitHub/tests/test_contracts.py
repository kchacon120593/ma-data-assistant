import pandas as pd
from ma_migration.contracts.runner import run_contract

def test_contract_allowed_values_and_length():
    df = pd.DataFrame({
        "NIP / VAT Number": ["1234567890", "123"],
        "Invoicing Coupling Code": ["0001", "BAD"],
        "Invoicing Cluster": ["0001", "12"]
    })
    contract = {
        "domain": "customers",
        "version": "1.0",
        "rules": [
            {"id":"VAT_LENGTH","column":"NIP / VAT Number","type":"length_equals","equals":10,"severity":"error"},
            {"id":"COUPLING_ALLOWED","column":"Invoicing Coupling Code","type":"allowed_values","values":["0001"],"severity":"error"},
            {"id":"CLUSTER_REGEX","column":"Invoicing Cluster","type":"regex","pattern":"^[0-9]{4}$","severity":"warning"},
        ],
    }
    report = run_contract(df, contract, strict=False)
    s = report.summary()
    assert s["errors"] == 2
    assert s["warnings"] == 1
