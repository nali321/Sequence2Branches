import os
import argparse
import methods
import gtdbtk_extractor
import summary
import gtotree_text
import switch_maker
from ete3 import Tree

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
    "conda_path": conda_profile, "envs_path": envs_path, "gtdbtk_path": gtdbtk_path}

#create config file
config_path = methods.config(d, "config1", outdir)