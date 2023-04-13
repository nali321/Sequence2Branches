OUTPUT = config["output"]
ENVS = config["envs_path"]
CONDA_PATH = config["conda_path"]

rule spades:
    input:
        one=f"{OUTPUT}/trimmed/forward_paired.fq.gz",
        two=f"{OUTPUT}/trimmed/reverse_paired.fq.gz",
        s=f"{OUTPUT}/trimmed/forward_unpaired.fq.gz"
    output:
        assembly=f"{OUTPUT}/spades/contigs.fasta"
    shell:
        '''
        source {CONDA_PATH}
        conda activate {ENVS}/spades
        spades.py -o {OUTPUT}/spades -1 {input.one} -2 {input.two} -s {input.s} -m 128 -k 33,55,77,99 --careful -t 16
        conda deactivate
        '''