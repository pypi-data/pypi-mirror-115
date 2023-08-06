
def cigar_splitter(cigar):

    # get the position of letters
    letter_pos_list = []
    n = 0
    for each_element in cigar:
        if (each_element.isalpha() is True) or (each_element == '='):
            letter_pos_list.append(n)
        n += 1

    # split cigar
    index = 0
    cigar_splitted = []
    while index <= len(letter_pos_list) - 1:
        if index == 0:
            cigar_splitted.append(cigar[:(letter_pos_list[index] + 1)])
        else:
            cigar_splitted.append(cigar[(letter_pos_list[index - 1] + 1):(letter_pos_list[index] + 1)])
        index += 1

    return cigar_splitted


def get_cigar_stats(cigar_splitted):

    # aligned_len: M I X =
    # clipping_len: S
    # mismatch_len: X I D
    # mismatch_pct = mismatch_len / aligned_len
    # aligned_pct  = aligned_len  / (aligned_len + clipping_len)
    # clipping_pct = clipping_len / (aligned_len + clipping_len)

    aligned_len = 0
    clipping_len = 0
    mismatch_len = 0
    for each_part in cigar_splitted:
        each_part_len = int(each_part[:-1])
        each_part_cate = each_part[-1]

        # get aligned_len
        if each_part_cate in {'M', 'm', 'I', 'i', 'X', 'x', '='}:
            aligned_len += each_part_len

        # get clipping_len
        if each_part_cate in ['S', 's']:
            clipping_len += each_part_len

        # get mismatch_len
        if each_part_cate in {'I', 'i', 'X', 'x', 'D', 'd'}:
            mismatch_len += each_part_len

    aligned_pct  = float("{0:.2f}".format(aligned_len * 100 / (aligned_len + clipping_len)))
    clipping_pct = float("{0:.2f}".format(clipping_len * 100 / (aligned_len + clipping_len)))
    mismatch_pct = float("{0:.2f}".format(mismatch_len * 100 / (aligned_len)))

    return aligned_len, aligned_pct, clipping_len, clipping_pct, mismatch_pct


def check_both_ends_clipping(cigar_splitted):

    both_ends_clipping = False
    if len(cigar_splitted) >= 3:
        if (cigar_splitted[0][-1] in ['S', 's']) and (cigar_splitted[-1][-1] in ['S', 's']):
            both_ends_clipping = True

    return both_ends_clipping


def remove_high_mismatch(sam_in, aln_len_cutoff, mismatch_cutoff, sam_out):

    sam_out_handle = open(sam_out, 'w')
    ref_len_dict = {}
    for each_read in open(sam_in):
        each_read_split = each_read.strip().split('\t')
        if each_read.startswith('@'):
            sam_out_handle.write(each_read)

            marker_id = ''
            marker_len = 0
            for each_element in each_read_split:
                if each_element.startswith('SN:'):
                    marker_id = each_element[3:]
                if each_element.startswith('LN:'):
                    marker_len = int(each_element[3:])
            ref_len_dict[marker_id] = marker_len

        else:
            ref_id = each_read_split[2]
            ref_pos = int(each_read_split[3])
            cigar = each_read_split[5]
            if cigar == '*':
                sam_out_handle.write(each_read)
            else:
                cigar_splitted = cigar_splitter(cigar)
                both_ends_clp = check_both_ends_clipping(cigar_splitted)
                if both_ends_clp is False:
                    r1_aligned_len, r1_aligned_pct, r1_clipping_len, r1_clipping_pct, r1_mismatch_pct = get_cigar_stats(cigar_splitted)
                    if r1_mismatch_pct <= mismatch_cutoff:

                        if r1_aligned_len >= aln_len_cutoff:

                            # check if clp in middle
                            if ('S' not in cigar) and ('s' not in cigar):
                                sam_out_handle.write(each_read)
                            else:
                                clip_in_middle = True
                                if (cigar_splitted[0][-1] in ['S', 's']) and (ref_pos == 1):
                                    clip_in_middle = False
                                if (cigar_splitted[-1][-1] in ['S', 's']):
                                    if (ref_pos + r1_aligned_len - 1) == ref_len_dict[ref_id]:
                                        clip_in_middle = False

                                if clip_in_middle is False:
                                    sam_out_handle.write(each_read)
    sam_out_handle.close()


