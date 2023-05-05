# Sequence2Branches

Sequence2Branches is a pipeline utilizing Snakemake designed to create a species-level phylogenetic tree from FASTQ paired reads. It handles trimming the reads, creating and annotating the assembly, identifying the species of the isolate, and creating the phylogenetic tree.

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
```

This pipeline was originally designed on an HPC-server without internet access on clusters, therefore pre-installing the conda environments/dependencies before running the Snakemake pipeline was implemented. This achieves the same result as if the conda module was used on Snakemake, where the conda environments are specifically downloaded to a separate folder instead of your main envs folder.

## Usage Guide:
### Quick Start
```
python /path/to/sequence2branches.py -r1 /path/to/read_1 -r2 /path/to/read_2 -i /path/to/illuminaclip -s /path/to/genbank/assembly_summary.txt -r path/to/genbank/references -g /path/to/gtdbtk -e /path/to/envs -m /path/to/metadata.csv -o /path/to/outdir
```
