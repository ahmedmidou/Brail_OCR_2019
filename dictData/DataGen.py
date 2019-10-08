import os


arBrailleCode1=[
  1,
  12,
  16,
  2345,
  1456,
  245,
  156,
  1346,
  145,
  2346,
  1235,
  1356,
  234,
  146,
  12346,
  1246,
  23456,
  123456,
  12356,
  126]

arBrailleCode2= [
  124,
  12345,
  13,
  123,
  134,
  1345,
  125,
  2456,
  135,
  24]


arNum= [
  1,
  12,
  14,
  145,
    15,
  124,
  1245,
  125,
  24,
  245]



frBrailleCode1=[
  1,
  12,
  14,
  145,
  15,
  124,
  1245,
  125,
  24,
  245,
  13,
  123,
  134,
  1345,
  135,
  1234,
  12345,
  1235,
  234,
  2345,
  136,
  1236,
  2456,
  1346,
  13456,
  1356]



frNum= [
  1,
  12,
  14,
  145,
    15,
  124,
  1245,
  125,
  24,
  245]







enBrailleCode1=[
  1,
  12,
  14,
  145,
  15,
  124,
  1245,
  125,
  24,
  245,
  13,
  123,
  134,
  1345,
  135,
  1234,
  12345,
  1235,
  234,
  2345,
  136,
  1236,
  2456,
  1346,
  13456,
  1356]



enNum= [
  1,
  12,
  14,
  145,
    15,
  124,
  1245,
  125,
  24,
  245]






with open('DataDump.py','w') as data_file :
  steps1=len(arBrailleCode1)
  steps2=len(arBrailleCode2)
  steps3=len(arNum)

  data_file.write("# -*- coding: latin-1 -*-\n")
  data_file.write("import os\n")
  data_file.write("import pickle\n\n")
  data_file.write("arabic_btx = {\n")
  for i in range(steps1) :
    data_file.write('  '+str(arBrailleCode1[i])+':("'+chr(1575+i)+'",),\n')
  for i in range(steps2) :
    data_file.write('  '+str(arBrailleCode2[i])+':("'+chr(1601+i)+'",),\n')
#  for i in range(steps3) :
#    data_file.write('  '+str(arNum[i])+':('+str(49+i)+'),\n')


  data_file.write("  3456:('-1',)  # flag for numbers\n")
  data_file.write("  }\n\n")




  data_file.write("arabic_num = {\n")
  for i in range(steps3) :
    data_file.write('  '+str(arNum[i])+':("'+chr(49+i)+'",),\n')
  data_file.write("  123456:('60',)  # sign +\n")
  data_file.write("  }\n\n")




  steps1=len(frBrailleCode1)
  steps2=len(frNum)
  data_file.write("french_btx = {\n")
  for i in range(steps1) :
    data_file.write('  '+str(frBrailleCode1[i])+':("'+chr(97+i)+'",),\n')
#  for i in range(steps2) :
#    data_file.write('  '+str(frNum[i])+':('+str(49+i)+'),\n')


  data_file.write("  6:('-1',)  # flag for numbers\n")
  data_file.write("  }\n\n")


  data_file.write("french_num = {\n")
  for i in range(steps2) :
    data_file.write('  '+str(frNum[i])+':("'+chr(49+i)+'",),\n')
  data_file.write("  123456:('60',)  # sign +\n")
  data_file.write("  }\n\n")














##############################################################

  steps1=len(enBrailleCode1)
  steps2=len(enNum)
  data_file.write("english_btx = {\n")
  for i in range(steps1) :
    data_file.write('  '+str(enBrailleCode1[i])+':("'+chr(97+i)+'",),\n')
#  for i in range(steps2) :
#    data_file.write('  '+str(frNum[i])+':('+str(49+i)+'),\n')


  data_file.write("  6:('-1',)  # flag for numbers\n")
  data_file.write("  }\n\n")


  data_file.write("english_num = {\n")
  for i in range(steps2) :
    data_file.write('  '+str(enNum[i])+':("'+chr(49+i)+'",),\n')
  data_file.write("  123456:('60',)  # sign +\n")
  data_file.write("  }\n\n")






  data_file.write("with open('arData', 'wb') as arDataFile:\n")
  data_file.write("  my_pickler = pickle.Pickler(arDataFile)\n")
  data_file.write("  my_pickler.dump(arabic_btx)\n\n")
  data_file.write("  my_pickler.dump(arabic_num)\n\n")






  data_file.write("with open('frData', 'wb') as frDataFile:\n")
  data_file.write("  my_pickler = pickle.Pickler(frDataFile)\n")
  data_file.write("  my_pickler.dump(french_btx)\n\n")
  data_file.write("  my_pickler.dump(french_num)\n\n")




  data_file.write("with open('enData', 'wb') as enDataFile:\n")
  data_file.write("  my_pickler = pickle.Pickler(enDataFile)\n")
  data_file.write("  my_pickler.dump(english_btx)\n\n")
  data_file.write("  my_pickler.dump(english_num)\n\n")



  data_file.write("print('operation succeeded !!')\n")
  #data_file.write("os.system('pause')\n")

#log="\n".join(os.popen("python DataDump.py"))
#print(log)





os.system("pause")
