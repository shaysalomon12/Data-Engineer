import tabula
import pandas as pd 
import numpy as np

################################################
InputFile = "c:\\aaa\\PDFs\\Ofir_Rozat.pdf"
OutputFile = InputFile + '.csv'
################################################


dfs = tabula.read_pdf(InputFile, pages='all')
print(dfs)


# convert PDF into CSV file
# tabula.convert_into(InputFile, OutputFile, output_format="csv", pages='all')


