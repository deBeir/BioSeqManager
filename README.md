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

#### MÓDULO *SeqBiologicasShell*
A classe *SeqBiologicasShell* presente neste módulo permite gerar um *interface*  de forma a que o utilizador seja capaz de manipular sequências biológicas. Dentro do interpretador de comandos, o utilizador poderá recorrer às seguintes funcionalidades:  

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
- *__Seqs_bd__*: mostra o conteúdo da base de dados.

Após a seleção do comando, este é processado e o método correspondente ao mesmo é chamado. Estes métodos 
permitem adicionar e tratar a informação proveniente do(s) *input(s)*. Para que os métodos da classe processem os dados é necessário fazer *import* do módulo *SeqBiologicasEngine*. 

> EXEMPLO   
Caso o usuário selecione o comando *__addseq__*, é chamado o método `do_addseq(self,arg)`, que permite inserir a sequência manualmente, bem como o ID da mesma. Opcionalmente, podem ser adicionadas diferentes propriedades, como, por exemplo, a classe e espécie da sequência ou o ID da sequência no NCBI (*National Center for Biotechnology Information*). Este método recorre ao método `add_seq` da *SeqBiologicasEngine* para adicionar a informação dos *inputs* à base de dados implementada no módulo *BD*.

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
Para além dos métodos implementados para que seja possível tratar os dados inseridos pelo usuário, existem ainda métodos adicionais que permitem gerir possíveis erros e verificar quando a execução do comando termina.

- `__comando_terminado(self)`: repete a mensagem de input caso este seja nulo (vazio).
- `__repeat_if_input_empty(self,text)`: responsável pelo retorno ao menu de seleção de comandos quando o comando atual acaba de executar.


#### MÓDULO *SeqBiologicasEngine*
Na classe *SeqBiologicaEngine* encontram-se os métodos que permitem de facto processar, gerir e guardar na base de dados (*BD*).

- *__getBD__*: retorna a base de dados (dicionário com as sequências).
- *__add_seq__*: permite realizar a inserção manual da sequência na base de dados, caso esta ainda não se encontre na mesma.
- *__import_seqfasta__*: processa um ficheiro em formato *FASTA* e insere a sequência na base de dados, caso esta não se encontre na mesma.
- *__import_seqtext__*: processa um ficheio "*.txt*" e insere a sequência na base de dados, caso esta não se encontre na mesma.
- *__guardaSeqs__*: guarda as sequências num ficheiro.
- *__alinhamento__*: realiza o alinhamento de uma sequência com as presentes na base de dados, retornando o alinhamento com maior score (sequência com mais homologia à sequência inserida).
- *__frequencia__*: conta a frequência de bases da sequência desejada.
- *__frequencia_subseq__*: encontra todas as ocorrências de uma sub-sequência da sequência dada.
- *__match_padrao__*: encontra todas as ocorrências de um padrão na sequência.
- *__arvore__*: gera a árvore filogenética das sequências.
- *__print_seq__*: dado um ID de uma sequência, se esta estiver presente na base de dados, retorna toda a informação presente sobre a mesma.
- *__printBD__*: retorna o conteúdo da base de dados.
- *__printSeqs__*: imprime todas as sequências presentes na base de dados.
 
#### MÓDULO BD
Na classe BD são guardadas todas as informações das sequências (sob a forma de um dicionário) numa base de dados (que é um dicionário).


