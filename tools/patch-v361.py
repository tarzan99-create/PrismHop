from pathlib import Path
import base64, gzip

root=Path('android')
asset=root/'app/src/main/assets/index.html.gz.b64'
html=gzip.decompress(base64.b64decode(asset.read_text().strip())).decode('utf-8')

def once(old,new):
    global html
    if old not in html:
        raise SystemExit('V3.6.1 patch anchor missing: '+old[:80])
    html=html.replace(old,new,1)

once('<main class="game" id="game"','<main class="game startup-active" id="game"')
once("<p>THERE'S MORE HOP</p>",'<p>FIND YOUR FLOW.</p>')
once("let pulseTimer=null,pulseBusy=false,result=null,dialogReturn=null,dialogResume=false,authBusy=false;","let pulseTimer=null,pulseBusy=false,pulseFailures=0,result=null,dialogReturn=null,dialogResume=false,authBusy=false;")
once("function stopPulse(){if(pulseTimer!==null)clearInterval(pulseTimer);pulseTimer=null;pulseBusy=false;}","function stopPulse(){if(pulseTimer!==null)clearInterval(pulseTimer);pulseTimer=null;pulseBusy=false;pulseFailures=0;}")
once("if(active===current&&r?.checkpoint_token)current.checkpoint_token=r.checkpoint_token;if(active===current&&!r?.active)loseConnection('The online session closed.');}\n   catch{if(active===current)loseConnection('The server connection was lost.');}finally{pulseBusy=false;}","if(active===current&&r?.checkpoint_token)current.checkpoint_token=r.checkpoint_token;if(active===current&&r?.active)pulseFailures=0;if(active===current&&!r?.active)loseConnection('The online session closed.');}\n   catch{if(active===current){pulseFailures++; if(pulseFailures>=3)loseConnection('The server connection was lost.');}}finally{pulseBusy=false;}")
once("$('home').addEventListener('scroll',()=>requestAnimationFrame(measureHero),{passive:true});", "let homeScrollTimer=null;\n  $('home').addEventListener('scroll',()=>{\n    measureHero();\n    game.classList.add('home-scrolling');\n    clearTimeout(homeScrollTimer);\n    homeScrollTimer=setTimeout(()=>game.classList.remove('home-scrolling'),110);\n  },{passive:true});")
css='''\n/* V3.6.1 — native polish pass. */\n.game{background:radial-gradient(circle at 50% 42%,rgba(116,84,199,.115),rgba(69,234,213,.045) 28%,transparent 62%),linear-gradient(180deg,#090916 0%,#0b0b18 48%,#090916 100%);}\n.topbar{background:transparent!important;backdrop-filter:none!important;-webkit-backdrop-filter:none!important;}\n.game[data-page="home"] .home{background:transparent!important;}\n.game[data-page="home"]::after{filter:blur(12px);}\n.game.home-scrolling::after{filter:none!important;opacity:.30!important;}\n#connection-chip{display:none!important;}\n.race-hud small,.demo-pill{font-size:0!important;}\n.race-hud small::after,.demo-pill::after{content:'PERSONAL';font-size:8px;}\n.game.startup-active #home{visibility:hidden;}\n.game.startup-active.startup-reveal #home{visibility:visible;}\n'''
once('<script id="v3311-connected-launch">',css+'\n<script id="v3311-connected-launch">')
asset.write_text(base64.b64encode(gzip.compress(html.encode('utf-8'))).decode('ascii'))

build=root/'app/build.gradle'
s=build.read_text().replace('versionCode 36','versionCode 37',1).replace("versionName '3.6.0-test'","versionName '3.6.1-test'",1)
build.write_text(s)
activity=root/'app/src/main/java/com/zarivostudios/prismhop/MainActivity.java'
s=activity.read_text().replace('private static final String APP_VERSION = "3.6.0-test";','private static final String APP_VERSION = "3.6.1-test";',1)
activity.write_text(s)
print('Applied Prism Hop V3.6.1 patch')
