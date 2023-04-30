python /mmfs1/home/4565alin/tools/READSTOTREE-V.2/OfflineG2T/offlineg2t.py \
-r1 /mmfs1/home/4565alin/all_genomes/assigned_reads/3_R1_001.fastq.gz \
-r2 /mmfs1/home/4565alin/all_genomes/assigned_reads/1_R2_001.fastq.gz \
-s /mmfs1/groups/HPC-Marshall/database/genbank_3-2022/assembly_summary.txt \
-r /mmfs1/groups/HPC-Marshall/database/genbank_3-2022/references -bt 1000 -lt 20 -pg 30 -o ~/V2_TEST

python ./ReadToTree/readtotree.py -r1 /mmfs1/home/4565alin/all_genomes/assigned_reads/1_R1_001.fastq.gz -r2 /mmfs1/home/4565alin/all_genomes/assigned_reads/1_R2_001.fastq.gz -e numair.ali@marquette.edu -o /mmfs1/home/4565alin/full_run_1

r1 = /mmfs1/home/4565alin/all_genomes/assigned_reads/1_R1_001.fastq.gz
r2 = /mmfs1/home/4565alin/all_genomes/assigned_reads/1_R2_001.fastq.gz

/mmfs1/home/4565alin/all_genomes/assigned_reads/2_R1_001.fastq.gz
/mmfs1/home/4565alin/all_genomes/assigned_reads/2_R2_001.fastq.gz

/mmfs1/home/4565alin/all_genomes/assigned_reads/3_R1_001.fastq.gz
/mmfs1/home/4565alin/all_genomes/assigned_reads/3_R2_001.fastq.gz

/mmfs1/home/4565alin/all_genomes/assigned_reads


#!/bin/bash

#SBATCH --job-name="offliner2t test"
#SBATCH --partition=batch
#SBATCH --time=200:00:00
#SBATCH --output=%x-%j.log
#SBATCH --nodes=1
#SBATCH --cpus-per-task=16
#SBATCH --mem=512GB
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=numair.ali@marquette.edu

for i in {1..24}; do
python ~/OfflineR2T/offliner2t.py -r1 /mmfs1/home/4565alin/2021_genomes/assigned_reads/"$i"_R1_001.fastq.gz -r2 /mmfs1/home/4565alin/2021_genomes/assigned_reads/"$i"_R2_001.fastq.gz -s /mmfs1/groups/HPC-Marshall/database/genbank_3-2022/assembly_summary.txt -r /mmfs1/groups/HPC-Marshall/database/genbank_3-2022/references -l 10 -o /mmfs1/home/4565alin/TEST/read_pair_"$i"
done

#install conda environments
python ~/tools/Sequence2Branches/conda_installer.py -o ~/SEQ2B_PREREQ/envs

#run without pangenome
python ~/tools/Sequence2Branches/sequence2branches.py -r1 /mmfs1/home/4565alin/reads2tree/2021_genomes/assigned_reads/1_R1_001.fastq.gz
-r2 /mmfs1/home/4565alin/reads2tree/2021_genomes/assigned_reads/1_R2_001.fastq.gz
-s /mmfs1/groups/HPC-Marshall/database/genbank_3-2022/assembly_summary.txt \
-r /mmfs1/groups/HPC-Marshall/database/genbank_3-2022/references \
-g /mmfs1/groups/HPC-Marshall/miniconda3/gtdbtk-2.1.0 \
-e /mmfs1/home/4565alin/SEQ2B_PREREQ/envs \
-o ~/seq2b_test \
-bt 20 -lt 10