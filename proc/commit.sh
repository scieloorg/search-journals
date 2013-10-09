if [ "$#" -ne 2 ]
then   
   echo "commit.sh" 
   echo "Uso:     commit.sh <server> <index>"
   echo 
   echo "Exemplo: commit.sh localhost solr/scielo-articles"
   echo
   exit
fi

SERVER=${1}
INDEX=${2}
PORT='8080'

echo "Commit index ${INDEX}"

curl http://${SERVER}:${PORT}/${INDEX}/update -H "Content-Type: text/xml"  --data-binary '<commit waitSearcher="false"/>'

