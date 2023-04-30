OUTPUT = config["output"]
ENVS = config["envs_path"]
CONDA_PATH = config["conda_path"]
GTDBTK_CONDA = config["gtdbtk_conda_path"]
GTDBTK_PATH = config["gtdbtk_path"]

rule gtdbtk:
    input:
        assembly=f"{OUTPUT}/spades/contigs.fasta"
    output:
        args=f"{OUTPUT}/gtdbtk/gtdbtk.bac120.summary.tsv"
    shell:
        '''
        set +eu
        mkdir {OUTPUT}/fna
        cp {input.assembly} {OUTPUT}/fna/contigs.fna
        source {GTDBTK_CONDA}
        conda activate {GTDBTK_PATH}
        gtdbtk classify_wf --genome_dir {OUTPUT}/fna --out_dir {OUTPUT}/gtdbtk --cpus 32
        conda deactivate
        set -eu
        '''