# import docx

# # Create a new Word document
# doc = docx.Document()

# # Add a title
# doc.add_heading('My Data Report', level=1)

# # Add some text
# doc.add_paragraph("This is an example report generated using python-docx.")
# doc.add_paragraph("Here's some data:")

# # Add a table
# data = [
#     ["Name", "Age", "Country"],
#     ["Alice", "25", "USA"],
#     ["Bob", "30", "Canada"],
#     ["Charlie", "28", "UK"],
# ]

# table = doc.add_table(rows=1, cols=len(data[0]))
# table.style = 'Table Grid'  # Apply a table style

# # Add data to the table
# for row_data in data:
#     cells = table.add_row().cells
#     for i, cell_text in enumerate(row_data):
#         cells[i].text = cell_text

# # Save the document
# doc.save("data_report.docx")

# print("Document saved as data_report.docx")







