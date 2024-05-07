#!/bin/bash
pyinstaller --onefile --windowed --noconsole sort_pics.py
mv dist/*.app ./
rm -rf build dist
rm ./sort_pics.spec
