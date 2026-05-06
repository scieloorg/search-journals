# Migração para PHP moderno

## Alvo

O alvo inicial de compatibilidade é PHP 8.5, a versão estável mais nova da
família PHP no momento desta migração.

## Estado atual

O runtime principal ainda usa Ubuntu 14.04, Apache e PHP 5. O primeiro passo
foi manter esse runtime funcionando e adicionar verificações que também rodam
contra PHP 8.5.

O código próprio da aplicação, excluindo `iahx/lib/silex/vendor`, passa no
lint de sintaxe com PHP 8.5:

```bash
npm run compat:php85
```

## Bloqueio conhecido

As dependências vendorizadas ainda não são compatíveis com PHP 8.5. O primeiro
erro de parse aparece em Swiftmailer antigo:

```text
iahx/lib/silex/vendor/swiftmailer/swiftmailer/lib/classes/Swift/Transport/AbstractSmtpTransport.php
```

O problema específico é acesso a caractere de string com chaves, como
`$line{3}`, sintaxe removida nas versões modernas do PHP.

## Dependências legadas

As versões atuais estão em `iahx/lib/silex/composer.json`:

```json
{
  "silex/silex": "1.*",
  "twig/twig": ">=1.2.0,<2.0-dev",
  "symfony/twig-bridge": "2.1.*",
  "swiftmailer/swiftmailer": "4.1.*"
}
```

Essas dependências são o maior bloqueio para trocar o container da aplicação
para PHP 8.5. A próxima etapa deve substituir o bootstrap Silex/Twig/Swift por
dependências modernas instaladas via Composer no nível do projeto, sem editar o
vendor antigo manualmente.

## Alvo de dependências modernas

O arquivo `composer.modern.json` define um alvo separado para a migração. Ele
não altera o runtime PHP 5 atual e instala dependências em `vendor-modern`.

O conjunto inicial substitui:

* Silex 1 por componentes Symfony 7 de HTTP, Kernel e Routing.
* Twig 1 por Twig 3.
* Swiftmailer 4 por Symfony Mailer/Mime 7.

Esse manifesto deve ser usado para construir o novo bootstrap antes de remover
`iahx/lib/silex/vendor`.
