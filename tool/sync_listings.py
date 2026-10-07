"""Refreshes tool/listings.json from the Play Developer API.

    python tool/sync_listings.py
    python tool/build.py

For every game in build.py it stores the en-US and tr-TR title and short
description, the number of store languages, and whether the game is live:
a completed production release AND a public store page. The second check
matters because a production release can still be in review, and linking
to it then gives every visitor a 404.

The service account key stays outside the repo; set PLAY_KEY to override.
"""
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

from google.oauth2 import service_account
from googleapiclient.discovery import build as api

sys.path.insert(0, str(Path(__file__).parent))
from build import GAMES, ROOT  # noqa: E402

KEY = os.environ.get('PLAY_KEY', r'C:\Users\gence\.sarjradar\play-service-account.json')


def public(pkg):
    url = f'https://play.google.com/store/apps/details?id={pkg}&hl=en'
    try:
        with urllib.request.urlopen(url, timeout=20) as r:
            return r.status == 200
    except urllib.error.HTTPError:
        return False


def main():
    creds = service_account.Credentials.from_service_account_file(
        KEY, scopes=['https://www.googleapis.com/auth/androidpublisher'])
    svc = api('androidpublisher', 'v3', credentials=creds, cache_discovery=False)
    path = ROOT / 'tool' / 'listings.json'
    old = json.loads(path.read_text(encoding='utf-8'))
    out = {}
    for key in [g[0] for games in GAMES.values() for g in games]:
        pkg = f'com.pikkogames.{key}'
        try:
            edit = svc.edits().insert(packageName=pkg, body={}).execute()['id']
        except Exception as e:  # app not created yet, or a transient 5xx
            print(f'{key}: kept old entry ({str(e)[:80]})')
            out[key] = old.get(key, {})
            continue
        try:
            listings = svc.edits().listings().list(packageName=pkg, editId=edit).execute().get('listings', [])
            tracks = svc.edits().tracks().list(packageName=pkg, editId=edit).execute().get('tracks', [])
        finally:
            svc.edits().delete(packageName=pkg, editId=edit).execute()
        by_lang = {l['language']: [l['title'], l['shortDescription']] for l in listings}
        in_production = any(r.get('status') == 'completed'
                             for t in tracks if t['track'] == 'production' for r in t.get('releases', []))
        entry = {k: by_lang[k] for k in ('en-US', 'tr-TR') if k in by_lang}
        # es-ES and es-419 are one language to a player.
        entry['languages'] = len({l.split('-')[0] for l in by_lang})
        entry['live'] = in_production and public(pkg)
        out[key] = entry
        print(f"{key}: {entry['languages']} languages, live={entry['live']}")
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('listings.json written')


if __name__ == '__main__':
    main()
