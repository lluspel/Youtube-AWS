import sys
import logging
import pymysql
import json
import time
import collections


rds_host = "database-1.cw673evurmzd.us-east-1.rds.amazonaws.com"

username = "admin"
password = "12345678"
dbname = "practica3"


try:
    conn = pymysql.connect(rds_host, user = username, passwd = password, db = dbname, connect_timeout = 5)
except pymysql.MySQLError as e:
    print (e)
    sys.exit()

def query(txt,user):
    query = "SELECT * FROM videos WHERE"
    if (txt):
        lista = txt.split()
        
        
        if (user):
            query+=" usuarioSubio='"+ user+"' AND "
        else:
            query+=" usuarioSubio LIKE '%' AND "
            
        for x in range(len(lista)-1):
            query+= "etiqueta LIKE '%"+lista[x]+"%' OR "
        
        query+= "etiqueta LIKE '%"+lista[-1]+"%'"
        
        return (query)
    else:
        if (user):
            query+=" usuarioSubio='"+ user+"'"
        else:
            query+=" usuarioSubio LIKE '%'"
        
        return (query)
        

def lambda_handler(event, context):
    try:
        with conn.cursor() as cur:
            txt = event['queryStringParameters']['etiqueta']
            user = event['queryStringParameters']['usuarioSubio']
            if(txt):
                print("usuario")
            qry = query(txt,user)
            print(qry)
            cur.execute(qry)
            conn.commit()
            rows = cur.fetchall()
            objects_list = []
            for row in rows:
                d = collections.OrderedDict()
                d['usuarioSubio'] = row[0]
                d['etiqueta'] = row[1]
                d['tamanio'] = row[2]
                d['fechaSubido'] = row[3].strftime("%y-%m-%d")
                d['urlArchivo'] = row[4]
                d['nombre'] = row[5]
                objects_list.append(d)
            return {'statusCode': 200,
                'headers': { 'Access-Control-Allow-Origin' : '*' },
                'body':json.dumps(objects_list )}
            
    except pymysql.MySQLError as e:
        print (e)
        sys.exit()
    
    return {'statusCode': 200,
            'headers': { 'Access-Control-Allow-Origin' : '*' },
            'body':json.dumps({ 'accesoConcedido' :  0 })}
    