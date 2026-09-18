from pathlib import Path
import re, gzip, base64

root=Path('android')
html=root/'app/src/main/assets/index.html'
s=html.read_text()

if '3.9.2-android' not in s:
    raise SystemExit('Expected V3.9.2 client marker missing')
s=s.replace('3.9.2-android','3.13.2-android',1)

old="let hapticsOn=store.get('haptics',false)===true;"
if old not in s:
    old="let hapticsOn=store.get('haptics',true)!==false;"
if old not in s:
    raise SystemExit('Haptic state target missing')
new="""let hapticsOn=store.get('haptics',true)!==false;
if(store.get('haptics-v3132-migrated',false)!==true){hapticsOn=true;store.set('haptics',true);store.set('haptics-v3132-migrated',true);}"""
s=s.replace(old,new,1)

# Haptic Feedback and Gentle Motion are independent settings.
s=s.replace("if(!hapticsOn||reduceMotion||realNow-hapticAt<=.035)return false;","if(!hapticsOn||realNow-hapticAt<=.035)return false;",1)
s=s.replace("if(!hapticsOn||reduceMotion)return;\n  if(kind==='hop'","if(!hapticsOn)return;\n  if(kind==='hop'",1)
s=s.replace("if(!hapticsOn||reduceMotion||realNow-hapticAt<=.035)return;","if(!hapticsOn||realNow-hapticAt<=.035)return;",1)

# Remove developer/web-prototype material from the public Settings page.
block=re.search(r'''      <label class="toggle-row"><span>Touch vibration<small>Where your browser supports it</small></span><input id="haptics" type="checkbox"></label>\n      <p class="mix-help" id="audio-status">Music starts when you play\.</p>\n      <section class="offline-settings".*?<details class="typography-settings">.*?</details>''',s,re.S)
if not block:
    raise SystemExit('Public Settings cleanup target missing')
replacement='''      <label class="toggle-row haptic-setting"><span>Haptic feedback<small>Tactile response for hops, Perfects and impacts</small></span><input id="haptics" type="checkbox"></label>
      <p class="mix-help" id="audio-status">Music starts when you play.</p>
      <div id="release-internal-controls" hidden aria-hidden="true"><p id="offline-copy"></p><p id="offline-ready"></p><input type="checkbox" id="personal-only"></div>'''
s=s[:block.start()]+replacement+s[block.end():]

# Keep compatibility nodes silent; do not expose implementation details to players.
s=s.replace("$('offline-copy').textContent='Personal play works offline. Online Classic runs use a server-issued sequence, event checkpoints and deterministic replay. Loss of connection keeps the run personal. Google Play Integrity is required for V3.7 Android competitive runs. Personal play remains available if attestation cannot be completed.';","$('offline-copy').textContent='';",1)

needle=" DEVICE_ATTESTATION_FAILED:'This Play build or device did not pass the competitive integrity check. Personal play still works.'"
repl=""" INVALID_REQUEST:'This version could not start a verified run. Update Prism Hop and try again.',
 DEVICE_ATTESTATION_FAILED:'Google Play could not verify this install for competitive scoring. Install Prism Hop from the Google Play testing track, then try again.'"""
if needle not in s:
    raise SystemExit('Competitive message target missing')
s=s.replace(needle,repl,1)

release_css='''
<style id="v3132-release-settings">
/* V3.13.2 — public release settings cleanup. */
#mixer{justify-content:flex-start!important;overflow-y:auto!important;-webkit-overflow-scrolling:touch!important;overscroll-behavior:contain!important;padding-bottom:calc(28px + env(safe-area-inset-bottom))!important}
#mixer .mixer-card{margin:0 auto!important;padding-bottom:8px!important}
#mixer #close-mix{position:static!important;bottom:auto!important;z-index:auto!important;margin:22px 0 6px!important;box-shadow:none!important}
.soundtrack-grid .track-card:first-child::after{left:42px!important;right:auto!important;top:12px!important;font-size:6px!important;letter-spacing:1.15px!important;max-width:96px!important;white-space:nowrap!important}
.soundtrack-grid .track-card:first-child .track-bars{right:14px!important;top:12px!important}
.haptic-setting span>small{color:#9fa6bd!important}
@media(max-width:380px){.soundtrack-grid .track-card:first-child::after{left:39px!important;font-size:5.5px!important}.track-card{padding-left:11px!important;padding-right:11px!important}}
</style>
'''
s=s.replace('</head>',release_css+'</head>',1)

