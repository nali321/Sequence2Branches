import os
import natsort
import yaml
import pandas as pd
from ete3 import Tree

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

#returns user-specified closest leaves from isolate
def closest_leaves(newick, size, nametodata, outgroup):

    #obtain the newick from the file
    file = open(newick, "r")
    data = file.read()
    file.close()

    #set tree from newick and outgroup
    t = Tree(data)
    q = outgroup[1].replace(" ", "_")
    t.set_outgroup(t&q)

    disttoname = {}
    distances = []
    #obtain distances from isolate and other leaves
    for x in t:
        iso = t&"isolate"
        d = iso.get_distance(x)

        if x.name != "isolate":
            distances.append(d)
            disttoname[d] = x.name

    #sort distances from least to greatest
    distances.sort()

    #pick user specified max amount of leaves for smaller tree
    little_leaves = []
    for x in distances:
        if len(little_leaves) < size:
            name = disttoname[x]
            little_leaves.append(nametodata[name])

    #create the gtotree text files for smaller tree
    #you need to re-add outgroup to little tree
    if outgroup not in little_leaves:
        little_leaves.append(outgroup)
    
    return little_leaves