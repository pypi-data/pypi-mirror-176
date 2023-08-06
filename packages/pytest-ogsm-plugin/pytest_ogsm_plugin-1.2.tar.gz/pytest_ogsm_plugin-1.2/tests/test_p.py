#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/11/10 3:29 PM
# @Author  : cw
import pytest


@pytest.mark.parametrize("name", ["小文", "小曾", "小s"])
def test_encode(name):
    print(name)
