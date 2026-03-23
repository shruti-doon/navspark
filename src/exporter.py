import pandas as pd
from pathlib import Path

def export_to_excel(data_list: list[dict], output_path: str | Path = "data/output/report.xlsx"):
    """
    Exports a list of parsed document dictionaries to an Excel file.
    """
    if not data_list:
        print("No data to export.")
        return
        
    # Flatten or normalize paths if needed, but since our schemas are flat, simple convert is fine.
    df = pd.DataFrame(data_list)
    
    out_path = Path(output_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    
    df.to_excel(out_path, index=False)
    print(f"Successfully exported {len(data_list)} records to {out_path.absolute()}")
