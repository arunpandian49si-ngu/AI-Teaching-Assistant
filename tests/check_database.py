
import hashlib
from collections import defaultdict

from src.vectorstore.chroma_store import collection

results = collection.get(
    include=["documents", "metadatas"]
)

file_content = defaultdict(list)

for text, metadata in zip(
    results["documents"],
    results["metadatas"]
):
    filename = metadata.get("filename", "Unknown")
    file_content[filename].append(text)

fingerprints = {}

for filename, chunks in file_content.items():

    # Sort to compare content independent of retrieval order
    normalized_content = "\n".join(sorted(chunks))

    fingerprint = hashlib.sha256(
        normalized_content.encode("utf-8")
    ).hexdigest()

    fingerprints[filename] = fingerprint

print("\n========== DUPLICATE CHECK ==========")

groups = defaultdict(list)

for filename, fingerprint in fingerprints.items():
    groups[fingerprint].append(filename)

for filenames in groups.values():

    if len(filenames) > 1:
        print("\nPossible duplicate files:")
        for filename in filenames:
            print("-", filename)

    else:
        print("\nUnique file:", filenames[0])

print("\n====================================")



