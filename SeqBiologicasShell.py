from cmd import *
from SeqBiologicasEngine import SeqBiologicasEngine
import Messages as Messages

class SeqBiologicasShell(Cmd):
    intro = '''
==================== WELCOME! =================
    Command shell to manage DNA sequences.  
    
    Type help or ? to list the available commands.\n 

addseq          addseq_fasta     addseq_text

export_seqs     alinMultiple     frequency
   
pattern          seqs_db         tree

similar      translation         help

blast           info             addseq_NCBI

alinMultiplO   treeO          exit            
            '''

    prompt = 'SeqBioDNA> '
    DB_NAME = "db_backup.txt"

    def do_addseq(self, arg):
        " Add biological sequences and its properties manually."
        try:
            seq = self.__repeat_if_input_empty("Sequence to add: ")
            seqId = self.__repeat_if_input_empty("Sequence ID: ")

            properties = []
            properties.append(input("Sequence class: "))
            properties.append(input("Sequence species: "))
            properties.append(input("Protein Code: "))
            properties.append(input("Swissprot ID: "))
            properties.append(input("NCBI ID: "))

            eng.add_seq(seqId, seq, properties)

        except:
            print (Messages.general_error())

        self.__done()

    def do_addseq_fasta(self, arg):
        " Add biological sequences (Fasta format)."
        try:
            filePath = self.__repeat_if_input_empty("Path to Fasta file: ")
            eng.import_seqfasta(filePath)
        except:
            print (Messages.general_error())

        self.__done()
    
    def do_addseq_text(self, arg):
        " Add biological sequences (.txt format)."
        try:
            filePath = self.__repeat_if_input_empty("Path to file: ")
            eng.import_seqtext(filePath)
        except:
            print (Messages.general_error())

        self.__done()

    def do_info(self, arg):
        " Show saved sequence data."
        try:
            idSeq = self.__repeat_if_input_empty("Sequence ID: ")
            
            eng.print_seq(idSeq)
        except:
            print(Messages.general_error())

        self.__done()

    def do_export_seqs(self, arg):
        " Export saved sequences to a text file."
        try:
            filePath = self.__repeat_if_input_empty("File name: ")
            eng.SaveSeqs(filePath)
        except:
            print (Messages.general_error())

        self.__done()

    def do_similar(self, arg):
        " Performs global alignment to search for the sequence that matches best with the one provided."
        try:
            
            seqInt = input("Sequence to analyse: ")
            eng.alignment(seqInt)  

        except Exception as e:
            print(e)
            print(Messages.general_error())

        self.__done()
   
    def do_frequency(self, arg):
        " Calculates the frequency of a symbol (or subsequence of k size) choosen by the user."
        try:
           while True:
              print("""
                    1 - Symbol frequency
                    2 - Sub sequence frequency
                    0 - exit
                    """)
              op = input("Option> ")
              if op == "1":                 
                 while True:                   
                    print("""
                            ================ Options ==============================
                             1 - In only one sequence
                             2 - In all sequences
                             0 - Exit
                             """)                       
                    op = input("Option> ")
                    if op == "1":      
                            id_seq = self.__repeat_if_input_empty("Sequence ID: ")
                            if id_seq in eng.getDB().getKeys():                        
                               res = eng.frequency(id_seq)                               
                               if res != None:
                                  print(f"A symbol shows up {res[0]} times!")
                                  print(f"C symbol shows up {res[1]} times!")
                                  print(f"G symbol shows up {res[2]} times!")
                                  print(f"T symbol shows up {res[3]} times!")
                            else:
                               print(Messages.nonexistent_sequence())
                            
                    elif op == "2":                        
                        #list = []
                        for id_seq in eng.getDB().getKeys():
                           res = eng.frequency(id_seq)  
                           if res != None:
                              print("Sequence: ", id_seq)
                              print(f"A symbol shows up {res[0]} times!")
                              print(f"C symbol shows up {res[1]} times!")
                              print(f"G symbol shows up {res[2]} times!")
                              print(f"T symbol shows up {res[3]} times!")
                             
                    elif op == "0":                       
                       break
                    else:
                       print("Invalid input!")
                   
              elif op == "2":
                 while True:                   
                    print("""
                            ================ Options ==============================
                             1 - In only one sequence
                             2 - In all sequences
                             0 - Exit
                             """)                       
                    op = input("Option> ")
                    if op == "1":      
                       sub_seq = self.__repeat_if_input_empty("Introduce the desired pattern: ")
                       id_seq = self.__repeat_if_input_empty("Sequence ID: ")
                       
                       if id_seq in eng.getDB().getKeys():
                          res = eng.frequency_subseq(sub_seq, id_seq)
                          print(f"The sub sequence '{sub_seq}' shows up {res} times!")
                       else:
                          print(Messages.nonexistent_sequence())
                    elif op == "2":                        
                       sub_seq = self.__repeat_if_input_empty("Introduce desired pattern: ")
                       for id_seq in eng.getDB().getKeys():
                          res = eng.frequency_subseq(sub_seq, id_seq)
                          print(f"Sequence: {id_seq}")
                          print(f"The sub sequence '{sub_seq}' shows up {res} times!")
                       else:
                          print(Messages.nonexistent_sequence())
                             
                    elif op == "0":                       
                       break
                    else:
                       print("Invalid input!")
                 
                    
              elif op == "0":
                 break
              else:
                 print("Invalid input!")
        
        except:
            print(Messages.general_error())
              
    
    def do_pattern(self,arg):
        " Searches how many times a pattern shows up in one or more sequences."

        try:
            while True:
                print("""
                    ================ Options ==============================
                      1 - Pattern in a sequence
                      2 - Pattern in all sequences
                      0 - Exit
                        """)
                op = input("Option> ")
                if op == "1":
                    padrao = self.__repeat_if_input_empty("Introduce the pattern: ")
                    id_seq = self.__repeat_if_input_empty("Sequence Id: ")
                                        
                    if id_seq in eng.getDB().getKeys():                        
                        res = eng.match_pattern(padrao,id_seq)
                        if res == None:
                            print("No match found.")
                        else:
                            print("A pattern was found in the sequence.", res)
                    else:
                        print(Messages.nonexistent_sequence())

                elif op == "2":
                    padrao = self.__repeat_if_input_empty("Introduce the pattern: ")
                    lista = []
                    for id_seq in eng.getDB().getKeys():
                        res = eng.match_pattern(pattern, id_seq)

                        if res != None:
                            lista.append(id_seq)
                    
                    print("List of sequence Ids that match the pattern:" + str(lista))
                elif op == "0":
                    break
                else:
                    print("Invalid command!")

        except Exception as e:
            print(e)
            print(Messages.general_error())

        self.__done()
   
    def do_tree(self, arg):
       "Construction of a phylogenetic tree from the given sequences"
       print("""
             ================ Options ==============================
             
             1 - Select specific sequences
             2 - Select all sequences
             0 - Exit
             """)
       while True:
          op = input("Option> ")
          if op == "1":
             list_seqs = []
             print("Id's of desired sequences:")
             while True:                
                id_seq = input("> ")
                if id_seq == "":
                   break
                else:
                   if id_seq in eng.getDB().getKeys():
                      list_seqs.append(id_seq)
                   else:
                      print(Messages.nonexistent_sequence())
             print(list_seqs)
             eng.tree(list_seqs)
             
          if op == "2":
             list_seqs = []
             for id_seq in eng.getDB().getKeys():
               list_seqs.append(id_seq)
             eng.tree(list_seqs)
          else:
             break
          
    def do_multiple_align(self, arg):
       """Performs multiple alignment of a set of sequences choosen by the user
       (or all sequences contained in the database)
       """
       print("""
======================= Options =========================
      1 - Selects sequences for the alignment
      2 - Aligns all sequences
      0 - Exit 
             """)
       while True:
          op = input("Option> ")
          if op == "1":
             list_seqs = []
             print("Id's of desired sequences:")
             while True:                
                id_seq = input("> ")
                if id_seq == "":
                   break
                else:
                   if id_seq in eng.getDB().getKeys():
                      list_seqs.append(id_seq)
                      
                   else:
                      print(Messages.nonexistent_sequence())
             print(list_seqs)
             eng.alinMultiple(list_seqs)
             
             
          if op == "2":
             list_seqs = []
             for id_seq in eng.getDB().getKeys():
               list_seqs.append(id_seq)
             eng.alinMultiple(list_seqs)
          else:
             break
    
    def do_traslation(self, arg):
       "Does the search and translation of proteins of all reading frames"
       id_seq = self.__repeat_if_input_empty("Sequence Id: ")
       if id_seq in eng.getDB().getKeys():
          print(id_seq)
          res = eng.translation(id_seq)
          print(res)
          eng.exportarOrfs(id_seq, res)
       else:
          print(Messages.nonexistent_sequence())
    
    def do_addseq_NCBI(self, arg):
        " Adds a NCBI sequence to database "
        try:
           id_seq = self.__repeat_if_input_empty("Sequence Id: ")
           eng.get_NCBI_seq(id_seq)
        except:
            print(Messages.general_error())

        self.__done()

    def do_blast(self,arg):
        " Executes blast"
        try:
           id_seq = self.__repeat_if_input_empty("Sequence Id: ")
           limit = input("Database search limit[5]: ")

           try:
               limit = int(s)
           except:
               limit = 5
               
           evalue = input("E-Value [0.001]: ")

           try:
               evalue = float(s)
           except:
               evalue = 0.001

           eng.execute_blast(id_seq, limit, evalue)
        except:
            print(Messages.general_error())

        self.__done()

    def do_multiple_alingW(self, arg):
        " Multiple Alignment with clustal"
        try:
           filename = self.__repeat_if_input_empty("File name: ")
           path = self.__repeat_if_input_empty("Path to clustalw2 software: ")
           eng.execute_other_mult_align(filename, path)

        except:
            print(Messages.general_error())

        self.__done()

    def do_treeW(self, arg):
        "Tree using another algorithm"
        try:
           filename = self.__repeat_if_input_empty("File na: ")
           eng.execute_external_tree(filename)
        except:
            print(Messages.general_error())
        
        self.__done()

    def __done(self):
        print("\n\n")
        print(self.intro)

    def __repeat_if_input_empty(self, text):
        " Repeats messages in case the input is null."
        tries = 0
        res = ""
        while res == "":
            if tries != 0:
                print("Please, insert a non empty input\n")
            
            res = input(text)
            tries +=1
        return res

    def do_exit(self, arg):
        "Exit BioSeqManager: exit!"
        eng.SaveSeqs(self.DB_NAME, True)
        print("Saved with success. See you later!")
        return True
    
    def do_seqs_db(self,arg):
        "Shows database contents."
        print(eng.printDB())


if __name__ == '__main__':
    eng = SeqBiologicasEngine()
    sh = SeqBiologicasShell()

    eng.import_seqtext(sh.DB_NAME) # Loads database 
    sh.cmdloop()
    
