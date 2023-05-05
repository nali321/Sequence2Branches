OUTPUT = config["output"]
ENVS = config["envs_path"]
CONDA_PATH = config["conda_path"]
ISOLATE_GFF = f"{OUTPUT}/isolate_prokka/genome_isolate.gff"

rule roary:
    input:
        gffs=f"{PANGENOME_PATH}/gffs"
    output:
        pangenome=f"{PANGENOME_PATH}/roary/gene_presence_absence.csv"
    shell:
        '''
        cp {ISOLATE_GFF} {input.gffs}
        source {CONDA_PATH}
        conda activate {ENVS}/roary
        roary -e --mafft -p 8 -f {PANGENOME_PATH}/roary {input.gffs}/*.gff
        conda deactivate
        '''