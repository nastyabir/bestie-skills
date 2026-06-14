from build_readme import render_readme

ENTRY_A = {
    "frontmatter": {
        "name": "alpha", "source_url": "https://e.com/a", "author": "a",
        "license": "MIT", "agents": ["claude-code"], "category": "coding",
        "summary": "Alpha skill.", "use_cases": ["x"], "why": "w",
        "status": "tested", "security": "pass",
        "added_by": "n", "added_date": "2026-06-15",
    },
    "body": "", "path": "entries/alpha.md",
}
ENTRY_B = {
    "frontmatter": {
        "name": "beta", "source_url": "https://e.com/b", "author": "b",
        "license": "MIT", "agents": ["codex"], "category": "workflow",
        "summary": "Beta skill.", "use_cases": ["y"], "why": "w",
        "status": "untested", "security": "manual-review",
        "added_by": "n", "added_date": "2026-06-15",
    },
    "body": "", "path": "entries/beta.md",
}


def test_render_includes_generated_header():
    out = render_readme([ENTRY_A])
    assert "auto-generated" in out.lower()


def test_render_links_skill_to_source():
    out = render_readme([ENTRY_A])
    assert "[alpha](https://e.com/a)" in out


def test_render_groups_by_category():
    out = render_readme([ENTRY_A, ENTRY_B])
    assert "## coding" in out
    assert "## workflow" in out
    assert out.index("alpha") < out.index("## workflow")


def test_render_shows_agents_and_badges():
    out = render_readme([ENTRY_B])
    assert "codex" in out
    assert "untested" in out
    assert "manual-review" in out
