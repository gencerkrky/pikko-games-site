"""Builds index.html from the game list below and tool/listings.json.

    python tool/build.py

When a game reaches production on Google Play, set its `live` to True and
rebuild: the card then links to the store instead of saying "Coming soon".
Until then the link would be a 404 for everyone outside the closed test.
listings.json holds each game's Play title and short description (en-US,
tr-TR), pulled from the Play API, so the site says what the store says.
"""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LISTINGS = json.loads((ROOT / 'tool' / 'listings.json').read_text(encoding='utf-8'))

# (key, live on Google Play, EN short name, TR short name)
GAMES = {
    'puzzle': [
        ('sudoku', True, 'Sudoku', 'Sudoku'),
        ('blockpuzzle', False, 'Block Puzzle', 'Blok Bulmaca'),
        ('oceandrop', False, 'Ocean Drop', 'Ocean Drop'),
    ],
    'card': [
        ('hearts', False, 'Hearts', 'Kupa'),
        ('spades', False, 'Spades', 'Spades'),
        ('euchre', False, 'Euchre', 'Euchre'),
        ('cribbage', False, 'Cribbage', 'Cribbage'),
        ('belote', False, 'Belote', 'Belote'),
        ('canasta', False, 'Canasta', 'Kanasta'),
        ('skat', False, 'Skat', 'Skat'),
        ('ginrummy', False, 'Gin Rummy', 'Gin Rummy'),
    ],
    'board': [
        ('mancala', False, 'Mancala', 'Mangala'),
        ('morris', False, "Nine Men's Morris", 'Dokuz Taş'),
    ],
    'idle': [
        ('reef', False, 'Pikko Aquarium', 'Pikko Aquarium'),
        ('streetfood', False, 'Street Food Idle', 'Sokak Lezzetleri'),
    ],
}

SECTIONS = {
    'puzzle': ('Puzzle', 'Bulmaca'),
    'card': ('Card games', 'Kart oyunları'),
    'board': ('Board games', 'Tahta oyunları'),
    'idle': ('Relaxing', 'Rahatlatıcı'),
}

YOUTUBE = 'https://www.youtube.com/@Pikko-Games'
INSTAGRAM = 'https://www.instagram.com/pikko.games/'
TIKTOK = 'https://www.tiktok.com/@pikkogames'
EMAIL = 'gencerkrky@gmail.com'


def t(en, tr):
    """Both languages in the page; CSS shows the one on <html lang>."""
    return f'<span lang="en">{html.escape(en)}</span><span lang="tr">{html.escape(tr)}</span>'


def card(key, live, name_en, name_tr):
    lst = LISTINGS[key]
    desc_en = lst['en-US'][1]
    desc_tr = lst.get('tr-TR', lst['en-US'])[1]
    url = f'https://play.google.com/store/apps/details?id=com.pikkogames.{key}'
    if live:
        action = f'<a class="btn" href="{url}" rel="noopener">{t("Free download", "Ücretsiz indir")}</a>'
    else:
        action = f'<span class="soon">{t("Coming soon", "Yakında")}</span>'
    return f'''
      <li class="game">
        <img src="assets/icons/{key}.png" alt="" width="72" height="72" loading="lazy">
        <div class="body">
          <h3>{t(name_en, name_tr)}</h3>
          <p>{t(desc_en, desc_tr)}</p>
          {action}
        </div>
      </li>'''


def page():
    sections = []
    for sid, games in GAMES.items():
        cards = ''.join(card(*g) for g in games)
        sections.append(f'''
    <section>
      <h2>{t(*SECTIONS[sid])}</h2>
      <ul class="games">{cards}
      </ul>
    </section>''')
    return TEMPLATE.replace('{{SECTIONS}}', ''.join(sections)).replace('{{YOUTUBE}}', YOUTUBE).replace('{{INSTAGRAM}}', INSTAGRAM).replace('{{TIKTOK}}', TIKTOK) \
        .replace('{{EMAIL}}', EMAIL).replace('{{COUNT}}', str(sum(len(g) for g in GAMES.values())))


TEMPLATE = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Pikko Games</title>
<meta name="description" content="Pikko Games makes calm, fair card, board and puzzle games for Android. Every game plays offline.">
<meta property="og:title" content="Pikko Games">
<meta property="og:description" content="Calm, fair card, board and puzzle games for Android. Every game plays offline.">
<meta property="og:image" content="https://gencerkrky.github.io/pikko-games-site/assets/og.jpg">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="assets/favicon.png">
<script>
  // Turkish visitors get Turkish; everyone else English. A choice made with
  // the switch is remembered on this device only.
  (function () {
    var l = null;
    try { l = localStorage.getItem('lang'); } catch (e) {}
    if (!l) l = (navigator.language || '').toLowerCase().indexOf('tr') === 0 ? 'tr' : 'en';
    document.documentElement.lang = l;
  })();
