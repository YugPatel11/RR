import requests

headers = {'User-Agent': 'RajasthanRoyalsResearch/1.0 (cricket@royals.com)'}

def search_cricket(name):
    query = f'"{name}"'
    params = {
        'action': 'query',
        'format': 'json',
        'generator': 'search',
        'gsrsearch': query,
        'gsrnamespace': 6,
        'gsrlimit': 5,
        'prop': 'imageinfo',
        'iiprop': 'url|size|extmetadata'
    }
    r = requests.get('https://commons.wikimedia.org/w/api.php', params=params, headers=headers).json()
    pages = r.get('query', {}).get('pages', {})
    print(f'=== {name} ===')
    for pid, p in pages.items():
        title = p.get('title', '')
        ii = p.get('imageinfo', [{}])[0]
        meta = ii.get('extmetadata', {})
        lic = meta.get('LicenseShortName', {}).get('value', 'Unknown')
        categories = meta.get('Categories', {}).get('value', '')
        desc = meta.get('ImageDescription', {}).get('value', '')[:80]
        print(f'  {title} | Lic: {lic} | Desc: {desc}')

test_names = [
    'Reeza Hendricks', 'David Miller', 'Tim David', 'Blessing Muzarabani', 
    'Gerald Coetzee', 'Jamie Overton', 'Shaheen Afridi', 'Matheesha Pathirana',
    'Riyan Parag', 'Ashutosh Sharma', 'Vaibhav Sooryavanshi', 'Mohammad Nawaz'
]
for n in test_names:
    search_cricket(n)

