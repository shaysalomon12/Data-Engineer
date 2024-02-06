from PyPDF2 import PdfReader
import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import filedialog
import json

################################################
# InputFile = "c:\\aaa\\PDFs\\PURNA_MISHRA.pdf"
# OutputFile = InputFile + '.txt'
################################################

# Open Dialog Window to choose file
# InputFile = askopenfilename()
filetypes = (
    ('PDF files', '*.pdf'),
    ('All files', '*.*'),
)

# Open-file dialog
InputFile = tk.filedialog.askopenfilename(
    title='Select a PDF file',
    filetypes=filetypes,
)

# Set output file
OutputFile = InputFile + '.json'

# Read file using pdfReader 
reader = PdfReader(InputFile)

# Open text file to wtite converted PDF
f = open(OutputFile, 'w', encoding="utf-8")

# Get num of pages
numOfPages = len(reader.pages)

# Loop over pages
for i in range(numOfPages):
    page = reader.pages[i]
    extracted_text = page.extract_text()
    
    # print(extracted_text)
    f.write(extracted_text)

f.close()

print ("****************************************************************************")
print ("PDF file " + InputFile + " Converted to Text as " + OutputFile)
print ("****************************************************************************")

