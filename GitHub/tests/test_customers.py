from ma_migration.domains.customers.pipeline import prepare_customers

def test_prepare_customers_non_strict(sample_customers):
    res = prepare_customers(sample_customers, strict=False)
    assert "customers_expanded" in res.data
    assert res.data["customers_expanded"].shape[0] == 3  # Both -> 2 rows

def test_prepare_customers_strict(sample_customers):
    res = prepare_customers(sample_customers, strict=True)
    assert res.data["customers_expanded"].shape[0] == 3
