OUTPUT = config["output"]

rule move_gffs:
    input:
        gffs=f"{OUTPUT}/prokka/{{sample}}/{{sample}}.gff"
    output:
        gffs_folder=f"{OUTPUT}/gffs/{{sample}}.gff"
    shell:
        '''
        mkdir -p {OUTPUT}/gffs
        cp {input.gffs} {output.gffs_folder}
        '''

rule move_isolate_gff:
    input:
        isolate=f"{OUTPUT}/isolate_prokka/genome_isolate.gff"
    output:
        moved=f"{OUTPUT}/gffs/isolate.gff"
    shell:
        '''
        mkdir -p {OUTPUT}/gffs
        cp {input.isolate} {output.moved}
        '''