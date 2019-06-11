# Pesquisa nos periódicos

Aplicação responsável por tornar os artigos ciêntificos da rede sciELO pesquisável.

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
* Exportação do resultado de pesquisa para os formato:
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

## Requisitos:

* PHP >= 5
* Apache2
* Solr


## Licença de uso:

Copyright 2019 SciELO <scielo-dev@googlegroups.com>. Licensed under the terms
of the BSD license. Please see LICENSE in the source code for more
information.

https://github.com/scieloorg/document-store/blob/master/LICENSE