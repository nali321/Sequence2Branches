import os
import natsort
import yaml
import pandas as pd
from ete3 import Tree

#compare two paths. used to check if conda profile path and gtdbtk env path
#are from the same conda profile
def path_compare(path1, path2):

    #if the paths contain two or more folders check if equal
    if path1.count(os.path.sep) >= 2 and path2.count(os.path.sep) >= 2:
        parent_path2 = os.path.dirname(path2)
        if path1 == parent_path2:
            return True
        else:
            return None
        
    #if the paths are only one folder long check if equal
    else:
        if path1 == path2:
            return True
        else:
            return None

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
    
    return distances, disttoname, little_leaves