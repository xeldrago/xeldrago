import os
from PyPDF2 import PdfMerger
entries = os.listdir(
    '\\\\DESKTOP-A89N0HD\\Users\\Public\\Documents\\jeff\\merging in pair\\')
onlyPDF = []
for i in entries:
    if i.endswith('.pdf'):
        onlyPDF.append(i)
# print(onlyPDF[0])
# first lets make lists of two sets


onlyPDF_even = []

for i in range(0, len(onlyPDF), 2):
    onlyPDF_even.append(onlyPDF[i])
# print(onlyPDF_even)
onlyPDF_odd = []
for i in range(1, len(onlyPDF), 2):
    onlyPDF_odd.append(onlyPDF[i])
# print(onlyPDF_odd)

onlyPDF_zip = list(zip(onlyPDF_even, onlyPDF_odd))
print(onlyPDF_zip)


for pds in onlyPDF_zip:
    print(pds)
    pdsf = list(pds)

    merger = PdfMerger()
    for poof in pdsf:
        merger.append(poof)
        G = pdsf[0].replace('.pdf', "")
    merger.write(G+"A.pdf")


merger.close()
