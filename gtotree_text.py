import os
import sys

#create fasta_files.txt
def fasta_files(path, leaves):
    all_accessions = []
 
    for x in leaves:
        all_accessions.append(x[0])

    f = open(f"{path}/fasta_files.txt", "w+")
    for x in all_accessions:
            f.write(x + ".fa.gz")
            f.write("\n")

    f.write("contigs.fa")

#create map_id.txt
#create a parameter to have user name contigs.fa
def map_id(path, leaves):

    f = open(f"{path}/map_id.txt", "w+")
    for x in leaves:
        accession = x[0]
        name = x[1]

        f.write(str(accession) + ".fa.gz" + "\t" + str(name))
        f.write("\n")

    f.write("contigs.fa" + "\t" + "isolate")