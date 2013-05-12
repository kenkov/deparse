#! /usr/bin/env python
# coding:utf-8

from __future__ import division
import CaboCha


class Parser(object):

    def __init__(self, s, *args):
        self._parser = CaboCha.Parser(*args)
        self._tree = self._parser.parse(s)

    def __iter__(self):
        self._chunk_index = 0
        return self

    #def parse(self, s):

    def next(self):
        if self._chunk_index >= self._tree.chunk_size():
            raise StopIteration
        else:
            ind = self._chunk_index
            self._chunk_index += 1
            return Chunk(self._tree,
                         ind)


class Chunk(object):

    def __init__(self, tree, i):
        self._chunk = tree.chunk(i)
        self._id = i
        self._tree = tree

    def __iter__(self):
        self._token_index = 0
        return self

    def next(self):
        if self._token_index >= self._chunk.token_size:
            raise StopIteration
        else:
            ind = self._token_index
            self._token_index += 1
            pos = self._chunk.token_pos + ind
            return Token(self._tree.token(pos),
                         pos)

    @property
    def id(self):
        return self._id

    @property
    def chunk(self):
        return self._chunk

    # CaboCha.Chunk propaties
    @property
    def additional_info(self):
        return self._chunk.additional_info

    @property
    def feature_list_size(self):
        return self._chunk.feature_list_size

    @property
    def func_pos(self):
        return self._chunk.func_pos

    @property
    def head_pos(self):
        return self._chunk.head_pos

    @property
    def link(self):
        return self._chunk.link

    @property
    def score(self):
        return self._chunk.score

    @property
    def token_pos(self):
        return self._chunk.token_pos

    @property
    def token_size(self):
        return self._chunk.token_size

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


class Token(object):

    def __init__(self, token, i):
        self._token = token
        self._id = i

    @property
    def additional_info(self):
        return self._token.additional_info

    @property
    def chunk(self):
        return self._token.chunk

    @property
    def feature(self):
        return self._token.feature.decode('utf-8')

    @property
    def feature_list_size(self):
        return self._token.feature_list_size

    @property
    def ne(self):
        return self._token.ne

    @property
    def normalized_surface(self):
        return self._token.normalized_surface.decode('utf-8')

    @property
    def surface(self):
        return self._token.surface.decode('utf-8')

    def __unicode__(self):
        fmt = u'<tok id={} feature={} ne={}>{}</tok>'
        return fmt.format(self._id,
                          self.feature,
                          self.ne,
                          self.surface)

    def __str__(self):
        return self.__unicode__().encode('utf-8')


if __name__ == '__main__':

    s = u"兄は今日鍋を食べる予定です。".encode('utf-8')
    parser = Parser(s, '--charset=UTF8')
    for chunk in parser:
        print chunk
        for token in chunk:
            print " ", token
