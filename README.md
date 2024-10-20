# btx-utils
A pair of command line scripts written in Python to convert Puyo BOX and Waku Puyo Dungeon's decompressed BTX files into PNG and back.



### Dependencies

The scripts use Pillow and Typer for PNG processing and CLI implementation respectively.

`pip install -r requirements.txt`

### Usage - BTX to PNG

`python3 ./btx2png.py -- help`

Displays a help message describing every input parameter.

`python3 ./btx2png.py [i_btx] [i_pal] [is_4bpp] [i_x_y] (Optional) [x_y_determine] (Optional) [o_png] (Optional)`

#### Parameters

- `[i_btx]` - string - File path for the input BTX file (uncompressed only, BTX file are compressed under CNX compression by default, Puyo Tools should be able to handle with that);

- `[i_pal]` - string - File path for the input CLUT palette file (One can easily get one from ripping a VRAM sample using your PS1 emulator of choice and putting it into PsxVram-DotNet);

- `[is_4bpp]` - boolean - Determines whether or not to treat the file as it's 8bpp or 4bpp (False for the former and True for the latter);

- `[i_x_y]` - integer - Value that is either the image's width or height (that gets determined by `[x_y_determine]` parameter), with the remaining one being determined automatically  - Optional (Default value is `256`);

- `[x_y_determine]` - boolean - Determines whether to treat `[i_x_y]` as height or width (False for width and True for height) - Optional (Default value is `False`)

- `[o_png]` - string - File path / File name for the output PNG file (The output PNG is in indexed mode with the palette information acquired from  the file dictated by`[i_pal]`) - Optional (Default behavior would put the output file in the same folder as the input BTX file with the same name but with the extension changed to `.png`).

  <a/>

  ### Usage - PNG to BTX

  `python3 ./png2btx.py -- help`

  Displays a help message describing every input parameter.

  `python3 ./png2btx.py [i] [is_4bpp] [o] (Optional)`

  #### Parameters

  - `[i]` - string - File path for input (indexed) PNG (While it should be able to output a file when inputting a indexed PNG with a palette entries amount that isn't 16 or 256, I wouldn't recommend it);

  - `[is_4bpp]` - boolean - Determines whether or not to treat the file as it's 8bpp or 4bpp (False for the former and True for the latter);

  - `[o]` - string - File path / File name for the output BTX file  - Optional (Default behavior would put the output file in the same folder as the input PNG file with the same name but with the extension changed to `.BTX`).

    <a/>

    ### License

    For license information please see LICENSE.md

    



