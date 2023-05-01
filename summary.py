import pandas as pd
import methods

#creates two dictionaries:
#name_structure: allows you to use taxa as the key to pull entries of accessions
#acc_structure: allows you to use accession name as the key to pull accession-specific entries
def structure(filepath):
    species_names = set()
    name_structure = {}
    acc_structure = {}

    #open the file and split up the contents of each row
    #and save it into a list of lists
    with open(filepath, 'r', encoding="utf-8") as file:
        header = True
        for line in file:
            if header != True:
                x = line.split('\t')
                
                #add to accession structure
                acc_structure[x[0]] = [x]

                #if its not in species list, create an empty list as an entry for that species name,
                #and add the entire row into it as a list within a list
                if x[7] not in species_names:
                    species_names.add(x[7])
                    name_structure[x[7]] = []
                    name_structure[x[7]].append(x)
                
                #if its already in, add that row as a list within the dictionary list
                else:
                    name_structure[x[7]].append(x)
            header = False
    
    return name_structure, acc_structure

#obtain a list of data for every leaf of the tree
#you need to try searching name first, and if that doesn't work, search the accession instead
def leaves(name_structure, acc_structure, max, species):
    leaves = []
    full = []
    partial = []
    #iterate through list of lists of species
    #x[0] = accession, x[7] = species name, x[8] = strain name, 
    #x[11] = assembly type, x[13] = genome_rep, x[19] = ftp path
    try:
        blank = 1
        diff = 1
        strain_names = set()
        entries = name_structure[species]

        #iterate through entries searched by species name
        #and keep going until the user specified max is reached
        for x in entries:
            if len(leaves) < max:
                #obtain the accession, strain name, and ftp link
                strain = x[8]
                level = x[11]
                rep = x[13]

                #check if 8th column (strain name) is empty, if so, use 9th
                if strain == '':
                    strain = x[9]

                    #if 9th column blank, give it its own name
                    if strain == '':
                        strain = "unique_" + str(blank)
                        strain = methods.standardize(strain)
                        blank+=1
                        if level == "Complete Genome":
                            leaves.append((x[0], strain, x[19][57:]))
                        elif level != "Complete Genome" and rep == "Full":
                            full.append((x[0], strain, x[19][57:]))
                        else:
                            partial.append((x[0], strain, x[19][57:]))

                    #duplicate check
                    elif strain in strain_names:
                        strain = strain + "_copy_" + str(diff)
                        strain = methods.standardize(strain)
                        diff+=1
                        if level == "Complete Genome":
                            leaves.append((x[0], strain, x[19][57:]))
                        elif level != "Complete Genome" and rep == "Full":
                            full.append((x[0], strain, x[19][57:]))
                        else:
                            partial.append((x[0], strain, x[19][57:]))
                    
                    #if its unique, add it normally
                    else:
                        strain = methods.standardize(strain)
                        strain_names.add(strain)
                        if level == "Complete Genome":
                            leaves.append((x[0], strain, x[19][57:]))
                        elif level != "Complete Genome" and rep == "Full":
                            full.append((x[0], strain, x[19][57:]))
                        else:
                            partial.append((x[0], strain, x[19][57:]))

                #if 8th column is there, remove "strain="
                elif strain[0:6] == "strain":
                    strain = strain[7:]

                    #duplicate check
                    if strain in strain_names:
                        strain = strain + "_copy_" + str(diff)
                        strain = methods.standardize(strain)
                        diff+=1
                        if level == "Complete Genome":
                            leaves.append((x[0], strain, x[19][57:]))
                        elif level != "Complete Genome" and rep == "Full":
                            full.append((x[0], strain, x[19][57:]))
                        else:
                            partial.append((x[0], strain, x[19][57:]))
                    
                    #if unique, add normally
                    else:
                        strain = methods.standardize(strain)
                        strain_names.add(strain)
                        if level == "Complete Genome":
                            leaves.append((x[0], strain, x[19][57:]))
                        elif level != "Complete Genome" and rep == "Full":
                            full.append((x[0], strain, x[19][57:]))
                        else:
                            partial.append((x[0], strain, x[19][57:]))

    except KeyError:
        print("Species name does not match collected NCBI entries")

    #lower quality genomes added if neccessary
    for x in full:
        if len(leaves) < max:
            leaves.append(full[x])
    
    for x in partial:
        if len(leaves) < max:
            leaves.append(partial[x])

    return leaves

#obtain outgroup data
def outgroup(name_structure, acc_structure, species, accession):
    outgroup = ()
    edit = ''

    #check gca accession for outgroup
    if accession[2] == "F":
        edit = list(accession)
        edit[2] = 'A'
        accession=''.join(edit)

    #take outgroup data
    for x in acc_structure[accession]:
        outgroup = (x[0], x[7], x[19][57:])
        return outgroup