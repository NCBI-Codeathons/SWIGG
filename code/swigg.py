#!/usr/bin/env python3

import argparse

import numpy as np
import pandas as pd

from collections import Counter
from Bio import SeqIO
import networkx as nx

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, \
description="""
swiggy.py

Given a list of fasta sequences, the script will produce an edge list of kmers chosen per various thresholds provided by user through arguments. This edge list is then further processed to create a graph (.gexf) file which can then be further visualized using graph visualizers such as Gephi.
""")

optional = parser._action_groups.pop()
required = parser.add_argument_group('required arguments')

########################################################
# required args:
required.add_argument("-k", "--kmer-length", type=int,
                    help="""required, the length of k-mer that needs to be used'
                    """,
                    required=True)
required.add_argument("-t", "--threshold", type=int,
                    help="required, minimum threshold for kmers to be chosen should be shared by at least these many sequences",
                    required=True)
required.add_argument("-f", "--fasta", nargs="+",
                    help="required, set of all fasta sequences",
                    required=True)
required.add_argument("-rw", "--repeat_threshold_within", type=int,
                    help="required, threshold for filtering kmers that can be used for graph building within the same sequence. If a certain kmer is present within the sequence above the threshold, it will be discarded",
                    required=True)
required.add_argument("-ra", "--repeat_threshold_across", type=int,
                    help="required, threshold for filtering kmers that can be used for graph building across all the sequences we are looking at. If a certain kmer is chosen, but is present more than the threshold mentioned across all sequences, it will be discarded. This is important to reduce repeats and avoid cyclic graphs.",
                    required=True)
required.add_argument("-o", "--out",
                    help='required, path to prefix of output file name. Two files will be created - 1. Edge file ".tsv" and 2. Graph file ".gexf" ',
                    required=True)

########################################################
# optional args:

# optional.add_argument("--reg",
#                     help="optional, .....")

# parser._action_groups.append(optional)
args = parser.parse_args()

########################################################
seq_list = []
for seqq in args.fasta:
    seq_list = seq_list + [(seqq, str(list(SeqIO.parse(seqq, "fasta"))[0].seq))]
seq_df = pd.DataFrame(seq_list).head()
seq_df.columns=['name', 'Sequence']

# Length of k-mers to search for.
k_length = int(args.kmer_length)
# Number of minimum strains that a k-mer must be in to be counted
min_alt_seqs = int(args.threshold)
# Number of minimum strains that a k-mer must be in to be counted.
repeat_threshold_within = args.repeat_threshold_within
# Number of minimum strains that a k-mer must be in to be counted.
repeat_threshold_across = int(args.repeat_threshold_across)

# Read in tables and format to dataframe.
print("Finding all possible kmers...", flush=True)
kmers = [(i_strain, seq[i_base:(i_base+k_length)], i_base) for i_strain,seq in enumerate(seq_df.Sequence.values) for i_base in range(len(seq)-k_length)]
kmers_df = pd.DataFrame(kmers, columns = ['alt_seq', 'kmer',  'pos_start'])
print(str(len(kmers)) + " total possible k-mers of length " + str(k_length), flush=True)


## Note: It's very important for the downstream steps that kmers_df is ordered by (alt_seq, pos_start).  If it is not read in in such a way (ie we end up parallelizing this running on GPUs or something, we will need to do:
# kmers_df = kmers_df.sort_values(['alt_seq', 'pos_start'])
print("Finding conserved & nonrepeating kmers...")
kmers_x_in_sequence_y = zip(kmers_df.kmer, kmers_df.alt_seq)
# Counts of (alt_seq, kmer) combos -- how many times kmer appears in alt_seq).
kmers_x_in_sequence_y_counts = Counter(kmers_x_in_sequence_y)
# How many sequences kmer appears in.
kmers_x_count = Counter([k[0] for k in kmers_x_in_sequence_y_counts.keys()]) 

