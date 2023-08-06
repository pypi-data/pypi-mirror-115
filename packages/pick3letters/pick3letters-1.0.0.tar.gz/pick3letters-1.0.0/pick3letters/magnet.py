import re
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse


# Trackers for bootstrapping the BitTorrent DHT
TRACKERS = ['udp://tracker.coppersurfer.tk:6969/announce', 'udp://tracker.openbittorrent.com:6969/announce', 'udp://tracker.opentrackr.org:1337', 'udp://tracker.leechers-paradise.org:6969/announce', 'udp://tracker.dler.org:6969/announce', 'udp://opentracker.i2p.rocks:6969/announce', 'udp://47.ip-51-68-199.eu:6969/announce']


def magnet2infohash(magnet_url):
    parsed = urlparse(magnet_url)
    if parsed.scheme != 'magnet':
        raise ValueError('URL scheme must be "magnet"')

    query = parse_qs(parsed.query)
    xt = query['xt'][0]
    m = re.fullmatch('urn:btih:([0-9a-fA-F]{40})', xt)
    if m is None:
        raise ValueError('No infohash found in URL')

    return m.group(1).lower()


def infohash2magnet(infohash):
    query = urlencode({'xt': [infohash.upper()], 'tr': TRACKERS}, doseq=True)
    return urlunparse(('magnet', None, '', None, query, None))
