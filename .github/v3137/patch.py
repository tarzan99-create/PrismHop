from pathlib import Path
import gzip,base64

root=Path('android')
p=root/'app/src/main/assets/index.html'
s=p.read_text()
if '3.13.6-android' not in s:
    raise SystemExit('v3136 marker missing')

# Version.
s=s.replace('3.13.6-android','3.13.7-android',1)
s=s.replace('V3.13.6 · PRISM ORIGINALS','V3.13.7 · PRISM ORIGINALS',1)

# Keep the existing centre Prism/ring completely untouched: no Crown attachment.
old="card.classList.toggle('p3136-self-crown',me?.place===1);home.classList.toggle('p3136-self-crown',me?.place===1);"
new="card.classList.toggle('p3136-self-crown',me?.place===1);home.classList.remove('p3136-self-crown');"
if old not in s:
    raise SystemExit('v3136 centre-crown runtime anchor missing')
s=s.replace(old,new,1)

# Match the approved 2D concept: separate player name, score and crest label for #2/#3.
old_podium='''      <span class="p3136-podium-preview">
        <span class="p3136-podium p2"><i class="p3136-crest luminous" aria-hidden="true"></i><span><small>#2 · LUMINOUS CREST</small><b id="p3136-second">OPEN</b></span></span>
        <span class="p3136-podium p3"><i class="p3136-crest fracture" aria-hidden="true"></i><span><small>#3 · FRACTURE CREST</small><b id="p3136-third">OPEN</b></span></span>
      </span>'''
new_podium='''      <span class="p3136-podium-preview">
        <span class="p3136-podium p2"><span class="p3137-place">#2</span><i class="p3136-crest luminous" aria-hidden="true"></i><span class="p3137-podium-copy"><strong id="p3136-second">OPEN</strong><b id="p3137-second-score">—</b><small>LUMINOUS CREST</small></span></span>
        <span class="p3136-podium p3"><span class="p3137-place">#3</span><i class="p3136-crest fracture" aria-hidden="true"></i><span class="p3137-podium-copy"><strong id="p3136-third">OPEN</strong><b id="p3137-third-score">—</b><small>FRACTURE CREST</small></span></span>
      </span>'''
if old_podium not in s:
    raise SystemExit('v3136 podium markup anchor missing')
s=s.replace(old_podium,new_podium,1)

old_rows="  $('p3136-second').textContent=rowText(second,'OPEN');$('p3136-third').textContent=rowText(third,'OPEN');"
new_rows="""  $('p3136-second').textContent=second?safeName(second.name||second.username||'PLAYER'):'OPEN';$('p3137-second-score').textContent=second?fmt(second.score):'—';
  $('p3136-third').textContent=third?safeName(third.name||third.username||'PLAYER'):'OPEN';$('p3137-third-score').textContent=third?fmt(third.score):'—';"""
if old_rows not in s:
    raise SystemExit('v3136 podium runtime anchor missing')
s=s.replace(old_rows,new_rows,1)

# Use the same time casing as the approved concept.
s=s.replace("return ms<=0?'CLOSED':h+'H '+String(m).padStart(2,'0')+'M'",
            "return ms<=0?'CLOSED':h+'h '+String(m).padStart(2,'0')+'m'",1)

