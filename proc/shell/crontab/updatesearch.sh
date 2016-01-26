# environment config

# starting virtualenv-wrapper
export SOLR_URL='http://127.0.0.1:8080/solr/scielo-articles'
export WORKON_HOME=/var/www/.virtualenvs
source /usr/bin/virtualenvwrapper.sh

# subindo virtualenv previamente criado.
workon updatesearch

# acessando local onde esta o ambiente de execução do warmup.
cd /var/www/search-journals/proc/updatesearch

# execucao do script
python updatesearch.py

# desativando environment
deactivate