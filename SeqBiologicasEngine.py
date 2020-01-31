from BD import BD
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
        self.bd = BD()

    def getBD(self):
        return self.bd

    def add_seq(self, id, seq, properties=[]):
        manual_seq = MySeq(seq)
        manual_seq.setId(id)
        
        if manual_seq.valida == False:
            print (Messages.seq_erro())
            return

        for i, elem in enumerate(properties):
            if i == 0:
                manual_seq.setClasse(elem)
            elif i == 1:
                manual_seq.setEspecie(elem)
            elif i == 2:
                manual_seq.setCode_protein(elem)
            elif i == 3:
                manual_seq.setID_swiss(elem)
            elif i == 4:
                manual_seq.setID_NCBI(elem)
        
        if not self.bd.setSeq(manual_seq, manual_seq.getId()):
            print(Messages.id_duplicado())

        print (Messages.seq_adicionada())

    def import_seqfasta(self, filename):
        try:
            fasta_sequences = SeqIO.parse(open(filename), 'fasta')
            for fasta in fasta_sequences:
                id = fasta.id
                sequence = str(fasta.seq)

                seq = MySeq(sequence)
                seq.setId(id)

                if seq.valida() and self.bd.setSeq(seq,id):
                    print (Messages.seq_adicionada())
                else:
                    print (Messages.seq_erro())

        except:
            print (Messages.ficheiro_invalido())
    
    def import_seqtext(self, filename):
        try:
            ficheiro = open(filename, 'r')
            lines = ficheiro.readlines()

            for line in lines:
                sequence_data = "".join(line).replace("\n", "")
                sequence_data_list = sequence_data.split(self.SEPARATOR)

                if not len(sequence_data_list) >= 2:
                    print(Messages.seq_erro())
                    return
                    
                id = sequence_data_list[0].strip()
                sequence = sequence_data_list[1].strip()

                seq = MySeq(sequence)
                seq.setId(id)

                sequence_properties = sequence_data_list[2:len(sequence_data_list)]

                for i, prop in enumerate(sequence_properties):
                    if i == 0: # classe
                        seq.setClasse(prop)
                    if i == 1: # especie
                        seq.setEspecie(prop)
                    if i == 2: # code protein
                        seq.setCode_protein(prop)
                    if i == 3: # id swiss
                        seq.setID_swiss(prop)
                    if i == 4: # id ncbi
                        seq.setID_NCBI(prop)

                if seq.valida() and self.bd.setSeq(seq,id):
                    print (Messages.seq_adicionada())
                else:
                    print (Messages.seq_erro())
        
        except:
            print (Messages.ficheiro_invalido())

    def guardarSeqs(self, filename, withProperties = False):
        dic = self.bd.getBD()

        try:
            with open(filename, "w") as file:
                for i in dic:
                    mySeq = dic[i]

                    line = f"{mySeq.getId()}{self.SEPARATOR}{mySeq.getSeq()}"

                    if withProperties == False :
                        line += f"{self.SEPARATOR}{mySeq.getClasse()}{self.SEPARATOR}{mySeq.getEspecie()}{self.SEPARATOR}{mySeq.getCode_protein()}{self.SEPARATOR}{mySeq.getID_NCBI()}{self.SEPARATOR}{mySeq.getID_swiss()}"

                    line += "\n"
                    file.writelines(line)
            
            print(Messages.ficheiro_criado())
        except:
            print(Messages.erro_criar_ficheiro())

    def alinhamento(self, seq):         
         seq_alin = MySeq(seq)

         if not seq_alin.valida():
             print(Messages.sequencia_invalida())
             return

         #valores para o alinhamento:
         match = int(input("Valor do match: "))
         mismatch = int(input("Valor do mismatch: "))          
         gap = int(input("Valor do espaçamento: "))
         
         # definição das matrizes:
         sm = SubstMatrix()
         sm.createFromMatchPars(match, mismatch, "ACGT")
         alin = AlignSeq(sm , gap)

         #alinhamento
         sc = 0
         seq_out = 0
         for sqs in self.bd.getSeqs():
            score = alin.needlemanWunsch(seq_alin, sqs)
            if score > sc:
               sc = score
               seq_out = sqs.getId()

         print ((sc, seq_out))
   
    def frequencia(self, id_seq):
       countA = 0
       countC = 0
       countG = 0
       countT = 0
       seq = self.bd.getSeq(id_seq)
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
    
    def frequencia_subseq(self, sub_seq, id_seq):
       res = self.match_padrao(sub_seq, id_seq)
       return len(res)
       
    def match_padrao(self, padrao, id_seq):  
       seq = self.bd.getSeq(id_seq) #memoria da seq no MySeq
       rgx = re.compile(padrao.upper())
       return rgx.findall(seq.getSeq())
    
    def arvore(self, lis_seqs):
          seqs = []
          for ids in lis_seqs:
             seqs.append(self.bd.getSeq(ids))
          print(seqs)
          sm = SubstMatrix()
          sm.createFromMatchPars(3,-1, "ACGT")
          alseq = AlignSeq(sm,-8)
          up = UPGMA(seqs, alseq)
          arv = up.run()
          arv.printtree()
    
    def alinMultiplo(self, list_seqs):
       seqs = []
       for ids in list_seqs:
          seqs.append(self.bd.getSeq(ids))
       
       print(seqs)
       sm = SubstMatrix()
       sm.createFromMatchPars(1,-1,"ACGT")
       alseq = AlignSeq(sm,-1)
       ma = MultipleAlign(seqs, alseq)
       al = ma.alignConsensus()
       print(al)
    
    def traducao(self, id_seq):
       seq = self.bd.getSeq(id_seq)
       res = seq.find_all_orfs_all_rf()
       return res
    
    def exportarOrfs(self, id_seq, orfs):
       try:
            with open("Orfs.txt", "a") as file:
               line =  f"\n{id_seq}{self.SEPARATOR}"
               for orf in orfs:
                  line += f"{orf} - "
               file.write(line)
       except:
            print (Messages.ficheiro_invalido())
    
    def print_seq(self, seqId):
        seq = self.bd.getSeq(seqId)

        if seq != None:
            print("\n--- Dados da sequência ---\n")
            print("Id Sequência: " + seq.getId())
            print("Sequência: " + seq.getSeq())
            print("Classe: " + seq.getClasse())
            print("Espécie: " + seq.getEspecie())
            print("Código proteína: " + seq.getCode_protein())
            print("Id NCBI: " + seq.getID_NCBI())
            print("Id SwissProt: " + seq.getID_swiss())

        else:
            print(Messages.sequencia_nao_existe())
    
    def printBD(self):
        return self.bd.getBD()
    
    def printSeqs(self):
       for sqs in self.bd.getSeqs():
          print(sqs)
   
    def get_NCBI_seq(self, id_NCBI):
        Entrez.email = "pg@uminho.pt"
        identificador = id_NCBI.split("_")

        lista_identificadores = ["AC", "NC", "NG", "NT", "NW", "NZ"]
        if identificador[0] not in lista_identificadores:
            print (Messages.sequencia_nao_importada())
            return

        try:
            handle_seq = Entrez.efetch(db = "nucleotide", id = id_NCBI, rettype = "fasta", retmode = "text")
            seq_record = SeqIO.read(handle_seq, "fasta")

            seq2 = MySeq(seq_record.seq)
            seq2.setId(id_NCBI)
            if seq2.valida() == False:
                print (Messages.sequencia_invalida())
            else:
                self.bd.setSeq(seq2, id)
        except:
            print (Messages.sequencia_nao_importada())

    def execute_blast(self, id_seq, limit, evalue):
        seq = self.bd.getSeq(id_seq)

        if seq == None:
            print(Messages.sequencia_nao_existe())
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
                    print("Inferior a evalue fornecido!")

    def execute_alinhamento_multiplo_outros(self, filename, path):
        al = ExternalMAlign(filename)
        filename2 = filename.split('.')
        al.clustalW(path)
        al.printAlign(f"{filename2[0]}.aln")

    def execute_external_tree(self, filename):
        t = ExternalTree(filename) # ficheiro com as distâncias
        tree = t.createTree()

        print(tree)