# Dúvidas Técnicas

Respostas a perguntas técnicas sobre a plataforma e suas capacidades.

## Limite de Caracteres

**P: Existe limite de caracteres para uma busca?**

R: Não há um limite específico de caracteres em termos de digitação. O que existe é um **limite de 1.024 combinações booleanas** (cláusulas) por busca.

### O que isso significa?

Uma "cláusula booleana" é cada vez que você usa AND, OR, ou NOT.

```
Exemplo: (educação AND tecnologia) OR (ensino AND digital)
Cláusulas: 4 (educação, tecnologia, ensino, digital)

O limite permite: até 1.024 cláusulas
```

### Na prática:

- ✅ **Funcionam bem:** Buscas normais (até 500 combinações)
- ✅ **Funcionam bem:** Pesquisas complexas (até 1.000 combinações)
- ❌ **Podem falhar:** Buscas com >1.000 combinações (muito raro)

### Exemplos que funcionam:

```
educação AND tecnologia AND Brasil
→ 3 cláusulas ✓

(saúde OR bem-estar) AND (mental OR psicológica) AND (crianças OR adolescentes)
→ 6 cláusulas ✓

(termo1 OR termo2 OR termo3) AND (termo4 OR termo5)
→ 5 cláusulas ✓
```

---

## Tratamento de Acentos e Maiúsculas

**P: Preciso digitar com acentos e maiúsculas corretas?**

R: **Não!** A plataforma **ignora automaticamente** acentos e maiúsculas.

### Exemplos equivalentes:

```
"educacao" = "educação"
"SAUDE" = "saúde"
"Pesquisa" = "pesquisa"
"CLIMATOLOGIA" = "climatologia"
```

### Consequência prática:

Você **não precisa se preocupar** com:
- Colocar acentos
- Usar MAIÚSCULAS ou minúsculas
- Cedilhas
- Til

A plataforma **entende tudo normalmente**.

---

## Tratamento de Hífens

**P: Palavras com e sem hífen são iguais?**

R: **Não!** Há uma diferença importante.

### Como funciona:

```
COM HÍFEN: sócio-econômico
→ É dividido em 2 termos: "sócio" + "econômico"

SEM HÍFEN: socioeconômico
→ É tratado como um único termo
```

### Consequência:

```
Busca por: "sócio-econômico"
Encontra: Artigos com ambas as palavras separadas

Busca por: "socioeconômico"
Encontra: Artigos com essa palavra específica

Resultado: NÃO encontram os mesmos artigos!
```

### Solução:

**Opção 1 - Fazer duas buscas:**
```
1ª: sócio-econômico
2ª: socioeconômico
```

**Opção 2 - Usar truncagem (melhor):**
```
socio* (encontra ambas as variações)
```

---

## Truncagem com Asterisco (*)

**P: Como exatamente funciona o asterisco (*)?**

R: O asterisco **substitui qualquer número de letras no final da palavra**.

### Funcionamento:

```
pesquis* = pesquisa, pesquisador, pesquisas, pesquisadores, pesquisar, pesquisando, etc.

educ* = educação, educador, educadores, educativa, educativo, educando, etc.

climat* = clima, climático, climatologia, climatização, climatizador, etc.
```

### Importante:

- ✅ O asterisco funciona **no final da palavra**
- ❌ O asterisco **NÃO funciona no meio**: `pesqu*sa` não funciona
- ❌ O asterisco **NÃO funciona no começo**: `*ologia` não funciona

### Quando usar:

- Quando quer todas as variações
- Quando não tem certeza da forma exata
- Para termos técnicos ou derivações complexas

---

## Operadores Booleanos: AND, OR, NOT

**P: Qual é a ordem de precedência dos operadores?**

R: **AND tem prioridade sobre OR**

### Exemplo:

```
A OR B AND C
É interpretado como: A OR (B AND C)

Não como: (A OR B) AND C
```

### Dica:

Use **parênteses** para deixar claro sua intenção:

```
(A OR B) AND C  ← Deixa explícito
```

---

## Busca Exata com Aspas

**P: Aspas garantem resultado 100% exato?**

R: **Parcialmente.** As aspas **garantem a sequência**, mas as análises de texto ainda se aplicam.

### O que aspas fazem:

```
"educação física"
→ Encontra: ...educação física...
→ Não encontra: ...educação e física... (com "e" no meio)
```

### O que aspas NÃO previnem:

```
"educacao" = "educação"  (acentos ignorados)
"Educacao" = "educação"  (maiúsculas ignoradas)
"sócio-econômico" ainda é dividido por hífens
```

