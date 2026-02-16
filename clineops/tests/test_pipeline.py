from clineops.etl.transform import transform

def test_valid_schema():
    assert transform({"price": 50}) == 50
