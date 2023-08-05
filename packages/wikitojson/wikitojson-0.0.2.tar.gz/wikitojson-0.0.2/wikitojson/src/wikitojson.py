import re
import requests

def get(title=None):
    content = _getwiki(title)
    return getdict(content)

def getdict(content):
    content = _getsections(content)
    return _sectiontodict(content)

def _getwiki(title):
    r = requests.get(
        'https://en.wikipedia.org/w/api.php',
        params={
            'action': 'query',
            'format': 'json',
            'titles': title,
            'prop': 'extracts',
            'explaintext': True,
        }, headers= {
            'User-Agent': 'wikitojson (https://github.com/Klaifer/wikitojson)'
        }
    ).json()

    pageid = next(iter(r['query']['pages']))
    if pageid == '-1':
        raise ValueError("Wikipedia page not found")

    return r['query']['pages'][pageid]['extract']

def _getsections(content):
    data = []
    name = "intro"
    level = 1

    for text in re.split("(=+.*=+)", content):
        title = re.search("(=+)([^=]*)=+", text)
        if title:
            if name:
                data.append({
                    'name': name,
                    'level': level
                })

            name = title.group(2).strip()
            level = len(title.group(1))
        else:
            data.append({
                'name': name,
                'level': level,
                'content': text.strip()
            })
            name = None

    return data

def _sectiontodict(data):
    data.reverse()

    for i, curr in enumerate(data):
        for tgt in data[i + 1:]:
            if tgt['level'] < curr['level']:
                del (curr['level'])
                childs = tgt.get('subsections', [])
                childs.insert(0, curr)
                tgt['subsections'] = childs
                break

    extracted = []
    for curr in data:
        if 'level' in curr:
            del (curr['level'])
            extracted.insert(0, curr)

    return extracted