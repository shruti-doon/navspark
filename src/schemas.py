from pydantic import BaseModel, Field
from typing import Optional


class EChallanSchema(BaseModel):
    """
    Pydantic schema representing the required fields for an eChallan document.
    """
    challan_number: Optional[str] = Field(None, description="The unique Challan Number")
    vehicle_number: Optional[str] = Field(None, description="The Vehicle Number/Registration Number")
    violation_date: Optional[str] = Field(None, description="The Date of Violation (e.g. YYYY-MM-DD or DD/MM/YYYY)")
    amount: Optional[int] = Field(None, description="The total fine or penalty Amount")
    offence_description: Optional[str] = Field(None, description="Description of the offence/violation")
    payment_status: Optional[str] = Field(None, description="Payment Status (e.g. Paid, Unpaid, Pending)")


class NAPermissionSchema(BaseModel):
    """
    Pydantic schema representing the required fields for an NA (Non-Agricultural) Permission document.
    """
    survey_number: Optional[str] = Field(None, description="The Survey Number or Block Number of the land")
    land_area: Optional[str] = Field(None, description="The Area of the land in square meters/hectares")
    owner_name: Optional[str] = Field(None, description="Name(s) of the land Owner(s)")
    order_date: Optional[str] = Field(None, description="The Date of the Order")
    authority_details: Optional[str] = Field(None, description="Details of the issuing Authority (e.g. Collector, TDO)")
