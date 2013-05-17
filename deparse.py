#! /usr/bin/env python
# coding:utf-8

from __future__ import division
import CaboCha


class Parser(object):

    def __init__(self, s, *args):
        self._parser = CaboCha.Parser(*args)
        self._tree = self._parser.parse(s)

    @property
    def tree(self):
        return Tree(self._tree)

    def __iter__(self):
        self._chunk_index = 0
        return self

    def next(self):
        if self._chunk_index >= self._tree.chunk_size():
            raise StopIteration
        else:
            ind = self._chunk_index
            self._chunk_index += 1
            return Chunk(self._tree.chunk(ind), ind, self._tree)


class Tree(object):
    """Wrapper class for CaboCha.Tree"""
    def __init__(self, tree):
        self._tree = tree

    def __getattr__(self, name):
        return getattr(self._tree, name)

    def __iter__(self):
        self._chunk_index = 0
        return self

    def next(self):
        if self._chunk_index >= self.chunk_size():
            raise StopIteration
        else:
            ind = self._chunk_index
            self._chunk_index += 1
            return Chunk(self.chunk(ind), ind, self._tree)


class Chunk(object):
    """Wrapper class for CaboCha.Chunk"""
    def __init__(self, chunk, i, tree):
        self._chunk = chunk
        self._id = i
        self._tree = tree

    def __getattr__(self, name):
        return getattr(self._chunk, name)

    def __iter__(self):
        self._token_index = 0
        return self

    def next(self):
        if self._token_index >= self._chunk.token_size:
            raise StopIteration
        else:
            ind = self._token_index
            self._token_index += 1
            pos = self.token_pos + ind
            return Token(self._tree.token(pos), pos)

    @property
    def id(self):
        return self._id

    @property
    def chunk(self):
        return self._chunk

    @property
    def tree(self):
        return self._tree

    def __unicode__(self):
        form = u'<chunk id={} link={} rel={} score={} head={} func={}>'
        return form.format(
            self.id,
            self.link,
            "",
            self.score,
            self.head_pos,
            self.func_pos,)

    def __str__(self):
        return self.__unicode__().encode('utf-8')

    def __repr__(self):
        return self.__str__()


class Token(object):
    """Wrapper class for CaboCha.Token"""
    def __init__(self, token, i):
        self._token = token
        self._id = i

    def __getattr__(self, name):
        if name == "feature":
            return self._token.feature.decode('utf-8')
        elif name == "surface":
            return self._token.surface.decode('utf-8')
        return getattr(self._token, name)

    @property
    def id(self):
        return self._id

    def __unicode__(self):
        fmt = u'<tok id={} feature={} ne={}>{}</tok>'
        return fmt.format(self._id,
                          self.feature,
                          self.ne,
                          self.surface)

    def __str__(self):
        return self.__unicode__().encode('utf-8')

    def __repr__(self):
        return self.__str__()


if __name__ == '__main__':

    s = u"兄は今日鍋を食べる予定です。".encode('utf-8')
    parser = Parser(s, '--charset=UTF8')
    for chunk in parser:
        print chunk
        for token in chunk:
            print " ", token
