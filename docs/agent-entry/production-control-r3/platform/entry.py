"""Single deterministic entry template. No per-task JavaScript or inline solution."""
import html,posixpath
def render_entry(entry,manifest,manifest_sha,reader):
    assert posixpath.dirname(entry)==posixpath.dirname(manifest)
    rel=posixpath.relpath(reader,posixpath.dirname(entry) or ".")
    m=html.escape(posixpath.basename(manifest),quote=True);r=html.escape(rel,quote=True)
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Protected learning candidate — HOLD</title><style>body{{font:16px system-ui;max-width:900px;margin:auto;padding:18px}}section{{border:1px solid #9eb7c2;border-radius:10px;padding:16px;margin:12px 0}}label{{display:block;margin:12px 0}}input,select,textarea,button{{font:inherit;display:block;max-width:100%;box-sizing:border-box;margin:6px 0;padding:8px}}textarea{{width:100%}}pre{{white-space:pre-wrap;overflow-wrap:anywhere}}button{{min-height:44px}}</style></head><body><h1>Protected learning candidate</h1><p id="status" role="status">Loading</p><main data-assessment data-manifest="{m}" data-pin="{manifest_sha}"></main><script type="module" src="{r}"></script></body></html>\n'''.encode("utf-8")
