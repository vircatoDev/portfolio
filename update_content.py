#!/usr/bin/env python3
"""Embed content.json in the static site after editing project descriptions."""
import json
import re
from pathlib import Path
root = Path(__file__).resolve().parent
content = json.loads((root / 'content.json').read_text())
for project in content['projects']:
    for frame in project['frames']:
        if not (root / 'dist' / frame['image']).is_file():
            raise FileNotFoundError(frame['image'])
page = root / 'dist/index.html'
payload = json.dumps(content, ensure_ascii=False).replace('<', r'\u003c')
pattern = r'(<script type="application/json" id="op-project-data">).*?(</script>)'
updated, count = re.subn(pattern, lambda match: match[1] + payload + match[2], page.read_text(), flags=re.S)
if count != 1:
    raise RuntimeError('Expected one project data block')
page.write_text(updated)
print('Updated dist/index.html. Refresh your browser.')
