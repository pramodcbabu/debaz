# Strategic Operating Manual: Nethra Project

## LaTeX Rendering Check
- **No spaces** after opening `$` or before closing `$` (e.g., `$HM$`, not `$ HM $`).
- **Underscores** (`_`) are allowed **only inside** math mode (`$...$`). Plain text must not contain `_`.
- **Block math** must be wrapped with `$$` on a single line before and after the equation, with **no blank lines** inside the block.
- **Validation step**: Before any `git push` to GitHub, run `pandoc --from=markdown --to=html` (or `chktex`) on all `.md` files. The commit is blocked if any LaTeX errors are reported.

*This rule is now part of the project’s operational guidelines and must be adhered to for all documentation.*