def keep_best_matches_in_sam(sam_in, sam_out):
    # get read_to_cigar_dict
    read_to_cigar_dict = {}
    for each_line in open(sam_in):
        each_line_split = each_line.strip().split('\t')
        if not each_line.startswith('@'):
            read_id = each_line_split[0]
            cigar = each_line_split[5]
            if cigar != '*':
                both_ends_clp = check_both_ends_clipping(cigar_splitter(cigar))
                if both_ends_clp is False:
                    if read_id not in read_to_cigar_dict:
                        read_to_cigar_dict[read_id] = {cigar}
                    else:
                        read_to_cigar_dict[read_id].add(cigar)

    # get min_mismatch for each read
    read_min_mismatch_dict = {}
    for each_read in read_to_cigar_dict:
        read_mismatch_set = set()
        for each_cigar in read_to_cigar_dict[each_read]:
            aligned_len, aligned_pct, clipping_len, clipping_pct, mismatch_pct = get_cigar_stats(cigar_splitter(each_cigar))
            read_mismatch_set.add(mismatch_pct)
        read_min_mismatch = min(read_mismatch_set)
        read_min_mismatch_dict[each_read] = read_min_mismatch

    sam_file_best_match_handle = open(sam_out, 'w')
    for each_line in open(sam_in):
        if each_line.startswith('@'):
            sam_file_best_match_handle.write(each_line)
        else:
            each_line_split = each_line.strip().split('\t')
            read_id = each_line_split[0]
            cigar = each_line_split[5]
            if cigar == '*':
                sam_file_best_match_handle.write(each_line)
            else:
                cigar_split = cigar_splitter(cigar)
                both_ends_clp = check_both_ends_clipping(cigar_splitter(cigar))
                if both_ends_clp is False:
                    aligned_len, aligned_pct, clipping_len, clipping_pct, mismatch_pct = get_cigar_stats(cigar_split)
                    if mismatch_pct <= (read_min_mismatch_dict[read_id]):

                        sam_file_best_match_handle.write(each_line)
    sam_file_best_match_handle.close()


bowtie_parameter                    = '--xeq --local --all --no-unal -N 1 -L 30'
pwd_bowtie2_exe                     = 'bowtie2'
pwd_samtools_exe                    = 'samtools'
reads_16s                           = '/srv/scratch/z5039045/MarkerMAG_wd/MBARC26/MBARC26_SILVA138_id99_Matam16S_wd/MBARC26_SILVA138_id99_16S_reads.fasta'
input_16s_qc_no_ext                 = '/srv/scratch/z5039045/MarkerMAG_wd/MBARC26/MBARC26_0727_45_45_min1200_mismatch2_iden99_diff80_MarkerMAG_wd/MBARC26_0727_45_45_min1200_mismatch2_iden99_diff80_rd1_wd/input_16S/MBARC26_SILVA138_polished.QC'
reads_16s_to_16s_sam                = 'reads_16s_to_16s_sam.sam'
reads_16s_to_16s_log                = 'reads_16s_to_16s_sam.log'
reads_16s_to_16s_sam_filtered       = 'reads_16s_to_16s_sam_filtered.sam'
mag_depth_txt                       = '/Users/songweizhi/Desktop/666/MBARC26_refined_bins_50_5_depth.txt'
ref_depth_txt                       = '/Users/songweizhi/Desktop/666/ref_depth.txt'
markermag_op                        = '/Users/songweizhi/Desktop/666/MBARC26_0727_45_45_min1200_mismatch2_iden99_diff80_linkages_by_genome.txt'
ref_16S_id_txt                      = '/Users/songweizhi/Desktop/666/ref_16S_id.txt'
num_threads                         = 12
aln_len_cutoff                      = 70


bowtie_read_to_16s_cmd  = '%s -x %s -U %s -S %s -p %s -f %s 2> %s'          % (pwd_bowtie2_exe, input_16s_qc_no_ext, reads_16s, reads_16s_to_16s_sam, num_threads, bowtie_parameter, reads_16s_to_16s_log)
print(bowtie_read_to_16s_cmd)

