import os
import random

from app.fragments import FragmentList

class FragmentGenerator:
    def __init__(self, config):

        self.ad_separation = int(config.get('content', 'ad_separation'))
        self.ads_per_pod = int(config.get('content', 'ads_per_pod'))

        self.content_fragments = FragmentList(
            os.path.join(os.getcwd(), config.get('content', 'manifest'))
        )

        self.ads = [FragmentList(os.path.join(os.getcwd(), path)) for _, path in config.items('ads')]

        self.content_index = 0
        self.ad_index = None
        self.ad_pod = None

        self.time_since_last_ad = 0.0

    def next_fragment(self):
        if self.ad_index is None:
            fragment = self.content_fragments.fragments[self.content_index]
            self.content_index += 1
            self.content_index %= len(self.content_fragments.fragments)
            self.time_since_last_ad += fragment.length
            if self.time_since_last_ad > self.ad_separation:
                self.time_since_last_ad = 0.0
                self.ad_pod = FragmentList()
                pod_ads = random.sample(self.ads, self.ads_per_pod)
                random.shuffle(pod_ads)
                for ad in pod_ads:
                    for f in ad.fragments:
                        self.ad_pod.push_fragment(f)
                self.ad_index = 0
        else:
            fragment = self.ad_pod.fragments[self.ad_index]
            fragment.is_ad = True
            self.ad_index += 1
            if self.ad_index >= len(self.ad_pod.fragments):
                self.ad_index = None
                self.ad_pod = None
        return fragment
        
