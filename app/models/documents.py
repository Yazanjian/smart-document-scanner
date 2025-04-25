from enum import Enum
from pydantic import BaseModel, Field
from typing import Type, Dict, Union, Optional, List


# Base class for document details
class DocumentDetails(BaseModel):
    """Base class for all document details."""


class BirthCertificate(DocumentDetails):
    full_name: Optional[str] = None
    date_of_birth: Optional[str] = None
    place_of_birth: Optional[str] = None
    father_name: Optional[str] = None
    mother_name: Optional[str] = None
    nationality: Optional[str] = None
    registration_number: Optional[str] = None
    date_of_issue: Optional[str] = None
    issuing_authority: Optional[str] = None


class GeneralDocument(DocumentDetails):
    issuing_country: Optional[str] = None
    document_title: Optional[str] = None
    document_number: Optional[str] = None
    date_of_issue: Optional[str] = None
    date_of_expiry: Optional[str] = None
    relevant_details: Optional[str] = None


class IDCard(DocumentDetails):
    issuing_country: Optional[str] = None
    id_number: Optional[str] = None
    full_name: Optional[str] = None
    date_of_birth: Optional[str] = None  # Format: DD-MM-YYYY
    nationality: Optional[str] = None
    date_of_issue: Optional[str] = None  # Format: DD-MM-YYYY
    date_of_expiry: Optional[str] = None  # Format: DD-MM-YYYY
    place_of_issue: Optional[str] = None
    sex: Optional[str] = None
    machine_readable_zone: Optional[str] = None  # MRZ if available


class Passport(DocumentDetails):
    issuing_country: Optional[str] = None
    passport_number: Optional[str] = None
    surname: Optional[str] = None
    given_names: Optional[str] = None
    nationality: Optional[str] = None
    date_of_birth: Optional[str] = None
    date_of_issue: Optional[str] = None
    date_of_expiry: Optional[str] = None
    place_of_issue: Optional[str] = None
    sex: Optional[str] = None
    machine_readable_zone: Optional[str] = None


class ReceiptItem(BaseModel):
    item_name: Optional[str] = Field(..., description="Name of the purchased item")
    quantity: Optional[int] = Field(..., description="Quantity of the item purchased")
    unit_price: Optional[float] = Field(..., description="Price per unit of the item")
    total_price: Optional[float] = Field(
        ..., description="Total price for this item (quantity * unit price)"
    )


class Receipt(DocumentDetails):
    receipt_number: Optional[str] = Field(
        None, description="Unique identifier for the receipt"
    )
    store_name: Optional[str] = Field(None, description="Name of the store or merchant")
    store_address: Optional[str] = Field(
        None, description="Physical or online address of the store"
    )
    store_phone: Optional[str] = Field(None, description="Contact number of the store")
    date_of_purchase: Optional[str] = Field(
        None, description="Date and time of the transaction"
    )
    items: List[ReceiptItem] = Field(..., description="List of purchased items")
    subtotal: float = Field(
        ..., description="Subtotal amount before taxes or discounts"
    )
    tax: Optional[float] = Field(None, description="Total tax applied to the purchase")
    discount: Optional[float] = Field(
        None, description="Total discount applied to the purchase"
    )
    total_amount: float = Field(
        ..., description="Final total amount after applying tax and discount"
    )
    payment_method: Optional[str] = Field(
        None, description="Payment method used (cash, credit card, etc.)"
    )
    transaction_id: Optional[str] = Field(
        None, description="Unique transaction ID for the payment"
    )
    cashier_name: Optional[str] = Field(
        None, description="Name of the cashier handling the transaction"
    )


class CV(DocumentDetails):
    full_name: Optional[str] = Field(None, description="Full name of the individual")
    date_of_birth: Optional[str] = Field(
        None, description="Date of birth (YYYY-MM-DD format)"
    )
    nationality: Optional[str] = Field(
        None, description="Nationality of the individual"
    )
    email: Optional[str] = Field(None, description="email address of the individual")
    mobile_number: Optional[str] = Field(
        None, description="Mobile Number of the individual"
    )
    address: Optional[str] = Field(None, description="Address of the individual")
    linkedin_profile: Optional[str] = Field(None, description="LinkedIn profile URL")
    github_profile: Optional[str] = Field(None, description="GitHub profile URL")

    education: Optional[List[str]] = Field(
        None, description="List of educational qualifications"
    )
    work_experience: Optional[List[str]] = Field(
        None, description="List of work experiences"
    )
    skills: Optional[List[str]] = Field(
        None, description="List of skills and competencies"
    )
    certifications: Optional[List[str]] = Field(
        None, description="List of certifications or courses"
    )
    languages: Optional[List[str]] = Field(
        None, description="Languages known by the individual"
    )
    summary: Optional[str] = Field(
        None, description="A brief summary or objective statement"
    )


# Generate Enum dynamically based on subclasses of DocumentDetails
def generate_document_type_enum():
    """Dynamically generate the DocumentTypeEnum."""
    subclasses_type_map = {
        cls.__name__: cls for cls in DocumentDetails.__subclasses__()
    }
    return (
        Enum(
            "DocumentTypeEnum", {name: name for name in subclasses_type_map}, type=str
        ),
        subclasses_type_map,
    )


# Generate the Enum
DocumentTypeEnum, DOCUMENT_TYPE_MAP = generate_document_type_enum()


# Get a list of all the supported types
def get_document_type_names():
    return [e.value for e in DocumentTypeEnum]


class Document(BaseModel):
    type: DocumentTypeEnum
    details: Union[*DocumentDetails.__subclasses__()]
