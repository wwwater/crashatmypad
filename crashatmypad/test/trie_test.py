import unittest

from crashatmypad.util.trie import Trie


class TrieTest(unittest.TestCase):
    def test_trie(self):
        trie = Trie()
        trie.add('abc')
        trie.add('abd')
        trie.add('bcd')

        assert trie.get('abc') == ['abc']
        assert trie.get('ab') == ['abc', 'abd']
        assert trie.get('xx') == []
        assert trie.get(None) == []

if __name__ == "__main__":
    unittest.main()
