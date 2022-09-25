pyinstaller gui.py -i logo.ico -w -n webJPG -y
cp convert.exe dist/webJPG
cp -r assets dist/webJPG
cp logo.ico dist/webJPG