# SWIGG - SWIft Genomes in a Graph

A pipeline for making SWIft Genomes in a Graph (SWIGG) using k-mers. We follow a multiscale approach to build genome graphs in a hierarchial way.

<img src="documentation/images/hiv_graph.jpg" align="left" height="150" width="150" ></a>
<br/><br/><br/><br/><br/><br/>

## Abstract
An automated pipeline to build graphs quick using kmer approach.
There are several sequences across human genome, viruses and also among other species that are known to have **conserved** and **variable** regions. These regions of are interest to the scientific community because of its dynamic characteristics. We want to be able to build graphs using alternative references that are representative of sequence of interest and also **fast**.

Building graphs for genomes, or large genomic regions is computationally very expensive and so we can use a multi-scale approach to build genome graphs in an hierarchial way. The idea is to create a sparse representation for multiple sequence alignment so we can visualize large scale difference such as stuctural variants in a succinct way. By representing a genome with graphs, we can create an anchor graph, which can then be further iteratively improved to include local sequence differences and possibly help us with genotyping and identifying true variants.

_**SWIGG**_ is a fast an efficient tool that can do this. The following is a graph created using SWIGG in less than three minutes that use 128-mers and builds on seven alternative references of MHC region (4.5Mb in size)

![mhc graph](documentation/images/mhc_graph.jpg)
<br/>
Fig: Genome graph built using 128-mers and seven alternative contigs of MHC gene

## Objective 

The primary objective is to build an open-source platorm tool that builds a genome graph by eluding the use of massive amounts of compute and/or advanced algorithms.

We can construct graph genomes of a small portion of the genome that can still lead to interesting insights and can be built, rendered, and analyzed using **memory and compute power equivalent to that of a local-CPU.**  We also want to be able to use **publicly accessible, easy-to-obtain data.**

## Getting Started
Follow the simple three step process to build and visualize amazing graphs
### Download Test Data
For test data, we will download and process seven alternative contigs of MHC sequences available from the GRCh38 genome.
- Add Reference of dataset download
### Requirements
- Python 3.7

### Build Graphs
- Alternatively, the following docker image and CWLTool can be used
Running command (CWL, Docker Image, etc.)

## Methods
![QuickGG_Workflow](documentation/images/quickgg_flowchard.png)

### Initial Algorithm Idea: K-mers

![K-mer graph_concept](documentation/images/kmer_graph.png)

### Graph Rendering

We used Gephi to visualize this graph. We use the ??? settings, which optimizes graphs like this for human vi,Here are some examples below (MHC region subsampled, HIV)

## Future Direction

1. Many k-mers happen to be adjacent to each other, which actually is just one large k-mer. We would like to merge these small k-mers to a merge larger k-mers.
2. We would also like to further improve the graph by iterating over local sequences
3. 

### Graph Rendering



## Other Graphs constructed
This work can then be extrapolated to 

![mhc graph2](documentation/images/mhc_2.jpg)
</br> 

![hiv graph](documentation/images/hiv_graph.jpg)
</br> 

### Understanding new sequences from the model.

We would like to be able to use this graph model to be able to analyze a new sequence, and understand where it's structural variation occurs (ie which "path" on the graph it follows"). 
