import chromadb

client = chromadb.PersistentClient(
    path="chroma_db"
)

collection = client.get_collection(
    name="teaching_documents"
)

print("Total stored records:", collection.count())

results = collection.peek(limit=2)

print("\nStored documents:")
print(results["documents"])

print("\nStored metadata:")
print(results["metadatas"])