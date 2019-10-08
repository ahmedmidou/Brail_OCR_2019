# -*- coding: latin-1 -*-
import os
import pickle

arabic_btx = {
  1:("�",),
  12:("�",),
  16:("�",),
  2345:("�",),
  1456:("�",),
  245:("�",),
  156:("�",),
  1346:("�",),
  145:("�",),
  2346:("�",),
  1235:("�",),
  1356:("�",),
  234:("�",),
  146:("�",),
  12346:("�",),
  1246:("�",),
  23456:("�",),
  123456:("�",),
  12356:("�",),
  126:("�",),
  124:("�",),
  12345:("�",),
  13:("�",),
  123:("�",),
  134:("�",),
  1345:("�",),
  125:("�",),
  2456:("�",),
  135:("�",),
  24:("�",),
  3:("�",),
  34:("�",),
  1256:("�",),
  13456:("�",),
  2:("�",),
  15:("�",),
  136:("�",),
  25:("�",),
  6:("�",),
  3456:('-1',)  # flag for numbers
  }

arabic_num = {
  1:("1",),
  12:("2",),
  14:("3",),
  145:("4",),
  15:("5",),
  124:("6",),
  1245:("7",),
  125:("8",),
  24:("9",),
  245:(":",),
  123456:('60',)  # sign +
  }

french_btx = {
  1:("a",),
  12:("b",),
  14:("c",),
  145:("d",),
  15:("e",),
  124:("f",),
  1245:("g",),
  125:("h",),
  24:("i",),
  245:("j",),
  13:("k",),
  123:("l",),
  134:("m",),
  1345:("n",),
  135:("o",),
  1234:("p",),
  12345:("q",),
  1235:("r",),
  234:("s",),
  2345:("t",),
  136:("u",),
  1236:("v",),
  2456:("w",),
  1346:("x",),
  13456:("y",),
  1356:("z",),
  6:('-1',)  # flag for numbers
  }

french_num = {
  1:("1",),
  12:("2",),
  14:("3",),
  145:("4",),
  15:("5",),
  124:("6",),
  1245:("7",),
  125:("8",),
  24:("9",),
  245:(":",),
  123456:('60',)  # sign +
  }

english_btx = {
  1:("a",),
  12:("b",),
  14:("c",),
  145:("d",),
  15:("e",),
  124:("f",),
  1245:("g",),
  125:("h",),
  24:("i",),
  245:("j",),
  13:("k",),
  123:("l",),
  134:("m",),
  1345:("n",),
  135:("o",),
  1234:("p",),
  12345:("q",),
  1235:("r",),
  234:("s",),
  2345:("t",),
  136:("u",),
  1236:("v",),
  2456:("w",),
  1346:("x",),
  13456:("y",),
  1356:("z",),
  6:('-1',)  # flag for numbers
  }

english_num = {
  1:("1",),
  12:("2",),
  14:("3",),
  145:("4",),
  15:("5",),
  124:("6",),
  1245:("7",),
  125:("8",),
  24:("9",),
  245:(":",),
  123456:('60',)  # sign +
  }

with open('arData', 'wb') as arDataFile:
  my_pickler = pickle.Pickler(arDataFile)
  my_pickler.dump(arabic_btx)

  my_pickler.dump(arabic_num)

with open('frData', 'wb') as frDataFile:
  my_pickler = pickle.Pickler(frDataFile)
  my_pickler.dump(french_btx)

  my_pickler.dump(french_num)

with open('enData', 'wb') as enDataFile:
  my_pickler = pickle.Pickler(enDataFile)
  my_pickler.dump(english_btx)

  my_pickler.dump(english_num)

print('operation succeeded !!')
