"""
Unit testing for the module invoices
"""

import unittest
from invoices import Invoice, InvoiceStats, InvoiceStatsTypeError, InvoiceValidationError, MaxNumberOfInvoicesError


class TestInvoices(unittest.TestCase):
    """Class to execute unit tests for the class Invoice.
    """

    def test_convert_to_pennies(self):
        """
        Test: convert_to_pennies method called on test_invoice_1 with value £19.84.
        Verification: Should return the value 1984 pennies.
        """
        test_invoice_1 = Invoice("Company-A", "Company-B", 19, 84)
        pennies_calculated = test_invoice_1.convert_to_pennies()
        pennies_expected = 1984

        self.assertEqual(pennies_calculated, pennies_expected)

    def test_invoice_negative_penny_amount(self):
        """
        Test: Invoice penny amount is negative.
        Verification: Should raise an InvoiceValidationError exception.
        """
        self.failUnlessRaises(InvoiceValidationError, Invoice, "Company-A", "Company-B", 1000, -99)

    def test_invoice_large_penny_amount(self):
        """
        Test: Invoice penny amount greater than 99.
        Verification: Should raise an InvoiceValidationError exception.
        """
        self.failUnlessRaises(InvoiceValidationError, Invoice, "Company-A", "Company-B", 1000, 121)

    def test_invoice_non_integer_pound_amount(self):
        """
        Test: Invoice pound is a float.
        Verification: Should raise an InvoiceValidationError exception.
        """
        self.failUnlessRaises(InvoiceValidationError, Invoice, "Company-A", "Company-B", 1000.5, 12)

    def test_invoice_amount_too_high(self):
        """
        Test: Invoice value is greater than the maximum allowed amount (£200,000,000.00)
        Verification: Should raise an InvoiceValidationError exception.
        """
        self.failUnlessRaises(InvoiceValidationError, Invoice, "Company-A", "Company-B", 2.1e10, 0)


class TestInvoiceStats(unittest.TestCase):
    """Class to execute unit tests for the class InvoiceStats.
    """
    test_invoice_1 = Invoice("Company-A", "Company-B", 1000, 0)
    test_invoice_2 = Invoice("Company-A", "Company-C", 2500, 0)
    test_invoice_3 = Invoice("Company-A", "Company-D", 3000, 0)

    def test_add_invoice(self):
        """
        Test: Call the add_invoice method to add test_invoice_1 to invoice_stat
        Verification: The last element of the invoice_list in invoice_stat should be equal to the invoice just added
        """
        invoice_stat = InvoiceStats()
        invoice_stat.add_invoice(self.test_invoice_1)
        self.assertEqual(self.test_invoice_1, invoice_stat.invoice_list[-1])

    def test_add_invoices(self):
        """
        Test: Call the add_invoice method to add test_invoice_[1,2] to invoice_stat
        Verification: The last two elements of the invoice_list in invoice_stat should be equal to the two invoices
        just added.
        """
        invoice_stat = InvoiceStats()
        invoice_stat.add_invoices([self.test_invoice_1, self.test_invoice_2])
        self.assertEqual([self.test_invoice_1, self.test_invoice_2], invoice_stat.invoice_list[-2:])

    def test_add_invoice_invalid_type(self):
        """
        Test: Add a non-Invoice object to InvoiceStats (in this case a String)
        Verification: Should raise an InvoiceStatsTypeError exception.
        """
        invoice_stat = InvoiceStats()
        with self.assertRaises(InvoiceStatsTypeError) as context:
            invoice_stat.add_invoice("invoice")

    def test_add_invoice_raise_validation_error(self):
        """
        Test: Add an invalid invoice to InvoiceStats, in this case a negative pound amount.
        Verification: Should raise an InvoiceValidationError exception.
        """
        invoice_stat = InvoiceStats()
        with self.assertRaises(InvoiceValidationError) as context:
            invoice_stat.add_invoice(Invoice("Company-A", "Company-B", -20000, 0))

    def test_max_num_invoices_in_invoice_stat(self):
        """
        Test: Set the invoice count of InvoiceStats to be equal to the limit (20,000,000), then try adding an invoice.
        Verification: Should raise an MaxNumberOfInvoicesError exception.
        """
        invoice_stat = InvoiceStats()
        invoice_stat.invoice_count = InvoiceStats._INVOICE_COUNT_MAX

        with self.assertRaises(MaxNumberOfInvoicesError) as context:
            invoice_stat.add_invoice(self.test_invoice_1)

    def test_round_half_down(self):
        """
        Test: Pass a series of values into round_half_down .
        Verification: List of expected values should match the results of the calculation.
        """
        test_values = [10.0, 10.2, 10.5, 10.5000001, 10.8]
        expected_results = [10, 10, 10, 11, 11]
        test_results = []

        for value in test_values:
            test_results.append(InvoiceStats.round_half_down(value))

        self.assertEqual(test_results, expected_results)

    def test_median(self):
        """
        Test: Add three test invoices to InvoiceStats, calculate the median and compare the result to the expected
        value.
        Verification: Expected median value should match the results of the calculation.
        """
        invoice_stats = InvoiceStats(self.test_invoice_1, self.test_invoice_2, self.test_invoice_3)
        median_calculated = invoice_stats.get_median()
        median_expected = 250000
        self.assertEqual(median_calculated, median_expected)

    def test_mean(self):
        """
        Test: Add three test invoices to InvoiceStats, calculate the mean and compare the result to the expected value.
        Verification: Expected mean value should match the results of the calculation.
        """
        invoice_stats = InvoiceStats(self.test_invoice_1, self.test_invoice_2, self.test_invoice_3)
        mean_calculated = invoice_stats.get_mean()
        mean_expected = 216667
        self.assertEqual(mean_calculated, mean_expected)

    def test_clear(self):
        """
        Test: Add three test invoices to InvoiceStats and then call the clear() method. Record the value of the invoice
        count before and after clearing, and compare to the expected values.
        Verification: Expected count values before and after should match the true count values before and after
        calling clear().
        """
        invoice_count_before_and_after = []
        invoice_count_before_and_after_expected = [3, 0]

        invoice_stats = InvoiceStats(self.test_invoice_1, self.test_invoice_2, self.test_invoice_3)
        invoice_count_before_and_after.append(invoice_stats.invoice_count)

        invoice_stats.clear()
        invoice_count_before_and_after.append(invoice_stats.invoice_count)

        self.assertEqual(invoice_count_before_and_after, invoice_count_before_and_after_expected)


if __name__ == "__main__":
    unittest.main()