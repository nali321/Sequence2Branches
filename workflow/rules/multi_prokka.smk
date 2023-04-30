OUTPUT = config["output"]
ENVS = config["envs_path"]
CONDA_PATH = config["conda_path"]

rule multi_prokka:
    input:
        assembly=f"{OUTPUT}/fastas/{{sample}}.fa"
    output:
        gff=f"{OUTPUT}/prokka/{{sample}}/{{sample}}.gff"
    shell:
        '''
        source {CONDA_PATH}
        conda activate {ENVS}/prokka
        prokka --centre X --force --locustag {wildcards.sample} --outdir {OUTPUT}/prokka/{wildcards.sample} --prefix {wildcards.sample} --gffver 3 --cpus 8 {input.assembly}
        conda deactivate
        '''