'''
An extension of SvgGenerator that handles the generation and storage of script files used to control axidraws.

Each project needs to implement the "create()" function.
The "generate()" function processes the information, create svg files for visualization and python script for
'''

from ..Generator.SvgGenerator import SvgGenerator

class ScriptGenerator(SvgGenerator):

    def prepare_script_writers(self):
        '''
        Initiate writers for python script.
        Import initial content from template

        Returns:

        '''
        self.axidraw_writers=[]
        self.axidraw_names={}
        


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