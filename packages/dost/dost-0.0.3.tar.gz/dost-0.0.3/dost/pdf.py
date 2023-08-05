"""
PDF module for dost. This module is used to extract data from PDF files.

Examples:
    >>> pdf.extract_all_tables(pdf_file_path="C:\\Users\\user\\Desktop\\demo.pdf",output_folder="C:\\Users\\user\\Desktop\\",output_filename = "demo")


The module contains the following functions:

- `extract_all_tables(pdf_file_path, output_folder, output_filename, table_with_borders)`: Extracts all tables from a pdf file and saves them as csv files in the specified folder.

"""


import os
from pathlib import WindowsPath
from typing import Union
from dost.helpers import dostify

output_folder_path = os.path.join(
    os.path.abspath(r'C:\Users\Public\PyBOTs LLC'), 'DOST', 'PDF Folder')

# create output folder if not present
if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)


@dostify(errors=[(FileNotFoundError, "")])
def extract_all_tables(pdf_file_path: Union[str, WindowsPath], output_folder: Union[str, WindowsPath], output_filename: str, table_with_borders: bool = True) -> None:
    """Extracts all tables from a pdf file and saves them as csv files in the specified folder.

    Args:
        pdf_file_path (str,WindowsPath): Path to the pdf file.
        output_folder (str,WindowsPath): Path to the output folder.
        output_filename (str): Name of the output file.
        table_with_borders (bool, optional): Whether the table has borders. Defaults to True.

    Examples:
        >>> pdf.extract_all_tables(pdf_file_path="C:\\Users\\user\\Desktop\\demo.pdf",output_folder="C:\\Users\\user\\Desktop\\",output_filename = "demo")

    """
    # Import Section
    import pdfplumber
    import pandas as pd
    import datetime

    # Code Section
    if not pdf_file_path:
        raise Exception("PDF file path cannot be empty")
    if (isinstance(pdf_file_path)):
        raise FileNotFoundError(f"File not found: {pdf_file_path}")
    if not output_folder:
        output_folder = output_folder_path
    if not output_filename:
        output_filename = "pdf_" + \
            str(datetime.datetime.now().strftime("%Y%m%d_%H%M%S")) + ".xlsx"
    else:
        if not output_filename.endswith(".xlsx"):
            output_filename += ".xlsx"

    pdf = pdfplumber.open(pdf_file_path)

    tables = []

    if table_with_borders:
        for each_page in pdf.pages:
            tables.append(each_page.extract_tables())
    else:
        table_settings = {
            "vertical_strategy": "text",
            "horizontal_strategy": "text"
        }
        for each_page in pdf.pages:
            tables.append(each_page.extract_tables(table_settings))

    # excel writer
    writer = pd.ExcelWriter(os.path.join(
        output_folder, output_filename), engine='openpyxl')

    for table in tables:
        df_main = []
        # list of the rows to dataframe
        for i in range(len(table)):
            df = pd.DataFrame(table[i])
            df_main.append(df)

        df_main = pd.concat(df_main)
        table_index = str(tables.index(table) + 1)

        df_main.to_excel(writer, sheet_name=table_index,
                         index=False, header=False)

    writer.save()

# write a function to extract desired table from desired page of pdf
