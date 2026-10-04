#!/usr/bin/env python3
"""Validação estática do plugin product-tools (somente stdlib).

Verifica: JSON dos manifestos, frontmatter de skills e agentes, nomes iguais ao
diretório/arquivo, ferramentas conhecidas nos agentes, hooks e links relativos
para arquivos de referência. Uso: python3 scripts/validate.py
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
errors: list[str] = []
KNOWN_TOOLS = {
    "Read", "Write", "Edit", "Bash", "Glob", "Grep", "WebSearch", "WebFetch",
    "NotebookEdit", "ToolSearch", "Agent", "Task", "Skill", "TodoWrite",
}


def err(msg: str) -> None:
    errors.append(msg)


def frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        err(f"{path.relative_to(ROOT)}: frontmatter ausente")
        return {}
    fm: dict[str, str] = {}
    key = None
    for line in m.group(1).splitlines():
        km = re.match(r"^([A-Za-z][\w-]*):\s*(.*)$", line)
        if km:
            key = km.group(1)
            fm[key] = km.group(2).strip().lstrip(">|").strip()
        elif key and line.startswith((" ", "\t")):
            fm[key] = (fm[key] + " " + line.strip()).strip()
    return fm


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        err(f"{path.relative_to(ROOT)}: JSON inválido ({e})")
        return None


# --- manifestos
plugin = load_json(ROOT / ".claude-plugin" / "plugin.json") or {}
market = load_json(ROOT / ".claude-plugin" / "marketplace.json") or {}
for field in ("name", "version", "description"):
    if not plugin.get(field):
        err(f"plugin.json: campo obrigatório ausente: {field}")
for key, cfg in (plugin.get("userConfig") or {}).items():
    for f in ("type", "title", "description"):
        if f not in cfg:
            err(f"plugin.json: userConfig.{key} sem '{f}'")
for p in market.get("plugins", []):
    if p.get("name") != plugin.get("name"):
        err("marketplace.json: nome do plugin difere de plugin.json")
    if "version" in p:
        err("marketplace.json: não duplique 'version' (vale a de plugin.json)")

# --- skills
skill_names = set()
for skill in sorted((ROOT / "skills").glob("*/SKILL.md")):
    fm = frontmatter(skill)
    name = fm.get("name")
    skill_names.add(name)
    if name != skill.parent.name:
        err(f"{skill.relative_to(ROOT)}: name '{name}' difere do diretório")
    desc = fm.get("description", "")
    if not desc:
        err(f"{skill.relative_to(ROOT)}: description ausente")
    elif len(desc) > 1536:
        err(f"{skill.relative_to(ROOT)}: description > 1536 caracteres")
    lines = skill.read_text(encoding="utf-8").count("\n")
    if lines > 500:
        err(f"{skill.relative_to(ROOT)}: {lines} linhas (> 500; mova detalhe para references/)")
    for ref in re.findall(r"`(references/[^`\s]+)`", skill.read_text(encoding="utf-8")):
        if not (skill.parent / ref).exists():
            err(f"{skill.relative_to(ROOT)}: referência inexistente {ref}")

# --- agentes
for agent in sorted((ROOT / "agents").glob("*.md")):
    fm = frontmatter(agent)
    if fm.get("name") != agent.stem:
        err(f"{agent.relative_to(ROOT)}: name '{fm.get('name')}' difere do arquivo")
    if not fm.get("description"):
        err(f"{agent.relative_to(ROOT)}: description ausente")
    tools = fm.get("tools", "")
    for t in [x.strip() for x in tools.split(",") if x.strip()]:
        if t not in KNOWN_TOOLS and not t.startswith("mcp__"):
            err(f"{agent.relative_to(ROOT)}: ferramenta desconhecida '{t}'")
    if "../" in agent.read_text(encoding="utf-8"):
        err(f"{agent.relative_to(ROOT)}: caminho relativo '../' (quebra no cache do plugin)")

# --- hooks
hooks = load_json(ROOT / "hooks" / "hooks.json")
for script in (ROOT / "hooks").glob("*.sh"):
    r = subprocess.run(["bash", "-n", str(script)], capture_output=True, text=True)
    if r.returncode:
        err(f"{script.relative_to(ROOT)}: erro de sintaxe: {r.stderr.strip()}")
if hooks:
    for groups in hooks.get("hooks", {}).values():
        for g in groups:
            for h in g.get("hooks", []):
                m = re.search(r"hooks/([\w.-]+\.sh)", h.get("command", ""))
                if m and not (ROOT / "hooks" / m.group(1)).exists():
                    err(f"hooks.json: script inexistente {m.group(1)}")

# --- evals
for ev in ROOT.glob("skills/*/evals/*.json"):
    load_json(ev)

if errors:
    print("FALHOU:")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)
print(f"OK — {len(skill_names)} skills, {len(list((ROOT / 'agents').glob('*.md')))} agentes validados.")
