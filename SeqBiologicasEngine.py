from DB import DB
from Bio import SeqIO
from MySeq import MySeq
import Messages as Messages
import re
from AlignSeq import AlignSeq
from SubstMatrix import SubstMatrix
from UPGMA import UPGMA
from MultipleAlign import MultipleAlign
from Bio import Entrez
from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML
from ExternalMAlign import ExternalMAlign
from ExternalTree import ExternalTree

class SeqBiologicasEngine:

    SEPARATOR = "---"

    def __init__(self):
        self.db = DB()

    def getDB(self):
        return self.db

    def add_seq(self, id, seq, properties=[]):
        manual_seq = MySeq(seq)
        manual_seq.setId(id)
        
        if manual_seq.valid == False:
            print (Messages.seq_erro())
            return

        for i, elem in enumerate(properties):
            if i == 0:
                manual_seq.setClass(elem)
            elif i == 1:
                manual_seq.setSpecie(elem)
            elif i == 2:
                manual_seq.setCode_protein(elem)
            elif i == 3:
                manual_seq.setID_swiss(elem)
            elif i == 4:
                manual_seq.setID_NCBI(elem)
        
        if not self.db.setSeq(manual_seq, manual_seq.getId()):
            print(Messages.double_id())

        print (Messages.seq_added())

    def import_seqfasta(self, filename):
        try:
            fasta_sequences = SeqIO.parse(open(filename), 'fasta')
            for fasta in fasta_sequences:
                id = fasta.id
                sequence = str(fasta.seq)

                seq = MySeq(sequence)
                seq.setId(id)

                if seq.valid() and self.db.setSeq(seq,id):
                    print (Messages.seq_added())
                else:
                    print (Messages.seq_error())

        except:
            print (Messages.invalid_file())
    
    def import_seqtext(self, filename):
        try:
            ficheiro = open(filename, 'r')
            lines = ficheiro.readlines()

            for line in lines:
                sequence_data = "".join(line).replace("\n", "")
                sequence_data_list = sequence_data.split(self.SEPARATOR)

                if not len(sequence_data_list) >= 2:
                    print(Messages.seq_error())
                    return
                    
                id = sequence_data_list[0].strip()
                sequence = sequence_data_list[1].strip()

                seq = MySeq(sequence)
                seq.setId(id)

                sequence_properties = sequence_data_list[2:len(sequence_data_list)]

                for i, prop in enumerate(sequence_properties):
                    if i == 0: # class
                        seq.setClass(prop)
                    if i == 1: # specie
                        seq.setSpecie(prop)
                    if i == 2: # code protein
                        seq.setCode_protein(prop)
                    if i == 3: # id swiss
                        seq.setID_swiss(prop)
                    if i == 4: # id ncbi
                        seq.setID_NCBI(prop)

                if seq.valid() and self.db.setSeq(seq,id):
                    print (Messages.seq_added())
                else:
                    print (Messages.seq_error())
        
        except:
            print (Messages.invalid_file())

    def SaveSeqs(self, filename, withProperties = False):
        dic = self.db.getDB()

        try:
            with open(filename, "w") as file:
                for i in dic:
                    mySeq = dic[i]

                    line = f"{mySeq.getId()}{self.SEPARATOR}{mySeq.getSeq()}"

                    if withProperties == False :
                        line += f"{self.SEPARATOR}{mySeq.getClass()}{self.SEPARATOR}{mySeq.getEspecie()}{self.SEPARATOR}{mySeq.getCode_protein()}{self.SEPARATOR}{mySeq.getID_NCBI()}{self.SEPARATOR}{mySeq.getID_swiss()}"

                    line += "\n"
                    file.writelines(line)
            
            print(Messages.file_generated())
        except:
            print(Messages.file_notgenerated())

    def alignment(self, seq):         
         seq_alin = MySeq(seq)

         if not seq_alin.valid():
             print(Messages.invalid_sequence())
             return

         #values for alignment:
         match = int(input("Match value: "))
         mismatch = int(input("Mismatch value: "))          
         gap = int(input("Spacing value: "))
         
         # matrices definition:
         sm = SubstMatrix()
         sm.createFromMatchPars(match, mismatch, "ACGT")
         alin = AlignSeq(sm , gap)

         #alignment
         sc = 0
         seq_out = 0
         for sqs in self.db.getSeqs():
            score = alin.needlemanWunsch(seq_alin, sqs)
            if score > sc:
               sc = score
               seq_out = sqs.getId()

         print ((sc, seq_out))
   
    def frequency(self, id_seq):
       countA = 0
       countC = 0
       countG = 0
       countT = 0
       seq = self.db.getSeq(id_seq)
       seq1 = seq.getSeq()
       for i in range(len(seq1)):
          if seq1[i] == "A":
             countA += 1
          elif seq1[i] == "G":
             countG += 1
          elif seq1[i] == "C":
             countC += 1
          elif seq1[i] == "T":
             countT += 1
       return countA, countC, countG, countT
    
    def frequency_subseq(self, sub_seq, id_seq):
       res = self.match_pattern(sub_seq, id_seq)
       return len(res)
       
    def match_pattern(self, pattern, id_seq):  
       seq = self.db.getSeq(id_seq) #memory of the sequence in MySeq 
       rgx = re.compile(pattern.upper())
       return rgx.findall(seq.getSeq())
    
    def tree(self, lis_seqs):
          seqs = []
          for ids in lis_seqs:
             seqs.append(self.db.getSeq(ids))
          print(seqs)
          sm = SubstMatrix()
          sm.createFromMatchPars(3,-1, "ACGT")
          alseq = AlignSeq(sm,-8)
          up = UPGMA(seqs, alseq)
          arv = up.run()
          arv.printtree()
    
    def alinMultiple(self, list_seqs):
       seqs = []
       for ids in list_seqs:
          seqs.append(self.db.getSeq(ids))
       
       print(seqs)
       sm = SubstMatrix()
       sm.createFromMatchPars(1,-1,"ACGT")
       alseq = AlignSeq(sm,-1)
       ma = MultipleAlign(seqs, alseq)
       al = ma.alignConsensus()
       print(al)
    
    def translation(self, id_seq):
       seq = self.db.getSeq(id_seq)
       res = seq.find_all_orfs_all_rf()
       return res
    
    def exportOrfs(self, id_seq, orfs):
       try:
            with open("Orfs.txt", "a") as file:
               line =  f"\n{id_seq}{self.SEPARATOR}"
               for orf in orfs:
                  line += f"{orf} - "
               file.write(line)
       except:
            print (Messages.invalid_file())
    
    def print_seq(self, seqId):
        seq = self.db.getSeq(seqId)

        if seq != None:
            print("\n--- Sequence data ---\n")
            print("Sequence ID: " + seq.getId())
            print("Sequences: " + seq.getSeq())
            print("Classes: " + seq.getClass())
            print("Species: " + seq.getSpecie())
            print("Protein code: " + seq.getCode_protein())
            print("NCBI ID: " + seq.getID_NCBI())
            print("SwissProt ID: " + seq.getID_swiss())

        else:
            print(Messages.nonexistent_sequence())
    
    def prinDB(self):
        return self.db.getDB()
    
    def printSeqs(self):
       for sqs in self.db.getSeqs():
          print(sqs)
   
    def get_NCBI_seq(self, id_NCBI):
        Entrez.email = "user@email.com"
        identifier = id_NCBI.split("_")

        identifiers_list = ["AC", "NC", "NG", "NT", "NW", "NZ"]
        if identifier[0] not in identifiers_list:
            print (Messages.sequence_notimported())
            return

        try:
            handle_seq = Entrez.efetch(db = "nucleotide", id = id_NCBI, rettype = "fasta", retmode = "text")
            seq_record = SeqIO.read(handle_seq, "fasta")

            seq2 = MySeq(seq_record.seq)
            seq2.setId(id_NCBI)
            if seq2.valida() == False:
                print (Messages.invalid_sequence())
            else:
                self.db.setSeq(seq2, id)
        except:
            print (Messages.sequence_notimported())

    def execute_blast(self, id_seq, limit, evalue):
        seq = self.db.getSeq(id_seq)

        if seq == None:
            print(Messages.nonexistent_sequence())
            return

        blast_result = NCBIWWW.qblast("blastn","nr", seq.getSeq(), hitlist_size= limit)

        file_blast = open(".blast_result.xml", "w")
        file_blast.write(blast_result.read())
        file_blast.close()

        file_blast=open(".blast_result.xml")
        blast_record = NCBIXML.read(file_blast)
        file_blast.close()

        for alignment in blast_record.alignments:
            for hsps in alignment.hsps:
                if hsps.expect < evalue:
                    print(f"sequence: {alignment.title}")
                    print(f"accession: {alignment.accession}")
                    print(f"length: {alignment.length}")
                    print(f"e value: {hsps.expect}")
                    print(f"score: {hsps.score}")
                    print(f"identities: {hsps.identities}")
                else:
                    print("Inferior to the provided evalue!")

    def execute_mult_alignW(self, filename, path):
        al = ExternalMAlign(filename)
        filename2 = filename.split('.')
        al.clustalW(path)
        al.printAlign(f"{filename2[0]}.aln")

    def execute_external_tree(self, filename):
        t = ExternalTree(filename) 
        tree = t.createTree()

        print(tree)