</script>
<style>
  :root {
    --bg: #f6f3ff; --bg2: #e6e0ff; --card: #ffffff; --ink: #161b48; --muted: #5d5f80;
    --brand: #6a5ae0; --brand-ink: #ffffff; --line: #e4defc; --chip: #efeaff;
  }
  @media (prefers-color-scheme: dark) {
    :root {
      --bg: #12132a; --bg2: #1d1b40; --card: #1c1d3a; --ink: #eceaff; --muted: #a9a8cc;
      --brand: #8f80ff; --brand-ink: #10112a; --line: #2c2b55; --chip: #262553;
    }
    /* The wordmark's navy "GAMES" disappears on a dark page: give it a light tile. */
    .hero img { background: #f6f3ff; border-radius: 28px; padding: 18px 28px; }
  }
  * { box-sizing: border-box; }
  html[lang="en"] [lang="tr"], html[lang="tr"] [lang="en"] { display: none; }
  body {
    margin: 0; color: var(--ink);
    background: linear-gradient(180deg, var(--bg) 0%, var(--bg2) 100%) fixed;
    font: 16px/1.55 "Segoe UI", -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
  }
  .wrap { max-width: 60rem; margin: 0 auto; padding: 0 16px; }
  header { padding: 1rem 0; display: flex; justify-content: flex-end; }
  .switch { display: inline-flex; background: var(--chip); border-radius: 999px; padding: 3px; }
  .switch button {
    border: 0; background: transparent; color: var(--muted); font: inherit; font-size: .85rem;
    font-weight: 600; padding: .3rem .8rem; border-radius: 999px; cursor: pointer;
  }
  html[lang="en"] .switch [data-l="en"], html[lang="tr"] .switch [data-l="tr"] { background: var(--card); color: var(--ink); }
  .hero { text-align: center; padding: 1.5rem 0 2.5rem; }
  .hero img { width: min(300px, 70vw); height: auto; }
  .hero h1 { font-size: clamp(1.4rem, 4vw, 2rem); line-height: 1.25; margin: 1.25rem auto .5rem; max-width: 34rem; }
  .hero p { color: var(--muted); margin: 0 auto; max-width: 34rem; }
  .facts { display: flex; flex-wrap: wrap; gap: .5rem; justify-content: center; margin-top: 1.25rem; padding: 0; list-style: none; }
  .facts li { background: var(--chip); color: var(--ink); border-radius: 999px; padding: .3rem .85rem; font-size: .9rem; font-weight: 600; }
  section { margin: 0 0 2.5rem; }
  h2 { font-size: 1.15rem; margin: 0 0 1rem; color: var(--brand); letter-spacing: .01em; }
  .games { list-style: none; margin: 0; padding: 0; display: grid; gap: 12px; grid-template-columns: repeat(auto-fill, minmax(17rem, 1fr)); }
  .game {
    display: flex; gap: 14px; align-items: flex-start; background: var(--card);
    border: 1px solid var(--line); border-radius: 18px; padding: 14px;
  }
  .game img { width: 72px; height: 72px; border-radius: 18px; flex: none; }
  .game .body { min-width: 0; }
  .game h3 { margin: 0 0 .2rem; font-size: 1.05rem; }
  .game p { margin: 0 0 .7rem; color: var(--muted); font-size: .92rem; }
  .btn {
    display: inline-block; background: var(--brand); color: var(--brand-ink); text-decoration: none;
    font-weight: 700; font-size: .88rem; padding: .45rem .9rem; border-radius: 999px;
  }
  .btn:hover { filter: brightness(1.08); }
  .soon { display: inline-block; background: var(--chip); color: var(--muted); font-weight: 600; font-size: .85rem; padding: .4rem .85rem; border-radius: 999px; }
  footer { border-top: 1px solid var(--line); padding: 2rem 0 3rem; text-align: center; color: var(--muted); font-size: .92rem; }
  footer nav { display: flex; flex-wrap: wrap; justify-content: center; gap: .5rem 1.5rem; margin-bottom: .75rem; }
  footer a { color: var(--brand); font-weight: 600; text-decoration: none; }
  footer a:hover { text-decoration: underline; }
</style>
</head>
<body>
<div class="wrap">
  <header>
    <div class="switch" role="group" aria-label="Language">
      <button type="button" data-l="en">English</button>
      <button type="button" data-l="tr">Türkçe</button>
    </div>
  </header>

  <div class="hero">
    <img src="assets/logo.png" alt="Pikko Games" width="480" height="305">
    <h1><span lang="en">Calm, fair card, board and puzzle games</span><span lang="tr">Sakin ve adil kart, tahta ve bulmaca oyunları</span></h1>
    <p><span lang="en">Made for Android. Clear rules, computer opponents that play fair, and no account to create.</span><span lang="tr">Android için. Kurallar açık, bilgisayar rakipler hile yapmaz, hesap açman gerekmez.</span></p>
    <ul class="facts">
      <li><span lang="en">{{COUNT}} games</span><span lang="tr">{{COUNT}} oyun</span></li>
      <li><span lang="en">Plays offline</span><span lang="tr">İnternetsiz oynanır</span></li>
      <li><span lang="en">No subscriptions</span><span lang="tr">Abonelik yok</span></li>
      <li><span lang="en">6+ languages</span><span lang="tr">6+ dil</span></li>
    </ul>
  </div>
{{SECTIONS}}
</div>

<footer>
  <div class="wrap">
    <nav>
      <a href="{{INSTAGRAM}}" rel="noopener">Instagram</a>
      <a href="{{TIKTOK}}" rel="noopener">TikTok</a>
      <a href="{{YOUTUBE}}" rel="noopener">YouTube</a>
      <a href="mailto:{{EMAIL}}"><span lang="en">Contact</span><span lang="tr">İletişim</span></a>
      <a href="privacy.html"><span lang="en">Privacy policy</span><span lang="tr">Gizlilik politikası</span></a>
    </nav>
    <div>© 2026 Pikko Games</div>
  </div>
</footer>

<script>
  document.querySelectorAll('.switch button').forEach(function (b) {
    b.addEventListener('click', function () {
      var l = b.getAttribute('data-l');
      document.documentElement.lang = l;
      try { localStorage.setItem('lang', l); } catch (e) {}
    });
  });
</script>
</body>
</html>
'''

if __name__ == '__main__':
    (ROOT / 'index.html').write_text(page(), encoding='utf-8')
    print('index.html written')
