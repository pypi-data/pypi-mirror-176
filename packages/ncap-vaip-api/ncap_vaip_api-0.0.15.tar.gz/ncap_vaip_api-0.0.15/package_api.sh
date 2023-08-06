[ -d "dist" ] && rm -r dist
python3 -m build
cp -r ncapvaip/data dist/ncap/data
python3 -m twine upload dist/*