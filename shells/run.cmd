del "Edit Columns.zip"
"c:\Program Files\7-Zip\7z.exe" a "Edit Columns.zip" *.py plugin-import-name-edit_columns.txt run.cmd images/* translations/*.po translations/*.mo
mode 165,999
calibre-debug -s
calibre-customize -a "Edit Columns.zip"
calibre-debug  -g