ui_haptic='''
<script id="v3132-ui-haptics">
(()=>{
 let last=0;
 document.addEventListener('pointerdown',event=>{
  if(!hapticsOn)return;
  const control=event.target.closest?.('button,input[type="checkbox"],select,summary');
  if(!control||control.disabled||control.closest('#playing'))return;
  const now=performance.now();if(now-last<55)return;last=now;
  try{window.PrismNative?.haptic?.('ui');}catch{}
 },{passive:true});
})();
</script>
'''
s=s.replace('</body>',ui_haptic+'</body>',1)

html.write_text(s)
(root/'app/src/main/assets/index.html.gz.b64').write_text(base64.b64encode(gzip.compress(s.encode(),9)).decode())

gradle=root/'app/build.gradle'
g=gradle.read_text()
if 'versionCode 43' not in g or "versionName '3.9.2-test'" not in g:
    raise SystemExit('Expected V3.9.2 Gradle version missing')
g=g.replace('versionCode 43','versionCode 49',1).replace("versionName '3.9.2-test'","versionName '3.13.2-test'",1)
gradle.write_text(g)

activity=root/'app/src/main/java/com/zarivostudios/prismhop/MainActivity.java'
a=activity.read_text()
old='private static final String APP_VERSION = "3.9.2-test";'
if old not in a:
    raise SystemExit('Expected V3.9.2 native version missing')
a=a.replace(old,'private static final String APP_VERSION = "3.13.2-test";',1)

old_event=re.search(r'''    private void hapticEvent\(String kind\) \{.*?\n    \}\n\n    private final class PrismNativeBridge''',a,re.S)
if not old_event:
    raise SystemExit('Native haptic target missing')
new_event='''    private Vibrator prismVibrator() {
        if (Build.VERSION.SDK_INT >= 31) return getSystemService(VibratorManager.class).getDefaultVibrator();
        return (Vibrator) getSystemService(VIBRATOR_SERVICE);
    }

    private void tactile(int effect, String fallbackPattern) {
        try {
            Vibrator vibrator = prismVibrator();
            if (vibrator == null || !vibrator.hasVibrator()) return;
            if (Build.VERSION.SDK_INT >= 29) vibrator.vibrate(VibrationEffect.createPredefined(effect));
            else vibrate(fallbackPattern);
        } catch (Exception ignored) { vibrate(fallbackPattern); }
    }

    private void hapticEvent(String kind) {
        switch(kind==null?"":kind){
            case "ui" -> tactile(VibrationEffect.EFFECT_TICK,"[6]");
            case "hop" -> tactile(VibrationEffect.EFFECT_TICK,"[7]");
            case "pass" -> tactile(VibrationEffect.EFFECT_CLICK,"[9]");
            case "perfect" -> tactile(VibrationEffect.EFFECT_DOUBLE_CLICK,"[11,18,14]");
            case "close" -> tactile(VibrationEffect.EFFECT_CLICK,"[10]");
            case "shard" -> tactile(VibrationEffect.EFFECT_TICK,"[7]");
            case "fragment" -> tactile(VibrationEffect.EFFECT_DOUBLE_CLICK,"[10,16,12]");
            case "milestone" -> tactile(VibrationEffect.EFFECT_DOUBLE_CLICK,"[12,19,14]");
            case "flow" -> tactile(VibrationEffect.EFFECT_HEAVY_CLICK,"[15,22,18]");
            case "shield-ready" -> tactile(VibrationEffect.EFFECT_DOUBLE_CLICK,"[9,16,9]");
            case "shield-break" -> tactile(VibrationEffect.EFFECT_HEAVY_CLICK,"[19,20,13]");
            case "death" -> vibrate("[30,22,42]");
            case "start" -> tactile(VibrationEffect.EFFECT_CLICK,"[8]");
            case "echo" -> tactile(VibrationEffect.EFFECT_DOUBLE_CLICK,"[10,17,10]");
            default -> tactile(VibrationEffect.EFFECT_CLICK,"[8]");
        }
    }

    private final class PrismNativeBridge'''
a=a[:old_event.start()]+new_event+a[old_event.end():]
activity.write_text(a)

print('V3.13.2 release cleanup applied')
