
_end = '_end_'


class Trie:
    def __init__(self):
        self.__trie__ = {}
        self.size = 0

    def add(self, word):
        word = word.lower()
        current_node = self.__trie__
        for letter in word:
            current_node = current_node.setdefault(letter, {})
        if _end not in current_node:
            current_node[_end] = _end
            self.size += 1

    def get(self, word):
        if word is None:
            return []
        word = word.lower()
        current_node = self.__trie__
        for letter in word:
            current_node = current_node.get(letter)
            if current_node is None:
                return []
        results = []
        self.__collect_words__(current_node, word, results)
        return results

    def __collect_words__(self, node, word, results):
        if _end in node:
            results.append(word)
        for letter in node.keys():
            if letter is not _end:
                self.__collect_words__(node[letter], word + letter, results)


