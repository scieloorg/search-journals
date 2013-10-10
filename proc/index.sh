#!/bin/sh
# Index shell script

scriptpath=$0

case $scriptpath in 
 ./*)  SCRIPT_PATH=`pwd`;;
  * )  SCRIPT_PATH=`dirname $scriptpath`
esac

INICIO=`date`

if [ "$#" -ne 3 ]
then   
   echo "solr index" 
   echo "Uso:     index.sh <arquivo xml> <server> <indice>"
   echo 
   echo "Exemplo: index.sh example.xml localhost solr/scielo-articles"
   echo
   exit
fi

XML=${1}
SERVER=${2}
INDEX=${3}
PORT="8080"

echo "Indexing ${XML} in ${INDEX} on server ${SERVER}: $INICIO" 

curl -d @${XML} -X POST http://${SERVER}:${PORT}/${INDEX}/update -H "Content-Type: text/xml; charset=utf-8"

FINAL=`date`

echo "Finished index of ${XML} in ${INDEX}: $FINAL" 


