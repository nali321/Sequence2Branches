OUTPUT = config["output"]
ENVS = config["envs_path"]
CONDA_PATH = config["conda_path"]
ISOLATE_GFF = f"{OUTPUT}/isolate_prokka/genome_isolate.gff"

# rule roary:
#     input:
#         gffs=f"{PANGENOME_PATH}/gffs"
#     output:
#         pangenome=f"{PANGENOME_PATH}/roary/gene_presence_absence.csv"
#     shell:
#         '''
#         cp {ISOLATE_GFF} {input.gffs}
#         source {CONDA_PATH}
#         conda activate {ENVS}/roary
#         roary -e --mafft -p 8 -f {PANGENOME_PATH}/roary {input.gffs}/*.gff
#         conda deactivate
#         '''
rule roary:
    input:
        gffs=expand(f"{PANGENOME_PATH}/prokka/{{sample}}/{{sample}}.gff", sample=SAMPLES)
    output:
        pangenome=f"{PANGENOME_PATH}/roary/gene_presence_absence.csv"
    shell:
        '''
        mkdir -p {PANGENOME_PATH}/gffs
        cp {ISOLATE_GFF} {PANGENOME_PATH}/gffs
        for gff in {input.gffs}; do
            cp $gff {PANGENOME_PATH}/gffs
        done
        source {CONDA_PATH}
        conda activate {ENVS}/roary
        roary -e --mafft -p 8 -f {PANGENOME_PATH}/roary {PANGENOME_PATH}/gffs/*.gff
        conda deactivate
        '''