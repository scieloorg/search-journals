if [ "$#" -ne 2 ]
then   
   echo "optimize.sh" 
   echo "Uso:     optimize.sh <server> <index>"
   echo 
   echo "Exemplo: optimize.sh localhost solr/scielo-articles"
   echo
   exit
fi

SERVER=${1}
INDEX=${2}
PORT='8080'

echo "Optimize index..."
curl -X POST http://${SERVER}:${PORT}/${INDEX}/update -H "Content-Type: text/xml; charset=utf-8" --data-binary '<optimize/>'

