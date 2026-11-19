
from src.ingestion.document_manager import get_document_intelligence

reports = get_document_intelligence("data/uploads")

if not reports:
    print("No PDF or DOCX files found.")

for report in reports:

    print("\n------------------------------")
    print("DOCUMENT INTELLIGENCE")
    print("------------------------------")

    print("Name:", report["filename"])
    print("Type:", report["file_type"])
    print("Size:", report["file_size_bytes"], "bytes")
    print("Pages:", report["page_count"])
    print("Words:", report["word_count"])
    print("Characters:", report["character_count"])
    print("Status:", report["extraction_status"])
