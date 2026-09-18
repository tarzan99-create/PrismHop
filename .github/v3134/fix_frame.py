from pathlib import Path
p=Path('android/app/src/main/java/com/zarivostudios/prismhop/MainActivity.java')
s=p.read_text()
old='''        if (Build.VERSION.SDK_INT >= 30) {
            try { webView.setFrameRate(60.0f, View.FRAME_RATE_COMPATIBILITY_FIXED_SOURCE); } catch (Exception ignored) {}
        }'''
alt='''        if (Build.VERSION.SDK_INT >= 30) {
            try { webView.setFrameRate(60.0f, Surface.FRAME_RATE_COMPATIBILITY_FIXED_SOURCE); } catch (Exception ignored) {}
        }'''
if old not in s and alt not in s:
    raise SystemExit('frame-rate block target missing')
if 'import android.view.WindowManager;' not in s:
    s=s.replace('import android.view.View;','import android.view.View;\nimport android.view.WindowManager;',1)
block='''        try {
            WindowManager.LayoutParams frameParams = getWindow().getAttributes();
            frameParams.preferredRefreshRate = 60.0f;
            getWindow().setAttributes(frameParams);
        } catch (Exception ignored) {}'''
s=s.replace(old if old in s else alt,block,1)
s=s.replace('import android.view.Surface;\n','')
p.write_text(s)
print('V3.13.4 Android preferred refresh rate fixed')
