# Sequence2Branches

Sequence2Branches is a pipeline utilizing Snakemake designed to create a species-level phylogenetic tree from FASTQ paired reads. It handles trimming the reads, creating and annotating the assembly, identifying the species of the isolate, and creating the phylogenetic tree.

## Features:
After identifying the taxonomy of the isolate, Sequence2Branches creates a phylogenetic tree selecting bacterial genomes that share the same species as the isolate from NCBI's [GenBank Database](https://www.ncbi.nlm.nih.gov/genbank/), to be used as leaves of the tree, as well as selecting an outgroup that shares the same genus as the isolate and leaves. The first tree, called "big tree" is made through the user selecting a number of leaves for the tree (default is 1000). A second, more readable tree, called "little tree", is also created with the user selecting the number of leaves (default is 50 and reccomended to be less than 100), but selects its leaves from the most closely related leaves to the isolate in the big tree. Creating the big tree, and then taking a "sub-tree" from it in the form of the little tree allows for the most accurate classification of the isolate given the taxonomic identity and quanity of genomes on NCBI for that specices is unknown.

## Prerequisites:
- Must be ran on Linux
- [Miniconda](https://docs.conda.io/en/latest/miniconda.html) installed and conda set up
- [Mamba](https://mamba.readthedocs.io/en/latest/installation.html) installed
- Install [GTDB-tk](https://github.com/Ecogenomics/GTDBTk) as a conda environment for taxonomic identification
- Download GenBank bacteria genomes locally:
```
#download all genbank genomes
mkdir /path/to/genbank
cd /path/to/genbank
wget ftp://ftp.ncbi.nih.gov/genomes/genbank/bacteria/assembly_summary.txt

#parse summary file
awk -F '\t' '{print $20}' assembly_summary.txt > assembly_summary_allftp_genomes.txt
sed -e "s/https\:\/\//ftp:\/\//g" -i assembly_summary_allftp_genomes.txt

#download all
for next in $(cat /path/to/genbank/assembly_summary_allftp_genomes.txt); do wget -P references "$next"/*genomic.fna.gz; done
```

## Installation:
```
git clone https://github.com/nali321/Sequence2Branches
```

## Setup:
Run conda_installer.py to create environments for pipeline.

```
python /path/to/conda_installer.py -o /path/to/envs
conda activate /path/to/envs/sequence2branches
```

This pipeline was originally designed on an HPC-server without internet access on clusters, therefore pre-installing the conda environments/dependencies before running the Snakemake pipeline was implemented. This achieves the same result as if the conda module was used on Snakemake, where the conda environments are specifically downloaded to a separate folder instead of your main envs folder.

## Usage Guide:
### Quick Start
```
python /path/to/sequence2branches.py -r1 /path/to/read_1 -r2 /path/to/read_2 -i /path/to/illuminaclip -s /path/to/genbank/assembly_summary.txt -r path/to/genbank/references -g /path/to/gtdbtk -e /path/to/envs -o /path/to/outdir
```

### All Parameters:
```
options:
  -h, --help            show this help message and exit
  -r1 READ1, --read1 READ1
                        Filepath of first half of read pair
  -r2 READ2, --read2 READ2
                        Filepath of second half of read pair
  -i ILLUMINACLIP, --illuminaclip ILLUMINACLIP
                        Illuminaclip used in Trimmomatic
  -s SUMMARY, --summary SUMMARY
                        Filepath to assembly_summary.txt
  -r REFERENCES, --references REFERENCES
                        Filepath to references folder
  -g GTDBTK, --gtdbtk GTDBTK
                        Filepath to GTDB-tk conda environment
  -e ENVS, --envs ENVS  Filepath to envs folder
  -o OUTDIR, --outdir OUTDIR
                        Directory where output will go
                        
  ###OPTIONAL
  
  -bt BIG_TREE, --big_tree BIG_TREE
                        Maximum number of leaves for the big tree. Default is 1000
  -lt LITTLE_TREE, --little_tree LITTLE_TREE
                        Maximum number of leaves for the little tree. Default is 50
  -pg PANGENOME_SIZE, --pangenome_size PANGENOME_SIZE
                        Maximum size of the pangenome
  -sc SNAKEMAKE_CORES, --snakemake_cores SNAKEMAKE_CORES
                        Number of cores for Snakemake to use. Default is 6
