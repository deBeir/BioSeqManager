# BioSeqManager
[MEBIOINF 2019/2020]

## SOBRE

No âmbito da unidade curricular de “Algoritmos para Análise de Sequências Biológicas” desenvolveu-se um programa que irá permitir ao usuário armazenar, gerir e manipular um conjunto de sequências de DNA e guardar propriedades do organismo da sequência e identificadores em bases de dados, onde poderão considerar anotações funcionais das sequências.
Este apresentará um menu principal, local onde permite ao utilizador escolher a funcionalidade a executar e voltar ao mesmo no final de cada funcionalidade, e sempre que o utilizador sair do programa a informação é guardada num ficheiro, de modo a ser possível a recuperação dos dados.


## OBJETIVOS

O projeto desenvolvido no âmbito da unidade curricular de “Algoritmos para Análise de Sequências Biológicas” teve por objetivo desenvolver em Python, um gestor de sequências biológicas, orientada a sequências de DNA.

## PRÉ-REQUISITOS

Para que se consigam executar certas funcionalidades do gerenciador de sequências, é necessário instalar o package *__Biopython__*.

`pip install biopython`

É também necessário instalar o __Clustal W/Clustal X__ para que se consigam realizar os alinhamentos múltiplos. O *download* encontra-se disponível [aqui](http://www.clustal.org/download/current/).

## FUNCIONALIDADES

Este projeto apresenta por base 15 classes:

  - SeqBiologicasShell
  - SeqBiologicasEngine
  - BD
  - ExternalMAlign
  - ExternalTree
  - Messages
  - AlignSeq*
  - BinaryTree*
  - ClustHier*
  - MatrixNum*
  - MyAlign*
  - MySeq*
  - SubsMatrix*
  - UPGMA*
  - MultipleAlign*

As classes marcadas com * foram desenvolvidas durante o decorrer das aulas de AASB.

#### MÓDULO *SeqBiologicasShell*
A classe *SeqBiologicasShell* presente neste módulo permite gerar um *interface*  de forma a que o utilizador seja capaz de manipular sequências biológicas. Dentro do interpretador de comandos, o utilizador poderá recorrer às seguintes funcionalidades:  

- *__addseq__*: adicionar sequências de forma manual.
- *__addseq_fasta__*: adicionar sequências a partir de um ficheiro em formato *FASTA*.
- *__addseq_text__*: adicionar sequências biológicas em formato de texto.
- *__export_seqs__*: exportar sequências guardadas num ficheiro.
- *__alinMultiplo__*: faz o alinhamento múltiplo das sequências.
- *__frequencia__*: calcula a frequência de um símbolo/sub-sequência de tamanho k.
- *__padrao__*: procura um padrão numa ou várias sequências.
- *__seqs_bd__*: mostra o conteúdo da base de dados.
- *__arvore__*: permite visualizar a árvore filogenética das sequências.
- *__semelhante__*: procura da sequência guardada mais semelhante.
- *__traducao__*: procura a tradução de proteínas de todas as *reading frames* a partir da sequência selecionada.
- *__help__*: comando de ajuda.
- *__blast__*: executa um blast de uma sequência contra a base de dados.
- *__info__*: mostrar informações detalhadas de uma sequência.
- *__addseq_NCBI__*: adiciona sequência retirada do NCBI.
- *__alinMultiploO__*: alinhamento múltiplo recorrendo ao *Clustal W*.
- *__arvoreO__*: gera árvore filogenética recorrendo a ficheiros proveninentes do alinhamento múltiplo com *Clustal W*.
- *__sair__*: permite sair do interpretador de comandos.

Após a seleção do comando, este é processado e o método correspondente ao mesmo é chamado. Estes métodos 
permitem adicionar e tratar a informação proveniente do(s) *input(s)*. Para que os métodos da classe processem os dados é necessário fazer *import* do módulo *SeqBiologicasEngine*. 

- __CMD__

Para criar o menu apresentado na classe *SeqBiologicasShell*, foi usada como base a biblioteca __Cmd__ que fornece uma estrutura simples para escrever comandos. Geralmente são úteis para equipamentos de teste, ferramentas administrativas e protótipos que posteriormente serão agrupados em interfaces mais complexas

> __EXEMPLO__   
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
- *__alinMultiplo__*: realiza o alinhamento múltiplo das sequências presentes na base de dados.
- *__traducao__*: procura a tradução de proteínas de todas as *reading frames* (ORFs) a partir da sequência selecionada.
- *__exportarOrfs__*: guarda todos os ORFs num ficheiro "*.txt*".
- *__print_seq__*: dado um ID de uma sequência, se esta estiver presente na base de dados, retorna toda a informação presente sobre a mesma.
- *__printBD__*: retorna o conteúdo da base de dados.
- *__printSeqs__*: imprime todas as sequências presentes na base de dados.
- *__get_NCBI_seq__*: recorre ao Entrez para retirar sequências de DNA do NCBI.
- *__execute_blast__*: realiza um programa de *blastn* dados certos parâmetros como o valor do *e-value*.
- *__execute_alinhamento_multiplo_outros__*: permite correr um programa de alinhamento múltiplo recorrendo ao *Clustal W*.
- *__execute_external_tree__*: dado o ficheiro gerado no alinhamento múltiplo com *Clustal W*, retorna uma árvore filogenética para as sequências contidas no ficheiro.
 
#### MÓDULO BD
Na classe BD são guardadas todas as informações das sequências (sob a forma de um dicionário) numa base de dados (que é um dicionário).


## CONCLUSÕES
Pode-se afirmar que o objetivo a que nos propusemos foi atingido, uma vez que o programa desenvolvido apresenta o menu sugerido onde o utilizador pode executar operações sobre uma sequência de bases de dados, pré-definidas pelo utilizador, bem como efetuar operações sobre bases de dados externas. 
Assim, a concretização deste trabalho foi fundamental na compreensão dos algoritmos existentes no tratamento de sequências biológicas, como DNA ou proteínas, e como aceder a bibliotecas existentes em python.

### CONTACTOS
GRUPO 3
- José Carvalho
- Rita Conde
- Sofia de Beir

Contacto: pg38263@alunos.uminho.pt
