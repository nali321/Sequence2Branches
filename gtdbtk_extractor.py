import pandas as pd

#extracts species name and h-flag from the 2nd column and of gtdbtk's .tsv file
def flag_extractor(filepath):
    
    file = open(filepath)
    df = pd.read_csv(file, delimiter="\t")

    #if proteobacteria phylum go to class
    #otherwise just use phylum
    phylum = "p__"
    clas = "c__"
    species = "s__"
    proteo = "p__Proteobacteria"

    #2nd column: classification
    #16th column: other_related_references(genome_id,species_name,radius,ANI,AF)
    acc = str(df['fastani_reference'].values[0])
    col = str(df['classification'].values[0])

    #split by semicolon
    z = col.split(';')

    #species name extracting
    h_flag_name = ""

    for x in z:
        
        #look for the species name tag
        if x[0:3] == species:
            names = x[3:].split()
            
            #avoid working with empty line
            if len(names) != 0:

                #remove underscore suffix if need be
                full_name = ""
                
                #iterate through family then species
                for name in names:
                    actual = name

                    #actual will be the name without underscore
                    if "_" in name:
                        actual = name.split("_", 1)[0]
                    
                    #if family name, add a space after
                    if name == names[0]:
                        full_name = actual + " "

                    else:
                        full_name+=actual     
        
        #save the phylum to use for h-flag
        if x[0:3] == phylum:
            switch = x
            if switch != proteo:
                h_flag_name = x[3:]
        
        #if the phylum was proteobacteria, switch to class
        if x[0:3] == clas:
            if switch == proteo:
                h_flag_name = x[3:]

    #extra checks
    if h_flag_name == "Actinobacteriota":
        h_flag_name = "Actinobacteria"

    return full_name, h_flag_name, acc

#extracts related species from 16th column of
#gtdbtk .tsv file
def other_related(filepath, species_name, species_accession, leaf_accessions):
    df = pd.read_csv(filepath, delimiter="\t")
    col = str(df["other_related_references(genome_id,species_name,radius,ANI,AF)"].values[0])

    z = col.split(';')

    outer = []
    for x in z:
        inner = x.split(",")

        #the first accession does not have a space
        #while everything after that does
        if inner[0][0] == " ":
            accession = inner[0][1:]

        else:
            accession = inner[0]

        names = inner[1][4:].split()

        #delete all underscores
        full_name = ""
        for name in names:
            actual = name

            if "_" in name:
                actual = name.split("_", 1)[0]
            
            #if family name, space
            if name == names[0]:
                full_name = actual + " "

            #add the two names together
            else:
                full_name+=actual

        outer.append([accession, full_name])

    #choose the first outgroup that doesn't match
    #the name of the species
    for x in outer:
        acc=x[0]
        name = x[1]

        #check if accession needs to be changed to gca
        if acc[2] == "F":
            edit = list(acc)
            edit[2] = 'A'
            acc=''.join(edit)

        #outgroup accession has to differ by both name and accession from
        #isolate species as well as leaves on the tree
        if name != species_name and acc != species_accession and acc not in leaf_accessions:
            return x