from pathlib import Path
import gzip,base64
root=Path('android')
p=root/'app/src/main/assets/index.html'
s=p.read_text()
if '3.13.4-android' not in s: raise SystemExit('v3134 marker missing')
s=s.replace('3.13.4-android','3.13.5-android',1)

css = """
<style id="v3135-spotlight-prestige">
.social-row,.social-link,.profile-social,.spotlight-social,[data-social],a[href*="instagram.com"],a[href*="tiktok.com"],a[href*="youtube.com"],a[href*="facebook.com"]{display:none!important}
#spotlight-prestige-card{margin:10px 0 12px;padding:14px 13px;border:1px solid rgba(255,255,255,.13);border-radius:18px;background:linear-gradient(135deg,rgba(255,255,255,.055),rgba(255,255,255,.018));text-align:center;overflow:hidden}
.sp-crown{position:relative;width:82px;height:70px;margin:0 auto 5px;filter:drop-shadow(0 0 14px rgba(255,220,120,.38));animation:spCrownFloat 2.8s ease-in-out infinite}
.sp-crown:before{content:"";position:absolute;left:10px;right:10px;bottom:9px;height:24px;border:2px solid rgba(255,225,145,.9);clip-path:polygon(0 100%,0 42%,18% 65%,34% 0,50% 60%,68% 0,83% 65%,100% 42%,100% 100%);background:linear-gradient(90deg,rgba(96,238,211,.18),rgba(255,220,130,.3),rgba(235,113,181,.18))}
.sp-crown:after{content:"";position:absolute;inset:2px 17px 22px;border-radius:50%;border:1px solid rgba(255,255,255,.35);box-shadow:0 0 14px rgba(255,255,255,.18)}
@keyframes spCrownFloat{50%{transform:translateY(-4px) rotate(1.5deg)}}
.sp-kicker{font:800 9px Oxanium,sans-serif;letter-spacing:2.2px;color:#ffd991}.sp-name{font:800 19px Oxanium,sans-serif;margin:2px 0}.sp-score{font:700 28px Oxanium,sans-serif}.sp-title{font:600 9px Oxanium,sans-serif;letter-spacing:1.2px;color:#b9bfd2}.sp-chase{margin-top:9px;font:700 10px Oxanium,sans-serif;letter-spacing:.8px;color:#aef3e2}
.sp-podium{display:grid;grid-template-columns:1fr 1fr 1fr;gap:7px;margin-top:10px}.sp-place{border:1px solid rgba(255,255,255,.1);border-radius:12px;padding:8px 4px;background:rgba(255,255,255,.025)}.sp-place b{display:block;font:800 9px Oxanium,sans-serif}.sp-place small{font:600 7px Oxanium,sans-serif;color:#969db1}
.sp-legacy{display:grid;grid-template-columns:repeat(4,1fr);gap:5px;margin-top:10px}.sp-stat{padding:7px 2px;border-radius:10px;background:rgba(255,255,255,.035)}.sp-stat b{display:block;font:800 13px Oxanium,sans-serif}.sp-stat small{font:600 6px Oxanium,sans-serif;letter-spacing:.7px;color:#8991a7}
.sp-run-chase{position:absolute;top:74px;left:50%;transform:translateX(-50%);z-index:12;padding:5px 10px;border-radius:999px;background:rgba(5,8,18,.72);border:1px solid rgba(255,255,255,.12);font:700 8px Oxanium,sans-serif;letter-spacing:1px;pointer-events:none;opacity:0;transition:opacity .22s}.sp-run-chase.show{opacity:.9}.sp-run-chase.crown{color:#ffe19b;box-shadow:0 0 18px rgba(255,217,125,.16)}
@media(prefers-reduced-motion:reduce){.sp-crown{animation:none}}
</style>
"""
s=s.replace('</head>',css+'</head>',1)

target='<main'
if target not in s: raise SystemExit('race-card missing')
card="""<div id="spotlight-prestige-card" aria-live="polite">
<div class="sp-kicker">TODAY'S SPOTLIGHT</div><div class="sp-crown" aria-hidden="true"></div>
<div class="sp-name" id="sp-winner-name">THE CROWN AWAITS</div><div class="sp-score" id="sp-winner-score">—</div>
<div class="sp-title">Keeper of Today's Light</div><div class="sp-chase" id="sp-chase">Set the first verified score and take the Crown</div>
<div class="sp-podium"><div class="sp-place"><b>PRISM CROWN</b><small>#1 · Crown Holder</small></div><div class="sp-place"><b>LUMINOUS CREST</b><small>#2 · Radiant status</small></div><div class="sp-place"><b>FRACTURE CREST</b><small>#3 · Podium status</small></div></div>
<div class="sp-legacy"><div class="sp-stat"><b id="sp-crowns">0</b><small>CROWNS</small></div><div class="sp-stat"><b id="sp-podiums">0</b><small>PODIUMS</small></div><div class="sp-stat"><b id="sp-best">—</b><small>BEST</small></div><div class="sp-stat"><b id="sp-high">0</b><small>VERIFIED HIGH</small></div></div>
</div>"""
s=s.replace(target,card+target,1)

