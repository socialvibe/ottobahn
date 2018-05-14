from datetime import datetime, timedelta

from app.fragments import FragmentList

class ActiveManifest:

    def __init__(self, config):
        self.window_size = int(config.get('content', 'window_size'))

        self.last_req = None
        self.remainder = 0.0
        self.seq_num = 0
        self.pgm_date_time = None
        self.filled = False

        self.active_fragments = FragmentList()

    def fill(self, generator):
        while self.active_fragments.sum < self.window_size:
            self.active_fragments.push_fragment(generator.next_fragment())
        if not self.filled:
            self.filled = True
            self.last_req = datetime.now()
            self.pgm_date_time = self.last_req - timedelta(seconds=self.active_fragments.sum)

    def roll(self):
        offset = (datetime.now() - self.last_req).total_seconds() + self.remainder
        self.last_req = datetime.now()
        while self.active_fragments.fragments[0].length < offset:
            length = self.active_fragments.pop_fragment().length
            offset -= length
            self.pgm_date_time += timedelta(seconds=length)
            self.seq_num += 1
        self.remainder = offset

    def build(self):
        result = ''
        result += '#EXTM3U\n'
        result += '#EXT-X-VERSION:3\n'
        result += '#EXT-X-MEDIA-SEQUENCE:' + str(self.seq_num) + '\n'
        result += '#EXT-X-TARGETDURATION:11\n'
        result += '#EXT-X-PROGRAM-DATE-TIME:' + self.pgm_date_time.astimezone().isoformat() + '\n'
        lastf = None
        for f in self.active_fragments.fragments:
            if lastf is not None:
                if f.follows_id != lastf.id:
                    result += '#EXT-X-DISCONTINUITY\n'
                if f.is_ad != lastf.is_ad:
                    result += '#EXT-X-CUE-'
                    result += 'IN' if lastf.is_ad else 'OUT'
                    result += '\n'
            lastf = f
            result += '#EXTINF:'
            result += str(f.length)
            result += '\n'
            result += 'f/'
            result += str(f.id)
            result += '\n'
        return result

    def fragment_path(self, id):
        return next(f.path for f in self.active_fragments.fragments if str(f.id) == id)
