
from src.teaching.document_analyzer import DocumentAnalyzer

analyzer = DocumentAnalyzer()

filename = "React_JS_Exam_Notes.docx"

print("\nStarting Document Analysis...\n")

result = analyzer.analyze(filename)

if result["success"]:

    print("\n================================")
    print("DOCUMENT ANALYSIS")
    print("================================")

    print("Document:", result["filename"])

    print(
        "Sections analyzed:",
        result["sections_analyzed"]
    )

    print("\n", result["analysis"])

else:

    print("Analysis failed:")
    print(result["analysis"])
