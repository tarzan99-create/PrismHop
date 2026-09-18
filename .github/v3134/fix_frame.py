from pathlib import Path
p=Path('android/app/src/main/java/com/zarivostudios/prismhop/MainActivity.java')
s=p.read_text()
if 'View.FRAME_RATE_COMPATIBILITY_FIXED_SOURCE' not in s:
    raise SystemExit('frame-rate compatibility target missing')
if 'import android.view.Surface;' not in s:
    s=s.replace('import android.view.View;','import android.view.View;\nimport android.view.Surface;',1)
s=s.replace('View.FRAME_RATE_COMPATIBILITY_FIXED_SOURCE','Surface.FRAME_RATE_COMPATIBILITY_FIXED_SOURCE',1)
p.write_text(s)
print('V3.13.4 Android frame-rate constant fixed')
