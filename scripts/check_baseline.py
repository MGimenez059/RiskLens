"""Check repository artifacts without implementing RiskLens product behavior."""

from __future__ import annotations

import ast
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
REQ = re.compile(r"(?:FR|NFR)-[A-Z]+-\d{3}")


def documents(root: Path) -> list[Path]:
    paths = list(root.glob("*.md"))
    for directory in ("docs", "prompts", "data"):
        paths.extend((root / directory).rglob("*.md"))
    return sorted(paths)


def metadata_and_style_errors(root: Path) -> list[str]:
    errors: list[str] = []
    for path in documents(root):
        content = path.read_text(encoding="utf-8")
        label = path.relative_to(root)
        for field, pattern in (
            ("Status", r"^Status: (Draft|Proposed|Accepted|Deprecated|Superseded)$"),
            ("Version", r"^Version: \d+\.\d+(?:\.\d+)?$"),
            ("Last Updated", r"^Last Updated: \d{4}-\d{2}-\d{2}$"),
        ):
            if not re.search(pattern, content, re.MULTILINE):
                errors.append(f"{label}: missing or invalid {field}")
        for number, line in enumerate(content.splitlines(), 1):
            if any(
                ord(char) in (0x2013, 0x2014, 0xFE0F)
                or 0x1F000 <= ord(char) <= 0x1FAFF
                or 0x2600 <= ord(char) <= 0x27BF
                for char in line
            ):
                errors.append(f"{label}:{number}: prohibited decorative punctuation or emoji")
    return errors


def link_errors(root: Path) -> list[str]:
    errors: list[str] = []
    for path in documents(root):
        for match in LINK.finditer(path.read_text(encoding="utf-8")):
            target = match.group(1).strip("<>")
            if "://" in target or target.startswith(("#", "mailto:")):
                continue
            target = unquote(target.split("#", 1)[0])
            if target and not (path.parent / target).exists():
                errors.append(f"{path.relative_to(root)}: broken local link {target}")
    return errors


def traceability_errors(root: Path) -> list[str]:
    requirements = root / "docs/01-requirements"
    functional = (requirements / "functional-requirements.md").read_text(encoding="utf-8")
    nonfunctional = (requirements / "non-functional-requirements.md").read_text(encoding="utf-8")
    defined = set(re.findall(r"^## (FR-[A-Z]+-\d{3}):", functional, re.MULTILINE))
    defined.update(re.findall(r"^\| (NFR-[A-Z]+-\d{3}) \|", nonfunctional, re.MULTILINE))
    matrix = (root / "docs/05-testing/traceability.md").read_text(encoding="utf-8")
    rows = re.findall(r"^\| ((?:FR|NFR)-[A-Z]+-\d{3}) \|(.+)$", matrix, re.MULTILINE)
    actual = [identifier for identifier, _ in rows]
    errors = [f"traceability: missing {item}" for item in sorted(defined - set(actual))]
    errors += [f"traceability: undefined {item}" for item in sorted(set(actual) - defined)]
    if len(actual) != len(set(actual)):
        errors.append("traceability: duplicate requirement row")
    for identifier, row in rows:
        cells = [cell.strip() for cell in row.strip("|").split("|")]
        if len(cells) != 7 or any(not cell for cell in cells):
            errors.append(f"traceability: incomplete mapping for {identifier}")
    criteria = (requirements / "acceptance-criteria.md").read_text(encoding="utf-8")
    covered = set(REQ.findall(criteria))
    for identifier in sorted(item for item in defined if item.startswith("FR-")):
        if identifier not in covered:
            errors.append(f"acceptance criteria: missing {identifier}")
    return errors


def domain_boundary_errors(root: Path) -> list[str]:
    errors: list[str] = []
    domain = root / "src/risklens/domain"
    # Domain imports only standard-library pure helpers or its own modules.
    blocked_stdlib = {"sqlite3", "socket", "subprocess", "http", "urllib"}
    for path in domain.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            modules: list[str] = []
            if isinstance(node, ast.Import):
                modules = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                if node.level:
                    if node.level > 1:
                        errors.append(f"{path.relative_to(root)}: outward relative import")
                    continue
                modules = [node.module or ""]
            for module in modules:
                top = module.split(".", 1)[0]
                own = module == "risklens.domain" or module.startswith("risklens.domain.")
                if not own and (top not in sys.stdlib_module_names or top in blocked_stdlib):
                    errors.append(f"{path.relative_to(root)}: forbidden domain import {module}")
    return errors


def identifier_errors(root: Path) -> list[str]:
    sources = {
        "P": "docs/00-project/principles.md",
        "GOV": "docs/00-project/baseline.md",
        "STYLE": "docs/00-project/writing-policy.md",
        "OQ": "docs/00-project/open-questions.md",
        "FR": "docs/01-requirements/functional-requirements.md",
        "NFR": "docs/01-requirements/non-functional-requirements.md",
        "AC": "docs/01-requirements/acceptance-criteria.md",
        "BR": "docs/02-domain/business-rules.md",
        "CT": "docs/02-domain/data-contracts.md",
        "EVAL": "docs/04-ai/evaluation-spec.md",
        "TOOL": "docs/04-ai/tool-contracts.md",
        "PROMPT": "docs/04-ai/prompt-specs.md",
        "AI": "docs/04-ai/agent-responsibilities.md",
    }
    known: set[str] = set()
    for prefix, relative in sources.items():
        content = (root / relative).read_text(encoding="utf-8")
        definition_pattern = rf"^(?:## |\| |- \*\*)({prefix}(?:-[A-Z]+)*-\d{{3}})\b"
        known.update(re.findall(definition_pattern, content, re.MULTILINE))
    for path in (root / "docs/adr").glob("ADR-*.md"):
        match = re.match(r"# (ADR-\d{3}):", path.read_text(encoding="utf-8"))
        if match:
            known.add(match.group(1))
    prefixes = "|".join([*sources, "ADR"])
    reference_pattern = re.compile(rf"\b((?:{prefixes})(?:-[A-Z]+)*-\d{{3}}(?:/\d{{3}})*)\b")
    errors: list[str] = []
    for path in documents(root):
        for match in reference_pattern.finditer(path.read_text(encoding="utf-8")):
            first, *suffixes = match.group(1).split("/")
            base = first.rsplit("-", 1)[0]
            for identifier in [first, *(f"{base}-{suffix}" for suffix in suffixes)]:
                if identifier not in known:
                    errors.append(f"{path.relative_to(root)}: undefined identifier {identifier}")
    return sorted(set(errors))


def main() -> int:
    errors = (
        metadata_and_style_errors(ROOT)
        + link_errors(ROOT)
        + traceability_errors(ROOT)
        + domain_boundary_errors(ROOT)
        + identifier_errors(ROOT)
    )
    if errors:
        print("\n".join(errors))
        return 1
    print(f"Baseline checks passed for {len(documents(ROOT))} Markdown documents.")
    print("These checks do not validate product behavior, English quality or semantic grounding.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
