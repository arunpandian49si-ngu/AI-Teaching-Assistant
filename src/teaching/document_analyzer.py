
from src.ingestion.document_manager import load_documents
from src.llm.ollama_client import get_llm
from src.teaching.teaching_prompts import (
    build_document_analysis_prompt
)


class DocumentAnalyzer:

    def __init__(self, folder_path="data/uploads"):

        self.folder_path = folder_path
        self.llm = get_llm()

    def split_text(self, text, chunk_size=6000, overlap=300):

        chunks = []

        start = 0

        while start < len(text):

            end = start + chunk_size

            chunks.append(text[start:end])

            start = end - overlap

        return chunks

    def analyze(self, filename):

        # Step 1: Load uploaded documents
        documents = load_documents(self.folder_path)

        # Step 2: Select the requested document
        selected_documents = [
            document for document in documents
            if document["metadata"].get("filename") == filename
        ]

        if not selected_documents:
            return {
                "success": False,
                "analysis": "Document not found.",
                "filename": filename
            }

        # Step 3: Combine document text
        full_text = "\n\n".join(
            document["text"]
            for document in selected_documents
            if document["text"].strip()
        )

        if not full_text.strip():
            return {
                "success": False,
                "analysis": "No readable text found in this document.",
                "filename": filename
            }

        # Step 4: Split large documents
        text_chunks = self.split_text(full_text)

        # Step 5: Analyze each part
        partial_analyses = []

        for index, chunk in enumerate(text_chunks):

            print(
                f"Analyzing document section "
                f"{index + 1}/{len(text_chunks)}"
            )

            prompt = build_document_analysis_prompt(
                context=chunk,
                filename=filename
            )

            response = self.llm.invoke(prompt)

            partial_analyses.append(response.content)

        # Step 6: Combine partial analyses
        combined_context = "\n\n".join(partial_analyses)

        final_prompt = f"""
You are an expert AI Teaching Assistant.

The following are analyses of different sections
of the same document: {filename}

Combine them into ONE complete document analysis.

Use these exact sections:

1. DOCUMENT SUMMARY
2. KEY TOPICS
3. IMPORTANT POINTS
4. CHAPTERS AND HEADINGS
5. LEARNING OBJECTIVES

RULES:
- Combine repeated information.
- Do not invent unsupported information.
- Preserve important technical terms.
- Use simple English.
- Avoid unnecessary repetition.
- Clearly mention when a section has no available information.

SECTION ANALYSES:
{combined_context}

Generate the final document analysis:
"""

        final_response = self.llm.invoke(final_prompt)

        return {
            "success": True,
            "filename": filename,
            "analysis": final_response.content,
            "sections_analyzed": len(text_chunks)
        }
