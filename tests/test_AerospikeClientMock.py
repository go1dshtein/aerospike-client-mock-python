import unittest
from AerospikeClientMock import AerospikeClientMock


class TestAerospikeClientMock(unittest.TestCase):
    def setUp(self):
        pass

    def test_blank_init(self):
        asm = AerospikeClientMock()
        self.assertEqual({}, asm.dump())

    def test_connected(self):
        asm = AerospikeClientMock()
        self.assertTrue(asm.is_connected())

    def test_put(self):
        asm = AerospikeClientMock()
        key = ("a", "b", "c")
        asm.put(key, {"a": 1})
        self.assertEqual({('a', 'b', 'c'): {'a': 1}}, asm.dump())
        self.assertEqual((('a', 'b', 'c'), {'gen': 1, 'ttl': 0}, {'a': 1}),
                         asm.get(key))
        asm.put(key, {"b": 1})
        self.assertEqual({('a', 'b', 'c'): {'a': 1, 'b': 1}}, asm.dump())
        self.assertEqual((('a', 'b', 'c'), {'gen': 2, 'ttl': 0}, {'a': 1, 'b': 1}),
                         asm.get(key))

    def test_dump(self):
        asm = AerospikeClientMock()
        key = ("a", "b", "c")
        asm.put(key, {"a": 1})
        self.assertEqual({('a', 'b', 'c'): {'a': 1}}, asm.dump())

    def test_incr(self):
        asm = AerospikeClientMock()
        key = ("a", "b", "c")
        asm.put(key, {"a": 1})
        asm.increment(key, "a", 1)
        self.assertEqual({('a', 'b', 'c'): {'a': 2}}, asm.dump())
        self.assertEqual((('a', 'b', 'c'), {'gen': 2, 'ttl': 0}, {'a': 2}),
                         asm.get(key))
        asm.increment(key, "a", 1)
        self.assertEqual({('a', 'b', 'c'): {'a': 3}}, asm.dump())
        self.assertEqual((('a', 'b', 'c'), {'gen': 3, 'ttl': 0}, {'a': 3}),
                         asm.get(key))

    def test_incr_value(self):
        asm = AerospikeClientMock()
        key = ("a", "b", "c")
        asm.put(key, {"a": 1})
        asm.increment(key, "a", 2)
        self.assertEqual({('a', 'b', 'c'): {'a': 3}}, asm.dump())
        self.assertEqual((('a', 'b', 'c'), {'gen': 2, 'ttl': 0}, {'a': 3}),
                         asm.get(key))

    def test_undefined_incr(self):
        asm = AerospikeClientMock()
        key = ("a", "b", "c")
        asm.increment(key, "a", 1)
        self.assertEqual({('a', 'b', 'c'): {'a': 1}}, asm.dump())
        self.assertEqual((('a', 'b', 'c'), {'gen': 1, 'ttl': 0}, {'a': 1}),
                         asm.get(key))
        asm.increment(key, "b", 1)
        self.assertEqual({('a', 'b', 'c'): {'a': 1, 'b': 1}}, asm.dump())
        self.assertEqual((('a', 'b', 'c'), {'gen': 2, 'ttl': 0}, {'a': 1, 'b': 1}),
                         asm.get(key))

    def test_append(self):
        asm = AerospikeClientMock()
        key = ("a", "b", "c")
        asm.put(key, {"word": "ello"})
        asm.prepend(key, "word", "h")
        self.assertEqual({('a', 'b', 'c'): {'word': 'hello'}}, asm.dump())
        self.assertEqual(
            (('a', 'b', 'c'), {'gen': 2, 'ttl': 0}, {'word': 'hello'}),
            asm.get(key))

    def test_prepend(self):
        asm = AerospikeClientMock()
        key = ("a", "b", "c")
        asm.put(key, {"word": "hell"})
        asm.append(key, "word", "o")
        self.assertEqual({('a', 'b', 'c'): {'word': 'hello'}}, asm.dump())
        self.assertEqual(
            (('a', 'b', 'c'), {'gen': 2, 'ttl': 0}, {'word': 'hello'}),
            asm.get(key))

    def test_get(self):
        asm = AerospikeClientMock()
        key = ("a", "b", "c")
        asm.put(key, {"a": 1})
        self.assertEqual((('a', 'b', 'c'), {'gen': 1, 'ttl': 0}, {'a': 1}),
                         asm.get(key))
        # test if not changing gen
        self.assertEqual((('a', 'b', 'c'), {'gen': 1, 'ttl': 0}, {'a': 1}),
                         asm.get(key))

    def test_select(self):
        asm = AerospikeClientMock()
        key = ("a", "b", "c")
        asm.put(key, {"a": 1, "b": 2, "c": 3})
        self.assertEqual(
            (('a', 'b', 'c'), {'gen': 1, 'ttl': 0}, {'a': 1, 'c': 3}),
            asm.select(key, ["a", "c"]))
        # test if not changing gen
        self.assertEqual(
            (('a', 'b', 'c'), {'gen': 1, 'ttl': 0}, {'a': 1, 'd': None}),
            asm.select(key, ["a", "d"]))

    def test_exists(self):
        asm = AerospikeClientMock()
        key = ("a", "b", "c")
        asm.put(key, {"a": 1})
        self.assertEquals((True, {'gen': 1, 'ttl': 0}), asm.exists(key))
        # test if not changing gen
        self.assertEquals((True, {'gen': 1, 'ttl': 0}), asm.exists(key))

    def test_not_exists(self):
        asm = AerospikeClientMock()
        key = ("a", "b", "c")
        self.assertEquals((False, None), asm.exists(key))

    def test_remove(self):
        asm = AerospikeClientMock()
        key = ("a", "b", "c")
        asm.put(key, {"a": 1})
        self.assertEquals({('a', 'b', 'c'): {'a': 1}}, asm.dump())
        asm.remove(key)
        self.assertEquals({}, asm.dump())
        self.assertEquals((False, None), asm.exists(key))

    def test_remove_bin(self):
        asm = AerospikeClientMock()
        key = ("a", "b", "c")
        asm.put(key, {"a": 1, "b": 1, "c": 1, "d": 1})
        self.assertEquals({('a', 'b', 'c'): {'a': 1, 'c': 1, 'b': 1, 'd': 1}},
                          asm.dump())
        self.assertEqual(
            (
                ('a', 'b', 'c'), {'gen': 1, 'ttl': 0},
                {'a': 1, 'c': 1, 'b': 1, 'd': 1}
            ), asm.get(key))
        asm.remove_bin(key, ["b", "d"])
        self.assertEquals({('a', 'b', 'c'): {'a': 1, 'c': 1}}, asm.dump())
        self.assertEqual(
            (('a', 'b', 'c'), {'gen': 2, 'ttl': 0}, {'a': 1, 'c': 1}),
            asm.get(key))
        asm.remove_bin(key, ["c"])
        self.assertEquals({('a', 'b', 'c'): {'a': 1}}, asm.dump())
        self.assertEqual((('a', 'b', 'c'), {'gen': 3, 'ttl': 0}, {'a': 1}),
                         asm.get(key))

    def test_get_many(self):
        asm = AerospikeClientMock()
        asm.put(("a", "b", 1), {"a": 1})
        asm.put(("a", "b", 2), {"a": 2})
        asm.put(("a", "b", 3), {"a": 3})
        asm.put(("a", "b", 4), {"a": 4})
        keys = [
            ("a", "b", 1),
            ("a", "b", 2),
            ("a", "b", 3),
            ("a", "b", 4),
            ("a", "b", 5),
        ]
        self.assertEqual(
            [
                (('a', 'b', 1, bytearray(b'u\x98t\x11La\x84\x9d\x94\xe3\xcdcSbn\xd7')), {'gen': 1, 'ttl': 0}, {'a': 1}),
                (('a', 'b', 2, bytearray(b'\xe7HY\x1f\x1f\xb8z\x8f\xf3\x0c\xf3\x04\xcc9\x14\xdc')), {'gen': 1, 'ttl': 0}, {'a': 2}),
                (('a', 'b', 3, bytearray(b'\xeb\x1a\x99(V\xd49\x01\xeeQ[\x92\x06-O\x08')), {'gen': 1, 'ttl': 0}, {'a': 3}),
                (('a', 'b', 4, bytearray(b'\xf3G\x1b\xba\xe2\xec\x11S\xc3\xc2\xab\x15\xb4\x1b\x96q')), {'gen': 1, 'ttl': 0}, {'a': 4}),
                (('a', 'b', 5, bytearray(b'd\t}\xc6`\xee\xe2\xf0)\x1f7\x9c\xfa\x8d\xa6\xd6')), None, None),
            ]
            , asm.get_many(keys))

    def test_exists_many(self):
        asm = AerospikeClientMock()
        asm.put(("a", "b", 1), {"a": 1})
        asm.put(("a", "b", 2), {"a": 2})
        asm.put(("a", "b", 3), {"a": 3})
        asm.put(("a", "b", 4), {"a": 4})
        keys = [
            ("a", "b", 1),
            ("a", "b", 2),
            ("a", "b", 3),
            ("a", "b", 4),
            ("a", "b", 5),
        ]
        self.assertEqual(
            [
                (("a", "b", 1), {'gen': 1, 'ttl': 0}),
                (("a", "b", 2), {'gen': 1, 'ttl': 0}),
                (("a", "b", 3), {'gen': 1, 'ttl': 0}),
                (("a", "b", 4), {'gen': 1, 'ttl': 0}),
                (("a", "b", 5), None),
            ]
            , asm.exists_many(keys))

    def test_select_many(self):
        asm = AerospikeClientMock()
        asm.put(("a", "b", 1), {"a": 1, "b": 1})
        asm.put(("a", "b", 2), {"a": 2, "b": 2})
        asm.put(("a", "b", 3), {"a": 3, "b": 3})
        asm.put(("a", "b", 4), {"a": 4, "b": 4})
        keys = [
            ("a", "b", 1),
            ("a", "b", 2),
            ("a", "b", 3),
            ("a", "b", 4),
            ("a", "b", 5),
        ]
        self.assertEqual(
            {
                ('a', 'b', 3): {'a': 3, 'b': 3},
                ('a', 'b', 2): {'a': 2, 'b': 2},
                ('a', 'b', 4): {'a': 4, 'b': 4},
                ('a', 'b', 1): {'a': 1, 'b': 1}
            },
            asm.dump())
        self.assertEqual(
            [
                (('a', 'b', 1), {'gen': 1, 'ttl': 0}, {'a': 1, 'b': 1}),
                (('a', 'b', 2), {'gen': 1, 'ttl': 0}, {'a': 2, 'b': 2}),
                (('a', 'b', 3), {'gen': 1, 'ttl': 0}, {'a': 3, 'b': 3}),
                (('a', 'b', 4), {'gen': 1, 'ttl': 0}, {'a': 4, 'b': 4}),
                None,
            ]
            , asm.select_many(keys, ["a", "b"]))
        self.assertEqual(
            [
                (('a', 'b', 1), {'gen': 1, 'ttl': 0}, {'b': 1}),
                (('a', 'b', 2), {'gen': 1, 'ttl': 0}, {'b': 2}),
                (('a', 'b', 3), {'gen': 1, 'ttl': 0}, {'b': 3}),
                (('a', 'b', 4), {'gen': 1, 'ttl': 0}, {'b': 4}),
                None,
            ]
            , asm.select_many(keys, ["b"]))


if __name__ == '__main__':
    unittest.main()