if '<div id="sp-run-chase"' not in s:
    s=s.replace('<canvas id="game"></canvas>','<canvas id="game"></canvas><div id="sp-run-chase" class="sp-run-chase"></div>',1)

runtime = r"""
<script id="v3135-spotlight-runtime">
(()=>{
 const st={crown:0,podium:0,loaded:false,last:""};
 const put=(id,v)=>{const e=document.getElementById(id);if(e)e.textContent=v};
 async function call(action){if(typeof supaFetch!=="function")return null;try{const r=await supaFetch(RUNS_URL,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({action:action})});return r&&r.ok?await r.json():null}catch(e){return null}}
 async function refresh(){
  const pair=await Promise.all([call("spotlight_showcase"),call("spotlight_legacy")]),show=pair[0],legacy=pair[1];
  if(show){const top=Array.isArray(show.top3)?show.top3:[],one=top[0];st.crown=Number(show.crown_score||0);st.podium=Number(show.podium_score||0);
   put("sp-winner-name",one?String(one.display_name||one.username||"PLAYER").replace(/[^A-Za-z0-9_ .-]/g,"").slice(0,24):"THE CROWN AWAITS");put("sp-winner-score",one?Number(one.score||0).toLocaleString():"—");
   const ch=document.getElementById("sp-chase");if(ch)ch.textContent=!one?"Set the first verified score and take the Crown":Number(show.my_position)===1?"YOU HOLD TODAY'S PRISM CROWN":Math.max(1,Number(show.to_crown||1)).toLocaleString()+" TO TAKE THE CROWN";
  }
  if(legacy){put("sp-crowns",Number(legacy.crowns||0));put("sp-podiums",Number(legacy.podiums||0));put("sp-best",legacy.best_finish?"#"+legacy.best_finish:"—");put("sp-high",Number(legacy.highest_verified||0).toLocaleString())}
  st.loaded=true;
 }
 function cue(){if(!st.loaded||typeof playing==="undefined"||!playing||typeof mode==="undefined"||mode!=="classic")return;const score=Number(points||0);let q="";
  if(st.crown>0&&score>st.crown)q="CROWN TAKEN";else if(st.crown>0&&st.crown-score<=25)q=Math.max(1,st.crown-score+1)+" TO #1";else if(st.podium>0&&st.podium-score<=75)q=Math.max(1,st.podium-score+1)+" TO PODIUM";
  if(!q||q===st.last)return;st.last=q;const e=document.getElementById("sp-run-chase");if(!e)return;e.textContent=q;e.classList.toggle("crown",q==="CROWN TAKEN");e.classList.add("show");clearTimeout(e._sp);e._sp=setTimeout(()=>e.classList.remove("show"),q==="CROWN TAKEN"?1700:1100)
 }
 setInterval(cue,350);setTimeout(refresh,900);document.addEventListener("visibilitychange",()=>{if(!document.hidden)refresh()});
 window.refreshSpotlightPrestige=refresh;window.prismSpotlightState=st;
})();
</script>
"""
s=s.replace('</body>',runtime+'</body>',1)
s=s.replace('LIVE VERIFIED TOP 3','LIVE VERIFIED TOP 3 · TAKE THE CROWN')

p.write_text(s)
(root/'app/src/main/assets/index.html.gz.b64').write_text(base64.b64encode(gzip.compress(s.encode(),9)).decode())

g=root/'app/build.gradle';gs=g.read_text()
if 'versionCode 51' not in gs: raise SystemExit('v51 missing')
g.write_text(gs.replace('versionCode 51','versionCode 52',1).replace("versionName '3.13.4-test'","versionName '3.13.5-test'",1))
a=root/'app/src/main/java/com/zarivostudios/prismhop/MainActivity.java';av=a.read_text()
if 'private static final String APP_VERSION = "3.13.4-test";' not in av: raise SystemExit('native v3134 missing')
a.write_text(av.replace('private static final String APP_VERSION = "3.13.4-test";','private static final String APP_VERSION = "3.13.5-test";',1))
print('V3.13.5 Spotlight Prestige applied')