### Exemplo real:

```
Busca: "educação física"

ENCONTRA:
✓ "educação física"
✓ "uma educação física renovada"
✓ "na educação física brasileira"

NÃO ENCONTRA:
✗ "educação e física" (ordem invertida ou com palavras no meio)
✗ "física educação" (ordem contrária)
```

---

## Performance e Velocidade de Busca

**P: Por que algumas buscas são mais lentas?**

R: A velocidade depende de vários fatores:

### Buscas mais rápidas:

- Buscas simples com 1-2 termos
- Buscas com filtros muito específicos
- Buscas com aspas (expressões exatas)

### Buscas mais lentas:

- Buscas muito genéricas (como buscar por "a" ou "o")
- Buscas com muitos ORs
- Buscas com truncagem muito curta (ex: `a*`, `ed*`)

### Dica para melhor performance:

```
❌ Evite: edu*
✓ Use: educa* (mais específico)

❌ Evite: saúde OR bem-estar OR... (muitos ORs)
✓ Use: "saúde e bem-estar" (expressão exata)
```

---

## Resultado Vazio ou Muito Poucos Resultados

**P: Por que uma busca retorna zero resultados?**

Possíveis razões:

### 1. Termo muito específico
```
Busca: "O impacto do grafeno na fotossíntese de orquídeas raras"
Resultado: Nenhum
Solução: Tente termos mais gerais: "grafeno" ou "fotossíntese"
```

### 2. Termo muito obscuro
```
Busca: Autor de publicação muito recente ou pouco conhecida
Resultado: Nenhum ou poucos
Solução: Use nome diferente ou variação do termo
```

### 3. Filtros muito restritivos
```
Busca: tema X + revista Y + ano exato Z + idioma específico
Resultado: Nenhum
Solução: Remova um filtro ou deixe mais abrangente
```

### 4. Erro de digitação
```
Busca: "educassão" (com SS)
Resultado: Nenhum
Solução: Verifique a ortografia
```

### Como resolver:

```
1. Simplifique: use termos mais gerais
2. Aumente: remova filtros restritos
3. Varie: tente sinônimos
4. Verifique: confira ortografia
```

---

## Qual é a Cobertura de Artigos?

**P: Quantos artigos estão indexados na plataforma?**

R: A plataforma indexa artigos científicos do **SciELO e redes associadas**.

### Cobertura:

- Centenas de periódicos científicos
- Milhões de artigos
- Principalmente de **América Latina, com foco em Brasil**
- Artigos em português, espanhol, inglês e outras línguas

### Não encontra:

- ❌ Artigos paywall de journals exclusivos (Nature, Science - restritos)
- ❌ Teses e dissertações (procure em repositórios institucionais)
- ❌ Livros (procure em bases de livros)
- ❌ Artigos pré-publicação (preprints - procure em arXiv)

---

## Compatibilidade com Navegadores

**P: Qual navegador devo usar?**

R: A plataforma é compatível com navegadores modernos:

### Navegadores recomendados:

- ✅ Chrome (versão recente)
- ✅ Firefox (versão recente)
- ✅ Safari (versão recente)
- ✅ Edge (versão recente)

### Versão mobile:

- ✅ Funciona em smartphones
- ✅ Funciona em tablets
- Otimizada para telas pequenas

---

## Cookies e Privacidade

**P: A plataforma usa cookies?**

R: Sim, para:

- Manter sua sessão ativa
- Lembrar preferências (idioma, etc)
- Analisar uso (privado)

### Você pode:

- Aceitar todos os cookies
- Gerenciar quais aceita
- Usar "modo privado/incógnito" para não salvar

---

## Acessibilidade

**P: A plataforma é acessível para usuários com deficiência?**

R: A plataforma busca ser acessível com:

- Compatibilidade com leitores de tela
- Navegação por teclado
- Contraste adequado
- Textos descritivos

### Se enfrentar problemas:

Entre em contato com a equipe de suporte do SciELO para relatar.

---

## Segurança de Dados

**P: Meus dados são seguros?**

R: Sim, a plataforma:

- ✅ Usa conexão segura (HTTPS)
- ✅ Não armazena senhas
- ✅ Segue práticas de privacidade
- ✅ Não compartilha dados pessoais com terceiros

---

## Próximos passos

- [Busca Básica](./search-basics.md) - Começa aqui
- [Operadores de Busca](./search-operators.md) - Aprenda técnicas
- [Busca Avançada](./advanced-search.md) - Buscas mais precisas

---

**Última atualização:** Junho de 2024
