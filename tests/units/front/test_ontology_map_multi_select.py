"""Contracts for Ontology Studio multi-select gestures on the D3 map."""

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
MAP_JS = REPO_ROOT / "src/front/static/ontology/js/ontology-map.js"


def _map_init_block():
    js = MAP_JS.read_text(encoding="utf-8")
    start = js.index("async function initOntologyMap()")
    end = js.index("function initMapSearch(nodes)", start)
    return js[start:end]


def test_modifier_click_toggles_without_opening_panel():
    block = _map_init_block()
    assert "event.ctrlKey || event.metaKey" in block
    assert "_toggleMapEntitySelection(d.name)" in block


def test_modifier_marquee_replaces_selection():
    block = _map_init_block()
    assert "function startMapMarquee(event)" in block
    assert "_setMapSelection(namesInside)" in block
    assert "ontologyMapZoom.filter" in block


def test_escape_clears_multi_selection():
    js = MAP_JS.read_text(encoding="utf-8")
    assert "function handleMapSelectionKeyDown(event)" in js
    assert "if (event.key !== 'Escape'" in js


def _marquee_block():
    block = _map_init_block()
    start = block.index("function startMapMarquee(event)")
    end = block.index("svg.on('pointerdown'", start)
    return block[start:end]


def test_marquee_starts_only_on_empty_canvas():
    marquee = _marquee_block()
    assert "event.target.tagName !== 'svg'" in marquee
    assert ".map-link" in marquee
    assert ".map-link-hitarea" in marquee
    assert ".map-link-label" in marquee


def _relationship_hitarea_block():
    block = _map_init_block()
    start = block.index(".attr('class', 'map-link-hitarea')")
    end = block.index(".attr('class', 'map-link-label')", start)
    return block[start:end]


def test_relationship_selection_clears_entity_set():
    hit = _relationship_hitarea_block()
    assert hit.count("_clearMapSelection()") == 2
    assert "d3.selectAll('.map-node').classed('selected', false)" not in hit
