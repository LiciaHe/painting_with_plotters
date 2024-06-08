'''
An extension of SettingAndStorageGenerator that handles the generation, manipulation, and storage of svg files.

Process paths to svg files.
Handles tool(svg attribute)

'''



import re
from bs4 import BeautifulSoup
import random,math
from ..Util import basic as UB
from ..Util import color as UC

from ..Generator.SettingAndStorageGenerator import SettingAndStorageGenerator

def apply_attrs_to_soup(soup,attrs):
    '''
    Given a soup (xml structure) and a dictionary, attach all the values in the attrs to the soup.
    Args:
        soup: beautiful soup object
        attrs: a dictionary

    Returns: None

    '''
    for key in attrs:
        soup.attrs[key]=attrs[key]
def init_empty_svg_soup():
    '''
    Generate a soup for an empty SVG.
    Returns:
    '''
    svg_starter = '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/2000/xlink"></svg>'
    svg_soup = BeautifulSoup(svg_starter, "html.parser")
    return svg_soup

def convert_to_export_ready_svg(base_soup):
    '''
    Convert the beautiful soup export to fit the format of svg by removing the closing tag (e.g., </path>)
    Args:
        base_soup: a beautiful soup base

    Returns: an export-ready svg string.

    '''
    node_to_modify = ["path", "rect", "circle", "line", "polygon"]
    svg_str = base_soup.prettify()
    for node_name in node_to_modify:
        if node_name in svg_str:
            svg_str = "".join(svg_str.split("</" + node_name + ">"))
            pathBackRef = re.compile("(<" + node_name + ".*?)(>)")
            svg_str = pathBackRef.sub(r'\1/>', svg_str)

    return svg_str
def create_tag(soup_base,parent_tag,tag_name,attrs):
    '''
    Create a new tag in soup_base using the given tag_name and attrs.
    Append the new tag to node_to_append

    Args:
        soup_base: the root soup
        parent_tag: where the new tag will be inserted into
        tag_name: name of the new tag. e.g., g, path, rect
        attrs: a dictionary of attributes to attach to the svg

    Returns:the new tag.
    '''
    tag = soup_base.new_tag(tag_name)
    apply_attrs_to_soup(tag,attrs)
    parent_tag.append(tag)
    return tag
def export_path_to_string(path,round_precision=2):
    '''
    Convert a path into a d path string (used for <path> element in svg).
    Args:
        path: [[x,y],[x1,y1]....] for a non-nested path
                If a path is nested, it is [[[x,y],[x1,y1]....],[[xn,yn]...]]
        round_precision: the precision setting for the exported value. By default, round to the 2nd place.

    Returns: A string in the format required for "d" attribute of the <path> element in SVG.
    '''

    d_str = "M" + " L".join([",".join([str(round(l, round_precision)) for l in xy[:2]]) for xy in path])
    return d_str
class SvgGenerator(SettingAndStorageGenerator):
    def extract_dimension_from_settings(self):
        '''
        Assuming all dimensions required for the generation of SVG are stored in self.basic_settings.
        Extract them, convert into pixels, and store the converted value.

        Required values in the basic settings:
        - unit
        - width
        - height

        Returns: None
        '''
        self.unit=self.get_value_from_basic_settings("unit")

        #extract and process width and height
        for key in ["width","height"]:
            val=self.get_value_from_basic_settings(key)
            converted_val=round(UB.unitConvert(val,self.unit,"px"),self.precision)
            setattr(self,key,converted_val)

        #extract and process margin
        margins_unit=self.get_value_from_basic_settings("margins")
        self.margins={}
        for key in margins_unit:
            val=margins_unit[key]
            self.margins[key]=round(UB.unitConvert(val,self.unit,"px"),self.precision)

        self.wh_m=[
            self.width-self.margins["l"]-self.margins["r"],
            self.height-self.margins["t"]-self.margins["b"],
        ] #width/height without margin, or content size
    def init_svg(self,additional_name=""):
        '''
        Initiate a svg using default dimensions.
        Append the svg to self.svg_storage

        Args:
            additional_name: If a non-empty string name is provided, store the value in self.svg_names and use index of the svg as the key.

        Returns: the svg soup, and the index of the svg (in self.svg_storage)
        '''
        svg_soup=init_empty_svg_soup()
        svg_attrs = {
            "width": f'{self.width}px',
            "height": f'{self.height}px',
            "viewBox": f'0 0 {self.width} {self.height}'
        }
        apply_attrs_to_soup(svg_soup.svg,svg_attrs)

        content_g=create_tag(
            svg_soup,
            svg_soup.svg,
            tag_name="g",
            attrs={
                "transform":f'translate({self.margins["l"]},{self.margins["r"]})'
            }
        )
        self.svg_storage.append(svg_soup)
        svg_idx=len(self.svg_storage)-1
        if additional_name:
            self.svg_names[str(svg_idx)]=additional_name

        return svg_soup,svg_idx
    def export_svgs(self):
        '''
        For all svg soups stored in self.svg_storage, export them to the default address.

        Returns:
        '''
        for i,svg_soup in enumerate(self.svg_storage):
            additional_tag=""
            if str(i) in self.svg_names:
                additional_tag=self.svg_names[str(i)]
            save_loc=self.get_full_save_loc(
                file_extension="svg",
                additional_tag=additional_tag
            )
            with open(save_loc, 'w') as saveFile:
                saveFile.write(convert_to_export_ready_svg(svg_soup))
        return

    def add_path_to_svg(self,svg_idx,path,tool_idx):
        '''
        Add a path (list of 2d points)
        Args:
            svg_idx: the index of the svg soup
            path: a list of 2d points
            tool_idx: index of the svg attribute to extract.

        Returns: the path tag (soup)

        '''
        svg_soup=self.svg_storage[svg_idx]

        path_attrs={
            "d":export_path_to_string(path,self.precision),
            "stroke":"black",
            "stroke-width":1,
        }
        create_tag(
            soup_base=svg_soup,
            parent_tag=svg_soup.g,
            tag_name="path",
            attrs=path_attrs
        )



    precision=2
    def __init__(self,settings, **kwargs):
        super().__init__(settings=settings,**kwargs)
        self.extract_dimension_from_settings()
        self.svg_storage=[]
        self.svg_names={}



