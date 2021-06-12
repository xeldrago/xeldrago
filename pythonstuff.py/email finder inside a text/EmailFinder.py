#email
import re
message='contact me at jeffrynspr@gmail.com and my phone number is 9994198795'
emails=re.findall(r'[\w.-]+@[\w\.-]+',message)
print(emails)
#number

ph_nbr_pattern =  r'^(\d{10})(?:\s|$)'
compile_obj = re.compile(ph_nbr_pattern)
phonefile='phonefile.txt'

file2read = open(phonefile, 'r')
for currentline in file2read or message:
    match_obj = compile_obj.search(currentline)
    if match_obj:
        p=currentline.rstrip()
        sp=re.sub("\D", "",p)
        print(sp)

file2read.close()
