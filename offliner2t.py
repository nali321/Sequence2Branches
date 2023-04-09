import os
import gtdbtk_extractor
import summary
import gtotree_text
import argparse
import switch_maker
from ete3 import Tree

parser = argparse.ArgumentParser()

parser.add_argument("-r1", "--read1", type=str,
                    help="Filepath of first half of read pair")

parser.add_argument("-r2", "--read2", type=str,
                    help="Filepath of second half of read pair")

parser.add_argument("-s", "--summary", type=str,
                    help="Filepath to assembly_summary.txt")

parser.add_argument("-r", "--references", type=str,
                    help="Filepath to references folder")

parser.add_argument("-bt", "--big_tree", type=int,
                    help="Maximum number of leaves for the big tree")

parser.add_argument("-lt", "--little_tree", type=int,
                    help="Maximum number of leaves for the little tree")

parser.add_argument("-pg", "--pangenome_size", type=int,
                    help="Maximum size of the pangenome")

parser.add_argument("-o", "--outdir", type=str,
                    help="Directory where output will go")

#make assembly summary filepath and references filepath flags
#make cpus flag

args = parser.parse_args()

#the input the user has to provide are the paired reads
read1 = args.read1
read2 = args.read2

#get filepath to assembly_summary
summary_path = args.summary

#get filepath to references folder
ref_path = args.references

#sets max number of leaves for big tree
if args.big_tree is None:
    big_tree_size = 1000
else:
    big_tree_size = args.big_tree

#set max number of leaves for small tree
if args.little_tree is None:
    little_tree_size = 50
else:
    little_tree_size = args.little_tree

#set max number of genomes for pangenome
if args.pangenome_size is None:
    pangenome_size = None
else:
    pangenome_size = args.pangenome_size

#if output directory already exists, send error message
path = args.outdir
try:
    os.mkdir(path)
except OSError as error:
    print(error)

#makes switches directory
switches = os.path.join(path, "switches").replace("\\", "/")
os.mkdir(switches)

#PIPELINE: trimmomatic > spades.py > quast.py > prokka > gtdbtk > gtotree

#trimmomatic
trim = os.path.join(path, "trim").replace("\\", "/")
os.mkdir(trim)
os.system(f"trimmomatic PE -phred33 {read1} {read2} {trim}/forward_paired.fq.gz {trim}/forward_unpaired.fq.gz {trim}/reverse_paired.fq.gz {trim}/reverse_unpaired.fq.gz ILLUMINACLIP://mmfs1//groups//HPC-Marshall//miniconda3//pkgs//trimmomatic-0.39-hdfd78af_2//share//trimmomatic-0.39-2//adapters//NexteraPE-PE.fa:2:30:10 LEADING:20 TRAILING:20 SLIDINGWINDOW:4:20 MINLEN:70")

#spades
spades = os.path.join(path, "spades").replace("\\", "/")
os.mkdir(spades)
os.system(f"spades.py -o {spades} -1 {trim}/forward_paired.fq.gz -2 {trim}/reverse_paired.fq.gz -s {trim}/forward_unpaired.fq.gz -m 128 -k 33,55,77,99 --careful -t 16")

#quast
quast = os.path.join(path, "quast").replace("\\", "/")
os.mkdir(quast)
os.system(f"/mmfs1/groups/HPC-Marshall/build/quast-5.1.0rc1/quast.py {spades}/contigs.fasta -o {quast}")

#prokka
prokka = os.path.join(path, "prokka").replace("\\", "/")
os.mkdir(prokka)
switch_maker.prokka_switch(switches, prokka, spades)
os.system(f"bash {switches}/prokka.sh")

#gtdbtk
#create a folder with contigs.fna in it
genome_dir = os.path.join(path, "genome_dir").replace("\\", "/")
os.mkdir(genome_dir)
os.system(f"cp {spades}/contigs.fasta {genome_dir}/contigs.fna")

gtdbtk = os.path.join(path, "gtdbtk").replace("\\", "/")
os.mkdir(gtdbtk)
switch_maker.gtdbtk_switch(switches, gtdbtk, genome_dir)
os.system(f"bash {switches}/gtdbtk.sh")

#gtotree
#call gtdbtk_extractor
filepath = f"{gtdbtk}/classify/gtdbtk.bac120.summary.tsv"

#get the species name and h-flag name
species_name, h_flag, species_acc = gtdbtk_extractor.flag_extractor(filepath)

#create the dictionary structure for species name lookup
name_structure, acc_structure = summary.structure(summary_path)

#GET LEAVES FOR THE BIG TREE
#obtain leaves by looking up species name
big_leaves = summary.leaves(name_structure, acc_structure, big_tree_size, species_name)

#take accessions from leaves and feed it into other_related to avoid outgroup
#accession matching one of the accessions of the leaves
leaf_accessions = []
for leaf in big_leaves:
    leaf_accessions.append(leaf[0])

#get the other related species name
other_related = gtdbtk_extractor.other_related(filepath, species_name, species_acc, leaf_accessions)

#obtain outgroup by searching its accession
outgroup = summary.outgroup(name_structure, acc_structure, other_related[1], other_related[0])

#combine outgroup tuple with leaves to get final list
big_leaves.append(outgroup)

