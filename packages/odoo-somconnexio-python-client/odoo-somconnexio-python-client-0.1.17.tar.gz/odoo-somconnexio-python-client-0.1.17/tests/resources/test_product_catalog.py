from __future__ import unicode_literals  # support both Python2 and 3

import pytest
import unittest2 as unittest

from odoo_somconnexio_python_client.resources.product_catalog import Product, ProductCatalog


class TariffTests(unittest.TestCase):
    @pytest.mark.vcr()
    def test_search_code(self):
        pricelists = ProductCatalog.search(code="21IVA")
        tariff_names = []
        tariff_codes = []
        tariff_available_for = []

        pricelist_21IVA = pricelists[0]
        self.assertIsInstance(pricelist_21IVA, ProductCatalog)
        self.assertEqual(pricelist_21IVA.code, '21IVA')
        self.assertEqual(len(pricelist_21IVA.products), 35)
        for product in pricelist_21IVA.products:
            self.assertIsInstance(product, Product)
            tariff_names.append(product.name)
            tariff_codes.append(product.code)
            tariff_available_for.append(product.available_for)

        self.assertIn(
            "ADSL 1000 min a fix",
            tariff_names
        )
        self.assertIn(
            "SE_SC_REC_BA_F_100",
            tariff_codes
        )
        self.assertIn(
            ["member"],
            tariff_available_for
        )

    @pytest.mark.vcr()
    def test_search_non_existant_code(self):
        pricelists = ProductCatalog.search(code="BBBB")
        self.assertEqual(len(pricelists), 0)

    @pytest.mark.vcr()
    def test_search_code_with_category_filter(self):
        pricelists = ProductCatalog.search(code="21IVA", category="mobile")
        tariff_codes = []

        pricelist_21IVA = pricelists[0]
        self.assertEqual(len(pricelist_21IVA.products), 29)
        for product in pricelist_21IVA.products:
            tariff_codes.append(product.code)
            self.assertEqual(product.category, "mobile")

        self.assertNotIn(
            "SE_SC_REC_BA_F_100",
            tariff_codes
        )
        self.assertIn(
            "SE_SC_REC_MOBILE_T_0_0",
            tariff_codes
        )
