import pandas as pd
import pytest

@pytest.fixture
def sample_customers():
    return pd.DataFrame({
        "CustomerID in HeliosDb": [1, 2],
        "NIP / VAT Number": ["1234567890", "0987654321"],
        "DepartmentID/BranchID in HeliosDb": [1, None],
        "Department/Branch Name": ["A", "B"],
        "Contract type (rental / laundry/ Both)": ["Rental", "Both"],
        "Invoicing Coupling Code": ["0001", "0090"],
        "Invoicing Cluster": ["1", "2"],
    })
