# webJPG

Eine einfache graphische Benutzeroberfläche für die Konvertierung von beliebig vielen Bildern in ein webkomatibles Format.

<p align="center">
<img src="https://user-images.githubusercontent.com/55287601/194712436-196af66c-c13f-4773-b6dc-c6564645adb6.png"/>
</p>
Die Anwendung ist in Python geschrieben und wird mit dem [pyinstaller](https://pyinstaller.org/en/stable/) in ein ausführbares Programm umgewandelt (im Moment nur für Windows 32bit) und mit [NSIS](https://nsis.sourceforge.io/Main_Page) in ein Setup gepackt.
Das Programm ist nur eine Schnittstelle für das tolle [ImageMagick convert](https://imagemagick.org/script/convert.php) CLI tool.
Unter der Haube wird für jedes ausgewähltes Bild folgender Befehl ausgeführt:

```
convert img.jpg -strip -interlace Plane -gaussian-blur 0.05 -quality 85% -sampling-factor 4:2:0 -adaptive-resize 448 -colorspace sRGB out.jpg
```
Abhängig vom Bildinhalt ist das resultierende Bild etwa zwischen 10KB und 50KB groß.

## Installation

Folgende Datei herunterladen:
https://github.com/lukas-blecher/webJPG/releases/download/0.4/webJPG-setup.exe
