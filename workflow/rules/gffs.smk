OUTPUT = config["output"]

rule move_gffs:
    input:
        gffs=f"{PANGENOME_PATH}/prokka/{{sample}}/{{sample}}.gff"
    output:
        gffs_folder=f"{PANGENOME_PATH}/gffs/{{sample}}.gff"
    shell:
        '''
        mkdir -p {PANGENOME_PATH}/gffs
        cp {input.gffs} {output.gffs_folder}
        '''

rule move_isolate_gff:
    input:
        isolate=f"{OUTPUT}/isolate_prokka/genome_isolate.gff"
    output:
        moved=f"{PANGENOME_PATH}/gffs"
    shell:
        '''
        mkdir -p {PANGENOME_PATH}/gffs
        cp {input.isolate} {output.moved}
        '''