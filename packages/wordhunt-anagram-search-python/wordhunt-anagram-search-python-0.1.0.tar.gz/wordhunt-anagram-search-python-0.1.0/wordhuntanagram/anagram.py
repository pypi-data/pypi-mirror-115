#!/usr/bin/python
# The MIT License (MIT)
# Copyright (c) 2017 "Allotey Immanuel Adotey"<imma.adt@gmail.com>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
# OR OTHER DEALINGS IN THE SOFTWARE.


__all__ = ("Anagram", )

from typing import Dict, List, Set, Tuple, Union
from wordhuntanagram.matrices import Matrix
from wordhuntanagram.base import WordBase


class Anagram(WordBase):

    def __init__(self, n_column: int=None, matrix: Matrix=None, args: Union[List, Tuple, str]=None, auto_input: bool=True) -> None:
        if matrix is None:
            if not auto_input:
                pass
            else:
                args = []
            super().__init__(n_column, state='anagram', force_state=True, auto_input=auto_input, args=args)
        else:
            super().__init__(word_matrix=matrix)

    def make_matrix(self, args: Union[List, Tuple, str]) -> None:
        i = 0
        for column in range(len(args)):
            self._matrix.insert(0, column, args[i])
            i += 1

    def hunt(self) -> None:
        words=self.findWords(self.root, self._matrix.as_string(flatten=True), '')
        for word in words:
            self.words[word] = 1

    def findWords(self, trie: Dict, word: str, currentWord: str) -> Set[str]:
        myWords = set()      
        for letter_index in range(len(word)):
            if word[letter_index] in trie:
                newWord = currentWord + word[letter_index]
                if trie[word[letter_index]]['isWord']:
                    myWords.add(newWord)
                myWords = myWords.union(self.findWords(trie[word[letter_index]], word[:letter_index]+word[letter_index+1:], newWord))
        return myWords