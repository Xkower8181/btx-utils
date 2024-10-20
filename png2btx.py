from PIL import Image, ImageDraw
from typing import Optional
from typing_extensions import Annotated
import os, sys, typer

# y'know what they say "reuse, reduce, recycle". - xkower
# hopefully this a lot more eligable, at least I think? - xkower, 18th october 2024

app = typer.Typer()

def extensionless_filename(filename: str):
	lastdot = (len(filename) - 1 - (filename[::-1].find('.')))
	return filename[:lastdot]

def topng_post_filecheck(input_filename: str, output_filename: str, work_directory: str, is_4bpp: bool, im: Image):
	pix = im.load()
	width, height = im.size
	output_byte_list = []

	if is_4bpp == True:
		for cur_h in range(0, height, 1):
			for cur_w in range(0, width, 2):
				# this one has the beginning "0x" cut out using the [2] at the end just so I can easily concatenate the nibbles into a proper hex string, which in turn gives us our final output byte for the nibble pair
				lower_nibble = hex(pix[cur_w, cur_h])[2]
				higher_nibble = hex(pix[cur_w + 1, cur_h])
				output_byte_list.append(int(higher_nibble + lower_nibble, 16))
	else:
		for cur_h in range(0, height, 1):
			for cur_w in range(0, width, 1):
				cur_byte = pix[cur_w, cur_h]
				output_byte_list.append(cur_byte)

	if output_filename == None:
		final_output_filename = os.path.join(work_directory, (extensionless_filename(input_filename) + ".BTX"))
	else:
		final_output_filename = os.path.join(work_directory, output_filename)
	with open(final_output_filename, 'wb') as file:
		for l in output_byte_list:
			file.write(bytes((l,)))
		file.close
	print(f"File created at: {final_output_filename}")
	return True

@app.command()
def tobtx(i : Annotated[str, typer.Argument(help="Filename of the input PNG file")], 
is_4bpp : Annotated[bool, typer.Argument(help="True for 4bpp / False for 8bpp")], 
o : Annotated[Optional[str], typer.Argument(help="Filename of output BTX file")] = None):
	cur_dir = os.getcwd()
	file_path = os.path.join(cur_dir, i)
	try:
		work_image = Image.open(file_path)
	except FileNotFoundError:
		print(f"Looks like there's no file at \n{file_path}")
	except:
		print("Looks like something else went wrong")
	else:
		topng_post_filecheck(i, o,  cur_dir, is_4bpp, work_image)
 
 
if __name__ == "__main__":
	app()
