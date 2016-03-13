from crashatmypad.util.trie import Trie


def test_trie():
    trie = Trie()
    trie.add('abc')
    trie.add('abd')
    trie.add('bcd')

    assert trie.get('abc') == ['abc']
    assert trie.get('ab') == ['abc', 'abd']
    assert trie.get('xx') == []


test_trie()