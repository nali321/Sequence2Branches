import pandas as pd

#creates the dictionary structure to easily search accessions by strain name
def structure(filepath):
    collection = []

    #open the file and split up the contents of each row
    #and save it into a list of lists
    with open(filepath, 'r', encoding="utf-8") as file:
        for line in file:
            z = line.split('\t')
            
            collection.append(z)
    
    collection.pop(0)

    name_structure = {}
    species_names = set()

    acc_structure = {}

    #creates a dictionary structure where keys are species names
    #allows for quick lookup of leaves for the tree
    for x in collection:
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

    return name_structure, acc_structure

#obtain a list of data for every leaf of the tree
#you need to try searching name first, and if that doesn't work, search
#the accession instead
def leaves(name_structure, acc_structure, max, species):
    leaves = []
    #iterate through list of lists of species
    #x[0] = accession, x[7] = species name, x[8] = strain name, 
    #x[11] = assembly type, x[19] = ftp path
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

                #check if 8th column (strain name) is empty, if so, use 9th
                if strain == '':
                    strain = x[9]

                    #if 9th column blank, give it its own name
                    if strain == '':
                        strain = "unique_" + str(blank)
                        blank+=1
                        leaves.append((x[0], strain, x[19][57:]))

                    #duplicate check
                    elif strain in strain_names:
                        strain = strain + "_copy_" + str(diff)
                        diff+=1
                        leaves.append((x[0], strain, x[19][57:]))
                    
                    #if its unique, add it normally
                    else:
                        strain_names.add(strain)
                        leaves.append((x[0], strain, x[19][57:]))

                #if 8th column is there, remove "strain="
                elif strain[0:6] == "strain":
                    strain = strain[7:]

                    #duplicate check
                    if strain in strain_names:
                        strain = strain + "_copy_" + str(diff)
                        diff+=1
                        leaves.append((x[0], strain, x[19][57:]))
                    
                    #if unique, add normally
                    else:
                        strain_names.add(strain)
                        leaves.append((x[0], strain, x[19][57:]))    

    except KeyError:
        print("species name doesn't match dictionary entry")

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