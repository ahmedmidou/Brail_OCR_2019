# Brail_OCR_2019
decode scanned A4 brail code page
i will explain in few words how this work.
first of all we need a paper in A4 format that contains few lines written with brail code.
this code can be hand writed or embossed(an embosser is a printer for brail code)
at this time the app. support only single side paper.
after scanning this page (.tif, .jpg, .png ...) at a resolution of 300dpi
using a twain scanner (epson perfection, HP Deskjet or any other scanner)
for this progect i note that i used only a simple twain scanner.

the GUI provide a combobox to choose a language for the decode process(English, French or Arabic)
after importing the image (e.g: c:\path\brail.jpg)
the user can easily press the process button to decode the scanned image into readable text (text.txt)
a spell check is available only for English and french only.


