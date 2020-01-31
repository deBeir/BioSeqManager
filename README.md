# BioSeqManager

## ABOUT

No âmbito da unidade curricular de “Algoritmos para Análise de Sequências Biológicas” desenvolveu-se um programa que irá permitir ao usuário armazenar, gerir e manipular um conjunto de sequências de DNA e guardar propriedades do organismo da sequência e identificadores em bases de dados, onde poderão considerar anotações funcionais das sequências.
Este apresentará um menu principal, local onde permite ao utilizador escolher a funcionalidade a executar e voltar ao mesmo no final de cada funcionalidade, e sempre que o utilizador sair do programa a informação é guardada num ficheiro, de modo a ser possível a recuperação dos dados.


## OBJETIVOS

O projeto desenvolvido no âmbito da unidade curricular de “Algoritmos para Análise de Sequências Biológicas” teve por objetivo desenvolver em Python, um gestor de sequências biológicas, orientada a sequências de DNA.

## PRÉ-REQUISITOS

Para que se consigam executar certas funcionalidades do gerenciador de sequências, é necessário instalar a livraria *__Biopython__* da forma abaixo exemplificada.
`pip install biopython`

## USAGE

Este projeto apresenta por base x classes:

  - SeqBiologicasShell
  - SeqBiologicasEngine
  - BD
  - Alinhamento
  - Arvores
  - IO
  - AlignSeq*
  - BinaryTree*
  - ClustHier*
  - MatrixNum*
  - MyAlign*
  - MySeq*
  - SubsMatrix*
  - UPGMA*

As classes marcadas com * foram desenvolvidas durante o decorrer das aulas de AASB.

#### MÓDULO *SeqBioShell*
A classe *SeqBiologicalShell* presente neste módulo permite gerar um *interface*  de forma a que o utilizador seja capaz de manipular sequências biológicas. Dentro do interpretador de comandos, o utilizador poderá recorrer às seguintes funcionalidades:  

- *__sair__*: permite sair do interpretador de comandos.
- *__addseq__*: adicionar sequências de forma manual.
- *__addseq_fasta__*: adicionar sequências a partir de um ficheiro em formato *FASTA*.
- *__addseq_text__*: adicionar sequências biológicas em formato de texto.
- *__export_seqs__*: exportar sequências guardadas num ficheiro.
- *__info__*: mostrar informações detalhadas de uma sequência.
- *__semelhante__*: procura da sequência guardada mais semelhante.
- *__padrao__*: procura um padrão numa ou várias sequências.
- *__arvore__*: permite visualizar a árvore filogenética das sequências.
- *__AlinMultiplo__*: faz o alinhamento múltiplo das sequências.
- *__Freq__*: calcula a frequência de um símbolo/sub-sequência de tamanho k.

Após a seleção do comando, este é processado e o método correspondente ao mesmo é chamado. Estes métodos 
permitem adicionar e tratar a informação proveniente do(s) *input(s)*. Para que os métodos da classe processem os dados é necessário fazer *import* do módulo *SeqBiologicasEngine*. 

> Exemplo: método `do_def`
```
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

            eng.add_seq(seq, seqId, properties)

        except:
            print (Messages.general_error())

        self.__comando_terminado()
```





