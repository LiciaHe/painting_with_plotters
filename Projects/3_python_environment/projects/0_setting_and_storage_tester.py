import sys
sys.path.insert(1,"../")

from PWP.Generator.SettingAndStorageGenerator import SettingAndStorageGenerator

settings={
    "name":"0_s_s_tester",
    "parameters":{},
    "basic_settings":{
        "export_loc": "",
    }
}
generator=SettingAndStorageGenerator(settings=settings)
print(generator.get_full_save_loc("txt"))