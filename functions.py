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

#any strain names that have a parenthesis will get removed in their
#gtotree .tre label name causing a key error down the line
#also key error if any spaces dont get turned into underscores
def standardize(string):
    string = string.replace('(', '_')
    string = string.replace(')', '_')
    string = string.replace(' ', '_')
    return string

#creates the config file for the snakefile
def config(d, name, outdir):
    path = os.path.join(f"{outdir}", f"{name}.yaml").replace("\\", "/")
    with open (path, "w") as outfile:
        yaml.dump(d, outfile)
    return path

#returns user-specified closest leaves from isolate
def closest_leaves(newick, size, nametodata, outgroup):

    #obtain the newick from the file
    with open(newick, "r") as file:
        data = file.read()

    #set tree from newick and outgroup
    t = Tree(data)
    q = outgroup[1].replace(" ", "_")
    t.set_outgroup(t&q)

    disttoname = {}
    distances = []
    #obtain distance from isolate then the loop over tree to get distances from other leaves
    #leaves can have the same distance, make a (dist, name) tuple to be unqiue
    iso = t&"isolate"
    for x in t:
        d = iso.get_distance(x)

        if x.name != "isolate":
            distances.append((d, x.name))

            #any parentheses in strain name get changed back to underscores
            if d in disttoname:
                print("DUPLICATE")
            disttoname[d] = x.name

    #sort distances from least to greatest
    sorted_distances = sorted(distances)

    #pick user specified max amount of leaves for smaller tree
    little_leaves = []
    for x in sorted_distances:
        if len(little_leaves) < size:
            # name = disttoname[x]
            name = x[1]
            little_leaves.append(nametodata[name])

    #create the gtotree text files for smaller tree
    #you need to re-add outgroup to little tree
    if outgroup not in little_leaves:
        little_leaves.append(outgroup)
    
    return sorted_distances, little_leaves