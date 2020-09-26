NomF="Edit Columns.zip"
rm -r "$NomF"
zip "$NomF" *.py plugin-import-name-edit_columns.txt images/* translations/*.po translations/*.mo

if [ "$ZIP_DEST" != "" ]
then
  cp "$NomF" "$ZIP_DEST"
  rm "$NomF"
fi
