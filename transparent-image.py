#!/usr/bin/env python
"""
A small python script to programatically turn pixels of a given RGB value transparent.
Takes a number of command line options'

Arguments
---------
file -- image file to wish to create a transparent version of
[-rgb | --color] -- 8-byte RGB value you're evaluating in comparision to
[-c | --comparision] -- Comparision operator; lt, gt, eq, or rg
[-z]  -- range to consider if -c == "rg"
[-a] -- 8-byte transparency values for pixels satisfy the cfunc
"""
import argparse
from PIL import Image

def turn_transparent(img, col, cfunc, a):
    """
    Function for turning pixels that satisfy cfunc for col into transparent pixels
    
    img0 -- PIL/pillow image object; needs to have getdata operation for RGB
    col -- a three tuple or list of 8-byte RGB colors
    cfunc -- comparision function; applied to each color in RGB tuple and col
    a -- 8-byte transparency value
    """    

    data = img.getdata()
    newData = []
    for item in data:
        # ensure the image is three channel RGB
        assert isinstance(item, tuple)

        t_color = all( cfunc(item[i], c) for i, c in enumerate(col) )

        if t_color:
            newData.append((item[0], item[1], item[2], a))
        else:
            newData.append((item[0], item[1], item[2], 255))

    new_img = Image.new("RGBA", img.size)
    new_img.putdata(newData)
    return new_img


def get_im_name(im_name):
        "strips the name at file extension and returns everything but the last split"
        no_ext = im_name.strip().split(".")[:-1]
        
        if len(no_ext) == 1:
            return no_ext[0]
        else:
            return ".".join(no_ext)

# dictionary matches flags to comparision functions
comps = {
    "eq": lambda x,y: x == y,
    "lt": lambda x,y: x < y,
    "gt": lambda x,y: x > y,
    "rg": lambda x,y: y + z > x > y - z,
}

if __name__ == "__main__":

    # create a parser object to help make the script more generally usable
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="image file to create a transparent version of")
    parser.add_argument("-rgb", "--color", nargs=3, type=int, default=[ 255, 255, 255 ],
                       help="8-byte RGB colors to use in comparision")
    parser.add_argument("-c", "--comparision", choices=["gt", "lt", "eq", "rg"],
                        default="eq", help="Operator used to compare pixel RGB")
    parser.add_argument("-z", nargs=1, type=int, default=[5], 
                        help="If -c is rg, parameter for size of a range to consider")
    parser.add_argument("-a", nargs=1, type=int, default=[0], help="8-byte transparency")
    args = parser.parse_args()
    
    # assign important variables and fetch comparision function
    image_name = args.file
    col = args.color
    cfunc = comps[args.comparision]
    z = args.z[0]
    a = args.a[0]

    
    # ensures logical RGBA values are given
    assert all( c <= 255 and c >= 0 for c in col )
    assert ( 0 <= a <= 255 )
    
    # ensure that the range is still in RGB values
    if args.comparision == "rg":
        assert all( ((c + z) <= 255) and ((c - z) >= 0) for c in col)
    
    with Image.open(image_name) as im:
        new_im = turn_transparent(im, col, cfunc, a)

    new_im.save("{}_transparent.png".format(get_im_name(image_name)))
    new_im.close()
