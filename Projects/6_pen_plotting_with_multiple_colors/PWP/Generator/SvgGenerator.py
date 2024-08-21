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
from ..Util import geometry as UG
from ..Util.Path import Path

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
            converted_val=round(UB.convert_unit(val,self.unit,"px"),self.precision)
            setattr(self,key,converted_val)

        #extract and process margin
        margins_unit=self.get_value_from_basic_settings("margins")
        self.margins={}
        for key in margins_unit:
            val=margins_unit[key]
            self.margins[key]=round(UB.convert_unit(val,self.unit,"px"),self.precision)

        self.wh_m=[
            self.width-self.margins["l"]-self.margins["r"],
            self.height-self.margins["t"]-self.margins["b"],
        ] #width/height without margin, or content size
    def init_svg(self,additional_tag=""):
        '''
        Initiate a svg using default dimensions.
        Append the svg to self.svg_storage

        Args:
            additional_tag: If a non-empty string name is provided,
            store the value in self.svg_names and use index of the svg as the key.

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
        if additional_tag:
            self.svg_names[str(svg_idx)]=additional_tag

        return svg_soup,svg_idx
    def export_svgs(self):
        '''
        For all svg soups stored in self.svg_storage, export them to the default address.

        Returns:
        '''
        for i,svg_soup in enumerate(self.svg_storage):

            if not svg_soup.find_all("path"):
                # the svg does not contain any <path> element.
                # skip the exporting process.
                continue

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
    def assign_color_to_a_tool(self,tool):
        '''
        Given a tool and its index, generate a random color fill the "stroke" and "fill" value.


        Args:
            tool: a dictionary
            tool_idx: an index of the tool

        Returns: None

        '''
        color=UC.make_random_hex()
        tool["stroke"]=f'#{color}'
        tool["fill"] = "none"

    def init_tools(self):
        '''
        Initiate a collection of tools (for modifying the attributes of svg paths).
        Required values in basic_settings:
        1) tools_ct: how many tools to create
        2) stroke-width
        Optional values:
        1) append_fill_to_path: a boolean value that controls whether to add fills to svg for easy visualization. By default, False.

        Returns:
        '''

        self.tools_ct=self.get_value_from_basic_settings("tools_ct")
        self.stroke_width=round(UB.convert_unit(self.get_value_from_basic_settings("stroke-width"),self.unit),self.precision)
        self.tools=[]

        for tool_idx in range(self.tools_ct):
            tool={
                "stroke-width":self.stroke_width
            }
            self.assign_color_to_a_tool(tool)
            self.tools.append(tool)
    def get_random_tool_idx(self):
        '''

        Generate a random integer that represent the index of a tool.
        Returns:

        '''
        return random.randint(0,self.tools_ct-1)  #randint is inclusive for its upper limit.
    tool_attr_keys_svg=["stroke","stroke-width"]
    def add_path_to_svg(self,svg_idx,path_coordinate,tool_idx,filled):
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
            "d":export_path_to_string(path_coordinate,self.precision),
            "fill":"none"
        }
        # print(path_attrs['d'])
        tool_reference=self.tools[tool_idx]
        for key in self.tool_attr_keys_svg:
            path_attrs[key]=tool_reference[key]

        if filled:
            path_attrs["fill"]=path_attrs["stroke"]

        path_tag=create_tag(
            soup_base=svg_soup,
            parent_tag=svg_soup.g,
            tag_name="path",
            attrs=path_attrs
        )
        return path_tag
    def create(self):
        '''
        A function that create a design (paths, and attributes related to these paths). Needs to be implemented by individual instances.

        Returns: a list of Path instances.
        '''

        raise NotImplementedError

    split_to_tool_svgs=False

    def prepare_svgs(self):
        '''
        Create main svg and tool svgs (if split_to_tool_svgs is true).
        Returns:

        '''
        self.main_svg,self.main_svg_idx=self.init_svg(additional_tag="main")
        if self.split_to_tool_svgs:
            # create a svg for each tool
            for i,tool in enumerate(self.tools):
                svg,svg_idx=self.init_svg(additional_tag=f'tool_{i}_0')
                tool["svg_idx"]=svg_idx


    def process_and_append_paths_to_tool_svgs(self,paths):
        if hasattr(self,"dist_split_paths_by_tool"):
            for tool_i,paths_per_file in enumerate(self.dist_split_paths_by_tool):
                for file_i,path_in_file in enumerate(paths_per_file):
                    if file_i==0:
                        svg_id=self.tools[tool_i]["svg_idx"]
                    else:
                        _,svg_id=self.init_svg(additional_tag=f'tool_{tool_i}_{file_i}')
                    for path_obj in path_in_file:
                        self.add_path_to_svg(
                            svg_idx=svg_id,
                            path_coordinate=path_obj.coordinates,
                            tool_idx=path_obj.tool_idx,
                            filled=False
                        )
        else:
            for path_obj in paths:
                tool_svg_idx = self.tools[path_obj.tool_idx]["svg_idx"]
                self.append_path_obj_to_svg(path_obj,tool_svg_idx)


    def produce_dist_split_paths_by_tool(self,paths):

        paths_by_tools=[[] for i in range(self.tools_ct)]
        self.dist_split_paths_by_tool=[[] for i in range(self.tools_ct)]
        for path_obj in paths:
            paths_by_tools[path_obj.tool_idx].append(path_obj)
        for tool_i,path_stack in enumerate(paths_by_tools):

            paths_for_current_file=[]
            current_dist = 0
            path_stack.reverse()
            # self.dist_split_paths_by_tool[tool_i].append(paths_for_current_file)
            while len(path_stack)>0:
                current_path=path_stack.pop()
                dist_quota = self.max_dist_per_file - current_dist
                break_idx = UG.find_pt_in_path_by_dist(current_path.coordinates, dist_quota)

                if break_idx is None:
                    # not breaking
                    paths_for_current_file.append(current_path)
                    current_dist += UG.calc_path_length(current_path.coordinates)
                    if current_path.filled:
                        for fill_path_obj in current_path.fill_path_objects:
                            path_stack.append(fill_path_obj)
                else:
                    # break_path into 2 parts
                    broken_path_start = Path(
                        coordinates=current_path.coordinates[:break_idx],
                        tool_idx=current_path.tool_idx,
                        filled=False
                    )
                    broken_path_end = Path(
                        coordinates=current_path.coordinates[break_idx:],
                        tool_idx=current_path.tool_idx,
                        filled=False
                    )

                    paths_for_current_file.append(broken_path_start)
                    path_stack.append(broken_path_end)
                    self.dist_split_paths_by_tool[tool_i].append(paths_for_current_file)
                    current_dist = 0
                    paths_for_current_file=[]

            if len(paths_for_current_file)>0 and self.dist_split_paths_by_tool[tool_i][-1]!=paths_for_current_file:
                self.dist_split_paths_by_tool[tool_i].append(paths_for_current_file)









    def append_path_obj_to_svg(self,path_obj,svg_idx):
        '''
        Append a path object go a given svg
        Args:
            path_obj:
            svg_idx:

        Returns:

        '''
        coordinates = path_obj.coordinates

        self.add_path_to_svg(
            svg_idx=svg_idx,
            path_coordinate=coordinates,
            tool_idx=path_obj.tool_idx,
            filled=False
        )
        if path_obj.filled:
            for path in path_obj.fill_path_objects:
                self.add_path_to_svg(
                    svg_idx=svg_idx,
                    path_coordinate=path.coordinates,
                    tool_idx=path_obj.tool_idx,
                    filled=False
                )
    def process_and_append_paths_to_svgs(self,paths):
        '''
        Given a list of path objects, process them and append them as <path> to svgs.
        Args:
            paths: a list of Path object.

        Returns:

        '''
        for path_obj in paths:
            self.append_path_obj_to_svg(path_obj, self.main_svg_idx)
        if self.split_to_tool_svgs:
            self.process_and_append_paths_to_tool_svgs(paths)

    reg_mark_length=10
    def produce_registration_marks(self):
        '''
        For each corner of the page, produce a small cross mark and store it in the registration_marks list
        Returns:
        '''
        self.registration_marks=[]
        cross_center=[
            [-self.reg_mark_length/2,-self.reg_mark_length/2],
            [-self.reg_mark_length/2,self.wh_m[1]+self.reg_mark_length/2],
            [self.wh_m[0]+self.reg_mark_length/2,-self.reg_mark_length/2],
            [self.wh_m[0]+self.reg_mark_length/2, self.wh_m[1] + self.reg_mark_length/2]
        ]
        for center in cross_center:
            self.registration_marks.append(
                Path(
                    coordinates=[
                        [center[0],center[1]-self.reg_mark_length/2],
                        [center[0],center[1]+self.reg_mark_length/2],
                    ], #horizontal line
                    tool_idx=0
                )
            )
            self.registration_marks.append(
                Path(
                    coordinates=[
                        [center[0] - self.reg_mark_length / 2, center[1]],
                        [center[0] + self.reg_mark_length / 2, center[1]],
                    ],  # horizontal line
                    tool_idx=0
                )
            )
    visualize_registration_marks=False


    path_unit_size=5
    split_paths_to_unit_size=False
    hatch_rotation_range=(-2*math.pi,2*math.pi)
    def process_paths(self,paths):
        '''
        Given a list of Path Object, perform the following actions

        1. If the path needs to be broken down, break the path down to have more closely-spaced coordinates.
        2. If the path has fill, generate the hatch line

        Args:
            paths: a list of Path element

        Returns: None. The action modify the Path object
        '''

        for path in paths:
            if self.split_paths_to_unit_size:
                path.split_to_unit_size(self.path_unit_size)
            if path.filled:
                path.produce_line_fills(
                    self.stroke_width,
                    rot_radians=random.uniform(*self.hatch_rotation_range),
                    split_to_unit=self.split_paths_to_unit_size,
                    path_unit_size=self.path_unit_size
                )

        if hasattr(self,"max_dist_per_file"):
            self.produce_dist_split_paths_by_tool(paths)

    def generate(self):
        '''
        The default pipeline for using this generator.
        Require the implementation of the create() function, which returns a list of paths and their required attributes.
        Initiate svgs, process these path information into svg, export the svgs.

        Returns: paths obtained from the create() function
        '''
        paths=self.create()
        self.produce_registration_marks()

        self.process_paths(paths)
        self.prepare_svgs()
        if self.visualize_registration_marks:
            self.process_and_append_paths_to_svgs(self.registration_marks)
        self.process_and_append_paths_to_svgs(paths)
        self.export_svgs()
        return paths


    precision=2
    def __init__(self,settings, **kwargs):

        super().__init__(settings=settings,**kwargs)
        self.extract_dimension_from_settings()
        self.svg_storage=[]
        self.svg_names={}
        self.init_tools()



