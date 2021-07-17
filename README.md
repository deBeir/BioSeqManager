# BioSeqManager

## ABOUT

A simple program that allows the user to keep, manage and manipulate a set of DNA sequences, as well as to keep the properties and identifiers of the organisms represented by their respective sequences. These properties are saved inside a simple database.


## PREREQUESITES 

In order to properly execute some functionalities of this sequence manager, it is necessary to install the *__Biopython__* package. 

`pip install biopython`

It is also required to install __Clustal W/Clustal X__ so that the multiple alignments can be executed. You can *download* it [here](http://www.clustal.org/download/current/).

## FUNCTIONALITIES

For this project, 15 classes were developed:

  - SeqBiologicasShell
  - SeqBiologicasEngine
  - BD
  - ExternalMAlign
  - ExternalTree
  - Messages
  - AlignSeq
  - BinaryTree
  - ClustHier
  - MatrixNum
  - MyAlign
  - MySeq
  - SubsMatrix
  - UPGMA
  - MultipleAlign


#### *SeqBiologicasShell* MODULE
The class *SeqBiologicasShell* allows the generation of an *interface* so that the user is capable of manipulating biological sequences. Inside of this command shell, the user can resort to the following functionalities:

- *__addseq__*: manually adds sequences to the database.
- *__addseq_fasta__*: adds sequences from a *FASTA* file.
- *__addseq_text__*: adds sequences from a text file.
- *__export_seqs__*: exports sequences saved in a text file.
- *__multiple_align__*: multiple alignment of sequences.
- *__frequency__*: calculates the frequency of a symbol or a subsequence of size *k*.
- *__pattern__*: searches for a pattern in one or more sequences.
- *__seqs_db__*: shows the content of the database.
- *__tree__*: allows the visualisation of phylogenetic trees of sequences.
- *__similar__*: searches for the most similar saved sequence (to the one given by the user).
- *__translation__*: searches for the translation of proteins of all *reading frames* starting from the selected sequences.
- *__help__*: help command.
- *__blast__*: blast of a sequence against the ones in the database.
- *__info__*: shows detailed information of a sequence.
- *__addseq_NCBI__*: adds sequences retrieved from NCBI.
- *__multiple_alignW__*: multiple alignment resorting to *Clustal W*.
- *__treeW__*: generates a phylogenetic tree resorting to files coming from *Clustal W* multiple alignments.
- *__exit__*: exits the shell.

After its selection, the command is processed and the corresponding method is called. These methods allow the addition and management of the information extracted from the *input(s)*. For these methods to properly work, it is mandatory to *import* the *SeqBiologicasEngine* module. 

#### *SeqBiologicasEngine* MODULE
The *SeqBiologicaEngine* class contains all of the methods that ultimately allow the processing and management of the database (*BD*).

- *__getDB__*: returns the database (dictionary of sequences).
- *__add_seq__*: allows the manual insertion of sequences to the database (unless the sequence is already in there).
- *__import_seqfasta__*: processes a *FASTA* file and inserts the sequence in the database (unless the sequence is already in there).
- *__import_seqtext__*: processes a "*.txt*" file and inserts the sequence in the database (unless the sequence is already in there).
- *__SaveSeqs__*: saves sequences in a text file.
- *__alignment__*: performs alignment of a sequence against the ones already in the database returning the alignment with the highest score (sequence more homologous to the input sequence one).
- *__frequency__*: counts the frequency of the bases of a given sequence.
- *__frequency_subseq__*: finds all the occurrences of a specific subsequence in a given sequence.
- *__match_pattern__*: finds all the occurrences of a specific pattern in a given sequence.
- *__tree__*: generates a phylogenetic tree for the sequences.
- *__alingMultiple__*: performs multiples alignment of sequences kept in the database.
- *__translation__*: searches the translation of proteins from all *reading frames* (ORFs) from the selected sequence.
- *__exportOrfs__*: saves the ORFs in a "*.txt*" file.
- *__print_seq__*: given a certain sequence ID, if it is already in the database, returns all the information kept about it.
- *__printDB__*: returns all the content kept in the database.
- *__printSeqs__*: prints all sequences inside of the database.
- *__get_NCBI_seq__*: resorts to Entrez in order to retrieve DNA sequences from NCBI. 
- *__execute_blast__*: performs *blastn* given certain parameters like the *e-value*.
- *__execute_multiple_alignW__*: performs multiple alignments resorting to *Clustal W*.
- *__execute_external_tree__*: given the output file generated during the multiple alignment with *Clustal W*, returns a phylogenetic tree with all the sequences present in the file.

#### *BD* MODULE
This class was specifically developed to store all of the sequences' information (as a dictionary) inside of a database (another dictionary).
