"""
PlugMind API Client - syncs frontend with Backend API
Used when PLUGMIND_API=1 and backend is running at localhost:8000
"""
import os
import requests

API_URL = os.environ.get("PLUGMIND_API_URL", "http://localhost:8000").rstrip("/")

def get_client():
    """Return API client wrapper (same interface as PDFQASystem)"""
    return APIClient()

class APIClient:
    """Mimics PDFQASystem interface, calls Backend API"""
    def __init__(self):
        self._info = None

    def _post(self, path: str, json: dict, timeout: int = 180):
        r = requests.post(f"{API_URL}{path}", json=json, timeout=timeout)
        r.raise_for_status()
        return r.json()

    def _get(self, path: str, timeout: int = 120):
        r = requests.get(f"{API_URL}{path}", timeout=timeout)
        r.raise_for_status()
        return r.json()

    def answer_question(self, question: str) -> str:
        return self._post("/answer", {"question": question})["answer"]

    def predict_loan_eligibility(self, applicant_data: dict) -> dict:
        return self._post("/predict", applicant_data)

    def _load_info(self):
        if self._info is None:
            self._info = self._get("/ready")

    @property
    def documents(self):
        self._load_info()
        return self._info.get("documents", [])

    @property
    def datasets(self):
        self._load_info()
        return {k: type('DF', (), {'shape': (0, 0)})() for k in self._info.get("datasets", [])}

    @property
    def sme_manager(self):
        self._load_info()
        experts = self._info.get("experts", [])
        plugins = self._info.get("plugins", {})
        class M:
            def list_plugins(self): return experts
            def __init__(self): self.plugins = plugins or {e: {"name": e, "domain": "", "expertise": [], "keywords": []} for e in experts}
        return M()

    @property
    def llm_enabled(self):
        self._load_info()
        return self._info.get("llm_enabled", False)

    llm_model = "llama3.2:3b"
    ollama_url = "http://localhost:11434"

    @property
    def model_loaded(self):
        self._load_info()
        return self._info.get("model_loaded", False)

    @property
    def loan_model(self):
        return True if self.model_loaded else None
