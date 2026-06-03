# Busca Avançada

Técnicas para pesquisadores e acadêmicos que precisam de resultados mais refinados.

## Busca por Campo Específico

Ao invés de buscar em todos os campos, procure em um específico.

### Campos disponíveis:

| Campo | Descrição | Exemplo |
|-------|-----------|---------|
| `título:` ou `ti:` | Título do artigo | `ti:"inteligência artificial"` |
| `autor:` ou `au:` | Nome do autor | `au:Silva` |
| `resumo:` ou `ab:` | Resumo do artigo | `ab:metodologia` |
| `palavras-chave:` ou `kw:` | Palavras-chave | `kw:climatologia` |
| `revista:` ou `journal:` | Nome da revista/periódico | `journal:Lancet` |
| `ano:` ou `da:` | Ano de publicação | `da:2023` |
| `idioma:` ou `la:` | Idioma (pt, en, es, etc) | `la:pt` |

### Exemplos práticos:

```
ti:"mudanças climáticas"
→ Busca "mudanças climáticas" apenas nos títulos

au:Costa AND au:Silva
→ Artigos de ambos os autores

kw:sustentabilidade AND au:Ferreira
→ Artigos sobre sustentabilidade do autor Ferreira
```

---

## Combinar Período de Datas

Filtre por anos específicos.

### Como fazer:

```
educação AND ano:2023
→ Artigos sobre educação publicados em 2023

saúde AND ano:(2020 OR 2021 OR 2022)
→ Artigos sobre saúde de 2020 a 2022

tecnologia AND ano:[2015 TO 2023]
→ Artigos de tecnologia entre 2015 e 2023
```

---

## Buscar por Revista Específica

Foque em periódicos importantes para sua área.

### Exemplos:

```
cancer treatment journal:Nature
→ Sobre câncer na revista Nature

educação journal:Pedagogia?
→ Sobre educação em revistas com "Pedagogia" no nome
```

---

## Combinar Autor, Título e Data

Busca bem direcionada para um artigo específico.

### Exemplo:

```
au:Einstein ti:"relativity" ano:1905
→ Artigo de Einstein sobre relatividade de 1905
```

---

## Usar Truncagem com Campos

Combine wildcards com buscas por campo.

### Exemplos:

```
au:Silva* ti:educação*
→ Autores com sobrenome começando em Silva + títulos sobre educação

kw:sustent* journal:"Environmental"
→ Palavras-chave sobre sustentabilidade em revistas ambientais
```

---

## Busca Negada em Campos

Exclua termos de campos específicos.

### Exemplos:

```
ti:câncer NOT ti:pele
→ Sobre câncer, mas não câncer de pele

au:Silva NOT ti:futebol
→ Artigos do Silva, mas não sobre futebol
```

---

## Buscar em Múltiplos Idiomas

Especifique o idioma dos artigos.

### Códigos de idioma:

- `pt` = Português
- `en` = English (Inglês)
- `es` = Español (Espanhol)
- `fr` = Français (Francês)

### Exemplos:

```
tecnologia la:pt
→ Artigos em português sobre tecnologia

inteligência artificial AND (la:pt OR la:en)
→ Sobre IA em português ou inglês
```

---

## Estratégia: Afunilamento Progressivo

Comece amplo e refine gradualmente.

### Passo a passo:

```
1ª busca: educação
   ↓ Resultado: 50.000 artigos (muitos!)

2ª busca: educação AND tecnologia
   ↓ Resultado: 5.000 artigos (melhor)

3ª busca: educação AND tecnologia AND Brasil
   ↓ Resultado: 500 artigos (mais específico)

4ª busca: "educação tecnológica" AND au:Silva AND ano:2020
   ↓ Resultado: 10 artigos (muito focado)
```

---

## Exemplo Real de Busca Avançada

### Cenário: Você procura artigos sobre Inteligência Artificial em Medicina

**Busca 1 - Ampla:**
```
inteligência artificial AND medicina
→ Resultado: 3.000 artigos
```

**Busca 2 - Refinar por data:**
```
inteligência artificial AND medicina AND ano:(2021 OR 2022 OR 2023)
→ Resultado: 1.200 artigos
```

**Busca 3 - Refinar por idioma:**
```
(inteligência artificial OR "machine learning") AND medicina AND (la:pt OR la:en) AND ano:(2021 OR 2022 OR 2023)
→ Resultado: 800 artigos
```

**Busca 4 - Refinar por tipo:**
```
ti:(diagnóstico* OR tratamento*) AND (inteligência artificial OR "machine learning") AND medicina AND ano:(2021 OR 2022 OR 2023)
→ Resultado: 150 artigos muito relevantes
```

---

## Dicas para Buscas Muito Específicas

### ✅ Faça assim:

```
"machine learning" AND "diagnóstico" AND medicina
→ Expressão exata + campo específico

au:LeCun* ti:deep* AND ano:2023
→ Combina autor aproximado + título aproximado + data

kw:neural AND ti:(rede OR network) AND idioma:en
→ Múltiplos campos + idioma
```

### ❌ Evite:

```
Machine Learning Machine Learning Machine Learning
→ Redundância (use uma vez)

NOT NOT NOT palavra
→ Negações em cascata

ti:a OR ti:o OR ti:de
→ Muito genérico
```

---

## Salvar e Compartilhar Buscas

### Muitas plataformas permitem:

- **Salvar** sua busca para reutilizar depois
- **Compartilhar** a URL da busca com colegas
- **Criar alertas** para novas publicações nesse tema

---

## Próximos passos

- [Operadores de Busca](./search-operators.md) - Detalhe sobre AND, OR, NOT
- [Filtros e Organização](./filters.md) - Como organizar resultados
- [Exportar Resultados](./export.md) - Salve seus resultados

---

**Última atualização:** Junho de 2024
