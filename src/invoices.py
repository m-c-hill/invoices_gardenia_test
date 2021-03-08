"""
invoices.py: Module to create invoices between two companies and analyse their statistics (mean and median amount owed)
with classes Invoice and InvoiceStats.
"""

from datetime import datetime
import math
import statistics


class Invoice:
    """Class to represent an invoice, with payment to be made from recipient to the supplier.

      Attributes:
          issue_dt (str): Invoice date of creation.
          supplier (str): Name of the company issuing the invoice.
          recipient (str): Name of the company receiving the invoice
          pounds (int): Pounds part of invoice amount (£799.99 -> 799)
          pennies_rem (int): Pennies part of invoice amount (£799.99 -> 99)
          pennies_tot (int): Invoice total value in pennies (£799.99 -> 79999)

    """

    _MAX_VALUE_PENNIES = 2E10  # Maximum value of an invoice is £200,000,000.00, given here in pennies

    def __init__(self, supplier, recipient, pounds, pennies_rem):
        """Invoice constructor

        Function performs a basic check for invalid inputs by executing
        check_valid_inputs(). This ensures that:
          > the input amounts are integer and non-negative,
          > the input amount is no greater than £200,000,000.00,
          > and pennies_rem does not exceed 99
        or else an InvoiceValidationError exception is raised.

        The function also sets issue_dt to the current date.

        Args:
            supplier (str): Name of the company issuing the invoice.
            recipient (str): Name of the company receiving the invoice
            pounds (int): Pounds part of invoice amount (£799.99 -> 799)
            pennies_rem (int): Pennies part of invoice amount (£799.99 -> 99)
        """

        self.issue_dt = datetime.now().strftime("%Y-%m-%d")
        self.supplier = supplier
        self.recipient = recipient
        self.pounds = pounds
        self.pennies_rem = pennies_rem
        self.pennies_tot = self.convert_to_pennies()

        self._check_valid_inputs()

    def __repr__(self):
        return f"Invoice({self.issue_dt}, {self.supplier!r}, {self.recipient!r}, {self.pounds}, {self.pennies_rem})"

    def __str__(self):
        return f"Invoice\nDate Created: {self.issue_dt}\n" \
               f"Supplier: {self.supplier}\nRecipient: {self.recipient}\n" \
               f"Amount due: £{self.pounds}.{self.pennies_rem:02d}\n"

    def convert_to_pennies(self):
        """int: Converts pounds and pennies to the total number of pennies"""
        return 100 * self.pounds + self.pennies_rem

    def _check_valid_inputs(self):
        """None: Executes checks to ensure the input amounts of the invoice are acceptable."""

        self._check_int_values()
        self._check_negative_values()
        self._check_pennies()
        self._check_max_value()

    def _check_int_values(self):
        """None: Check if pounds and pennies_rem are integer values. If not, an InvoiceValidationError exception is
        raised.
        """
        if not isinstance(self.pounds, int):
            raise InvoiceValidationError(
                f"Pounds cannot be of type {type(self.pounds).__name__}. "
                f"For valid invoice, pounds must be an integer value.")

        if not isinstance(self.pennies_rem, int):
            raise InvoiceValidationError(
                f"Pennies cannot be of type {type(self.pennies_rem).__name__}. "
                f"For valid invoice, pennies must be an integer value.")

    def _check_negative_values(self):
        """None: Check if pounds and pennies_rem are non-negative values. If not, an InvoiceValidationError exception is
        raised.
        """
        if self.pounds < 0 or self.pennies_rem < 0:
            raise InvoiceValidationError("Invoice values cannot be negative.")

    def _check_pennies(self):
        """None: Check that input pennies is less that 100. If not, an InvoiceValidationError exception is raised.
        """
        if self.pennies_rem > 99:
            raise InvoiceValidationError("Pennies cannot be greater than 99.")

    def _check_max_value(self):
        """None: Check if pennies_tot is greater than the maximum allowed invoice value. If so, an
        InvoiceValidationError exception is raised.
        """
        if self.pennies_tot > self._MAX_VALUE_PENNIES:
            raise InvoiceValidationError(
                f"Total invoice amount cannot be greater than £200,000,000.00. Attempted invoice value: "
                f"£{self.pounds}.{self.pennies_rem}.")


