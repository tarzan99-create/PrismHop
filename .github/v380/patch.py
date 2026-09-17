from pathlib import Path

html_path = Path('android/app/src/main/assets/index.html')
gradle_path = Path('android/app/build.gradle')
activity_path = Path('android/app/src/main/java/com/zarivostudios/prismhop/MainActivity.java')

s = html_path.read_text()

replacements = [
    ('3.7.0-android', '3.8.0-android'),
    ('Spotlight previews the previous verified V1 Top 3. Official awards remain disabled until native Android device integrity.',
     'Daily Spotlight features the previous day\'s final Top 3 for 24 hours. Only server-replay-verified runs that passed Google Play Integrity can qualify.'),
    ('Server replay V1 · public cards · verified Spotlight preview',
     'Server replay + Play Integrity · official Daily Spotlight'),
    ('<div class="v33-warning"><b>VERIFIED V1 · PREVIEW</b><p>These positions come only from server-replay-verified V1 race receipts. Official Spotlight awards remain disabled until native device integrity is added.</p></div>',
     '<div class="v33-warning"><b>OFFICIAL · PLAY INTEGRITY</b><p>Daily Spotlight is now official. Final positions are frozen at UTC close and only include server-replay-verified runs that passed Google Play Integrity.</p></div>'),
    ('The final verified Top 3 when today’s UTC race closes become the next Spotlight preview. Official awards remain off until native device integrity is active.',
     'The final Play-Integrity-attested Top 3 at today’s UTC close become the next official Daily Spotlight.'),
    ('24-hour preview', '24-hour Spotlight'),
    ("spotDoc?.featured_until?'Featured preview · 24 hours':'24-hour Spotlight'",
     "spotDoc?.featured_until?'Official Spotlight · 24 hours':'24-hour Spotlight'"),
    ("'Provisional place '+e.place", "'Official place '+e.place"),
    ('Hold a Top 3 place until UTC close to enter the next Spotlight preview. Official awards remain off until native device integrity is active.',
     'Hold a Top 3 place until UTC close to enter the next official Daily Spotlight.'),
    ('Latest closed race received · verified V1 preview.',
     'Official Spotlight loaded · Play Integrity + server replay verified.'),
    ('No verified V1 podium scores in the latest closed race.',
     'No eligible Play-Integrity-attested podium scores in the latest closed race.'),
    ('Spotlight preview unavailable. ', 'Spotlight unavailable. '),
]

for old, new in replacements:
    if old in s:
        s = s.replace(old, new)

old_validator = "function validateSpot(v){const integer=n=>Number.isSafeInteger(n)&&n>=0; if(!v||v.schema_version!==2||v.provisional!==true||v.official_awards_enabled!==false||v.validation_level!=='server_replay_v1'||!Array.isArray(v.entries)||v.entries.length>3)throw new Error('Spotlight response was not recognised.');for(const e of v.entries){if(!integer(e.place)||e.place<1||e.place>3||!integer(e.score)||typeof e.name!=='string'||(e.public_ref!==null&&e.public_ref!==undefined&&!/^[0-9a-f-]{36}$/i.test(e.public_ref)))throw new Error('Spotlight entry was incomplete.');}return v;}"
new_validator = "function validateSpot(v){const integer=n=>Number.isSafeInteger(n)&&n>=0; if(!v||v.schema_version!==4||v.provisional!==false||v.official_awards_enabled!==true||v.validation_level!=='server_replay_v1+play_integrity'||v.device_attested!==true||!Array.isArray(v.entries)||v.entries.length>3)throw new Error('Spotlight response was not recognised.');for(const e of v.entries){if(!integer(e.place)||e.place<1||e.place>3||!integer(e.score)||typeof e.name!=='string'||e.device_attested!==true||e.validation_level!=='server_replay_v1+play_integrity'||(e.public_ref!==null&&e.public_ref!==undefined&&!/^[0-9a-f-]{36}$/i.test(e.public_ref)))throw new Error('Spotlight entry was incomplete.');}return v;}"
if old_validator not in s:
    raise SystemExit('V3.8 Spotlight validator baseline not found')
s = s.replace(old_validator, new_validator, 1)

# Make current live-race copy match the attested board now feeding official Spotlight.
s = s.replace(
    "$('v35-live-foot').textContent=me&&me.place<=3?'You are currently #'+me.place+' with '+fmt(me.score)+' verified points. Hold a Top 3 place until UTC close to enter the next official Daily Spotlight.':'The final Play-Integrity-attested Top 3 at UTC close become the next official Daily Spotlight.';",
    "$('v35-live-foot').textContent=me&&me.place<=3?'You are currently #'+me.place+' with '+fmt(me.score)+' verified points. Hold a Top 3 place until UTC close to enter the next official Daily Spotlight.':'The final Play-Integrity-attested Top 3 at UTC close become the next official Daily Spotlight.';"
)

html_path.write_text(s)

g = gradle_path.read_text()
if 'versionCode 39' not in g or "versionName '3.7.0-test'" not in g:
    raise SystemExit('V3.7 gradle baseline not found')
g = g.replace('versionCode 39', 'versionCode 40', 1)
g = g.replace("versionName '3.7.0-test'", "versionName '3.8.0-test'", 1)
gradle_path.write_text(g)

a = activity_path.read_text()
if 'private static final String APP_VERSION = "3.7.0-test";' not in a:
    raise SystemExit('V3.7 MainActivity version baseline not found')
a = a.replace('private static final String APP_VERSION = "3.7.0-test";', 'private static final String APP_VERSION = "3.8.0-test";', 1)
activity_path.write_text(a)

# Build-time assertions for the feature contract.
checks = [
    '3.8.0-android',
    'schema_version!==4',
    'server_replay_v1+play_integrity',
    'OFFICIAL · PLAY INTEGRITY',
    'Official Spotlight loaded · Play Integrity + server replay verified.',
]
for check in checks:
    if check not in s:
        raise SystemExit(f'missing expected V3.8 marker: {check}')
