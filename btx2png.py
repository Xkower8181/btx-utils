from PIL import Image, ImageDraw
import os, sys, math, itertools, typer
from typing import Optional
from typing_extensions import Annotated

# 11 March 2024, 13 o'clock something minutes.
# Okay I'm gonna refactor this codebase into a .png maker for the .BTX format. Man this thing's a mess. Apologies to whoever might witness this thing (including myself)
# oh god I forgot about python's tab/spaces syntax, hopefully I won't struggle for too long. Anyway the former "wacky and silly" variable names are coming back to byte me but I have figured it out. Helps that I can throw out chunks of the script related to the grouping indexing system.

# 15 October 2024 12 AM
# Gonna now have to add palette indexes to this thing so that I don't run into the issue the PNG to BTX converter confusing palette indexes with identical RGB values.

# 20 October 2024 10 PM
# I'm done implementing CLI and refactoring this behemoth to be "cleaner". Hopefully my efforts will be appreciated.

app = typer.Typer()

def extensionless_filename(filename: str):
	# we find the first period in the reversed version of the filename, substract that from the length of the filename itself and also -1 to get the position of the dot itself
	lastdot = (len(filename) - 1 - (filename[::-1].find('.')))
	return filename[:lastdot]

def process_palette(pal_hex_list: list) -> list:
	color_index = []
	pal_indexes_amount = (int(len(pal_hex_list) / 2))
	
	for i in range(0, pal_indexes_amount):
		twobyte_pal_index = ((pal_hex_list[i * 2 + 1] << 8) + pal_hex_list[i * 2])
		redpart = (twobyte_pal_index & 31) * 8
		greenpart = ((twobyte_pal_index >> 5) & 31) * 8
		bluepart = ((twobyte_pal_index >> 10) & 31) * 8
		# CLUT entry structure is like this: STP (transparency flag which we are going to ignore), 5 bits for blue, 5 bits for green and 5 bits for red, with the LSB being the beginning of red.
		if i == 0:
			temp_color_list = [redpart, greenpart, bluepart, 0]
		else:
			temp_color_list = [redpart, greenpart, bluepart, 255]
		color_index.append(temp_color_list)
		
	output_palette_list = list(itertools.chain.from_iterable(color_index))
	return output_palette_list

def tobtx_post_pal_init(input_filename: str, work_directory: str, btx_byte_list: list, i_pal_list: list, i_x_y: int, is_4bpp: bool, x_or_y: bool, output_filename: str):
	final_list = []
	for i in btx_byte_list:
		if is_4bpp == False:
			# For 8bpp we just put the byte as is
			final_list.append(i)
		else:
			# For 4bpp we split the bytes into their nibbles
			final_list.append(i & 15)
			final_list.append(i >> 4)		

	modulo_list_len = len(final_list) % i_x_y
	all_lines = int((len(final_list) - modulo_list_len) / i_x_y)
	if x_or_y == False:
		final_x = i_x_y
		final_y = all_lines
	else:
		final_x = all_lines
		final_y = i_x_y

	if output_filename == None:
		final_output_filename = os.path.join(work_directory, (extensionless_filename(input_filename) + ".png"))
	else:
		final_output_filename = os.path.join(work_directory, output_filename)
		
	img = Image.new('P', (final_x, final_y))  # setting up our image
	img.putpalette(i_pal_list, rawmode='RGBA')
	d = ImageDraw.Draw(img, mode="P")
	for image_x in range(final_x):
		for image_y in range(final_y):
			cur_symbol = final_list[image_x + final_x * image_y]
			d.point((image_x, image_y), fill=cur_symbol)
	img.save(final_output_filename, transparency=0)
	print(f"File created at: {final_output_filename}")
	return True


@app.command()
def topng(i_btx : Annotated[str, typer.Argument(help="Filename of the input BTX file")], 
i_pal : Annotated[str, typer.Argument(help="Filename of the input CLUT palette file")], 
is_4bpp : Annotated[bool, typer.Argument(help="True for 4bpp / False for 8bpp")], 
i_x_y : Annotated[int, typer.Argument(help="Value that's either width or height, with the other one getting determined automatically")] = 256, 
x_y_determine : Annotated[bool, typer.Argument(help="Use value as False - width / True - height")] = False, 
o_png : Annotated[Optional[str], typer.Argument(help="Filename of output PNG file")] = None):

	cur_dir = os.getcwd()
    # First let's get the palette processing out of the way, that should be
	file_path_pal = os.path.join(cur_dir, i_pal)
	try:
		with open(file_path_pal, 'rb') as existing_pal_file:
			pal_bin = existing_pal_file.read()
	except FileNotFoundError:
		print(f"Palette file at '{file_path_pal}' couldn't be found.")
	except Exception as e:
		print(f"Error: {e}")
	else:
		hexed_pal = pal_bin.hex(' ').split(' ')
		pal_file_byte_list = [int(('0x' + item), 16) for item in hexed_pal]
		existing_pal_file.close()
		pal_list = process_palette(pal_file_byte_list)
		# I must complain about repeating code, but I must get on with my life and just do the quickest option.
		file_path_btx = os.path.join(cur_dir, i_btx)
		try:
			with open(file_path_btx, 'rb') as existing_btx_file:
				btx_bin = existing_btx_file.read()
		except FileNotFoundError:
			print(f"Palette file at '{file_path_btx}' couldn't be found.")
		except Exception as e:
			print(f"Error: {e}")
		else:
			hexed_btx = btx_bin.hex(' ').split(' ')
			btx_file_byte_list = [int(('0x' + item), 16) for item in hexed_btx]
			existing_btx_file.close()
			tobtx_post_pal_init(i_btx, cur_dir, btx_file_byte_list, pal_list, i_x_y, is_4bpp, x_y_determine, o_png)

if __name__ == "__main__":
	app()
