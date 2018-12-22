# Medium-to-Hugo

Convert a medium export into a format suitable for running a blog with Hugo. This is old, poorly written code. I used it once and put it up on the Internet as a starting point for others. Good luck.

## Install

`pip install -r requirements.txt`

## Run

Modify `config.py` to set the import and output dirs.

Run parser via `python3 parse.py`.


TODO:
- Create test files
- Create setup files
- Make parallel
- PNGs should have a white background
- The bulleted lists being produced by pandoc are oddly spaced
- Subheadings are also weirdly parse by pandoc
- Section seperations mess up the image downloading
