# Introduction

Mutation load tool can be used to permutate VCF files for given BAM file with the same amount and similar mutations as in the corresponding VCF file, depending on the given permutation options. In addition, it can be used to plot CDF function for read depths.

# Before you use the tool

Before you can use Mutation load tool, you need to specify path to SAMtools in mutation_load_config.ini file. In addition, if you want to use BED file(s) to limit BAM region, you need to specify the location of BEDtools in the same file.

After modifying the configuration file, you should run the program with command

```python3 --bam "<file1.bam> <file2.bam> <file3.bam>" --get_id_only```.

The program should give different name for each BAM file, so in the real run it can give different names to files corresponding to different BAM files. By default, Mutation load tool creates the name by taking 10 first characters from the original file name, but this can be modified with ```--name_start_index``` and ```--name_end_index``` options. Another way is to use ```--regex_sampleid``` and modify regex_patterns.py so that it returns wanted sample ids. This should again be tested with ```--get_id_only``` option.

Also, when running the tool with permutation or CDF mode, you need to provide reference fasta file (like Homo_sapiens.GRCh38.dna.primary_assembly.fa) for SAMtools with ```--reference``` argument.

# Filtering BAM files

Program uses SAMtools to read BAM files and keep count on genomic positions to which it can later permutate mutations. In addition, CDF plot is made based on the output of SAMtools. By default, there are no bitflags filtered, but you can use basic SAMtools filtering by giving bits with ```-f 4 -F 8```. If you have other SAMtools arguments you want to use, you can give them with ```--other "-q 10 -m 3"```.

In addition, you can use BED files with ```-L "file1.bed file2.bed"```, and flank them (increase the area) with for example ```--flank_downstream 5 --flank_upstream 10```.

Both SAMtools filtering and BED files can be used to limit the CDF area as well as permutation. However, one can also limit permutation regions with read depth limits. If one gives ```--depth_lim 20```, mutations can be permutated from only those genomic positions that have read depth 20 or more. In addition, mutations in original VCF that are located in positions that have read depth under the limit are ignored, unless ```--no_vcf_filter``` is given. Similarly ```--rev_limit``` and ```--for_limit``` can be used to limit permutation regions based on forward and reverse strand read depths.


# Permutation

## Mandatory options

To permutate VCF files, you need to give BAM file(s) with --bam "file1.bam file2.bam", as well as VCF file(s) with --vcf_file "file1.vcf file2.vcf". Order of the given files is important, since for example the first BAM file is paired with the first VCF file, the second BAM file with the second VCF file and so on. Instead of using --bam, you can also get all BAM files from certain directory with --directory "path/to/dir/". However, then you need to give VCF files in the same order as BAM files are found with os.walk("path/to/dir/", topdown=True).

Other mandatory argument is --destination "path/to/destination_dir". Folder named mutation_load_tool is made to the given destination folder, if one does not yet exist. All files and directories, temporal as well as permanent, made by Mutation load tool, are created to that directory. In addition, when you run the permutation, you need to specify table_annovar.pl with --table_annovar and ANNOVAR folder with --annovar.

## Other important options

In addition, one should give --perm_amount argument to define, how many permutated VCF files she wants to create per BAM-VCF-pair. Default is 100.

One can also choose what kind of mutations are permutated and skipped. For example with argument ```--skip_nonexon``` all non exonic regions are skipped in the original VCF, and only exonic mutations are permutated. This can also be used without ```--separate_regions``` option, which makes sure, that program permutates the same amount of mutations from the same regions as in the original VCF. If one wants to permutate similar amount of synonymous, nonsynonymous and other type of mutations as in the original VCF, instead of permutating just the same amount of mutations, one can give ```--separate_syn``` argument. This cannot be used if ```--separate_regions``` is not given.

## Example

One could run mutation_load.py with permutation for example using command

```python3 mutation_load.py --bam "file1.bam file2.bam" --vcf_file "file1.vcf file2.vcf" --destination "path/to/destination_dir" --table_annovar /path/to/table_annovar.pl --annovar /path/to/humandb_060418```.

This would create 100 permutated VCF files for both file1.bam and file2.bam, that have the same amount of SNV and indel mutations as in the original corresponding VCF files. With command

```python3 mutation_load.py --bam "file1.bam file2.bam" --vcf_file "file1.vcf file2.vcf" --destination "path/to/destination_dir" --table_annovar /path/to/table_annovar.pl --annovar /path/to/humandb_060418 --separate_regions --separate_syn```

there would again be same amount of SNV and indel mutations in the permutated VCF files, but in addition, the amount of for example splice site and intronic as well as nonsynonymous and synonymous exonic mutations would be same as in the original corresponding VCF files.

## Continue permutation

If program crashed during permutation, or you want to permutate more VCF files and you still have temporal generated VCF files, you can continue the permutation with ```--continue```. In addition, you need to give the location of the generated VCF files (the path of mutation_load_tool folder) with ```--gen_vcf_location``` and previous report with ```--report```. In addition, you need to give all the usual permutation options.
 
# CDF plot of the read depths

One can also use the program to plot CDF of read depths of the given BAM files with ```--plot_cdf``` option. You can skip all other steps with options ```--skip_permutation``` and ```--no_vcf_generate```. Thus, the command to plot read depth CDF plots would be

```python3 mutation_load.py --bam "file1.bam file2.bam" --destination "path/to/destination_dir" --table_annovar /path/to/table_annovar.pl --annovar /path/to/humandb_060418 --plot_cdf --skip_permutation --no_vcf_generate```.

