import os
from pypdf import PdfReader
from PIL import Image
from utils.output_writer import write_extracted_signal

# --------------------------------------------------
# App root (one-time definition)
# --------------------------------------------------
APP_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

DATA_ROOT = os.path.join(APP_ROOT, "data")


def _resolve_path(relative_path: str) -> str:
    """
    Resolve paths relative to the app's data directory.
    """
    resolved = os.path.join(DATA_ROOT, relative_path)
    if not os.path.exists(resolved):
        raise FileNotFoundError(f"Data file not found: {resolved}")
    return resolved


def _read_pdf(relative_path: str) -> str:
    pdf_path = _resolve_path(relative_path)
    reader = PdfReader(pdf_path)
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def _analyze_image_stub(relative_path: str) -> dict:
    img_path = _resolve_path(relative_path)
    Image.open(img_path)  # validates image
    return {
        "suspected_condition": "degenerative joint disease",
        "confidence": 0.80,
        "source": "stub_vlm"
    }


def intake_agent(state: dict) -> dict:
    document_signals = {}
    image_signals = {}

    # ---- Documents (appeals, medical reports, policies)
    for value in state["documents"].values():
        if isinstance(value, list):
            for path in value:
                document_signals[path] = _read_pdf(path)
        else:
            document_signals[value] = _read_pdf(value)

    # ---- Images
    for img_path in state.get("images", []):
        image_signals[img_path] = _analyze_image_stub(img_path)

    write_extracted_signal("document_signals.json", document_signals)
    write_extracted_signal("image_signals.json", image_signals)

    return {
        **state,
        "doc_signals": document_signals,
        "image_signals": image_signals
    }
