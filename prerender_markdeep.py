#!/usr/bin/env python3
"""
This scripts copies filed from one folder ("src") to another ("docs").
All html files are processed so that:

	* Any equations written using Markdeep syntax gets prerendered as SVG.
	* All "<!-- insert SOME_FILE here -->" are replaced with the content of SOME_FILE (non-recursively).
"""
from multiprocessing.dummy import Pool
from pathlib import Path
import re
import shutil
import urllib
import urllib.request


def fetch_svg(equation: str):
	# Alternative: https://github.com/kgryte/tex-equation-to-svg
	# npm install g tex-equation-to-svg
	try:
		quoted_equation = urllib.parse.quote(equation, safe='')
		svg_url = "https://latex.codecogs.com/svg.latex?{" + quoted_equation + "}"
		svg = urllib.request.urlopen(svg_url).read().decode('utf-8')
		svg = svg[svg.index("<svg"):] # Ignore preamble (<xml-tag, comments, etc)
		return svg
	except Exception as e:
		print("FAILED to convert equation:\n\n" + equation + "\n\n" + str(e))
		return equation


pool = Pool(32)
future_from_eq = {}


def fetch_svg_async(equation: str, initial_pass: bool):
	if initial_pass:
		if equation not in future_from_eq:
			future_from_eq[equation] = pool.apply_async(fetch_svg, [equation])
		return "[WAIT FOR IT]"
	else:
		# Block waiting from svg:
		assert equation in future_from_eq
		return future_from_eq[equation].get()


def render_math(text: str, initial_pass: bool) -> str:
	def replace_multiline(match):
		svgs = fetch_svg_async(match.group(1), initial_pass)
		return "<center>{}</center>".format(svgs)

	def replace_inline(match):
		return fetch_svg_async(match.group(1), initial_pass)

	text = re.sub(r"\\begin\{equation\}\n(.*?)\n[ \t+]*\\end\{equation\}", replace_multiline, text, flags=re.MULTILINE|re.DOTALL)
	text = re.sub(r"\$([^$]+)\$", replace_inline, text)
	return text


def convert_file(in_filepath: Path, out_filepath: Path, initial_pass: bool):
	if not str(in_filepath).endswith(".html"):
		out_filepath.parent.mkdir(parents=True, exist_ok=True)
		shutil.copyfile(in_filepath, out_filepath)
		print("COPIED {} => {}".format(in_filepath, out_filepath))
		return

	with open(str(in_filepath), 'r') as f:
		text = f.read()

	def replace_insertion(match):
		insert_filename = match.group(1)
		insert_filepath = in_filepath.parent / insert_filename
		with open(str(insert_filepath), 'r') as f:
			return f.read()

	# Apply (insert header.html here) thingy everywhere:
	# text = re.sub(r"\(insert (.*) here\)", replace_insertion, text)

	# Apply <!-- insert header.html here --> everywhere:
	text = re.sub(r"<!-- insert (.*) here -->", replace_insertion, text)

	text = render_math(text, initial_pass)
	text = "<!-- PRERENDERED DOCUMENT - DO NOT EDIT!!!! -->\n" + text

	if initial_pass:
		print("STARTED {} => {}".format(in_filepath, out_filepath))
	else:
		out_filepath.parent.mkdir(parents=True, exist_ok=True)

		with open(str(out_filepath), 'w') as f:
			f.write(text)

		print("ENDED {} => {}".format(in_filepath, out_filepath))


def convert_all(in_root: Path, out_root: Path, initial_pass: bool):
	for in_filepath in in_root.glob('**/*'):
		if in_filepath.is_file():
			out_filepath = out_root / in_filepath.relative_to(in_root)
			convert_file(in_filepath, out_filepath, initial_pass=initial_pass)


def main():
	IN_ROOT=Path("src")
	OUT_ROOT=Path("docs")
	shutil.rmtree(OUT_ROOT, ignore_errors=True)
	convert_all(IN_ROOT, OUT_ROOT, initial_pass=True)
	convert_all(IN_ROOT, OUT_ROOT, initial_pass=False)
	print("{} equations converted to svg".format(len(future_from_eq)))


if __name__ == "__main__":
	main()
