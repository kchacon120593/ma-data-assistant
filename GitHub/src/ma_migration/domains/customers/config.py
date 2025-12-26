from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class CustomersConfig:
    customer_id_col: str = "Source Customer ID"
    industry_col: str = "Industry Category"
    customer_name_col: str = "Customer Name"
    vat_col: str = "NIP / VAT Number"
    contract_number_col: str = "Contract Number"
    contract_type_col: str = "Contract Type"
    contract_signed_date_col: str = "Contract Signed Date"
    contract_term_col: str = "Contract Term"
    amount_of_employees_col: str = "Amount of Employees"
    customer_postal_code_col: str = "Customer Postal Code"
    customer_city_col: str = "Customer City"
    customer_town_col: str = "Customer Town"
    customer_address_col: str = "Customer Address"
    
    contact_person_col: str = "Contact Person"
    contact_role_col: str = "Contact Role"
    contact_phone_col: str = "Contact Phone Number"
    contact_email_col: str = "Contact Email"
    
    invoicing_coupling_col: str = "Invoicing Coupling Code"
    invoicing_cluster_col: str = "Invoicing Cluster"
    invoicing_payment_term_col: str = "Invoicing Payment Term"
    invoicing_method_col: str = "Invoicing Method"
    invoicing_postal_code_col: str = "Invoicing Postal Code"
    invoicing_city_col: str = "Invoicing City"
    invoicing_town_col: str = "Invoicing Town"
    invoicing_address_col: str = "Invoicing Address"
    
    customer_price_model_col: str = "Customer Price Model"
    customer_hasRentedLocker_col: str = "Has Rented Locker?"
    customer_hasLockerManagement_col: str = "Has Locker Management?"
    

    # business enums (kept as in notebook)
    valid_invoicing_coupling: tuple[str, ...] = ("0001","0090","0091","0092","0093","0094")
    valid_contract_types: tuple[str, ...] = ("Rental","Laundry")
