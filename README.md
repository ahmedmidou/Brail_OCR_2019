# Brail_OCR_2019
decode scanned A4 brail code page
i will explain in few words how this work.

first of all we need a paper in A4 format that contains few lines written with brail code.

this code can be hand writed or embossed(an embosser is a printer for brail code)

at this time the app. support only single side paper.

after scanning this page (.tif, .jpg, .png ...) at a resolution of 300dpi,
using a twain scanner (epson perfection, HP Deskjet or any other scanner)

for this progect i note that i used only a simple twain scanner.


the GUI provide a combobox to choose a language for the decode process(English, French or Arabic)

after importing the image (e.g: c:\path\brail.jpg)

the user can easily press the process button to decode the scanned image into readable text (text.txt)

a spell check is available only for English and french only.

i'll quickly explain the main tasks of the decode process:
1- image processing(ImgProcess.py)
this task performs a simple resolution check (300dpi)
and a function to Blur, Erode and Thresh this image to thresh.jpg

2-this task(DotCenters.py) calculates the (x,y) dot centers,
these dots can be concidered as multiple blobs.

3-Cropping the brail dot lines(LineCropper.py).

4-performing the horizontal and vertical align of dots for each line (DotAlign.py),
and store the calculated results : dots and lines in a 'dlData' file.

5-this task is for decoding the brail code using the language selected by user. (TextDecoder.py)

