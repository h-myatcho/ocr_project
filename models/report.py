class Cell:
    def __init__(self, column_id, text, score):
        self.column_id = column_id
        self.text = text
        self.score = score

    def __repr__(self):
        return f"Cell(column_id={self.column_id}, text={self.text}, score={self.score})"


class Row:
    def __init__(self, row_id, cells):
        self.row_id = row_id
        self.cells = cells

    def __repr__(self):
        return f"Row(row_id={self.row_id}, cells={self.cells})"


class Table:
    def __init__(self):
        self.rows = []

    def add_row(self, row):
        self.rows.append(row)

    def __repr__(self):
        return f"Table(rows={self.rows})"


class Report:
    def __init__(self):
        self.tables = []

    def add_table(self, table):
        self.tables.append(table)

    def __repr__(self):
        return f"Report(tables={self.tables})"


def buildReport(tablesJson):
    # function to build report.

    report = Report()

    # Loop table cells to build tables
    for table_data in tablesJson:

        table = Table()

        # Loop every cell in a table to rebuild rows and columns.
        for cell_data in table_data.get("cells", []):

            # Get row number of a cell and create a new cell first before assigning into its row.
            row_id = cell_data.get("row")
            cell = Cell(
                column_id=cell_data.get("col"),
                text=cell_data.get("text"),
                score=cell_data.get("score")
            )

            # Try to find the existing row with the same row_id.
            existing_row = next((row for row in table.rows if row.row_id == row_id), None)

            # If the row doesn't exist, create a new row and add it to the table.
            if not existing_row:
                new_row = Row(row_id=row_id, cells=[cell])
                table.add_row(new_row)
            else:
                # Add the cell to the existing row
                existing_row.cells.append(cell)
        # Add created table with full of data into report object.
        report.add_table(table)

    return report
