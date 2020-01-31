from cmd import *
from SeqBiologicasEngine import SeqBiologicasEngine
import Messages as Messages

class SeqBiologicasShell(Cmd):
    intro = '''
==================== BEM VINDO! =================
    Interpretador de comandos para a gestão de Sequências Biológicas de DNA. 
    
    Escrever help ou ? para listar os comandos disponíveis.\n 

addseq          addseq_fasta     addseq_text

export_seqs     alinMultiplo     frequencia 
   
padrao          seqs_bd          arvore

semelhante      traducao         help

blast           info             addseq_NCBI

alinMultiploO   arvoreO          sair            
            '''

    prompt = 'SeqBioDNA> '
    DB_NAME = "bd_backup.txt"

    def do_addseq(self, arg):
        " Adicionar sequências biológicas e propriedades manualmente."
        try:
            seq = self.__repeat_if_input_empty("Sequencia a adicionar: ")
            seqId = self.__repeat_if_input_empty("ID da sequência: ")

            properties = []
            properties.append(input("Classe da sequencia: "))
            properties.append(input("Espécie da sequencia: "))
            properties.append(input("Código da proteína: "))
            properties.append(input("ID Swissprot: "))
            properties.append(input("ID NCBI: "))

            eng.add_seq(seqId, seq, properties)

        except:
            print (Messages.general_error())

        self.__comando_terminado()

    def do_addseq_fasta(self, arg):
        " Adcionar sequências biológicas em formato Fasta."
        try:
            filePath = self.__repeat_if_input_empty("Caminho do ficheiro FASTA: ")
            eng.import_seqfasta(filePath)
        except:
            print (Messages.general_error())

        self.__comando_terminado()
    
    def do_addseq_text(self, arg):
        " Adicionar sequências biológicas em formato Texto."
        try:
            filePath = self.__repeat_if_input_empty("Caminho do ficheiro: ")
            eng.import_seqtext(filePath)
        except:
            print (Messages.general_error())

        self.__comando_terminado()

    def do_info(self, arg):
        " Mostra dados guardados da sequencia."
        try:
            idSeq = self.__repeat_if_input_empty("ID da sequência: ")
            
            eng.print_seq(idSeq)
        except:
            print(Messages.general_error())

        self.__comando_terminado()

    def do_export_seqs(self, arg):
        " Exportar sequências guardadas para um ficheiro."
        try:
            filePath = self.__repeat_if_input_empty("Nome do ficheiro: ")
            eng.guardarSeqs(filePath)
        except:
            print (Messages.general_error())

        self.__comando_terminado()

    def do_semelhante(self, arg):
        " Realiza o alinhamento global para achar a sequencia mais semelhante à sequência indicada."
        try:
            
            seqInt = input("Sequencia a analisar: ")
            eng.alinhamento(seqInt)  

        except Exception as e:
            print(e)
            print(Messages.general_error())

        self.__comando_terminado()
   
    def do_frequencia(self, arg):
        "Calcula a frequencia de um simbolo ou sub-sequência de tamanho k escolhidos pelo utilizador"
        try:
           while True:
              print("""
                    1 - Frequencia de simbolo
                    2 - Frequencia de uma sub-sequência
                    0 - sair
                    """)
              op = input("Opção> ")
              if op == "1":                 
                 while True:                   
                    print("""
                             1 - Numa unica sequência
                             2 - Em todas as sequencias
                             0 - sair
                             """)                       
                    op = input("Opção> ")
                    if op == "1":      
                            id_seq = self.__repeat_if_input_empty("Id da sequência: ")
                            if id_seq in eng.getBD().getKeys():                        
                               res = eng.frequencia(id_seq)                               
                               if res != None:
                                  print(f"Simbolo A aparece {res[0]} vezes!")
                                  print(f"Simbolo C aparece {res[1]} vezes!")
                                  print(f"Simbolo G aparece {res[2]} vezes!")
                                  print(f"Simbolo T aparece {res[3]} vezes!")
                            else:
                               print(Messages.sequencia_nao_existe())
                            
                    elif op == "2":                        
                        #lista = []
                        for id_seq in eng.getBD().getKeys():
                           res = eng.frequencia(id_seq)  
                           if res != None:
                              print("Sequência: ", id_seq)
                              print(f"Simbolo A aparece {res[0]} vezes!")
                              print(f"Simbolo C aparece {res[1]} vezes!")
                              print(f"Simbolo G aparece {res[2]} vezes!")
                              print(f"Simbolo T aparece {res[3]} vezes!")
                             
                    elif op == "0":                       
                       break
                    else:
                       print("Comando inválido!")
                   
              elif op == "2":
                 while True:                   
                    print("""
                             1 - Numa unica sequência
                             2 - Em todas as sequencias
                             0 - sair
                             """)                       
                    op = input("Opção> ")
                    if op == "1":      
                       sub_seq = self.__repeat_if_input_empty("Introduza o padrão: ")
                       id_seq = self.__repeat_if_input_empty("Id da sequência: ")
                       
                       if id_seq in eng.getBD().getKeys():
                          res = eng.frequencia_subseq(sub_seq, id_seq)
                          print(f"A sub-sequência '{sub_seq}' aparece {res} vezes!")
                       else:
                          print(Messages.sequencia_nao_existe())
                    elif op == "2":                        
                       sub_seq = self.__repeat_if_input_empty("Introduza o padrão: ")
                       for id_seq in eng.getBD().getKeys():
                          res = eng.frequencia_subseq(sub_seq, id_seq)
                          print(f"Sequência: {id_seq}")
                          print(f"A sub-sequência '{sub_seq}' aparece {res} vezes!")
                       else:
                          print(Messages.sequencia_nao_existe())
                             
                    elif op == "0":                       
                       break
                    else:
                       print("Comando inválido!")
                 
                    
              elif op == "0":
                 break
              else:
                 print("Comando inválido!")
        
        except:
            print(Messages.general_error())
              
    
    def do_padrao(self,arg):
        " Procura ocorrencia de padrões numa sequencia ou em várias."

        try:
            while True:
                print("""
                      1 - Padrão numa Sequência
                      2 - Encontrar padrão em todas as sequências
                      0 - Sair
                        """)
                op = input("Opção> ")
                if op == "1":
                    padrao = self.__repeat_if_input_empty("Introduza o padrão: ")
                    id_seq = self.__repeat_if_input_empty("Id da sequência: ")
                                        
                    if id_seq in eng.getBD().getKeys():                        
                        res = eng.match_padrao(padrao,id_seq)
                        if res == None:
                            print("Não tem nenhum match.")
                        else:
                            print("Existe padrão nesta sequência.", res)
                    else:
                        print(Messages.sequencia_nao_existe())

                elif op == "2":
                    padrao = self.__repeat_if_input_empty("Introduza o padrão: ")
                    lista = []
                    for id_seq in eng.getBD().getKeys():
                        res = eng.match_padrao(padrao, id_seq)

                        if res != None:
                            lista.append(id_seq)
                    
                    print("Lista de IDs de sequências que têm match com padrão: " + str(lista))
                elif op == "0":
                    break
                else:
                    print("Comando inválido!")

        except Exception as e:
            print(e)
            print(Messages.general_error())

        self.__comando_terminado()
   
    def do_arvore(self, arg):
       "construção da arvore filogenetica a partir de um conjunto de sequências"
       print("""
             ================ Opções ==============================
             
             1 - Selecionar Sequencias
             2 - Escolher todas as sequências
             0 - Sair
             """)
       while True:
          op = input("Opção> ")
          if op == "1":
             list_seqs = []
             print("Id's das sequências pretendidas:")
             while True:                
                id_seq = input("> ")
                if id_seq == "":
                   break
                else:
                   if id_seq in eng.getBD().getKeys():
                      list_seqs.append(id_seq)
                   else:
                      print(Messages.sequencia_nao_existe())
             print(list_seqs)
             eng.arvore(list_seqs)
             
          if op == "2":
             list_seqs = []
             for id_seq in eng.getBD().getKeys():
               list_seqs.append(id_seq)
             eng.arvore(list_seqs)
          else:
             break
          
    def do_alinMultiplo(self, arg):
       """realiza o alinhamento multiplo de um conjunto de sequencias escolhidas pelo utilizador
       ou a todas as sequencias
       """
       print("""
======================= Opções =========================
      1 - Selecionar Sequências para o alinhamento
      2 - Alinhamento a todas as sequências
      0 - Sair 
             """)
       while True:
          op = input("Opção> ")
          if op == "1":
             list_seqs = []
             print("Id's das sequências pretendidas:")
             while True:                
                id_seq = input("> ")
                if id_seq == "":
                   break
                else:
                   if id_seq in eng.getBD().getKeys():
                      list_seqs.append(id_seq)
                      
                   else:
                      print(Messages.sequencia_nao_existe())
             print(list_seqs)
             eng.alinMultiplo(list_seqs)
             
             
          if op == "2":
             list_seqs = []
             for id_seq in eng.getBD().getKeys():
               list_seqs.append(id_seq)
             eng.alinMultiplo(list_seqs)
          else:
             break
    
    def do_traducao(self, arg):
       """"
       Realiza o a procura e traduçao de proteinas de todas as reading frames
       a partir da sequência selecionada pelo utilizador
       """
       id_seq = self.__repeat_if_input_empty("Id da sequência: ")
       if id_seq in eng.getBD().getKeys():
          print(id_seq)
          res = eng.traducao(id_seq)
          print(res)
          eng.exportarOrfs(id_seq, res)
       else:
          print(Messages.sequencia_nao_existe())
    
    def do_addseq_NCBI(self, arg):
        " Adicionar Sequência existente numa base de dados NCBI."
        try:
           id_seq = self.__repeat_if_input_empty("Id da sequência: ")
           eng.get_NCBI_seq(id_seq)
        except:
            print(Messages.general_error())

        self.__comando_terminado()

    def do_blast(self,arg):
        " Executa processo de Blast sobre sequencia da base de dados"
        try:
           id_seq = self.__repeat_if_input_empty("Id da sequência: ")
           limit = input("Limite de procura na base de dados[5]: ")

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

        self.__comando_terminado()

    def do_alinMultiploO(self, arg):
        " Processo de alinhamento multiplo com outro algoritmo"
        try:
           filename = self.__repeat_if_input_empty("Nome ficheiro: ")
           path = self.__repeat_if_input_empty("Caminho do executavel clustalw2: ")
           eng.execute_alinhamento_multiplo_outros(filename, path)

        except:
            print(Messages.general_error())

        self.__comando_terminado()

    def do_arvoreO(self, arg):
        " Arvore filogenetica com outro algoritmo"
        try:
           filename = self.__repeat_if_input_empty("Nome ficheiro: ")
           eng.execute_external_tree(filename)
        except:
            print(Messages.general_error())
        
        self.__comando_terminado()

    def __comando_terminado(self):
        print("\n\n")
        print(self.intro)

    def __repeat_if_input_empty(self, text):
        " Repete mensagem de input caso o input do utilizador seja vazio"
        tries = 0
        res = ""
        while res == "":
            if tries != 0:
                print("Por favor, insira um valor não vazio\n")
            
            res = input(text)
            tries +=1
        return res

    def do_sair(self, arg):
        "Sair do programa SeqBiológicas: sair"
        eng.guardarSeqs(self.DB_NAME, True)
        print("Estado guardado com sucesso! Até à próxima")
        return True
    
    def do_seqs_bd(self,arg):
        "Mostra o conteudo da base de dados"
        print(eng.printBD())


if __name__ == '__main__':
    eng = SeqBiologicasEngine()
    sh = SeqBiologicasShell()

    eng.import_seqtext(sh.DB_NAME) # Carregar base de dados 
    sh.cmdloop()
    