import requests

headers = {'User-Agent': 'RajasthanRoyalsResearch/1.0 (cricket@royals.com)'}

queries = [
    ('David Miller', 'David Miller cricketer'),
    ('David Miller 2', 'David Miller cricket'),
    ('Tim David', 'Tim David cricket'),
    ('Mohammad Nawaz', 'Mohammad Nawaz cricket'),
    ('Abrar Ahmed', 'Abrar Ahmed cricket'),
    ('Rishad Hossain', 'Rishad Hossain cricket'),
    ('Sufiyan Muqeem', 'Sufiyan Muqeem cricket'),
    ('Matheesha Pathirana', 'Matheesha Pathirana cricket'),
    ('Riyan Parag', 'Riyan Parag cricket'),
    ('Ashutosh Sharma', 'Ashutosh Sharma cricketer'),
    ('Shubham Dubey', 'Shubham Dubey cricket'),
    ('Anshul Kamboj', 'Anshul Kamboj cricket'),
    ('Stadium', 'Sawai Mansingh Stadium'),
    ('Hawa Mahal', 'Hawa Mahal Jaipur'),
    ('Stepwell', 'Chand Baori Jaipur')
]

for label, q in queries:
    params = {
        'action': 'query',
        'format': 'json',
        'generator': 'search',
        'gsrsearch': q,
        'gsrnamespace': 6,
        'gsrlimit': 4,
        'prop': 'imageinfo',
        'iiprop': 'url|size|extmetadata'
    }
    try:
        r = requests.get('https://commons.wikimedia.org/w/api.php', params=params, headers=headers, timeout=10).json()
        pages = r.get('query', {}).get('pages', {})
        print(f'=== {label} ({q}) ===')
        for pid, p in pages.items():
            title = p.get('title', '')
            ii = p.get('imageinfo', [{}])[0]
            meta = ii.get('extmetadata', {})
            lic = meta.get('LicenseShortName', {}).get('value', 'Unknown')
            artist = meta.get('Artist', {}).get('value', 'Unknown')[:30]
            print(f'  {title} | Lic: {lic} | Artist: {artist}')
    except Exception as e:
        print(f'Error for {label}: {e}')

