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
    assert hit.count("_clearMapSelection({ closePanel: false })") == 2
    assert "d3.selectAll('.map-node').classed('selected', false)" not in hit
    assert "guardedCloseSharedPanel" not in hit
    assert "await guardedCloseSharedPanel" not in hit
    assert "editPropertyByName(d.name)" in hit


def test_selection_helpers_support_close_panel_option():
    js = MAP_JS.read_text(encoding="utf-8")
    start = js.index("function _setMapSelection(names, options)")
    end = js.index("function handleMapSelectionKeyDown(event)", start)
    helpers = js[start:end]
    assert "options.closePanel === false" in helpers
    assert "function _clearMapSelection(options)" in helpers


def test_canvas_click_clears_selection_then_closes_panel_once():
    block = _map_init_block()
    start = block.index("svg.on('click', function()")
    end = block.index("function startMapMarquee(event)", start)
    canvas = block[start:end]
    assert "_clearMapSelection({ closePanel: false })" in canvas
    assert canvas.count("guardedCloseSharedPanel()") == 1
    assert "await guardedCloseSharedPanel" not in canvas


def _function_block(js, signature):
    start = js.index(signature)
    next_positions = []
    for needle in ("\nfunction ", "\nasync function "):
        pos = js.find(needle, start + 1)
        if pos != -1:
            next_positions.append(pos)
    end = min(next_positions) if next_positions else len(js)
    return js[start:end]


def test_selected_drag_translates_whole_group():
    block = _map_init_block()
    assert "mapDragStartPositions = new Map" in block
    assert "node.fx = start.x + deltaX" in block


def test_multi_context_menu_limits_actions():
    js = MAP_JS.read_text(encoding="utf-8")
    block = _function_block(js, "function showMapMultiSelectContextMenu(")
    assert "Create Business View" in block
    assert "Delete ${names.length} entities" in block
    assert "create-relationship" not in block
    assert "createBusinessViewFromSelection(names)" in block
    assert "deleteEntitiesFromMap(names)" in block


def test_multi_delete_mutates_and_saves_once():
    js = MAP_JS.read_text(encoding="utf-8")
    block = _function_block(js, "async function deleteEntitiesFromMap(")
    assert "const namesSet = new Set(names)" in block
    assert "await saveConfigToSession()" in block
    assert block.count("initOntologyMap()") == 1
    assert "title: 'Delete entities'" in block
    assert "typeof showConfirmDialog !== 'function'" in block
    assert block.count("showConfirmDialog(") == 1
    assert "async function createBusinessViewFromSelection(names)" in js


def test_multi_business_view_keeps_only_internal_links():
    js = MAP_JS.read_text(encoding="utf-8")
    block = _function_block(js, "async function createBusinessViewFromSelection(")
    assert "const visibleNames = new Set(names)" in block
    assert "visibleNames.has(source) && visibleNames.has(target)" in block
    assert "let viewName = 'Auto_Selection'" in block
    assert "const cx = 450, cy = 280, radius = 230" in block
    assert "hiddenEntities" in block
    assert "hiddenRelationships" in block
    assert "hiddenInheritances" in block
    assert "/domain/design-views/create" in block
    assert "/domain/design-views/switch" in block
    assert "/domain/design-views/save-current" in block
    assert "SidebarNav.switchTo('design')" in block
    assert "neighbourNames" not in block


def test_single_entity_business_view_stays_one_hop():
    js = MAP_JS.read_text(encoding="utf-8")
    block = _function_block(js, "async function createBusinessViewFromEntity(")
    assert "let viewName = `Auto_${selectedName}`" in block
    assert "const neighbourNames = new Set()" in block
    assert "const allEntityNames = [selectedName, ...Array.from(neighbourNames)]" in block
