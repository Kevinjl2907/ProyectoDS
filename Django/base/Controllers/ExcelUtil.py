import pyexcel

def importTable(excelFile):
    excel = pyexcel.load_book_from_memory("xlsx",excelFile)
    dictExcel = excel.to_dict()
    return dictExcel[list(dictExcel.keys())[0]]