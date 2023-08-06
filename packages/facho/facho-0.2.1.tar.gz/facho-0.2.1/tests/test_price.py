#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of facho.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

"""Tests for `facho` package."""

import pytest

import facho.fe.form as form

def test_price_amount():
    price = form.Price(
        amount = form.Amount(50.00),
        type_code = '01',
        type = 'x',
        quantity = 2
    )
    assert price.amount == form.Amount(100.00)
