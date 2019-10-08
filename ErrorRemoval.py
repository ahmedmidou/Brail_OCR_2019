# -*- coding: latin-1 -*-
#latin-1
#python ErrorRemoval.py -t 5 -l fr

import argparse
from spellchecker import SpellChecker

def main(lang) :

  content=""
  spell = SpellChecker(language=lang)
  corr=''

  with open ("text.txt","r", encoding='latin-1') as fp:
      content=fp.read()

  lines=content.split('\n')
  for L in lines :
    words=L.split(' ')
      # find those words that may be misspelled
  #  misspelled = spell.unknown(words)
    for word in words :
      # Get the one `most likely` answer
      corr+= spell.correction(word)+' '
      #print("type :",type(corr))
  #    if 'ê' in spell.correction(word) :
  #      print('exist')

    corr+='\n'


  #    if word in L :
  #      L=L.replace(word, spell.correction(word))
  #      corr+=L+'\n'
  #    else :
  #      print(word,' not exist')







  with open("correction.txt","w", encoding='utf8') as f :
  #  for m in corr :
      f.write(corr)



if __name__ == "__main__":

  ap = argparse.ArgumentParser()
  ap.add_argument("-t", "--token", required=True,type=int,
    help="dummy int as token")

  ap.add_argument("-l", "--lang",type=str,default='ar',
    help="language used to decode brail dots")


  args = vars(ap.parse_args())



  lang=args["lang"]
  main(lang)


