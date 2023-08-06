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

__all__ = ("WordHunt",)

from typing import Dict, List, Tuple, Union
from wordhuntanagram.matrices import Matrix
from wordhuntanagram.base import WordBase



class WordHunt(WordBase): 

    def __init__(self, n_column:int=None, n_rows:int=None, matrix:Matrix=None, args:list[str]=None, auto_input:bool=True):
        if matrix is None:
            if not auto_input:
                pass
            else:
                args = []
            super().__init__(n_column*n_rows, state='wordhunt', force_state=True, auto_input=auto_input, split=(n_column, n_rows), args=args)
        else:
            super().__init__(word_matrix=matrix)
                
    def hunt(self) -> None:
        # start_with 3 letter words
        matrix = self._matrix
        # pick a point and use that point to find words
        for row in range(matrix.len_row()):
            for column in range(matrix.len_column()):
                self.walk_ordered([[[column, row]]])

    def make_matrix(self, args: Union[List, str, Tuple]) -> None:
        i = 0
        for row in range(self._matrix.len_row()):
            for column in range(self._matrix.len_column()):
                self._matrix.insert(row, column, args[i])
                i += 1

    def is_word(self, word: str, words: Union[List[str], Dict[str, int]]) -> bool:
        return word in words
        
    def walk(self, path:List[List[int, int]]) -> str:
        word = ""
        for step in path:
            word += self._matrix.index(step[1], step[0])
        return word

    def is_in_trie(self, word: str, path: List[List[int, int]]) -> bool:
        trie = self.root
        for letter in word:
            if letter in trie:
                trie = trie[letter]
            else:
                return False
        if trie['isWord']:
            self.words[word] = path
        return True

    def walk_ordered(self, paths: List[List[List[int, int]]], new_paths: Union[List[List[List[int, int]]], None]=None, index: int=0, trie: Dict=None) -> List[List[List[int, int]]]:
        if not new_paths:
            new_paths = []
        if not trie:
            trie = self.root
        for path in paths:
            word_initial = self.walk(path)
            for direction in [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
                new_path = [path[-1][0]+direction[0], path[-1][1]+direction[1]]
                if 0 <= new_path[0] < self._matrix.len_column() and 0 <= new_path[1] < self._matrix.len_row() and new_path not in path:
                    path_moved = path + [new_path]
                    word = word_initial + self._matrix.index(new_path[1], new_path[0])
                    if self.is_in_trie(word, path_moved):
                        new_paths.append(path_moved)
                    else:
                        pass
        if new_paths:
            paths += self.walk_ordered(new_paths, index=index+1)
        return paths
        
    def get_word(self, path: List[List[int, int]]) -> str:
        return self._matrix.index(path[1], path[0])

        