reads_16s_to_16s_sam                = '/Users/songweizhi/Desktop/666/reads_16s_to_16s_sam.sam'
reads_16s_to_16s_sam_filtered_mis0  = '/Users/songweizhi/Desktop/666/reads_16s_to_16s_sam_filtered_mis0.sam'
reads_16s_to_16s_sam_filtered_mis1  = '/Users/songweizhi/Desktop/666/reads_16s_to_16s_sam_filtered_mis1.sam'
reads_16s_to_16s_sam_filtered_mis2  = '/Users/songweizhi/Desktop/666/reads_16s_to_16s_sam_filtered_mis2.sam'
# remove_high_mismatch(reads_16s_to_16s_sam, aln_len_cutoff, 0, reads_16s_to_16s_sam_filtered_mis0)
# remove_high_mismatch(reads_16s_to_16s_sam, aln_len_cutoff, 1, reads_16s_to_16s_sam_filtered_mis1)
# remove_high_mismatch(reads_16s_to_16s_sam, aln_len_cutoff, 2, reads_16s_to_16s_sam_filtered_mis2)


reads_to_16s_sam_filtered                   = '/Users/songweizhi/Desktop/666/MBARC26_0727_45_45_min1200_mismatch2_iden99_diff80_input_reads_to_16S_sorted.sam'
reads_to_16s_sam_filtered_mis0              = '/Users/songweizhi/Desktop/666/MBARC26_0727_45_45_min1200_mismatch2_iden99_diff80_input_reads_to_16S_sorted_mis0.sam'
reads_to_16s_sam_filtered_mis0_best_match   = '/Users/songweizhi/Desktop/666/MBARC26_0727_45_45_min1200_mismatch2_iden99_diff80_input_reads_to_16S_sorted_mis0_best_match.sam'
reads_to_16s_sam_filtered_mis1              = '/Users/songweizhi/Desktop/666/MBARC26_0727_45_45_min1200_mismatch2_iden99_diff80_input_reads_to_16S_sorted_mis1.sam'
reads_to_16s_sam_filtered_mis1_best_match   = '/Users/songweizhi/Desktop/666/MBARC26_0727_45_45_min1200_mismatch2_iden99_diff80_input_reads_to_16S_sorted_mis1_best_match.sam'
reads_to_16s_sam_filtered_mis2              = '/Users/songweizhi/Desktop/666/MBARC26_0727_45_45_min1200_mismatch2_iden99_diff80_input_reads_to_16S_sorted_mis2.sam'
reads_to_16s_sam_filtered_mis2_best_match   = '/Users/songweizhi/Desktop/666/MBARC26_0727_45_45_min1200_mismatch2_iden99_diff80_input_reads_to_16S_sorted_mis2_best_match.sam'

# remove_high_mismatch(reads_to_16s_sam_filtered, aln_len_cutoff, 2, reads_to_16s_sam_filtered_mis2)
# keep_best_matches_in_sam(reads_to_16s_sam_filtered_mis2, reads_to_16s_sam_filtered_mis2_best_match)

# remove_high_mismatch(reads_to_16s_sam_filtered, aln_len_cutoff, 0, reads_to_16s_sam_filtered_mis0)
# keep_best_matches_in_sam(reads_to_16s_sam_filtered_mis0, reads_to_16s_sam_filtered_mis0_best_match)

#remove_high_mismatch(reads_to_16s_sam_filtered, aln_len_cutoff, 1, reads_to_16s_sam_filtered_mis1)
#keep_best_matches_in_sam(reads_to_16s_sam_filtered_mis1, reads_to_16s_sam_filtered_mis1_best_match)


ref_to_read_dict = {}
ref_len_dict = {}
read_len_dict = {}
for each_line in open(reads_to_16s_sam_filtered_mis0_best_match):
    each_line_split = each_line.strip().split('\t')
    if each_line.startswith('@'):
        mini_assembly_id = ''
        mini_assembly_len = 0
        for each_element in each_line_split:
            if each_element.startswith('SN:'):
                mini_assembly_id = each_element[3:]
            if each_element.startswith('LN:'):
                mini_assembly_len = int(each_element[3:])
        ref_len_dict[mini_assembly_id] = mini_assembly_len
    else:
        read_id = each_line_split[0]
        ref_id = each_line_split[2]
        read_len = len(each_line_split[9])
        if ref_id not in ref_to_read_dict:
            ref_to_read_dict[ref_id] = {read_id}
        else:
            ref_to_read_dict[ref_id].add(read_id)
        read_len_dict[read_id] = read_len


mag_depth_dict = {}
for each_mag_depth in open(mag_depth_txt):
    if not each_mag_depth.startswith('MAG	Length(bp)	Depth'):
        each_mag_depth_split = each_mag_depth.strip().split('\t')
        mag_depth_dict[each_mag_depth_split[0]] = float(each_mag_depth_split[2])

