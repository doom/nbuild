#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

import stdlib
import fnmatch
import itertools
import collections


class Aggregate(collections.MutableMapping):
    def __init__(self, *packages):
        self._pkgs = dict()
        self.push(*packages)

    def push(self, *packages):
        for package in packages:
            self._pkgs[package.id.name] = package

    def filter(self, predicate):
        for pkg in self._pkgs.values():
            if fnmatch.fnmatch(pkg.id.name, predicate):
                yield pkg

    def __getitem__(self, key) -> stdlib.Package:
        return self._pkgs[key]

    def __setitem__(self, key, value):
        self._pkgs[key] = value

    def __delitem__(self, key):
        del self._pkgs[key]

    def __iter__(self):
        return iter(self._pkgs.values())

    def __len__(self):
        return len(self._pkgs)

    def __add__(self, rvalue: 'Aggregate'):
        ret = stdlib.Aggregate()
        ret._pkgs.update(self._pkgs)
        ret._pkgs.update(rvalue._pkgs)
        return ret

    def __iadd__(self, rvalue: 'Aggregate'):
        self._pkgs.update(rvalue._pkgs)
        return self
