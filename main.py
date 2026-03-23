import os
import argparse
from pathlib import Path
from dotenv import load_dotenv

from src.extractor import extract_text_from_pdf
from src.llm_parser import parse_document_text
from src.exporter import export_to_excel

# Load env variables
load_dotenv()

def determine_doc_type(text: str) -> str:
    """
    Very basic heuristic to determine if it's an echallan or na_permission.
    """
    text_lower = text.lower()
    if "challan" in text_lower or "vehicle" in text_lower or "offence" in text_lower:
        return "echallan"
    return "na_permission"

# Removed list_ollama_models
def process_single_pdf(pdf_path: Path, model: str) -> dict | None:
    print(f"Processing: {pdf_path.name}")
    try:
        text = extract_text_from_pdf(pdf_path)
        doc_type = determine_doc_type(text)
        print(f"  Detected Document Type: {doc_type}")
        
        parsed_data = parse_document_text(text, filename=pdf_path.name, doc_type=doc_type, model=model)
        if parsed_data:
            print("  Extraction Successful!")
            parsed_data["source_file"] = pdf_path.name
            parsed_data["document_type"] = doc_type
        return parsed_data
        
    except Exception as e:
        print(f"  Error processing {pdf_path.name}: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(
        description="NavSpark: LLM-powered PDF Extraction Pipeline (using Gemini API)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("input_path", nargs="?", help="Path to a PDF file or a directory containing PDFs")
    parser.add_argument("--output", default="data/output/report.xlsx", help="Path to save the generated Excel report")
    parser.add_argument("--model", default="gemini-2.5-flash", help="The Gemini model to use")
    
    args = parser.parse_args()

    if not args.input_path:
        parser.print_help()
        return

    input_path = Path(args.input_path)
    
    print(f"Using model '{args.model}' via Google Gemini API")

    all_parsed_data = []

    if input_path.is_file() and input_path.suffix.lower() == ".pdf":
        data = process_single_pdf(input_path, model=args.model)
        if data:
            all_parsed_data.append(data)
            
    elif input_path.is_dir():
        pdf_files = list(input_path.glob("*.pdf"))
        if not pdf_files:
            print(f"No PDF files found in {input_path}")
            return
            
        for pdf_file in pdf_files:
            data = process_single_pdf(pdf_file, model=args.model)
            if data:
                all_parsed_data.append(data)
    else:
        print(f"Invalid input path: {input_path}")
        return

    if all_parsed_data:
        export_to_excel(all_parsed_data, output_path=args.output)
    else:
        print("No data extracted. Skipping export.")


if __name__ == "__main__":
    main()
