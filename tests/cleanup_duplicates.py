
from src.vectorstore.chroma_store import collection

# Keep one copy of each document.
# Delete only the verified duplicate filenames.

duplicate_files = [
    "React_JS_Exam_Notes_1.docx",
    "sample_1.docx",
    "sample_2.docx",
    "sample_3.docx"
]

print("\n========== DUPLICATE CLEANUP ==========")

for filename in duplicate_files:

    collection.delete(
        where={"filename": filename}
    )

    print("Deleted duplicate:", filename)

print("\nCleanup completed!")

print("Remaining chunks:", collection.count())

print("======================================")
