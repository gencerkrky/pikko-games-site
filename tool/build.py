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
        ('killersudoku', False, 'Killer Sudoku', 'Killer Sudoku'),
        ('blockpuzzle', False, 'Block Puzzle', 'Blok Bulmaca'),
        ('oceandrop', False, 'Ocean Drop', 'Ocean Drop'),
        ('petek', False, 'Honeycomb', 'Honeycomb'),
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
        ('fetih', False, 'Conquest Isles', 'Conquest Isles'),
    ],
    'idle': [
        ('reef', False, 'Pikko Aquarium', 'Pikko Aquarium'),
        ('streetfood', False, 'Street Food Idle', 'Sokak Lezzetleri'),
        ('koy', False, 'Stack Village', 'Stack Village'),
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

# Brand marks from simple-icons (CC0), inlined so the page has no extra requests.
ICON_PATHS = {
    'instagram': 'M7.0301.084c-1.2768.0602-2.1487.264-2.911.5634-.7888.3075-1.4575.72-2.1228 1.3877-.6652.6677-1.075 1.3368-1.3802 2.127-.2954.7638-.4956 1.6365-.552 2.914-.0564 1.2775-.0689 1.6882-.0626 4.947.0062 3.2586.0206 3.6671.0825 4.9473.061 1.2765.264 2.1482.5635 2.9107.308.7889.72 1.4573 1.388 2.1228.6679.6655 1.3365 1.0743 2.1285 1.38.7632.295 1.6361.4961 2.9134.552 1.2773.056 1.6884.069 4.9462.0627 3.2578-.0062 3.668-.0207 4.9478-.0814 1.28-.0607 2.147-.2652 2.9098-.5633.7889-.3086 1.4578-.72 2.1228-1.3881.665-.6682 1.0745-1.3378 1.3795-2.1284.2957-.7632.4966-1.636.552-2.9124.056-1.2809.0692-1.6898.063-4.948-.0063-3.2583-.021-3.6668-.0817-4.9465-.0607-1.2797-.264-2.1487-.5633-2.9117-.3084-.7889-.72-1.4568-1.3876-2.1228C21.2982 1.33 20.628.9208 19.8378.6165 19.074.321 18.2017.1197 16.9244.0645 15.6471.0093 15.236-.005 11.977.0014 8.718.0076 8.31.0215 7.0301.0839m.1402 21.6932c-1.17-.0509-1.8053-.2453-2.2287-.408-.5606-.216-.96-.4771-1.3819-.895-.422-.4178-.6811-.8186-.9-1.378-.1644-.4234-.3624-1.058-.4171-2.228-.0595-1.2645-.072-1.6442-.079-4.848-.007-3.2037.0053-3.583.0607-4.848.05-1.169.2456-1.805.408-2.2282.216-.5613.4762-.96.895-1.3816.4188-.4217.8184-.6814 1.3783-.9003.423-.1651 1.0575-.3614 2.227-.4171 1.2655-.06 1.6447-.072 4.848-.079 3.2033-.007 3.5835.005 4.8495.0608 1.169.0508 1.8053.2445 2.228.408.5608.216.96.4754 1.3816.895.4217.4194.6816.8176.9005 1.3787.1653.4217.3617 1.056.4169 2.2263.0602 1.2655.0739 1.645.0796 4.848.0058 3.203-.0055 3.5834-.061 4.848-.051 1.17-.245 1.8055-.408 2.2294-.216.5604-.4763.96-.8954 1.3814-.419.4215-.8181.6811-1.3783.9-.4224.1649-1.0577.3617-2.2262.4174-1.2656.0595-1.6448.072-4.8493.079-3.2045.007-3.5825-.006-4.848-.0608M16.953 5.5864A1.44 1.44 0 1 0 18.39 4.144a1.44 1.44 0 0 0-1.437 1.4424M5.8385 12.012c.0067 3.4032 2.7706 6.1557 6.173 6.1493 3.4026-.0065 6.157-2.7701 6.1506-6.1733-.0065-3.4032-2.771-6.1565-6.174-6.1498-3.403.0067-6.156 2.771-6.1496 6.1738M8 12.0077a4 4 0 1 1 4.008 3.9921A3.9996 3.9996 0 0 1 8 12.0077',
    'tiktok': 'M12.525.02c1.31-.02 2.61-.01 3.91-.02.08 1.53.63 3.09 1.75 4.17 1.12 1.11 2.7 1.62 4.24 1.79v4.03c-1.44-.05-2.89-.35-4.2-.97-.57-.26-1.1-.59-1.62-.93-.01 2.92.01 5.84-.02 8.75-.08 1.4-.54 2.79-1.35 3.94-1.31 1.92-3.58 3.17-5.91 3.21-1.43.08-2.86-.31-4.08-1.03-2.02-1.19-3.44-3.37-3.65-5.71-.02-.5-.03-1-.01-1.49.18-1.9 1.12-3.72 2.58-4.96 1.66-1.44 3.98-2.13 6.15-1.72.02 1.48-.04 2.96-.04 4.44-.99-.32-2.15-.23-3.02.37-.63.41-1.11 1.04-1.36 1.75-.21.51-.15 1.07-.14 1.61.24 1.64 1.82 3.02 3.5 2.87 1.12-.01 2.19-.66 2.77-1.61.19-.33.4-.67.41-1.06.1-1.79.06-3.57.07-5.36.01-4.03-.01-8.05.02-12.07z',
    'youtube': 'M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z',
}


def socials():
    links = [('Instagram', INSTAGRAM, 'instagram'), ('TikTok', TIKTOK, 'tiktok'), ('YouTube', YOUTUBE, 'youtube')]
    return ''.join(
        f'<a href="{url}" rel="noopener" aria-label="{name}" title="{name}">'
        f'<svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><path d="{ICON_PATHS[key]}"/></svg></a>'
        for name, url, key in links)


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
    return TEMPLATE.replace('{{SECTIONS}}', ''.join(sections)).replace('{{YOUTUBE}}', YOUTUBE).replace('{{INSTAGRAM}}', INSTAGRAM).replace('{{TIKTOK}}', TIKTOK).replace('{{SOCIAL}}', socials()) \
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
  .social { display: flex; justify-content: center; gap: .75rem; margin-top: 1.25rem; }
  .social a {
    width: 44px; height: 44px; border-radius: 50%; display: grid; place-items: center;
    background: var(--card); border: 1px solid var(--line); color: var(--ink); transition: transform .15s, color .15s;
  }
  .social a:hover { transform: translateY(-2px); color: var(--brand); }
  .social svg { fill: currentColor; }
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
    <div class="social">{{SOCIAL}}</div>
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
