def parse_m3u(manifest_file):
    url = M3UURL()
    for line in [l.rstrip() for l in open(manifest_file, 'r')]:
        if (line.startswith('#')):
            url.tags.append(M3UTag(line))
        else:
            url.url = line
            yield url
            url = M3UURL()
    if len(url.tags) or url.url:
        yield url

class M3UURL:
    def __init__(self):
        self.tags = []
        self.url = None

    def has_tag(self, tag):
        return self.get_tag(tag) is not None

    def get_tag(self, tag):
        matches = [t for t in self.tags if t.name == tag]
        if len(matches):
            return matches[0]
        return None

class M3UTag:
    def __init__(self, line):
        colon_loc = line.find(':')
        if colon_loc == -1:
            self.name = line[1:]
        else:
            self.name = line[1:colon_loc]
            self.param_string = line[colon_loc + 1:]

    def params(self):
        in_quote = False
        last_start = 0
        for i in range(0, len(self.param_string)):
            c = self.param_string[i]
            if c == '"':
                in_quote = not in_quote
            if not in_quote and c == ',':
                yield M3UTagParam(self.param_string[last_start:i])
                last_start = i + 1
        if last_start < len(self.param_string):
            yield M3UTagParam(self.param_string[last_start:])


class M3UTagParam:
    def __init__(self, raw):
        eq_loc = raw.find('=')
        if eq_loc == -1:
            self.key = raw
            self.val = None
        else:
            self.key = raw[:eq_loc]
            self.val = raw[eq_loc + 1:]
            if self.val[0] == '"' and self.val[-1] == '"':
                self.val = self.val[1:-1]
                self.quoted = True
            else:
                self.quoted = False
        self.key = self.key.strip()
        if self.val:
            self.val = self.val.strip()
