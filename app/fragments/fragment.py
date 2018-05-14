import uuid


class M3UFragment:
    def __init__(self, path, length):
        self.id = uuid.uuid4()
        self.path = path
        self.length = length
        self.follows_id = None
        self.is_ad = False
