
from src.ingestion.document_manager import load_documents


folder_path = "data/uploads"

documents = load_documents(folder_path)

print("Total extracted records:", len(documents))

for index, document in enumerate(documents, start=1):

    print("\n--------------------------")
    print("Record:", index)
    print("Metadata:", document["metadata"])
    print("Text:", document["text"][:200])
