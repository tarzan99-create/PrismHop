from pathlib import Path
import base64,gzip

root=Path('android')
html=root/'app/src/main/assets/index.html'
s=html.read_text()
old="'pause-overlay'"
if s.count(old) != 2:
    raise SystemExit(f'expected 2 pause-overlay references, found {s.count(old)}')
s=s.replace(old,"'paused'")
html.write_text(s)
raw=html.read_bytes()
(root/'app/src/main/assets/index.html.gz.b64').write_text(base64.b64encode(gzip.compress(raw,9)).decode())
print('V3.9.2 paused Back target fixed')