# Keep kmers that repeat a small number of times (<= repeat_threshold_within) for each sequence.
kmers_unique_in_one_sequence = set([el[0] for el in kmers_x_in_sequence_y_counts.keys() if
                    (kmers_x_in_sequence_y_counts[el] > 0) & (kmers_x_in_sequence_y_counts[el] <= repeat_threshold_within)])

# Dump kmers that are repeat too many times (> repeat_threshold_across) in any single sequence.
kmers_repeat_too_many_times = set([el[0] for el in kmers_unique_in_one_sequence if
                    (kmers_x_in_sequence_y_counts[el] > repeat_threshold_across)])

# Keep kmers that are conserved in >=min_alt_seqs sequences.
kmers_approx_nonrepeat = kmers_unique_in_one_sequence.difference(kmers_repeat_too_many_times)
conserved_seqs = set([el for el in kmers_approx_nonrepeat if kmers_x_count[el] >= min_alt_seqs])
kmers_df_filt = kmers_df[[k in conserved_seqs for k in kmers_df.kmer]]
print(str(len(kmers_df_filt)) + " conserved/nonrepeating kmers.", flush=True)

# Get rid of kmers that are just right next to each other.
print("Getting rid of direct neighbor kmers...")
kmers_df_filt['order'] = range(len(kmers_df_filt))
kmer_grouped_df_expanded = kmers_df_filt[:-1][(kmers_df_filt.pos_start.values[1:]-kmers_df_filt.pos_start.values[:-1]>k_length) &
                                       (kmers_df_filt.alt_seq.values[1:]==kmers_df_filt.alt_seq[:-1])]
kmer_grouped_df_expanded.head()
print(str(len(kmer_grouped_df_expanded)) + " distinct kmers.", flush=True)

# Turn into edge list.
print("Computing edges", flush=True)
edges = dict()
for i in range(1,len(kmer_grouped_df_expanded)):
    if kmer_grouped_df_expanded.iloc[i-1].alt_seq==kmer_grouped_df_expanded.iloc[i].alt_seq:
        edges[(kmer_grouped_df_expanded.iloc[i-1].alt_seq, kmer_grouped_df_expanded.iloc[i-1].pos_start, kmer_grouped_df_expanded.iloc[i-1].kmer,
               kmer_grouped_df_expanded.iloc[i].pos_start, kmer_grouped_df_expanded.iloc[i].kmer)] = 0

# Convert to data frame and compute distance.
edges_df = pd.DataFrame(list(edges))
edges_df.columns = ['alt_seq', 'pos_1', 'kmer_1', 'pos_2', 'kmer_2']
edges_df['distance'] = [pos_2 - ((len(kmer_1)) + pos_1) for kmer_1, pos_1, pos_2 in 
                        zip(edges_df.kmer_1, edges_df.pos_1,edges_df.pos_2)]
edges_df['kmer_1_'] = edges_df['kmer_1']
edges_df['kmer_2_'] = edges_df['kmer_2']
print(str(len(edges)) + " total edges in all sequences.", flush=True)

print("Grouping by kmer1, kmer2 combinations", flush=True)
edges_df_group = edges_df.groupby(['kmer_1_', 'kmer_2_'])
print(str(len(edges_df_group.groups)) + " unique edges.", flush=True)

# Convert to edge list appropriate for csv.
print("Converting to CSV...", flush=True)
kmers_1 = pd.DataFrame(edges_df_group['kmer_1'].apply(lambda x: list(x)[0]))['kmer_1'].values
edges_to_csv=pd.DataFrame(kmers_1)
edges_to_csv.columns = ['kmer_1']
edges_to_csv['kmer_2'] = edges_df_group['kmer_2'].apply(lambda x: list(x)[0]).values
edges_to_csv['distance'] = edges_df_group['distance'].apply(np.mean).values
edges_to_csv.to_csv(args.out+'.tsv', sep="\t", header=None, index_label=None)

# Creating graph file
print("Creating graph file...", flush=True)

G = nx.DiGraph()
with open(args.out+'.tsv') as f:
   for row in f:
       row = row.strip().split()
       G.add_edge(row[1], row[2])
    
nx.write_gexf(G, args.out+'.gexf')

print("Success!", flush=True)
