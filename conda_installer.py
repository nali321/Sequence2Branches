import os
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-o", "--outdir", type=str,
                    help="Directory where environments will go", required=True)

args = parser.parse_args()

#create output directory
outdir = args.outdir
try:
    os.mkdir(outdir)
except OSError as error:
    print(error)

#get conda profile path
conda_path_file = os.path.join(outdir, "CONDA_PATH.txt").replace("\\", "/")
os.system(f"conda info --root > {conda_path_file}")
with open (conda_path_file, 'r') as file:
    for line in file:
        conda_profile = os.path.join(line.strip('\n'), "etc/profile.d/conda.sh").replace("\\", "/")
        break

#get the script path
home_dir = os.path.dirname(os.path.abspath(__file__))
envs_dir = os.path.join(home_dir, "workflow/envs")

#iterate over predownloaded envs folder, and download them from the .yamls
for filename in os.listdir(envs_dir):
    z = os.path.join(envs_dir, filename).replace("\\", "/")
    env = os.path.join(outdir, filename.split(".")[0])
    os.mkdir(env)
    os.system(f"mamba env create -f {z} -p {env}")
