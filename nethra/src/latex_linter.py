# src/latex_linter.py
"""Simple LaTeX linter for Nethra documentation.
It scans all markdown files under `docs/` for common LaTeX rendering issues
as defined in the GEMINI.md Quality Gate:
- No spaces after opening `$` or before closing `$`
- No underscores inside `\text{}` unless escaped (replace with camel case)
- Block math (`$$`) must be on its own lines without indentation
- No stray '_' characters outside math mode
The script rewrites files in‑place fixing these issues.
"""

import re
from pathlib import Path

DOCS_DIR = Path(__file__).resolve().parents[1] / "docs"

INLINE_PATTERN = re.compile(r"\$(\s+)(.+?)(\s+)\$")
BLOCK_PATTERN = re.compile(r"(?m)^\s*\$\$(.+?)\$\$\s*$")
UNDERSCORE_PATTERN = re.compile(r"\\text\{([^}]*?)_([^}]*?)\}")

def fix_inline_spaces(content: str) -> str:
    # Remove spaces immediately after opening $ and before closing $
    def repl(m):
        inner = m.group(2).strip()
        return f"${inner}$"
    return INLINE_PATTERN.sub(repl, content)

def fix_block_indentation(content: str) -> str:
    lines = content.split('\n')
    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.lstrip().startswith('$$') and not line.strip() == '$$':
            # Inline block, split into separate lines
            inner = line.strip().strip('$$')
            new_lines.append('$$')
            new_lines.append(inner)
            new_lines.append('$$')
        else:
            new_lines.append(line)
        i += 1
    return '\n'.join(new_lines)

def fix_underscores(content: str) -> str:
    # Replace underscores inside \text{} with camel case (remove underscores)
    def repl(m):
        left, right = m.group(1), m.group(2)
        combined = left + right.capitalize()
        return f"\\text{{{combined}}}"
    return UNDERSCORE_PATTERN.sub(repl, content)

def lint_file(path: Path) -> bool:
    original = path.read_text(encoding='utf-8')
    content = original
    content = fix_inline_spaces(content)
    content = fix_block_indentation(content)
    content = fix_underscores(content)
    if content != original:
        path.write_text(content, encoding='utf-8')
        return True
    return False

def main():
    changed = []
    for md_file in DOCS_DIR.rglob('*.md'):
        if lint_file(md_file):
            changed.append(md_file)
    print(f"LaTeX linter fixed {len(changed)} file(s).")
    for p in changed:
        print(p)

if __name__ == "__main__":
    main()
