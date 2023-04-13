import os
import natsort
import yaml
import pandas as pd

#natsort a directory
def nsort(dir, full_path):
    nsort = []
    for filename in os.listdir(dir):
        if full_path == True:
            nsort.append(os.path.join(dir, filename).replace("\\", "/"))
        else:
            nsort.append(filename)
    nsort = natsort.natsorted(nsort)
    return nsort

#creates the config file for the snakefile
def config(d, name, outdir):
    path = os.path.join(f"{outdir}", f"{name}.yaml").replace("\\", "/")
    with open (path, "w") as outfile:
        yaml.dump(d, outfile)
    return path