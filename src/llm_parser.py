import os
import json
from google import genai
from pydantic import BaseModel
from typing import Type

from src.audit_logger import AuditLogger
from src.schemas import EChallanSchema, NAPermissionSchema


def parse_document_text(text: str, filename: str, doc_type: str, model: str = "gemini-2.5-flash") -> dict | None:
    """
    Uses Google's Gemini API to parse the document text according to the specific document type.
    Enforces a JSON output schema by using structured outputs.
    """
    logger = AuditLogger()
    
    if doc_type == "echallan":
        schema_class: Type[BaseModel] = EChallanSchema
        sys_prompt = "You are an expert legal document parser. Extract the eChallan details from the given text."
    elif doc_type == "na_permission":
        schema_class: Type[BaseModel] = NAPermissionSchema
        sys_prompt = "You are an expert legal document parser. Extract the Non-Agricultural (NA) Permission details from the text."
    else:
        raise ValueError("Unsupported doc_type. Use 'echallan' or 'na_permission'.")
        
    prompt = f"Text:\n{text[:100000]}"
    
    try:
        client = genai.Client()
        response = client.models.generate_content(
            model=model,
            contents=[sys_prompt, prompt],
            config={
                "response_mime_type": "application/json",
                "response_schema": schema_class,
                "temperature": 0.0
            }
        )
        
        response_text = response.text
        if response_text:
            parsed_data = json.loads(response_text)
            logger.log_interaction(filename, prompt, response_text, parsed_data, status="SUCCESS")
            return parsed_data
            
    except Exception as e:
        logger.log_interaction(filename, prompt, str(e), None, status="FAILED")
        print(f"Failed to parse {filename}: {e}")
        return None
        
    return None
