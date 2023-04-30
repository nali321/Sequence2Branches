OUTPUT = config["output"]
ENVS = config["envs_path"]
CONDA_PATH = config["conda_path"]

rule prokka:
    input:
        assembly=f"{OUTPUT}/spades/contigs.fasta"
    output:
        gff=f"{OUTPUT}/isolate_prokka/genome_isolate.gff"
    shell:
        '''
        source {CONDA_PATH}
        conda activate {ENVS}/prokka
        prokka --centre X --force --locustag isolate --outdir {OUTPUT}/prokka --prefix genome_isolate --gffver 3 --cpus 8 {input.assembly}
        conda deactivate
        '''