class InvoiceStats:
    """Class to store invoices and calculate the mean and median of stored invoice amounts.

      Attributes:
        invoice_list (list): list to store all invoices.
        invoice_count (int): running total of invoices stored in invoice_list.
    """

    _INVOICE_COUNT_MAX = 2E7  # Maximum number of invoices that InvoiceStats can contain: 20,000,000

    def __init__(self, *args):
        """InvoiceStats constructor

        Args:
            *args: undefined number of Invoices may be passed in when InvoiceStats is initialised.
        """
        self.clear()
        self.add_invoices(list(args))

    def add_invoices(self, invoices):
        """Appends multiple invoices to the internal list of invoices

        Args:
          invoices (list): list of invoices to process
        Returns:
          None
        """
        for invoice in invoices:
            self.add_invoice(invoice)

    def add_invoice(self, invoice):
        """Appends a single invoice to the internal list of invoices and increments the invoice_count by 1.

        Also executes is_invoice() to check if the argument 'invoice' is an Invoice object. If not, an
        InvoiceStatsTypeError exception is raised.

        Args:
          invoice (Invoice): invoice to be stored
        Returns:
          None
        """
        self.is_invoice(invoice)
        self.check_max_invoice_num()
        self.invoice_count += 1
        self.invoice_list.append(invoice)

    def clear(self):
        """None: Resets the internal storage and clears all data by emptying the invoice list and setting the invoice
        count to zero"""
        self.invoice_list = []
        self.invoice_count = 0

    def invoice_amounts(self):
        """tuple: Returns a tuple containing the amounts of each invoice in pennies"""
        return (amount.pennies_tot for amount in self.invoice_list)

    def get_median(self):
        """double: Calculates the median invoice amount for all stored invoices in pennies, rounded half down"""
        _invoice_amounts = self.invoice_amounts()
        return self.round_half_down(statistics.median(_invoice_amounts))

    def get_mean(self):
        """double: Calculates the mean invoice amount for all stored invoices in pennies, rounded half down"""
        _invoice_amounts = self.invoice_amounts()
        return self.round_half_down(statistics.mean(_invoice_amounts))

    @staticmethod
    def round_half_down(pennies):
        """Rounds an input value of pennies half down (ie. 98.7 -> 99, 99.3 -> 99, 99.5 -> 99).

        Calculates the fractional part of 'pennies' using the modulus operator, then returns
        pennies rounded down if this fractional part is less than or equal to 0.5. If not,
        it returns the rounded up value. This is achieved using the math.floor and math.ceil
        functions, respectively.

        Args:
          pennies (double):
        Returns:
          int: pennies, rounded half down
        """
        fractional_penny = pennies % 1
        return math.floor(pennies) if (fractional_penny <= 0.5) else math.ceil(pennies)

    def is_invoice(self, invoice):
        """None: Check if 'invoice' is an instance of the class Invoice. If not, raise an InvoiceStatsTypeError
        exception.
        """

        if not isinstance(invoice, Invoice):
            raise InvoiceStatsTypeError(type(invoice).__name__)

    def check_max_invoice_num(self):
        """None: Check if invoice count is greater than the maximum number of invoices which can be stored. If so, an
        InvoiceValidationError exception is raised.
        """
        if self.invoice_count >= self._INVOICE_COUNT_MAX:
            raise MaxNumberOfInvoicesError(self._INVOICE_COUNT_MAX)


class InvoiceValidationError(Exception):
    def __init__(self, message):
        super().__init__(message)


class InvoiceStatsTypeError(Exception):
    def __init__(self, data_type):
        super().__init__(f"Cannot pass type {data_type} into InvoiceStats")


class MaxNumberOfInvoicesError(Exception):

    def __init__(self, max_invoice_num):
        super().__init__(f"InvoiceStats has reached maximum number of stored invoices: {max_invoice_num}. "
                         f"Use the clear() function to reduce memory load.")