ref_depth_dict = {}
for each_ref_depth in open(ref_depth_txt):
    each_ref_depth_split = each_ref_depth.strip().split('\t')
    ref_id = each_ref_depth_split[0].split('_')[0]
    ref_depth = float(each_ref_depth_split[1])
    ref_depth_dict[ref_id] = ref_depth


gnm_to_linked_16s_dict = {}
for each_linkage in open(markermag_op):
    each_linkage_split = each_linkage.strip().split('\t')
    if not each_linkage.startswith('MarkerGene	GenomicSeq	Linkage	Round'):
        id_16s = each_linkage_split[0]
        id_gnm = each_linkage_split[1]
        if id_gnm not in gnm_to_linked_16s_dict:
            gnm_to_linked_16s_dict[id_gnm] = {id_16s}
        else:
            gnm_to_linked_16s_dict[id_gnm].add(id_16s)


ref_to_16s_dict = {}
for each_line in open(ref_16S_id_txt):
    gnm_id = each_line.strip().split('_')[0]
    if gnm_id not in ref_to_16s_dict:
        ref_to_16s_dict[gnm_id] = {each_line.strip()}
    else:
        ref_to_16s_dict[gnm_id].add(each_line.strip())


print('Genome\tMAG\tREF\tmag_16s_depth\tref_16s_depth\tmag_depth\tref_depth')
mag_16s_depth_dict = {}
for each_mag in gnm_to_linked_16s_dict:
    linked_16s_set = gnm_to_linked_16s_dict[each_mag]
    linked_16s_len_list = [ref_len_dict[s16] for s16 in linked_16s_set]
    linked_16s_mean_len = sum(linked_16s_len_list)/len(linked_16s_len_list)
    current_mag_linked_16s_read_set = set()
    for each_linked_16s in linked_16s_set:
        current_16s_mapped_reads = ref_to_read_dict.get(each_linked_16s, [])
        for i in current_16s_mapped_reads:
            current_mag_linked_16s_read_set.add(i)

    current_mag_linked_16s_total_len = 0
    for read_len_id in current_mag_linked_16s_read_set:
        current_mag_linked_16s_total_len += read_len_dict[read_len_id]

    ref_depth = ref_depth_dict[each_mag]
    ref_16s_copy_num = len(ref_to_16s_dict[each_mag])
    ref_16s_depth = ref_depth * ref_16s_copy_num
    ref_16s_depth = float("{0:.2f}".format(ref_16s_depth))

    mag_16s_depth = current_mag_linked_16s_total_len / linked_16s_mean_len
    mag_16s_depth = float("{0:.2f}".format(mag_16s_depth))
    mag_16s_depth_dict[each_mag] = mag_16s_depth
    mag_depth = mag_depth_dict[each_mag]
    copy_num = mag_16s_depth / mag_depth
    copy_num = float("{0:.2f}".format(copy_num))

    print('%s\t%s\t%s\t%s\t%s\t%s\t%s' % (each_mag, copy_num, ref_16s_copy_num, mag_16s_depth, ref_16s_depth, mag_depth, ref_depth))




'''
module unload python
module load python/3.7.3
source ~/mypython3env/bin/activate
module unload R
module load R/4.0.2
module load blast+/2.11.0
module load bowtie/2.3.5.1
module load samtools/1.10
module load spades/3.14.0
module load gcc/8.4.0
module load boost/1.73.0-gcc8   
module load mira/v5rc2
module load java/8u201-jdk
module load seqtk/20190219
module load mafft/7.407
module load perl/5.28.0
module load hmmer/3.2.1
module load bedtools/2.27.1
module load barrnap/0.9

cd /srv/scratch/z5039045/MarkerMAG_wd/MBARC26/MBARC26_0727_45_45_min1200_mismatch2_iden99_diff80_MarkerMAG_wd/reads_16s_to_16s_sam
bowtie2 -x /srv/scratch/z5039045/MarkerMAG_wd/MBARC26/MBARC26_0727_45_45_min1200_mismatch2_iden99_diff80_MarkerMAG_wd/MBARC26_0727_45_45_min1200_mismatch2_iden99_diff80_rd1_wd/input_16S/MBARC26_SILVA138_polished.QC -U /srv/scratch/z5039045/MarkerMAG_wd/MBARC26/MBARC26_SILVA138_id99_Matam16S_wd/MBARC26_SILVA138_id99_16S_reads.fasta -S reads_16s_to_16s_sam.sam -p 12 -f --xeq --local --all --no-unal -N 1 -L 30 2> reads_16s_to_16s_sam.log



'''