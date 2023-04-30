OUTPUT = config["output"]
ENVS = config["envs_path"]
CONDA_PATH = config["conda_path"]

rule roary:
    input:
        gffs=f"{OUTPUT}/gffs"
    output:
        pangenome=f"{OUTPUT}/roary/gene_presence_absence.csv"
    shell:
        '''
        source {CONDA_PATH}
        conda activate {ENVS}/roary
        roary -e --mafft -p 8 -f {OUTPUT}/roary {input.gffs}/*.gff
        conda deactivate
        '''