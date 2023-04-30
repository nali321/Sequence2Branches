#need contigs.fa
OUTPUT = config["output"]
ENVS = config["envs_path"]
CONDA_PATH = config["conda_path"]
TREE = config["tree_type"]
TEXT_FILES = config["gtotree_text"]
H_FLAG = config["h_flag"]

rule gtotree:
    input:
        fasta=f"{TEXT_FILES}/fasta_files.txt",
        map=f"{TEXT_FILES}/map_id.txt"
    output:
        tre=f"{OUTPUT}/{TREE}_tree/{TREE}_tree.tre"
    shell:
        '''
        cp {OUTPUT}/spades/contigs.fasta {OUTPUT}/accessions/contigs.fa
        source {CONDA_PATH}
        conda activate {ENVS}/gtotree
        cd {OUTPUT}/accessions
        GToTree -f {input.fasta} -H {H_FLAG} -t -L Species,Strain -m {input.map} -F -T IQ-TREE -j 16 -o {OUTPUT}/{TREE}_tree
        conda deactivate
        '''