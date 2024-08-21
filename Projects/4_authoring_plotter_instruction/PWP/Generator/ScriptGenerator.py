'''
An extension of SvgGenerator that handles the generation and storage of script files used to control axidraws.

Each project needs to implement the "create()" function.
The "generate()" function processes the information, create svg files for visualization and python script for
'''

from ..Generator.SvgGenerator import SvgGenerator
import json
import importlib.resources
from ..Util import basic as UB

class ScriptWriter:
    '''
    A class that handles script writer (a io.TextWrapper) object.
    Stores information such as
    - processed_paths
    - options
    - other attributes
    '''
    def update_options(self,options):
        '''
        Update the axidraw configs
        Args:
            options: a dictionary that will overwrite the default pyaxidraw options.

        Returns:

        '''
        self.options.update(options)
    def __init__(self,writer_addr):
        self.writer_addr=writer_addr
        self.writer=open(writer_addr,"w")
        self.options={
            "model": 2,  # 1 for SE/A4, 2 for SE/A3, 5 for SE/A1
            # "penlift": 3,# If the plotter has the brushless servo upgrade, use 3. Otherwise, omit this or use default value 1.
            "pen_pos_up": 80,  # Pen height when the pen is up (Z axis). 0-100.
            "pen_pos_down": 0,  # Pen height when the pen is down (Z axis). 0-100.
            "pen_rate_lower": 75,  # Rate for z-axis movement (0-100)
            "pen_rate_raise": 75,  # Rate for z-axis movement (0-100)
            "accel": 90,  # accelerate rate(1-100)
            "unit": 0,  # 0 for inch, 1 for cm, 2 for mm. Default 0
            "speed_pendown": 80,  # Maximum XY speed when the pen is down (0-100)
            "speed_penup": 80  # Maximum XY speed when the pen is up (0-100)
        }
        self.paths=[]# used to store paths included in this writer.
        self.registration_marks=[] #stores paths that make registration marks.
    def process_and_append_path(self,path_obj,margins,storage=None):
        '''
        Given a path object, generate the unit converted path, store the path in self.paths
        Args:
            path_obj:

        Returns:

        '''
        if storage is None:
            storage=self.paths
        storage.append(path_obj)
        unit_to=["inch","cm","mm"][self.options["unit"]]
        path_obj.create_margined_unit_path(unit_to,margins)

    def produce_options_str(self):
        '''
        Convert the options into a string to be written to the final script.

        Returns: a string that contains information stored in the options.

        '''
        option_strs=f'options = {json.dumps(self.options)}'
        return option_strs

    precision=4

    def produce_paths_str(self,):
        '''
        Convert the coordinate information stored in individual path objects into a string.

        Returns: a string that contains all the path information.

        '''

        path_str='paths=['
        for i,path_obj in enumerate(self.paths):
            rounded_list = [[round(val, self.precision) for val in pt] for pt in path_obj.unit_path]
            path_str+=str(rounded_list)
            if i!=len(self.paths)-1:
                path_str+=","

        path_str+="]"

        path_str = path_str.replace("'", "")
        return path_str
    def produce_registration_str(self):
        '''
        Treat all Paths stored in self.registration_paths and store into the variable registration_marks
        Returns:

        '''
        path_str='registration_marks=['
        for i,path_obj in enumerate(self.registration_marks):
            rounded_list = [[round(val, self.precision) for val in pt] for pt in path_obj.unit_path]
            path_str+=str(rounded_list)
            if i!=len(self.registration_marks)-1:
                path_str+=","

        path_str+="]"

        path_str = path_str.replace("'", "")
        return path_str


    def export(self):
        '''

        Assemble path and option information into a script.
        Close the writer.

        Information:
        - paths: a list of paths, formatted into string
        - options:

        Returns:

        '''
        if len(self.paths)<1:
            # This writer does not have any content to write
            self.writer.close()
            # try to remove the empty python file.
            UB.rmfile(self.writer_addr)
            return

        with importlib.resources.open_text('PWP.static', "axidraw_template.py") as file:
        # with open("../static/axidraw_template.py","r") as tf:
            template_content=file.read()

        content_to_write=[
            self.produce_options_str(),
            self.produce_registration_str(),
            self.produce_paths_str(),
            template_content
        ]

        for content in content_to_write:
            self.writer.write("\n")
            self.writer.write(content)
            self.writer.write("\n")

        self.writer.close()

class ScriptGenerator(SvgGenerator):

    def init_script_writer(self,additional_tag=""):
        '''
        Initiate an empty writer (an io.TextIoWrapper) object.

        Args:
            additional_tag: If a non-empty string name is provided,
            store the value in self.script_names and use index of the writer as the key.

        Returns:

        '''
        writer_addr=self.get_full_save_loc(file_extension="py",additional_tag=additional_tag)
        writer=ScriptWriter(writer_addr)
        self.script_writers.append(writer)
        writer_idx=len(self.script_writers)-1

        if self.get_value_from_basic_settings("script_options"):
            writer.update_options(self.get_value_from_basic_settings("script_options"))

        for reg_path in self.registration_marks:
            writer.process_and_append_path(reg_path,self.margins,writer.registration_marks)

        return writer_idx

    split_to_tool_pys=False
    def prepare_script_writers(self):
        '''
        Initiate writers for python script.

        Create a main script writer,
        and one for each tool if self.split_to_tool_pys is True.

        Returns:

        '''
        self.script_writers=[]
        # self.script_names={}
        # initiate main
        self.main_script_idx=self.init_script_writer(additional_tag="main")
        if self.split_to_tool_pys:
            for i,tool in enumerate(self.tools):
                script_idx=self.init_script_writer(additional_tag=f'tool_{i}')
                tool["script_idx"] = script_idx


    def process_and_append_paths_to_script(self,paths):
        '''
        Given a list of path objects, process them and append them to the script writer.
        Args:
            paths: a list of Path object.

        Returns:

        '''
        main_writer=self.script_writers[self.main_script_idx]

        for path_obj in paths:
            main_writer.process_and_append_path(path_obj,self.margins)
            if self.split_to_tool_pys:
                tool=self.tools[path_obj.tool_idx]
                tool_writer=self.script_writers[tool["script_idx"]]
                tool_writer.process_and_append_path(path_obj,self.margins)

    def export_scripts(self):
        for script_writer in self.script_writers:
            script_writer.export()
    def generate(self):
        '''
        The default pipeline for using this generator.

        Require the implementation of the create() function, which returns a list of paths and their required attributes.

        The pipeline:
        0) call the create() function to obtain a list of paths

        ### covered by SvgGenerator
        1) Initiate svgs
        2) process these path information into svg
        3) export the svgs.

        4) Initiate script writers (from template)
        5) process these path information into script writers
        6) export the scripts.

        Returns:

        '''
        paths=super().generate()
        self.prepare_script_writers()
        self.process_and_append_paths_to_script(paths)
        self.export_scripts()