css=r'''
<style id="v3137-exact-home-prestige">
/* V3.13.7 — exact approved 2D Home composition. No changes to the centre ring animation. */
.home.p3136-self-crown .home-prism-orbit::before{display:none!important;content:none!important;animation:none!important}
.game .home{
  padding:84px 24px calc(var(--dock-height) + 4px)!important;
  overflow-y:hidden!important;
}
.game .home .eyebrow{margin:2px 0 10px!important;font-size:8px!important;letter-spacing:2.15px!important}
.game .home h1{font-size:56px!important;line-height:.88!important;letter-spacing:-2.8px!important}
.game .home .hero-space{min-height:78px!important;flex:0 0 78px!important;margin:4px 0 0!important}
.home-records{padding:9px 0!important;margin:0 0 9px!important}
.home-records > div{padding-top:0!important;padding-bottom:0!important}
.home-records small{font-size:7.5px!important}
.home-records strong{font-size:21px!important;margin:5px 0 4px!important}
.home-records span{font-size:8.5px!important}
.game .home .mode-switch{min-height:44px!important}
.game .home .mode-btn{min-height:40px!important;padding:6px!important;font-size:12px!important}
.mode-btn small{font-size:8.5px!important;margin-top:3px!important}
.game .home .mode-desc{font-size:9.5px!important;line-height:1.2!important;margin:6px 0 8px!important}
.game .home .play-hero{min-height:52px!important;height:52px!important;border-radius:17px!important;padding:0 14px 0 22px!important;font-size:18px!important}
.play-disc{width:33px!important;height:33px!important}
.home-footnote{display:none!important}

/* Spotlight card deliberately extends wider than PLAY, as in the approved mock-up. */
.home-race-card.p3136-prestige-home{
  width:calc(100% + 18px)!important;
  height:202px!important;
  min-height:202px!important;
  margin:10px -9px 0!important;
  padding:9px 10px 8px!important;
  border-radius:18px!important;
  border:1px solid rgba(190,151,255,.82)!important;
  background:linear-gradient(145deg,rgba(29,24,48,.985),rgba(12,13,26,.99))!important;
  box-shadow:0 0 0 1px rgba(83,213,235,.07),0 8px 24px rgba(0,0,0,.18)!important;
}
.home-race-card.p3136-prestige-home::before{
  background:linear-gradient(90deg,rgba(155,111,255,.055),transparent 34%,transparent 68%,rgba(69,234,213,.035))!important;
}
.p3136-spot-head{
  height:19px!important;padding:0 2px 6px!important;border-bottom:0!important;
  font-size:7.2px!important;letter-spacing:.12em!important
}
.p3136-spot-head i{font-size:5.8px!important;padding:1px 4px!important}
.p3136-spot-head b{font-size:7.2px!important;color:#e78fc5!important}
.p3136-spot-head b::before{content:"◷";margin-right:5px;color:#e78fc5}

.p3136-crown-row{
  grid-template-columns:103px minmax(0,1fr) 14px!important;
  gap:8px!important;min-height:73px!important;height:73px!important;padding:2px 0 3px!important
}
.p3136-crown-art{width:96px!important;height:70px!important}
.p3136-prism{left:32px!important;top:28px!important;width:31px!important;height:38px!important;border-color:#77dce2!important}
.p3136-orbit{left:18px!important;top:29px!important;width:60px!important;height:35px!important;border-color:rgba(211,125,240,.62)!important}
.p3136-crown{left:25px!important;top:0!important;width:47px!important;height:29px!important;border-color:#f0ca66!important;background:rgba(248,212,107,.065)!important}
.p3136-shard{display:none!important}

.p3136-holder-copy small{font-size:7.2px!important;letter-spacing:.16em!important;color:#e6c66d!important}
.p3136-holder-copy strong{font-size:15px!important;margin:3px 0 2px!important}
.p3136-holder-copy>b{font-size:23px!important;color:#f1d15f!important}
.p3136-holder-copy em{font-size:7.8px!important;margin-top:3px!important;color:#aaa1b6!important}
.p3136-card-arrow{width:14px!important;height:14px!important;color:#c2b6d1!important}

.p3136-chase{
  grid-template-columns:31px 1fr 10px!important;
  min-height:34px!important;height:34px!important;
  margin:0 2px 6px!important;padding:4px 9px!important;gap:7px!important;
  border-color:rgba(237,203,101,.72)!important;border-radius:10px!important;
  background:linear-gradient(100deg,rgba(248,212,107,.045),rgba(164,138,255,.025))!important
}
.p3136-chase::after{content:"›";font-size:18px;line-height:1;color:#dfc66d}
.p3136-mini-crown{width:22px!important;height:14px!important}
.p3136-chase small{font-size:6.8px!important;letter-spacing:.15em!important}
.p3136-chase b{font-size:7.7px!important;margin-top:1px!important;color:#c3b8cc!important}

.p3136-podium-preview{gap:6px!important;height:48px!important}
.p3136-podium{
  position:relative!important;
  display:grid!important;grid-template-columns:23px 34px minmax(0,1fr)!important;
  gap:5px!important;min-height:48px!important;height:48px!important;
  padding:5px 6px!important;border-radius:10px!important;text-align:left!important
}
.p3136-podium.p2{border-color:rgba(72,195,255,.58)!important;background:linear-gradient(130deg,rgba(37,58,92,.26),rgba(20,19,35,.38))!important}
.p3136-podium.p3{border-color:rgba(235,88,220,.48)!important;background:linear-gradient(130deg,rgba(83,35,89,.24),rgba(22,18,35,.38))!important}
.p3137-place{font-size:12px!important;font-weight:750!important;color:#e3ddec!important;align-self:start!important;margin-top:3px!important}
.p3136-crest{width:21px!important;height:28px!important}
.p3137-podium-copy{display:block!important;min-width:0!important}
.p3137-podium-copy strong{display:block!important;overflow:hidden!important;text-overflow:ellipsis!important;white-space:nowrap!important;font-size:7.7px!important;line-height:1.05!important;color:#c8bed4!important;font-weight:550!important}
.p3137-podium-copy b{display:block!important;font-size:11.5px!important;line-height:1.05!important;margin:3px 0 2px!important;font-variant-numeric:tabular-nums!important}
.p2 .p3137-podium-copy b,.p2 .p3137-podium-copy small{color:#5ed7e4!important}
.p3 .p3137-podium-copy b,.p3 .p3137-podium-copy small{color:#e483df!important}
.p3137-podium-copy small{display:block!important;font-size:5.3px!important;letter-spacing:.06em!important;white-space:nowrap!important}

.home-race-card.p3136-prestige-home.p3136-self-crown{
  border-color:rgba(190,151,255,.82)!important;
  box-shadow:0 0 0 1px rgba(83,213,235,.07),0 8px 24px rgba(0,0,0,.18)!important;
}

@media(max-width:365px){
  .game .home{padding-left:22px!important;padding-right:22px!important}
  .home-race-card.p3136-prestige-home{width:calc(100% + 16px)!important;margin-left:-8px!important;margin-right:-8px!important}
  .p3136-crown-row{grid-template-columns:94px minmax(0,1fr) 12px!important}
  .p3136-crown-art{transform:scale(.93)!important}
}
@media(max-height:735px){
  .game .home{padding-top:77px!important}
  .game .home h1{font-size:52px!important}
  .game .home .hero-space{min-height:70px!important;flex-basis:70px!important}
  .home-records{padding:7px 0!important;margin-bottom:7px!important}
  .game .home .mode-desc{margin:4px 0 6px!important}
  .game .home .play-hero{height:49px!important;min-height:49px!important}
  .home-race-card.p3136-prestige-home{height:192px!important;min-height:192px!important;margin-top:8px!important}
  .p3136-crown-row{height:68px!important;min-height:68px!important}
  .p3136-crown-art{transform:scale(.91)!important}
  .p3136-podium-preview{height:45px!important}
  .p3136-podium{height:45px!important;min-height:45px!important}
}
</style>
'''
s=s.replace('</head>',css+'</head>',1)

p.write_text(s)
(root/'app/src/main/assets/index.html.gz.b64').write_text(base64.b64encode(gzip.compress(s.encode(),9)).decode())

g=root/'app/build.gradle'
gs=g.read_text()
if 'versionCode 53' not in gs:
    raise SystemExit('v53 missing')
g.write_text(gs.replace('versionCode 53','versionCode 54',1).replace("versionName '3.13.6-test'","versionName '3.13.7-test'",1))

a=root/'app/src/main/java/com/zarivostudios/prismhop/MainActivity.java'
av=a.read_text()
if 'private static final String APP_VERSION = "3.13.6-test";' not in av:
    raise SystemExit('native v3136 missing')
a.write_text(av.replace('private static final String APP_VERSION = "3.13.6-test";','private static final String APP_VERSION = "3.13.7-test";',1))
print('V3.13.7 exact 2D Home prestige applied')
