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


import json
from wordhuntanagram.file_tree import resource_path
from wordhuntanagram.logger import directLog
import os
from wordhuntanagram.matrices import Matrix
import math

# Load words into memory
WORDS_FILE = resource_path('words.json')
TRIE_FILE = resource_path('data/trie_store.json')


def load_words() -> dict:
    """
    Loads dictionary trie into the memory
    """
    with open(WORDS_FILE, 'rb') as w_file:
        return json.load(w_file)

def unload_words() -> bool:
    """
    Removes dictionary json from memory
    """
    global WORDS_JSON
    WORDS_JSON = None
    return True


class InitFile(object):

    def __init__(self, words:dict) -> None:
        self.root = {'isWord': False}
        if not words:
            words = load_words()
        if not self._get_trie():
            self.make_trie(words)
        # self.hunt(words)

    def make_trie(self, word_dict:dict) -> None:
        """
        Creates trie from word dictionary
        """
        for word in word_dict:
            if len(word) >= 3:
                self._add_to_trie(self.root, word)
        self.json_store()
        
    def json_store(self) -> None:
        with open(TRIE_FILE, 'w') as json_trie:
            json.dump(self.root, json_trie)
    
    def _add_to_trie(self, child:dict, word:str, index:int=0):
        if index >= len(word):
            child['isWord'] = True
            return
        if word[index] not in child:
            child[word[index]] = {'isWord': False}
        else:
            pass
        self._add_to_trie(child[word[index]], word, index+1)

    def _get_trie(self):
        if os.path.exists(TRIE_FILE):
            try:
                with open(TRIE_FILE, 'r') as file:
                    self.root = json.load(file)
            except Exception as E:
                directLog(f"Exception {E} occured. Creating new trie...")
                return False
            else:
                return True
        else:
            return False

    def get_trie(self):
        return self.root


WORDS_JSON = load_words()
WORDS_TRIE = InitFile(WORDS_JSON).get_trie()

class WordBase(object):
    _state = None
    _n_words = None
    __states = ['anagram', 'wordhunt']

    def __init__(self, n_words:int=6, word_matrix:Matrix=None, auto_input:bool=True, force_state:bool=False, state:str=None, split:tuple[int, int]=None, args:list=None) -> None:
        self.words = {}
        self.root = WORDS_TRIE
        self._force_state = force_state
        if self._force_state:
            if state == 'wordhunt':
                self._split = split
            elif state == 'anagram':
                self._split = (1, len(args)) if len(args) else (1, 0)
            self.state = state
        if not word_matrix:
            self.n_words = n_words
        else:
            self.word_matrix = word_matrix
            if self.state == 'anagram':
                self._split = (1, len(word_matrix))
        if auto_input:
            self.add_input_from_prompt()
        else:
            self.make_matrix(args)

    def make_matrix(self, args:list):
        """Making matrix"""

    def hunt(self) -> None:
        """
        Starts the search fpr words in a module
        """
        return ValueError("Not implemented")

    @property
    def word_matrix(self) -> Matrix:
        return self._matrix

    @word_matrix.setter
    def word_matrix(self, value):
        if isinstance(value, Matrix):
            self._matrix = value

    @property
    def state(self) -> str:
        """
        Returns the state of the class
        """
        return self._state

    @state.setter
    def state(self, value):
        if value in self.__states:
            self._state = value
        else:
            raise ValueError(f"Unrecognized state: {value}, must be in {self.__states}")

    @property
    def n_words(self):
        return self._n_words

    @n_words.setter
    def n_words(self, value):
        if isinstance(value, int):
            self._n_words = value
            symmetry_value = math.sqrt(value)
            if not self._force_state:
                if symmetry_value.is_integer():
                    self._matrix = Matrix(i=int(symmetry_value), j=int(symmetry_value), args=['' for _ in range(int(value))])
                    self.state = 'wordhunt'
                else:
                    self._matrix = Matrix(j=1, i=value, args=['' for _ in range(value)])
                    self.state = 'anagram'
            else:
                if self.state == 'anagram':
                    self._matrix = Matrix(j=1, i=value, args=['' for _ in range(value)])
                elif self.state == 'wordhunt':
                    if self._split:
                        i = self._split[0]
                        j = self._split[1]
                    else:
                        i=int(symmetry_value)
                        j=int(symmetry_value)
                    self._matrix = Matrix(i=j, j=i, args=['' for _ in range(int(i*j))])
                    self._n_words = i*j
                else:
                    raise ValueError(f"Unrecognized state {self.state}")    
                
        elif value is None:
            if self._split:
                i = self._split[0]
                j = self._split[1]
                self._matrix = Matrix(i=i, j=j, args=['' for _ in range(int(i*j))])
                self._n_words = i*j
                print('done')
            else:
                raise ValueError(f'Number of words must be an integer else split must be defined : {self._split}')
        else:
            raise ValueError(f"Number of words must be an integer, not {type(value)}")

    def add_input_from_prompt(self) -> None:
        """
        Halts the program to allow user to change matrix. For console use only.
        """
        if self._state == 'anagram':
            for column in range(self.n_words):
                requested_value = input(f'AnagramWord index: {column}>> ')
                self._matrix.insert(0, column, requested_value)
        elif self._state == 'wordhunt':
            for row in range(self._matrix.len_row()):
                for column in range(self._matrix.len_column()):
                    requested_value = input(f'Wordhunt index: {column} x {row}>> ')
                    self._matrix.insert(row, column, requested_value)

    def __repr__(self):
        return str(self._matrix)