from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader

def extract_text_from_pdf(  file_path: Path) -> str:
  loader = PyPDFLoader(str(file_path))
  documents = loader.load()

  return "\n".join(
    document.page_content
    for document in documents
  )