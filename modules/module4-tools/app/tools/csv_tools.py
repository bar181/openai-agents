"""
CSV Tools Module

Provides functions to parse CSV strings into lists of dictionaries and generate CSV strings from data.
"""

import csv
import io

class ParseCsvTool:
    @staticmethod
    def function(*, csv_str: str) -> list:
        reader = csv.DictReader(io.StringIO(csv_str))
        return list(reader)

class GenerateCsvTool:
    @staticmethod
    def function(*, data: list) -> str:
        if not data:
            return ""
        output = io.StringIO()
        fieldnames = data[0].keys()
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)
        return output.getvalue()

# Expose tool instances.
parse_csv = ParseCsvTool()
generate_csv = GenerateCsvTool()
