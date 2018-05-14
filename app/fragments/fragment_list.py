import os

from app.fragments import M3UFragment
from app.parser.m3uparser import parse_m3u

class FragmentList:
    def __init__(self, manifest_path=None):
        self.fragments = []
        self.sum = 0.0
        self.manifest_path = manifest_path
        if manifest_path is not None:
            prev = None
            for url in parse_m3u(manifest_path):
                extinf = url.get_tag('EXTINF')
                if extinf is not None:
                    frag = M3UFragment(
                        os.path.join(os.path.dirname(manifest_path), url.url),
                        float(next(extinf.params()).key)
                    )
                    if prev is not None and not url.has_tag('EXT-X-DISCONTINUITY'):
                        frag.follows_id = prev.id
                    prev = frag
                    self.push_fragment(frag)

    def push_fragment(self, fragment):
        self.fragments.append(fragment)
        self.sum += fragment.length

    def pop_fragment(self):
        frag = self.fragments.pop(0)
        self.sum -= frag.length
        return frag
