version=`grep version __init__.py | grep -v calibre | sed 's/^.*(//
						  s/).*$//
                                                  s/, */\./g'`
echo $version
NomF="Edit Columns_"$version".zip"
zip "versiones/$NomF" *.py plugin-import-name-edit_columns.txt images/* translations/*.po translations/*.mo
git add "versiones/$NomF"