#create the text files needed for big gtotree
big_gtotree_text_files = os.path.join(path, "big_gtotree_text_files").replace("\\", "/")
os.mkdir(big_gtotree_text_files)
gtotree_text.fasta_files(big_gtotree_text_files, big_leaves)
gtotree_text.map_id(big_gtotree_text_files, big_leaves)

#EXTRACT FILEPATH NAME FROM COLUMN 20: "FTP_PATH", AND ADD "_genomic.fna.gz" AT THE END TO FIND
#IT IN REFERENCES: /mmfs1/groups/HPC-Marshall/database/genbank_3-2022/references
#need to rename .fa.gz file as accession.fa.gz file only

#move accessions and rename them in the main directory
#leaves[0] = accession | leaves[1] = strain name | leaves[2] = ftp path
#also assign name key to accession value
nametodata = {}
for x in big_leaves:
    acc = x[0] + ".fa.gz"
    ftp = x[2] + "_genomic.fna.gz"
    ftp_path = os.path.join(ref_path, ftp).replace("\\", "/")
    acc_path = os.path.join(path, acc).replace("\\", "/")
    os.system(f"cp {ftp_path} {acc_path}")

    nametodata[x[1]] = (x[0], x[1].replace(" ", "_"), acc_path)

#THIS IS THE ISOLATE
#move contigs.fasta from ./spades to main dir, renamed contigs.fa
isolate = os.path.join(path, "contigs.fa").replace("\\", "/")
os.system(f"cp {spades}/contigs.fasta {isolate}")

#create the gtotree switch and gtotree output folder for the big tree
big_gtotree = os.path.join(path, "big_gtotree").replace("\\", "/")

#use gtotree switch
switch_maker.gtotree_switch(path, big_gtotree_text_files, switches, big_gtotree, h_flag, "big")
os.system(f"bash {switches}/big_gtotree.sh")

#BIG TREE MADE  

#TAKE THE NEWICK FROM
big_newick_file = f"{big_gtotree}/big_gtotree.tre"

#obtain the newick from the file
file = open(big_newick_file, "r")
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
    if len(little_leaves) < little_tree_size:
        name = disttoname[x]
        little_leaves.append(nametodata[name])

#create the gtotree text files for smaller tree
#you need to re-add outgroup to little tree
if outgroup not in little_leaves:
    little_leaves.append(outgroup)

#create the text files needed for big gtotree
little_gtotree_text_files = os.path.join(path, "little_gtotree_text_files").replace("\\", "/")
os.mkdir(little_gtotree_text_files)
gtotree_text.fasta_files(little_gtotree_text_files, little_leaves)
gtotree_text.map_id(little_gtotree_text_files, little_leaves)

#create output path for little gtotree run
little_gtotree = os.path.join(path, "little_gtotree").replace("\\", "/")

#use gtotree switch
switch_maker.gtotree_switch(path, little_gtotree_text_files, switches, little_gtotree, h_flag, "little")
os.system(f"bash {switches}/little_gtotree.sh")

#LITTLE TREE MADE

#OPTINAL PANGENOME MAKING STEP
if pangenome_size != None:
    #move closest genomes to gffs folder, unzip them, and run prokka on them
    #get the filepaths of the user specified closest genomes to isolate
    roary_genomes = []
    for x in distances:
        if len(roary_genomes) < pangenome_size:
            name = disttoname[x]
            roary_genomes.append(nametodata[name][2])

    pan_dir = os.path.join(path, "pangenome").replace("\\", "/")
    os.mkdir(pan_dir)

    #create fastas folder
    fastas_dir = os.path.join(pan_dir, "fastas").replace("\\", "/")
    os.mkdir(fastas_dir)

    #move genomes to fastas folder and collect future unzipped file name
    fasta_genomes = []
    for x in roary_genomes:
        os.system(f"cp {x} {fastas_dir}")
        unzip = os.path.basename(x)[:-3]
        fasta_genomes.append(os.path.join(fastas_dir, unzip))

    #unzip all the .gz files
    os.system(f"gzip -d {fastas_dir}/*.gz")

    #create prokka directory
    pan_prokka_dir = os.path.join(pan_dir, "prokka").replace("\\", "/")
    os.mkdir(pan_prokka_dir)

    #run prokka
    for x in fasta_genomes:
        name = os.path.basename(x)
        name_dir = os.path.join(pan_prokka_dir, name).replace("\\", "/")
        switch_maker.pan_prokka_switch(switches, name, x, name_dir)
        os.system(f"bash {switches}/{name}_prokka.sh")

    #create gffs folder
    gffs = os.path.join(pan_dir, "gffs").replace("\\", "/")
    os.mkdir(gffs)

    #extract .gff folders from prokka output folders and place them into gffs
    for x in fasta_genomes:
        name = os.path.basename(x)
        os.system(f"cp {pan_prokka_dir}/{name}/genome.gff {gffs}/{name}.gff")

    #move isolate gff to folder
    os.system(f"cp {prokka}/genome.gff {gffs}/isolate.gff")

    #create roary folder
    roary_dir = os.path.join(pan_dir, "roary").replace("\\", "/")

    #run roary on the gffs folder
    #roary -e --mafft -p *.gff
    switch_maker.roary_switch(switches, gffs, roary_dir)
    os.system(f"bash {switches}/roary.sh")