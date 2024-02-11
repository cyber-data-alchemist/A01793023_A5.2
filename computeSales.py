#!/usr/bin/env python3
# pylint: disable=invalid-name
"""
This module calls a ProductList.json and a Sales.Json to compute sales.
"""

import os
import sys
import json
import time
import csv


class ComputeSales:
    """
    It loads a list of products and sales and compute the totals.

    Methods:

    """
    def __init__(self, file_path_catalogue, file_path_sales):
        """
        Initiates the class.
        """
        self.file_path_catalogue = file_path_catalogue
        self.file_path_sales = file_path_sales
        self.data_errors = []
        self.catalogue_data = []
        self.sales_data = []
        self.computed_sales = []
        self.__load_data__()
        self.compute_sales()

    def __validate_file_exists__(self, file_path):
        """
        Check if the file exists. If not, raise an error.
        """
        if not os.path.isfile(file_path):
            self.data_errors.append(f"File {file_path} does not exist.")

    def __validate_catalogue_file__(self):
        """
        Validates the catalogue file is a valid json.
        Required keys: 'title' and 'price'.
        """
        for idx, product in enumerate(self.catalogue_data, start=1):
            for key in ['title', 'price']:
                if key not in product:
                    self.data_errors.append(
                        f"Line {idx}: Missing key '{key}' in catalogue file."
                        )

    def __validate_sales_file__(self):
        """
        Validates the sale file is a valid json.
        Required keys: 'Product' and 'Quantity'.
        """
        for idx, sale in enumerate(self.sales_data, start=1):
            for key in ['Product', 'Quantity']:
                if key not in sale:
                    self.data_errors.append(
                        f"Line {idx}: Missing key '{key}' in sales file."
                        )

    def __load_data__(self):
        """
        Loads the data from provided files.
        """
        self.__validate_file_exists__(self.file_path_catalogue)
        try:
            with open(self.file_path_catalogue, 'r', encoding='utf-8') as file:
                self.catalogue_data = json.load(file)
        except json.JSONDecodeError as err_read:
            self.data_errors.append(f"Catalogue file format error: {err_read}")

        self.__validate_file_exists__(self.file_path_sales)
        try:
            with open(self.file_path_sales, 'r', encoding='utf-8') as file:
                self.sales_data = json.load(file)
        except json.JSONDecodeError as err_read:
            self.data_errors.append(f"Sales file format error: {err_read}")

        self.__validate_catalogue_file__()
        self.__validate_sales_file__()

    def get_data(self):
        """
        Returns the loaded data.
        """
        return {
            "catalogue": self.catalogue_data,
            "sales": self.sales_data
            }

    def compute_sales(self):
        """
        Compute the sales by merging catalogue and sales data.
        Output as JSON: Product, Sales.
        """
        # Create a dictionary from the catalogue data for easy lookup
        cat_dict = {
            item['title']: item['price']
            for item in self.catalogue_data
            }

        # Initialize a dictionary to hold the total sales per product
        total_sales_per_product = {}

        # Iterate over sales data, compute total sales per product
        for sale in self.sales_data:
            product = sale['Product']
            quantity = sale['Quantity']
            if product in cat_dict:
                sales = quantity * cat_dict[product]
                if product not in total_sales_per_product:
                    total_sales_per_product[product] = 0
                total_sales_per_product[product] += sales
            else:
                self.data_errors.append(product)

        # Convert total sales per product to the desired JSON format
        self.computed_sales = [
            {"Product": product, "Sales": round(sales, 2)}
            for product, sales in total_sales_per_product.items()
            ]

    def compute_total_sales(self):
        """
        Compute the total sales from the computed sales JSON.
        Returns the total sales value.
        """
        if not self.computed_sales:
            self.compute_sales()

        total_sales = sum(item['Sales'] for item in self.computed_sales)
        return round(total_sales, 2)

    def display_sales_table(self):
        """
        Displays the computed sales in a table format and the grand total.
        """
        if not self.computed_sales:
            self.compute_sales()

        # Table formatted
        print("\n")
        print("-" * 52)
        print(f"{'Product':<30} | {'Total Sales':>18}")
        print("-" * 52)
        for sale in self.computed_sales:
            print(f"{sale['Product']:<30} | {sale['Sales']:>18}")
        for error in self.data_errors:
            print(f"{error:<30} | {'null':>18}")
        print("-" * 52)
        grand_total = self.compute_total_sales()
        print(f"{'Grand Total':<32} {grand_total:>18}")
        print("-" * 52)
        print("\n")

    def display_errors(self):
        """
        Displays any errors encountered during computation.
        """
        if not self.computed_sales:
            self.compute_sales()

        if self.data_errors:
            print("Errors:")
            for error in self.data_errors:
                print(f"- {error} not found")

    def display_grand_total(self):
        """
        Displays only the grand total of all sales.
        """
        if not self.computed_sales:
            self.compute_sales()

        grand_total = self.compute_total_sales()
        print(f"Grand Total: {grand_total}")

    def print_sales(self):
        """
        Prints the sales.
        """
        self.display_sales_table()
        self.display_errors()

    def generate_file(self):
        """
        Writes the sales results and errors to 'SalesResults.csv'.
        Errors are included with 'null' in the Total Sales column.
        """
        if not self.computed_sales:
            self.compute_sales()

        with open('SalesResults.csv', 'w',
                  newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Product', 'Total Sales']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()

            # Write sales data
            for sale in self.computed_sales:
                writer.writerow({
                    'Product': sale['Product'],
                    'Total Sales': sale['Sales']
                    })

            # Write errors with 'null' for Total Sales
            for error in self.data_errors:
                writer.writerow({
                    'Product': error,
                    'Total Sales': 'null'
                    })

            # Wite Grand Total
            writer.writerow({
                'Product': "Grand Total",
                'Total Sales': self.compute_total_sales()
                })


if __name__ == "__main__":

    # Review if program was initiated properly.
    if len(sys.argv) != 3:
        FILE_1 = "priceCatalogue.json"
        FILE_2 = "salesRecord.json"
        MSG = f"Usage: python computeSales.py {FILE_1}  {FILE_2}"
        print(MSG)
        sys.exit(1)

    # Time start
    start_time = time.time()

    # Initiate class
    FILE_PATH_CATALOGUE = sys.argv[1]
    FILE_PATH_SALES = sys.argv[2]
    compute_sales = ComputeSales(FILE_PATH_CATALOGUE, FILE_PATH_SALES)
    compute_sales.generate_file()
    compute_sales.print_sales()

    # Time End
    end_time = time.time()

    # Print elapsed time
    elapsed_time = end_time - start_time
    print(f"Time elapsed: {elapsed_time}")
