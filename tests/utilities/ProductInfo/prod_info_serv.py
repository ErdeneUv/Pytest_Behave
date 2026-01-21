import csv
import json
import os
from pathlib import Path
from time import sleep
from typing import Dict, Any, Optional

import pandas as pd

from dotenv import load_dotenv  # type: ignore
from tests.utilities.api_utilities import get_product_info



def gsheet_url(sheet_url: str) -> str:
    """Construct a CSV export URL from a standard Google Sheets URL.

    Google Sheets supports exporting sheet data as CSV by replacing the
    ``/edit`` part of the URL with ``/export?format=csv``. An optional
    gid parameter may be included to select a specific worksheet.

    Args:
        sheet_url: The original Google Sheets URL.

    Returns:
        A URL that triggers a CSV export of the first worksheet.
    """
    if not sheet_url:
        raise ValueError("Sheet URL must not be empty.")
    # If the URL already contains an export=csv query, use as is
    if "/export?format=csv" in sheet_url:
        return sheet_url
    base = sheet_url.split("/edit")[0]
    gid: Optional[str] = None
    if "gid=" in sheet_url:
        # Extract the first gid value from the query string
        parts = sheet_url.split("gid=")[1].split("&", 1)[0]
        gid = parts.strip()
    if gid:
        return f"{base}/export?format=csv&gid={gid}"
    return f"{base}/export?format=csv"


def load_sheet(url: str) -> pd.DataFrame:
    """Load Google Sheet data into a DataFrame using gspread or CSV fallback.

    This function first attempts to downloading the sheet's CSV
    representation using pandas.

    Args:
        url: The URL of the Google Sheet.

    Returns:
        A pandas DataFrame containing the sheet data.

    Raises:
        RuntimeError: If the sheet cannot be loaded via gspread or CSV.
    """
    # Fallback: download as CSV via HTTP. Note: Only works if the sheet
    # is published or the user has access to the export URL.
    csv_url = gsheet_url(url)
    try:
        return pd.read_csv(csv_url)
    except Exception as exc:
        raise RuntimeError(f"Failed to load sheet data: {exc}")


def run_test() -> Dict[str, Any]:
    """Execute the ad hoc product page test.

    This function loads the Google Sheet specified by the ``gsheet_url``
    environment variable, extracts the first 20 rows of brand and product
    page columns, and then queries each product page using
    ``get_prod()``. Results are returned as a dictionary and also
    printed as a summary.

    Returns:
        A dictionary mapping variable names (``<brand>_product_<n>``) to
        either the HTTP status code or the response body text.
    """
    sheet_url = os.getenv("GSHEET_URL")
    if not sheet_url:
        raise RuntimeError(
            "Environment variable 'gsheet_url' is not set. Please define it in .env or the environment."
        )
    # Load sheet data
    df = load_sheet(sheet_url)
    if df.empty:
        raise RuntimeError("Loaded sheet is empty. Ensure the sheet has data.")
    # Normalize columns by stripping whitespace
    print(f'before normalize columns:{df.columns}\n')
    df.columns = [c.strip() for c in df.columns]

    # Map known columns to internal keys
    brand_col: Optional[str] = None
    prod1_col: Optional[str] = None
    prod2_col: Optional[str] = None
    prod3_col: Optional[str] = None
    for col in df.columns:
        key = col.lower()
        if key == "brand name":
            brand_col = col
        elif key in ("product page", "product page 1"):
            prod1_col = col
        elif key == "product page 2":
            prod2_col = col
        elif key == "product page 3":
            prod3_col = col
    # Validate required columns
    if brand_col is None or prod1_col is None:
        raise RuntimeError(
            "Required columns 'Brand Name' and 'Product Page'/'Product Page 1' were not found in the sheet."
        )
    # Only keep the first 20 rows
    subset = df.iloc[:20]
    results: Dict[str, Any] = {}
    # Process each row
    for _, row in subset.iterrows():
        raw_brand = str(row[brand_col]).strip()
        #skipped the sanitizing brand names
        safe_brand = raw_brand
        # Iterate over the three possible product columns
        for idx, col in enumerate([prod1_col, prod2_col, prod3_col], start=1):
            if not col:
                raise RuntimeError(f"Expected Product Page {idx} column, but it was not found in the sheet.")
            url_value = row[col]
            # Skip blank or missing values
            if pd.isna(url_value) or not str(url_value).strip():
                continue
            url = str(url_value).strip()
            sleep(1)
            try:
                response = get_product_info(url)
                print(f'response: {response}\n{response.text}')
                status = getattr(response, "status_code", None)
            except Exception as exc:
                # If an exception occurs during the HTTP call, record the error message
                results[f"{safe_brand}_product_{idx}"] = f"ERROR: {exc}"
                continue
            # If status code is 200, capture the body text; otherwise record the status
            if status == 200:
                body: Optional[str] = None
                if hasattr(response, "text"):
                    body = response.text  # type: ignore
                elif hasattr(response, "content"):
                    try:
                        body = response.content.decode("utf-8", errors="replace")  # type: ignore
                    except Exception:
                        body = None
                results[f"{safe_brand}_product_{idx}"] = body
            else:
                # For non-200 responses, attempt to extract a "detail" message from
                # a JSON API error payload if present. If found, store both the
                # status and the detail; otherwise store just the status code.
                detail_msg: Optional[str] = None
                raw_body: Optional[str] = None
                # Try to get raw text body
                if hasattr(response, "text") and isinstance(response.text, str):
                    raw_body = response.text
                elif hasattr(response, "content"):
                    try:
                        raw_body = response.content.decode("utf-8", errors="replace")  # type: ignore
                    except Exception:
                        raw_body = None
                if raw_body:
                    try:
                        parsed = json.loads(raw_body)
                        # Expecting structure {"errors": [{"detail": "..."}]}
                        if (
                                isinstance(parsed, dict)
                                and "errors" in parsed
                                and isinstance(parsed["errors"], list)
                                and parsed["errors"]
                                and isinstance(parsed["errors"][0], dict)
                                and "detail" in parsed["errors"][0]
                        ):
                            detail_msg = str(parsed["errors"][0]["detail"])
                    except Exception:
                        detail_msg = None
                if detail_msg:
                    results[f"{safe_brand}_product_{idx}"] = {"status": status, "detail": detail_msg}
                else:
                    results[f"{safe_brand}_product_{idx}"] = status
    # Print summary of results
    for name, value in results.items():
        # If the value is a dict with status/detail (non-200 with parsed error detail)
        if isinstance(value, dict) and "status" in value:
            status = value.get("status")
            detail = value.get("detail")
            if detail:
                print(f"{name}: HTTP {status} - {detail}")
            else:
                print(f"{name}: HTTP {status}")
        elif isinstance(value, int):
            print(f"{name}: HTTP {value}")
        elif isinstance(value, str) and value and value.startswith("ERROR"):
            print(f"{name}: {value}")
        else:
            # Print only a truncated preview of the body to avoid flooding the console
            preview = value if isinstance(value, str) else str(value)
            if preview is None:
                preview = "<no body>"
            elif len(preview) > 20:
                preview = preview[:20] + "..."
            print(f"{name}: BODY {preview}")
    return results


if __name__ == "__main__":
    run_test()