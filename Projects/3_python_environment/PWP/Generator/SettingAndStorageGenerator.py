'''
A project management system for developing generative projects.
Handles random seed, setting, and storage.
'''

from ..Util import basic as UB
import datetime,random,os


class SettingAndStorageGenerator:

    def get_value_from_basic_settings(self,key):
        '''
        Get a value from the basic setting
        Args:
            key: a key to search in the basic_settings dictionary

        Returns: the value associated with the key, or None if the key does not exist.
        '''

        if key in self.basic_settings:
            return self.basic_settings[key]
        return None

    def get_value_from_parameters(self,key):
        '''
        Get a value from the parameters
        Args:
            key: a key to search in the parameters dictionary

        Returns: the value associated with the key, or None if the key does not exist.
        '''
        if key in self.parameters:
            return self.parameters[key]
        return None

    random_bits_ct=8

    def create_save_name(self,file_extension,additional_tag=""):
        '''
        Create a string that contains batch name (if it exists), the time_tag (start of the project), and some random bits.

        Args:
            file_extension: an extension(string) to be added to the save name. e.g., "jpg", "txt", "python","py"
            additional_tag: an optional string to be appended to the start of the name. Default value is an empty string.

        Returns: A string suitable for the name of a file to be stored
        '''
        name=""
        if additional_tag:
            name+=f'{additional_tag}_'

        if hasattr(self,"batch_name"):
            name+=self.batch_name


        return f'{name}{self.time_tag}_{random.getrandbits(self.random_bits_ct)}.{file_extension}'

    def get_full_save_loc(self,file_extension,additional_tag=""):
        return f'{self.dated_folder}{self.create_save_name(file_extension,additional_tag)}'



    def set_random_seed(self):
        '''
        Set the random seed for the project.
        The seed could be stored in the class, or passed through the basic_settings.
        If it's not available, use f'{self.time_tag}_{self.batch_name}'

        Returns:the random seed.
        '''
        seed = f'{self.time_tag}'
        if hasattr(self,"batch_name"):
            seed+= f'_{self.batch_name}'
        if hasattr(self,"seed"):
            seed=self.seed
        if self.get_value_from_basic_settings("seed"):
            seed=self.get_value_from_basic_settings("seed")

        self.seed=seed
        random.seed(a=self.seed)
    def export_seed(self):
        '''
        Export the seed to a txt file
        Returns:None
        '''
        with open(f'{self.dated_folder}seed.txt',"w") as sf:
            sf.write(str(self.seed))


    def init_storage(self):
        '''
        Initiate values used for the storage system.
        Returns:
        '''

        #get export loc
        export_loc=self.get_value_from_basic_settings("export_loc")
        if export_loc:
            UB.mkdir(export_loc)
        self.save_loc = f'{export_loc}{self.name}/'
        UB.mkdir(self.save_loc)

        self.dated_folder = f'{self.save_loc}{str(datetime.datetime.now().strftime("%Y-%m-%d"))}/'
        UB.mkdir(self.dated_folder)
        print(self.dated_folder)

        if self.get_value_from_basic_settings("batch_name"):
            self.batch_name=self.get_value_from_basic_settings("batch_name")

        if hasattr(self,"batch_name") and self.batch_name:
            self.dated_folder+=self.batch_name+"/"
            UB.mkdir(self.dated_folder)

        self.time_tag = str(datetime.datetime.now().strftime("%H%M%S"))
        self.dated_folder+=f'{self.time_tag}/'
        UB.mkdir(self.dated_folder)



    def __init__(self,settings,**kwargs):
        '''
        Initiate a storage management system.
        Minimally, requires input a setting
        Args:
            settings:
            **kwargs:
        '''
        self.settings=settings

        for key in kwargs:
            setattr(self,key,kwargs[key])

        self.name=self.settings["name"]
        self.basic_settings=self.settings["basic_settings"]
        self.parameters=self.settings["parameters"]
        self.init_storage()
        self.set_random_seed()
        self.export_seed()