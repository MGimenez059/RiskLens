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


def specification_records(path: Path, prefix: str) -> dict[str, str]:
    content = path.read_text(encoding="utf-8")
    expression = rf"^## ({prefix}(?:-[A-Z]+)*-\d{{3}}):.*?(?=^## |\Z)"
    return {
        match.group(1): match.group(0)
        for match in re.finditer(expression, content, re.MULTILINE | re.DOTALL)
    }


def milestone_errors(root: Path) -> list[str]:
    errors: list[str] = []
    requirements = root / "docs/01-requirements"
    functional = specification_records(requirements / "functional-requirements.md", "FR")
    criteria = specification_records(requirements / "acceptance-criteria.md", "AC")
    contracts = specification_records(root / "docs/02-domain/data-contracts.md", "CT")
    expected = {
        "FR-DQ-001": "M02",
        "FR-DQ-002": "M02",
        "FR-DQ-003": "M02",
        "FR-RISK-001": "M02",
        "FR-RISK-002": "M03",
        "FR-RISK-003": "M03",
        "FR-AI-001": "M03",
        "FR-AI-002": "M04",
        "FR-AI-003": "M04",
        "FR-UI-001": "M02",
        "FR-UI-002": "M04",
        "FR-OBS-001": "M02",
        "FR-OBS-002": "M03",
        "FR-OBS-003": "M02",
        "AC-AI-001": "M03",
        "AC-AI-002": "M04",
        "AC-AI-003": "M04",
        "AC-UI-001": "M02",
        "AC-UI-002": "M04",
    }
    for identifier, stage in expected.items():
        record = {**functional, **criteria}.get(identifier, "")
        pattern = rf"^\s*(?:- )?Applicability: {stage}\b"
        if not re.search(pattern, record, re.MULTILINE):
            errors.append(f"milestone: {identifier} requires explicit {stage} applicability")
    for identifier, record in {**functional, **criteria, **contracts}.items():
        if not re.search(r"^\s*(?:- )?Status: (Proposed|Accepted|Deprecated)$", record, re.M):
            errors.append(f"specification: missing per-ID status for {identifier}")
        if not re.search(r"^\s*(?:- )?Applicability: .+$", record, re.M):
            errors.append(f"specification: missing applicability for {identifier}")
    if re.search(r"\bdefault_rate\b", contracts.get("CT-004", ""), re.I):
        errors.append("active-v1 metric schema must not contain the deferred default_rate field")
    request = contracts.get("CT-016", "")
    stage_row = next((line for line in request.splitlines() if "| requested_stages |" in line), "")
    if "Exactly validate_portfolio, calculate_metrics." not in stage_row:
        errors.append("M02 request stages must be explicit validation and deterministic metrics")
    if re.search(r"human_review|pending_review|generate_insights|retrieve_policy", stage_row):
        errors.append("M02 request cannot require AI, policy or human-review stages")
    synthesis = functional.get("FR-AI-001", "").lower()
    insight = contracts.get("CT-008", "").lower()
    if "empty recommendations in m03" not in synthesis or "recommendations is empty" not in insight:
        errors.append("M03 synthesis must explicitly prohibit business-action recommendations")
    graph = (root / "docs/03-architecture/graph-spec.md").read_text(encoding="utf-8")
    for node in ("analyze_risk", "generate_insights", "validate_insights"):
        row = next((line for line in graph.splitlines() if line.startswith(f"| {node} |")), "")
        cells = [cell.strip() for cell in row.strip("|").split("|")]
        transition = cells[-2] if len(cells) == 8 else ""
        if "review_gate" in transition:
            if "M04" not in transition or not re.search(
                r"finalize in M03|M03 finalize", transition
            ):
                errors.append(f"M03 graph route for {node} cannot require review_gate")
    return errors


def contract_traceability_errors(root: Path) -> list[str]:
    defined = specification_records(root / "docs/02-domain/data-contracts.md", "CT")
    matrix = (root / "docs/05-testing/traceability.md").read_text(encoding="utf-8")
    rows = re.findall(r"^\| (CT-\d{3}) \|(.+)$", matrix, re.MULTILINE)
    mapped = [identifier for identifier, _ in rows]
    errors = [
        f"contract traceability: missing {item}" for item in sorted(set(defined) - set(mapped))
    ]
    if len(mapped) != len(set(mapped)):
        errors.append("contract traceability: duplicate contract row")
    for identifier, row in rows:
        if identifier not in defined:
            errors.append(f"contract traceability: unknown {identifier}")
        if not REQ.search(row):
            errors.append(f"contract traceability: {identifier} has no requirement mapping")
    return errors


def acceptance_and_identity_errors(root: Path) -> list[str]:
    errors: list[str] = []
    mixed = (
        "docs/01-requirements/functional-requirements.md",
        "docs/01-requirements/non-functional-requirements.md",
        "docs/01-requirements/acceptance-criteria.md",
        "docs/02-domain/business-rules.md",
        "docs/02-domain/data-contracts.md",
        "docs/02-domain/domain-model.md",
    )
    for relative in mixed:
        content = (root / relative).read_text(encoding="utf-8")
        first = re.search(r"^Status: (\w+)$", content, re.M)
        if first and first.group(1) == "Accepted":
            rest = content[first.end() :]
            if re.search(r"^\s*(?:- )?Status: Proposed|^\| [^|]+ \| Proposed \|", rest, re.M):
                errors.append(
                    f"acceptance: mixed-stage document cannot be blanket Accepted: {relative}"
                )
    rules = (root / "docs/02-domain/business-rules.md").read_text(encoding="utf-8")
    identity = next((line for line in rules.splitlines() if "| BR-DQ-001 |" in line), "")
    if "globally unique" not in identity or "exactly one portfolio_id owner" not in identity:
        errors.append(
            "snapshot identity: global uniqueness and exactly one portfolio owner required"
        )
    if "portfolio_id plus snapshot_id" in identity:
        errors.append("snapshot identity: composite-only identity conflicts with global references")
    return errors


def main() -> int:
    errors = (
        metadata_and_style_errors(ROOT)
        + link_errors(ROOT)
        + traceability_errors(ROOT)
        + domain_boundary_errors(ROOT)
        + identifier_errors(ROOT)
        + milestone_errors(ROOT)
        + contract_traceability_errors(ROOT)
        + acceptance_and_identity_errors(ROOT)
    )
    if errors:
        print("\n".join(errors))
        return 1
    print(f"Baseline checks passed for {len(documents(ROOT))} Markdown documents.")
    print("These checks do not validate product behavior, English quality or semantic grounding.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
