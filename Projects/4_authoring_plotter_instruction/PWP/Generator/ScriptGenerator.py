'''
An extension of SvgGenerator that handles the generation and storage of script files used to control axidraws.

Each project needs to implement the "create()" function.
The "generate()" function processes the information, create svg files for visualization and python script for
'''

from ..Generator.SvgGenerator import SvgGenerator

class ScriptWriter:
    def __init__(self,addr):

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
        writer=open(writer_addr,"w")
        self.script_writers.append(writer)
        writer_idx=len(self.script_writers)-1
        if additional_tag:
            self.script_names[str(writer_idx)]=additional_tag
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
        self.script_names={}
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
        # self.export_paths()