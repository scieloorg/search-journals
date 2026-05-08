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

## Container PHP 8.5 paralelo

O arquivo `docker-compose-php85.yml` define um serviço `php85` separado do
runtime PHP 5. Ele usa `Dockerfile-php85` e serve para validações de
compatibilidade enquanto a aplicação ainda roda no container legado.

Comandos úteis:

```bash
npm run compat:php85:version
npm run compat:php85:deps
npm run compat:php85:modern-advanced
npm run compat:php85:modern-app
npm run compat:php85:modern-bootstrap
npm run compat:php85:modern-bookmark
npm run compat:php85:modern-history
npm run compat:php85:modern-http
npm run compat:php85:modern-list-filter
npm run compat:php85:modern-mailer
npm run compat:php85:modern-resource
npm run compat:php85
```

Esse container ainda não substitui o webapp Apache. A troca do runtime depende
da remoção do vendor Silex/Twig/Swiftmailer antigo ou da criação de um novo
bootstrap compatível com Symfony/Twig/Mailer modernos.

## Bootstrap moderno em andamento

`iahx/lib/modern/twig.php` inicia a camada paralela para Twig 3. Ela registra
as mesmas funções e filtros Twig usados pelos templates legados, mas usando as
classes modernas `TwigFunction` e `TwigFilter`.

Essa camada ainda não atende requisições HTTP. Por enquanto, ela é validada por
`tests/php_compat/modern_bootstrap.php`, que garante que o Twig 3 inicializa,
registra extensões e renderiza uma expressão mínima com os helpers existentes.

`iahx/lib/modern/mailer.php` inicia a substituição paralela do Swiftmailer por
Symfony Mailer. O teste `tests/php_compat/modern_mailer.php` reutiliza a
configuração SMTP conceitual do legado e envia uma mensagem real para o MailHog
do Docker pela porta exposta em `localhost:1025`.

`iahx/lib/modern/http.php` inicia a substituição paralela do Silex por
componentes Symfony de HTTP e Routing. A primeira versão mantém a superfície
essencial usada pelas views (`get`, `post`, `match`, `handle` e `run`) para que
as rotas possam ser migradas gradualmente.

`iahx/lib/modern/app.php` monta essas peças em um único objeto de aplicação,
registrando `twig`, `mailer` e `session` como serviços acessíveis por
`$app[...]`. Esse é o ponto de entrada inicial para portar as views sem depender
do container Silex.

`iahx/lib/modern/session.php` cria a sessão moderna via Symfony HttpFoundation.
O adaptador HTTP também cobre `->value(...)`, usado por rotas Silex com
parâmetros opcionais.

`tests/php_compat/modern_bookmark_route.php` é o primeiro teste carregando uma
rota real legada dentro do bootstrap moderno. Ele valida `views/bookmark.php`
com sessão, parâmetros opcionais e respostas Symfony no PHP 8.5.

`tests/php_compat/modern_history_route.php` carrega `views/history.php` no
bootstrap moderno e valida o caminho HTTP + sessão + Twig com uma view real.

`tests/php_compat/modern_advanced_route.php` carrega `views/advanced.php` no
bootstrap moderno e valida renderizacao Twig, sessão e logging no PHP 8.5.

`tests/php_compat/modern_list_filter_route.php` carrega `views/list_filter.php`
no bootstrap moderno com uma implementação fake de `Dia`, validando a rota real
e seu template sem consultar o Solr.

`tests/php_compat/modern_resource_route.php` carrega `views/resource.php` no
bootstrap moderno com uma implementação fake de `Dia`, validando renderização
Twig mobile, sessão e logging sem consultar o Solr.
