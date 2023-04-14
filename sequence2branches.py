import os
import argparse
import methods
import gtdbtk_extractor
import summary
import gtotree_text

parser = argparse.ArgumentParser()

#required flags

parser.add_argument("-r1", "--read1", type=str,
                    help="Filepath of first half of read pair", required=True)

parser.add_argument("-r2", "--read2", type=str,
                    help="Filepath of second half of read pair", required=True)

parser.add_argument("-s", "--summary", type=str,
                    help="Filepath to assembly_summary.txt", required=True)

parser.add_argument("-r", "--references", type=str,
                    help="Filepath to references folder", required=True)

parser.add_argument("-g", "--gtdbtk", type=str,
                    help="Filepath to GTDB-tk conda environment", required=True)

parser.add_argument("-e", "--envs", type=str,
                    help="Filepath to envs folder", required=True)

parser.add_argument("-o", "--outdir", type=str,
                    help="Directory where output will go", required=True)

#optional flags

parser.add_argument("-bt", "--big_tree", type=int,
                    help="Maximum number of leaves for the big tree", default="1000")

parser.add_argument("-lt", "--little_tree", type=int,
                    help="Maximum number of leaves for the little tree", default="50")

parser.add_argument("-pg", "--pangenome_size", type=int,
                    help="Maximum size of the pangenome")

parser.add_argument("-sc", "--snakemake_cores", type=str,
                    help="Number of cores for Snakemake to use. Default is 6", default="6")

args = parser.parse_args()

r1 = args.read1
r2 = args.read2
summary_path = args.summary
ref_path = args.references
gtdbtk_path = args.gtdbtk
envs_path = args.envs
sc = args.snakemake_cores
big_tree_size = args.big_tree
little_tree_size = args.little_tree

#set max number of genomes for pangenome
if args.pangenome_size is None:
    pangenome_size = None
else:
    pangenome_size = args.pangenome_size

#if output directory already exists, send error message
outdir = args.outdir
try:
    os.mkdir(outdir)
except OSError as error:
    print(error)

#get the snakefile, script, and dependencies path
home_dir = os.path.dirname(os.path.abspath(__file__))
snake_dir = os.path.join(home_dir, "workflow")
scripts_dir = os.path.join(home_dir, "workflow/scripts")
dep = os.path.join(envs_path, "dependencies").replace("\\", "/")

#get conda profile path
conda_path_file = os.path.join(outdir, "CONDA_PATH.txt").replace("\\", "/")
os.system(f"conda info --root > {conda_path_file}")
with open (conda_path_file, 'r') as file:
    for line in file:
        conda_profile = os.path.join(line.strip('\n'), "etc/profile.d/conda.sh").replace("\\", "/")
        break

#create config file for isolate proccessing
d = {"output": outdir, "r1": r1, "r2": r2,
    "conda_path": conda_profile, "envs_path": envs_path, 
    "gtdbtk_path": gtdbtk_path, "tree_type": "N/A", 
    "gtotree_text": "N/A", "h_flag": "N/A", "rule_type": "isolate"}

#create config file
config_path = methods.config(d, "isolate_config", outdir)

#call isolate snakefile
os.system(f"snakemake --cores {sc} --directory {outdir} --snakefile {snake_dir}/Snakefile all --configfile {config_path}")

#get the species name and h-flag name
gdtbtk_summary = f"{outdir}/gtdbtk/gtdbtk.bac120.summary.tsv"
species_name, h_flag, species_acc = gtdbtk_extractor.flag_extractor(gdtbtk_summary)

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
other_related = gtdbtk_extractor.other_related(gdtbtk_summary, species_name, species_acc, leaf_accessions)

#obtain outgroup by searching its accession
outgroup = summary.outgroup(name_structure, acc_structure, other_related[1], other_related[0])

#combine outgroup tuple with leaves to get final list
big_leaves.append(outgroup)

#create the text files needed for big gtotree
big_gtotree_text_files = os.path.join(outdir, "big_gtotree_text_files").replace("\\", "/")
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
os.mkdir(f"{outdir}/accessions")
for x in big_leaves:
    acc = x[0] + ".fa.gz"
    ftp = x[2] + "_genomic.fna.gz"
    ftp_path = os.path.join(ref_path, ftp).replace("\\", "/")
    acc_path = os.path.join(f"{outdir}/accessions", acc).replace("\\", "/")
    os.system(f"cp {ftp_path} {acc_path}")
    nametodata[x[1]] = (x[0], x[1].replace(" ", "_"), acc_path)

# #THIS IS THE ISOLATE
# #move contigs.fasta from ./spades to main dir, renamed contigs.fa
# isolate = os.path.join(f"{outdir}/accessions", "contigs.fa").replace("\\", "/")
# os.system(f"cp {outdir}/spades/contigs.fasta {isolate}")

#create config file for gtotree
d = {"output": outdir, "r1": "N/A", "r2": "N/A",
    "conda_path": conda_profile, "envs_path": envs_path, 
    "gtdbtk_path": "N/A", "tree_type": "big", "gtotree_text": big_gtotree_text_files, 
    "h_flag": h_flag, "rule_type": "gtotree"}

#create config file
config_path = methods.config(d, "gtotree_config", outdir)

#call big gtotree snakefile
os.system(f"snakemake --cores {sc} --directory {outdir} --snakefile {snake_dir}/Snakefile all --configfile {config_path}")

#get leaves for small tree
little_leaves = methods.closest_leaves(f"{outdir}/big_gtotree.tre", little_tree_size, nametodata, outgroup)

#create the text files needed for big gtotree
little_gtotree_text_files = os.path.join(outdir, "little_gtotree_text_files").replace("\\", "/")
os.mkdir(little_gtotree_text_files)
gtotree_text.fasta_files(little_gtotree_text_files, little_leaves)
gtotree_text.map_id(little_gtotree_text_files, little_leaves)

#create config file for gtotree
d = {"output": outdir, "r1": "N/A", "r2": "N/A",
    "conda_path": conda_profile, "envs_path": envs_path, 
    "gtdbtk_path": "N/A", "tree_type": "little", "gtotree_text": little_gtotree_text_files, 
    "h_flag": h_flag, "rule_type": "gtotree"}

#create config file
config_path = methods.config(d, "gtotree_config2", outdir)

#call small gtotree snakefile
os.system(f"snakemake --cores {sc} --directory {outdir} --snakefile {snake_dir}/Snakefile all --configfile {config_path}")

#optional pangenome making step 
if pangenome_size != None:
    #move closest genomes to gffs folder, unzip them, and run prokka on them
    #get the filepaths of the user specified closest genomes to isolate
    roary_genomes = []
    for x in distances:
        if len(roary_genomes) < pangenome_size:
            name = disttoname[x]
            roary_genomes.append(nametodata[name][2])