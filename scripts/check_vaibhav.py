import requests

headers = {'User-Agent': 'RajasthanRoyalsResearch/1.0 (cricket@royals.com)'}
params = {
    'action': 'query',
    'format': 'json',
    'titles': 'File:Prime Minister of Bharat, Shri Narendra Damodardas Modi meets young cricketing sensation Vaibhav Suryavanshi.jpg',
    'prop': 'imageinfo',
    'iiprop': 'url|size|extmetadata'
}
r = requests.get('https://commons.wikimedia.org/w/api.php', params=params, headers=headers).json()
pages = r.get('query', {}).get('pages', {})
for pid, p in pages.items():
    ii = p.get('imageinfo', [{}])[0]
    meta = ii.get('extmetadata', {})
    lic = meta.get('LicenseShortName', {}).get('value', 'Unknown')
    print('Vaibhav license:', lic)

