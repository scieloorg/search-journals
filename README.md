# Pesquisa nos periódicos

Aplicação responsável por tornar os artigos ciêntificos da rede SciELO pesquisável.

## TOC:

 - [Capacidades](#capacidades)
 - [Integrações](#integrações)
 - [Requisitos](#requisitos)
 - [Licença de Uso](#licença-de-uso)

## Capacidades:

* Pesquisa contextualizada
* Pesquisa utilizando operadores booleanos
* Pesquisa aglomerada (cluster)
* Visualização dos resultado da pesquisa em registro simples e completo
* Envio do resultado de pesquisa por e-mail
* Exportação do resultado de pesquisa para os formatos:
    * RIS
    * BibTex
    * Citação
    * CSV
* Ordenação por:
    * Publicação - Mais novos primeiro
    * Publicação - Mais antigos primeiro
    * Relevância
    * Citações - Mais citados primeiro
    * Acessos - Mais acessados primeiro
* Realizar compartilhamento nas redes sociais
* Visualizar os resumos nos diversos idiomas
* Imprimi o resultado de pesquisa

## Integrações:

* Solr 5.5.5 (https://lucene.apache.org/solr/)
* iahx-controller (https://github.com/bireme/iahx-controller)

```
+-------------------+       +------------------------------+      +--------------+
|Pesquisa Integrada |------>|       iahx-controller        |----->|     SOLR     |
+-------------------+       +------------------------------+      +--------------+
```


## Multisite

A aplicação esta preparada para atender múltiplos sites usando o mesmo conjunto principal de arquivos do IAHX (arquivos core). Para isso é necessário:

* Replicar uma estrutura de um site existente abaixo do diretório **iahx-sites/**. 
* Ajustar o arquivo de configuração **config.xml** que se encontra abaixo do diretório **config/** deste novo site:
    * Indicar no parâmetro ```<site>``` o nome do índice SOLR onde serão realizadas as buscas
    * Caso seja um índice SOLR compartilhado por vários sites indicar no parâmetro ```<initial_filter>``` qual filtro dever ser aplicado para cada busca realizada pelo usuario. 
Exemplo ```<initial_filter>network:"rve"</initial_filter>```
    * Ajustar os demais parâmetros do config.xml, como por exemplos filtros disponíveis, url da homepage, etc.
* Realizar ajustes de aparência da interface (CSS, imagens, etc) usando os arquivos disponíveis abaixo do diretório **static/**
* Realizar ajustes nos templates de apresentação (apresentar ou eliminar campos na apresentação, etc) alterando o template no diretório **templates/custom/**


## Requisitos:

* PHP >= 5
* Apache2
* Solr


## Licença de uso:

Copyright 2019 SciELO <scielo-dev@googlegroups.com>. Licensed under the terms
of the BSD license. Please see LICENSE in the source code for more
information.

https://github.com/scieloorg/search-journals/blob/master/LICENSE
