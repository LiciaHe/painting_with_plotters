'''
A class that represent one path in the design. Used to store path (coordinates) and tool (index) together.
'''
class Path:
    def __init__(self,path,tool_idx,filled=False):
        '''
        Stores the given information
        Args:
            path: a list of 2d points
            tool_idx: an integer
            filled: a boolean value. By default, False.
        '''
        self.path=path
        self.tool_idx=tool_idx
        self.filled=filled