If you only give 1 BAM file, the plot would be like in Figure 1. If you give more than 1 BAM file, the plot would be like in Figure 2.

# Running parallel runs to the same destination

Permutation takes time, but you can run parallel runs to the same destination with different BAM-VCF-pairs. However, you should then give ```--keep_temp_files```, because otherwise the program deletes all the temporan directories after one run has finished, and all the files from other files are deleted.

# Different options

```
-h, --help                                  Show this help message and exit.

Input options (Define your input files and directories.):
    -b BAM, --bam=BAM                       Bam file(s) that will be used in permutation or plot.

    --vcf_file=VCF_FILE                     VCF file(s) for permutation given in the same order as the 
                                            corresponding bam files.

    -d DIRECTORY, --directory=DIRECTORY     If you want the program to run through all bam files in a 
                                            certain directory.

Output options (Define output directory and if you want to keep all temporal files for debugging.):

    --destination=DESTINATION               Destination for cdf file, report, permutations etc.
    
    --plot_cdf                              If you do not want CDF plot of read depths. Then you also need R packages
                                            ggplot2, dplyr, RColorBrewer and scales. Default: False.
    
    --lbuffer=LBUFFER                       Maximum number of lines per generated vcf_file to save memory. Default is
                                            821600, which takes 3G memory with ANNOVAR.

    --no_vcf_generate                       If you do not want to generate VCF with all possible mutations.
                                            They are needed in permutation. Default: False.

    --keep_temp_files                       If you want to keep temporal anno files, generated VCF and temporal 
                                            mutation files for debugging. Set True, if you have parallel runs to 
                                            the same destination. Default: False.

Permutation options (With these options you can for example decide which mutations you want to include and 
keep count on permutation):

    --perm_amount=PERM_AMOUNT               How many permutations you want for every bam, default: 100.

    --skip_permutation                      If you do not want permutations.

    --no_vcf_filter                         If you do not want to filter given VCF based on BAM read depths.

    --skip_nonexon                          If you want to skip all non exon mutations in permutation.
                                            Can be used without --separate_regions.

    --separate_regions                      If you want to permutate same amount of mutations in same regions.

    --separate_syn                          If you want same amount of synonymous and nonsynonymous mutations as in input VCF.
                                            Does not work without --separate_regions.

Naming policy (Naming options for files and sample names in coverages plot.):

    --prefix=PREFIX                         Prefix for you files.

    --name_start_index=NAME_START_INDEX     Starting index of BAM file when creating name for plot and permutation files.
                                            Default: 0

    --name_end_index=NAME_END_INDEX         Ending index of BAM file when creating name for plot and permutation files.
                                            Default: 10.

    --get_id_only                           If you want to check how program identifies the sample ids.

    --regex_sampleid                        If you want to use modified regex_patterns.py to find sample ids 
                                            for files. Default: False.

Trimming and samtools options (With these options you can choose reference fasta file and exclude for example reads
with certain bitflags or too little read depth.):

    --depth_lim=DEPTH_LIM                   Minimum depth to reads for coverages  and permutation files, default: 10.

    --rev_limit=REV_LIMIT                   Minimum reverse depth for coverages and permutation files, default: 3.

    --for_limit=FOR_LIMIT                   Minimum forward depth for coverages and permutation files, default: 3.

    --reference=REFERENCE                   Reference fasta file (--reference /path/to/reference).

    -L BED, --bed_file=BED                  If you want to limit area to certain certain region with (a) BED file(s).

    --flank_upstream=FLANK_UPSTREAM         How much you want to expand BED file coordinates to upstream. Default: 0.

    --flank_downstream=FLANK_DOWNSTREAM     How much you want to expand BED file coordinates to downstream.
                                            Default: 0.

    -F IGNORE                               Bit flags you want to ignore.

    -f INCLUDE                              Bit flags you want to be set.

    --headn=HEAD                            If you want to limit area to certain size, write for example
                                            '-headn 10000'.

    --other=OTHER_ARGS                      If you want to use other samtools view -arguments, write for example 
                                            '-- other "-q 10 -m 3"'.

CDF options (With these options you can decide information you want from CDF part):
    
    -p PERCENT_INTERVAL, --percent_interval=PERCENT_INTERVAL
                                            Percent with what distance the CDF-function will be at least printed,
                                            default: 5. For example '-p 5'.

    -r, --reverse                           If you want to count CDF from largest to smallest, type -r. Default:
                                            False.

    -n NUMBER, --number=NUMBER              If you only want to know how many numbers have less reads than given
                                            number (or more when compared to -m).

    -m, --more                              If you want to know how many genomic positions have more reads than given
                                            number.

    -l LIMIT, --limit=LIMIT                 Program writes how many genomic positions have more reads covering site
                                            than given limit. Default: 1.

    --lower                                 If you want to know average of reads below the limit, default is average
                                            of reads exceeding the limit.

ANNOVAR options:
    
    --table_annovar=TABLE_ANNOVAR           Location of table_annovar.pl.

    --annovar=ANNOVAR                       Location of ANNOVAR.

    --buildver=BUILDVER                     Buildver version, default: hg38.

Continue from permutation:

    --continue                              If you want to skip the first part.

    --gen_vcf_location=GEN_VCF_LOCATION     Directory containing generated large VCF files containing all possible
                                            mutations for every genomic position from bam files (recursive,
                                            subdirectories don't matter).

    --report=REPORT                         Original report from earlier run.

Other options:
    --bed_prefix=BED_PREFIX                 Prefix for temporal bed files (for debugging or for parallel runs).                
```
