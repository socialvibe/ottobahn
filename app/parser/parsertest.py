import os
import unittest

from m3uparser import parse_m3u as p

class TestM3UParser(unittest.TestCase):
    def test_parse_simple(self):
        urls = list(p(os.path.join(os.getcwd(), 'test_assets', 'simple.m3u')))

        self.assertIsNotNone(urls)
        self.assertEqual(1, len(urls))

        url = urls[0]
        self.assertEqual(4, len(url.tags))
        self.assertEqual('0.ts', url.url)

        tag = url.tags[0]
        self.assertEqual('EXTM3U', tag.name)

        tag = url.tags[1]
        self.assertEqual('EXT-X-VERSION', tag.name)
        params = list(tag.params())
        self.assertEqual(1, len(params))
        self.assertEqual('3', params[0].key)
        self.assertIsNone(params[0].val)

    def test_parse_complex(self):
        urls = list(p(os.path.join(os.getcwd(), 'test_assets', 'complex.m3u')))

        self.assertEqual(8, len(urls))

        url = urls[0]
        self.assertEqual(9, len(url.tags))
        self.assertEqual('https://x-live-fox-stgec.uplynk.com/80C078/ausw/slices/7e9/8baebcb1115a4bb78fa90c40ae8d81aa/7e986864b3014522ae734a1213ee3c80/B000008D2.ts?pbs=c46967324531414fae658ee72847012e&_jt=l&chid=86c8f49a240b4c6ba8b4028cda89a401&si=0', url.url)

        tag = url.tags[4]
        self.assertEqual('UPLYNK-SEGMENT', tag.name)
        params = list(tag.params())
        self.assertEqual(3, len(params))
        self.assertEqual('7e986864b3014522ae734a1213ee3c80', params[0].key)
        self.assertIsNone(params[0].val)
        self.assertEqual('000008D2', params[1].key)
        self.assertIsNone(params[1].val)
        self.assertEqual('segment', params[2].key)
        self.assertIsNone(params[2].val)

        tag = url.tags[7]
        self.assertEqual('EXT-X-KEY', tag.name)
        params = list(tag.params())
        self.assertEqual(3, len(params))
        self.assertEqual('METHOD', params[0].key)
        self.assertEqual('AES-128', params[0].val)
        self.assertFalse(params[0].quoted)
        self.assertEqual('URI', params[1].key)
        self.assertEqual('https://content-ausc4.uplynk.com/check2?b=7e986864b3014522ae734a1213ee3c80&v=86c8f49a240b4c6ba8b4028cda89a401&r=b&c=86c8f49a240b4c6ba8b4028cda89a401&pbs=c46967324531414fae658ee72847012e', params[1].val)
        self.assertTrue(params[1].quoted)
        self.assertEqual('IV', params[2].key)
        self.assertEqual('0x000000000000000000000000000008D2', params[2].val)
        self.assertFalse(params[2].quoted)

        url = urls[5]
        self.assertEqual(2, len(url.tags))
        self.assertEqual('https://x-live-fox-stgec.uplynk.com/80C078/ausw/slices/7e9/8baebcb1115a4bb78fa90c40ae8d81aa/7e986864b3014522ae734a1213ee3c80/B000008D7.ts?pbs=c46967324531414fae658ee72847012e&_jt=l&chid=86c8f49a240b4c6ba8b4028cda89a401&si=0', url.url)

        tag = url.tags[0]
        self.assertEqual('EXT-X-KEY', tag.name)
        params = list(tag.params())
        self.assertEqual(3, len(params))
        self.assertEqual('METHOD', params[0].key)
        self.assertEqual('AES-128', params[0].val)
        self.assertFalse(params[0].quoted)
        self.assertEqual('URI', params[1].key)
        self.assertEqual('https://content-ausc4.uplynk.com/check2?b=7e986864b3014522ae734a1213ee3c80&v=86c8f49a240b4c6ba8b4028cda89a401&r=b&c=86c8f49a240b4c6ba8b4028cda89a401&pbs=c46967324531414fae658ee72847012e', params[1].val)
        self.assertTrue(params[1].quoted)
        self.assertEqual('IV', params[2].key)
        self.assertEqual('0x000000000000000000000000000008D7', params[2].val)
        self.assertFalse(params[2].quoted)

        tag = url.tags[1]
        self.assertEqual('EXTINF', tag.name)
        params = list(tag.params())
        self.assertEqual(1, len(params))
        self.assertEqual('4.0960', params[0].key)
        self.assertIsNone(params[0].val)
