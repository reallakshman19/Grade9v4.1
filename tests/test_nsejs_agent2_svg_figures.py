"""Original Agent 2 SVG diagrams — structural validation, not science review."""
from pathlib import Path
from xml.etree import ElementTree as ET
import pytest

ROOT = Path(__file__).resolve().parents[1]
TOPICS = [f"PH{i:02d}" for i in range(7,13)]

@pytest.mark.parametrize("topic",TOPICS)
def test_draft_science_figure_is_original_accessible_valid_svg(topic):
    folder=ROOT / f"nsejs/physics/curriculum/topics/{topic}"
    image=folder/"figures/lead-concept.svg"
    text=image.read_text(encoding="utf-8")
    root=ET.fromstring(text)
    assert root.tag.endswith("svg")
    assert root.attrib.get("viewBox")
    assert root.attrib.get("role")=="img"
    assert len(root.findall("{http://www.w3.org/2000/svg}title"))==1
    assert len(root.findall("{http://www.w3.org/2000/svg}desc"))==1
    page=(folder/"index.html").read_text(encoding="utf-8")
    assert 'src="figures/lead-concept.svg"' in page
    assert "review HOLD" in page or "review pending" in page
