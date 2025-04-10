import fitz
import requests
import tempfile
import os

doi_prefixes = ["https://doi.org/", "http://dx.doi.org/"]

class ExtractionAgent:
    def extract_text(self, file_path):
        doc = fitz.open(file_path)
        return "\n".join(page.get_text() for page in doc)

    def extract_from_url(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(response.content)
                tmp_path = tmp_file.name
            text = self.extract_text(tmp_path)
            os.remove(tmp_path)
            return text
        return ""

    def extract_from_doi(self, doi):
        # Handle arXiv DOI
        if doi.startswith("10.48550/arXiv."):
            arxiv_id = doi.split("arXiv.")[1]
            pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
            return self.extract_from_url(pdf_url)

        # Existing logic (PDF header fetch)
        for prefix in ["https://doi.org/", "http://dx.doi.org/"]:
            full_url = prefix + doi if not doi.startswith(prefix) else doi
            try:
                headers = {"Accept": "application/pdf"}
                response = requests.get(full_url, headers=headers, timeout=10, allow_redirects=True)
                if response.status_code == 200 and "application/pdf" in response.headers.get("Content-Type", ""):
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                        tmp_file.write(response.content)
                        tmp_path = tmp_file.name
                    text = self.extract_text(tmp_path)
                    os.remove(tmp_path)
                    return text
            except Exception:
                continue
        return ""
