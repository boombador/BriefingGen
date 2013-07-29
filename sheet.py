import xlrd

workbook = xlrd.open_workbook("practices.xlsx")
sheet = workbook.sheet_by_index(0)
print sheet.cell(2, 2)
