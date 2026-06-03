# Operadores de Busca

Aprenda a combinar termos e técnicas avançadas para buscas mais precisas.

## Busca Exata com Aspas

Use **aspas duplas** para buscar uma expressão exata.

### Como funciona:

```
SEM aspas: educação física
RESULTADO: Encontra artigos com "educação" E "física" (em qualquer ordem/lugar)

COM aspas: "educação física"
RESULTADO: Encontra artigos com ESSA sequência exata
```

### Exemplos práticos:

| Busca | O que encontra |
|-------|---|
| `educação física` | "educação" e "física" separadamente |
| `"educação física"` | "educação física" como expressão |
| `"mudanças climáticas"` | Exatamente essa sequência |
| `"análise de variância"` | A frase completa junta |

### Quando usar aspas:

- ✅ **Títulos de trabalhos**: `"Impacto da inteligência artificial"`
- ✅ **Termos técnicos**: `"fotossíntese"` (em vez de foto síntese)
- ✅ **Nomes de autores**: `"Silva, João"`
- ❌ **Não é necessário para palavras comuns**: `"o"`, `"a"`, `"de"`

---

## Truncagem com Asterisco (*)

Use **asterisco** para buscar todas as variações de uma palavra.

### Como funciona:

O asterisco substitui qualquer número de letras **no final** da palavra.

```
pesquis*
Encontra:
✓ pesquisa
✓ pesquisador
✓ pesquisadores
✓ pesquisas
✓ pesquisar
```

### Exemplos práticos:

| Busca | Encontra |
|-------|----------|
| `educat*` | educação, educador, educadores, educativo |
| `desenv*` | desenvolvimento, desenvolvido, desenvolver |
| `tecnolog*` | tecnologia, tecnológico, tecnólogo |
| `saúd*` | saúde, saudável, saudavelmente |
| `climat*` | clima, climático, climatologia, climatização |
| `biotech*` | biotecnologia, biotecnológico |

### Vantagens da truncagem:

- ✅ **Abrangência**: Encontra todas as variações
- ✅ **Tempo**: Busca mais rápida que múltiplas buscas
- ✅ **Flexibilidade**: Cobre singular, plural, derivações

### Quando usar truncagem:

- ✅ Quando quer todas as variações de uma palavra
- ✅ Quando não tem certeza da forma exata
- ✅ Para termos muito específicos de um campo

### Quando NÃO usar:

- ❌ Com truncagem muito curta: `te*` (encontra demais)
- ❌ No meio da palavra: `pesqu*sa` (não funciona assim)

---

## Operadores Booleanos: AND, OR, NOT

Combine múltiplos termos com lógica booleana.

### AND - Ambos os termos

Encontra artigos que contêm **TODOS** os termos.

```
educação AND tecnologia
RESULTADO: Artigos sobre AMBOS os temas
```

### Exemplos:

| Busca | Resultado |
|-------|-----------|
| `educação AND tecnologia` | Artigos com os dois temas |
| `python AND programação` | Sobre programação em Python |
| `câncer AND tratamento` | Artigos sobre tratamento de câncer |

### OR - Um ou outro termo

Encontra artigos que contêm **QUALQUER UM** dos termos.

```
saúde OR bem-estar
RESULTADO: Artigos sobre saúde OU bem-estar (ou ambos)
```

### Exemplos:

| Busca | Resultado |
|-------|-----------|
| `COVID OR pandemia` | Artigos sobre COVID ou pandemia |
| `câncer OR tumor` | Sobre câncer ou tumor (abrange variações) |
| `IA OR inteligência artificial` | Sobre IA (com as duas variações) |

### NOT - Excluir um termo

Encontra artigos com o primeiro termo **SEM** o segundo.

```
educação NOT superior
RESULTADO: Artigos sobre educação, EXCETO educação superior
```

### Exemplos:

| Busca | Resultado |
|-------|-----------|
| `saúde NOT mental` | Saúde em geral, mas NÃO saúde mental |
| `Brasil NOT futebol` | Artigos sobre Brasil, exceto sobre futebol |
| `tecnologia NOT arma` | Tecnologia civil, excluindo militares |

---

## Combinando Operadores

Você pode combinar vários operadores para buscas complexas.

### Exemplos avançados:

```
(educação OR aprendizado) AND tecnologia
Encontra: Artigos sobre (educação OU aprendizado) E tecnologia

inteligência artificial AND (educação OR saúde)
Encontra: IA aplicada a educação OU IA aplicada a saúde

mudança climática AND Brasil NOT Sul
Encontra: Mudança climática no Brasil, excluindo região Sul
```

---

## Hífen na Busca: Atenção!

Palavras **com hífen** são tratadas diferente de palavras **sem hífen**.

### Importante:

```
COM HÍFEN: sócio-econômico
→ É dividido em: "sócio" E "econômico"

SEM HÍFEN: socioeconômico
→ É tratado como: um único termo
```

### Consequência:

| Busca | O que encontra |
|-------|---|
| `sócio-econômico` | Artigos com "sócio" E "econômico" |
| `socioeconômico` | Artigos com a palavra "socioeconômico" |
| Resultado | **NÃO encontra os mesmos artigos!** |

### Solução:

Se quer cobrir ambas as variações, faça **duas buscas**:

```
1ª busca: "sócio-econômico"
2ª busca: "socioeconômico"
```

Ou use truncagem:

```
socio* (encontra ambas as variações)
```

---

## Limite de Complexidade

### Qual é o limite?

A plataforma suporta até **1.024 combinações** em uma única busca. Isso é bem abrangente!

### Exemplo que funciona:

```
(educação OR aprendizado OR pedagogia) AND 
(tecnologia OR IA OR digital) AND 
Brasil AND (2020 OR 2021 OR 2022 OR 2023)
```

### Como não atingir esse limite:

- A maioria das buscas normais usa menos de 20 combinações
- Você só atingiria o limite com centenas de termos
- Caso encontre erro, simplifique a busca

---

## Dicas de Ouro

### ✅ Melhores práticas:

```
"educação física" AND Brasil
→ Expressão exata + filtro específico

technolog* AND educação AND (Brasil OR Portugal)
→ Truncagem + múltiplos termos + alternativas

"machine learning" AND (saúde OR medicina)
→ Expressão técnica + áreas relacionadas
```

### ❌ Evite:

```
a* OR b* OR c*
→ Muito genérico, encontra tudo

educação AND educação AND educação
→ Redundante, use uma única vez

NOT NOT NOT NOT palavra
→ Muito complexo, evite duplas negações
```

---

## Próximos passos

- [Filtros e Organização](./filters.md) - Refine ainda mais seus resultados
- [Busca Avançada](./advanced-search.md) - Interface avançada
- [Dúvidas Técnicas](./technical.md) - Perguntas sobre a plataforma

---

**Última atualização:** Junho de 2024
