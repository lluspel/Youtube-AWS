import sys
import logging
import pymysql
import json
import time


rds_host = "database-1.cw673evurmzd.us-east-1.rds.amazonaws.com"

username = "admin"
password = "12345678"
dbname = "practica3"

date = time.strftime("%y-%m-%d")

try:
    conn = pymysql.connect(rds_host, user = username, passwd = password, db = dbname, connect_timeout = 5)
except pymysql.MySQLError as e:
    print (e)
    sys.exit()
    
def lambda_handler(event, context):
    try:
        with conn.cursor() as cur:
            existe = 0 # no
            cur.execute("SELECT * FROM videos WHERE urlArchivo='"+ event['queryStringParameters']['urlArchivo'] +"'")
            conn.commit()
            for row in cur:
                existe = 1
                
            if (existe == 0):
                cur.execute("INSERT INTO videos(usuarioSubio, etiqueta, tamanio, fechaSubido, urlArchivo, nombre) VALUES ('"
                + event['queryStringParameters']['usuarioSubio'] +"','"
                + event['queryStringParameters']['etiqueta'] +"','"
                + event['queryStringParameters']['tamanio'] +"','"
                + date +"','"
                + event['queryStringParameters']['urlArchivo'] +"','"
                + event['queryStringParameters']['nombre'] +"')")
                conn.commit()
                cur.execute("SELECT * FROM videos WHERE urlArchivo='"+ event['queryStringParameters']['urlArchivo'] +"'")
                conn.commit()
                
            if (existe == 1):
                cur.execute("UPDATE videos SET usuarioSubio='"
                + event['queryStringParameters']['usuarioSubio'] +"', etiqueta='"
                + event['queryStringParameters']['etiqueta'] +"', tamanio='"
                + event['queryStringParameters']['etiqueta'] +"', fechaSubido='"
                + date +"' WHERE urlArchivo='"+ event['queryStringParameters']['urlArchivo'] +"'")
                conn.commit()
                
            cur.execute("SELECT * FROM videos WHERE urlArchivo='"+ event['queryStringParameters']['urlArchivo'] +"'")
            conn.commit()
            for row in cur:
                return {'statusCode': 200,
                    'headers': { 'Access-Control-Allow-Origin' : '*' },
                    'body':json.dumps({ 'accesoConcedido' :  1 })} # subido
                    
    except pymysql.MySQLError as e:
        print (e)
        sys.exit()

    return {'statusCode': 200,
            'headers': { 'Access-Control-Allow-Origin' : '*' },
            'body':json.dumps({ 'accesoConcedido' :  0 })}