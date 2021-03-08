import invoices

def main():
    """Example of the module invoices, demonstrating the classes Invoice and InvoiceStats, and their associated methods.

    For unit testing, please see test_invoices.py
    """

    # Company A issues 3 invoices to Companies B, C & D

    invoice_1 = invoices.Invoice("Company-A", "Company-B", 12955, 79)
    print(invoice_1)

    invoice_2 = invoices.Invoice("Company-A", "Company-C", 36001, 12)
    print(invoice_2)

    invoice_3 = invoices.Invoice("Company-A", "Company-D", 9849, 9)
    print(invoice_3)

    # Company A creates InvoiceStat to calculate the mean and median owed to them

    invoice_stat = invoices.InvoiceStats(invoice_1, invoice_2, invoice_3)

    # Company A needs to add a missed invoice to Company E by calling the add_invoice method

    invoice_4 = invoices.Invoice("Company-A", "Company-E", 18500, 50)
    print(invoice_4)
    invoice_stat.add_invoice(invoice_4)

    # Company A now calculates the median and mean of the owed amount in pennies

    mean_amount = invoice_stat.get_mean()
    print(f"Mean: £{str(mean_amount)[:-2]}.{str(mean_amount)[-2:]}")

    median_amount = invoice_stat.get_median()
    print(f"Median: £{str(median_amount)[:-2]}.{str(median_amount)[-2:]}")


if __name__ == "__main__":
    main()