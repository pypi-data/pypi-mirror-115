import os
import glob

#Path
root_path = os.path.dirname(os.path.realpath(__file__))
output_path = root_path + "//output//"


def clean_up():
    os.chdir(output_path) 
    filelist = glob.glob(os.path.join(output_path, "*"))
    #print("start")
    #print(os.getcwd())
    for f in filelist:
        #print(f)
        os.remove(f)

clean_up()