import json
import sys
import logging
import pymysql


rds_host = "database-1.cw673evurmzd.us-east-1.rds.amazonaws.com"

username = "admin"
password = "12345678"
dbname = "practica3"

try:
    conn = pymysql.connect(rds_host, user = username, passwd = password, db = dbname, connect_timeout = 5)
except pymysql.MySQLError as e:
    print (e)
    sys.exit()

def lambda_handler(event, context):
    
    url_event= event["queryStringParameters"]["urlArchivo"]
    
    try:
    
        with conn.cursor() as cur:
            
            cur.execute("SELECT usuarioSubio FROM videos WHERE urlArchivo=%s", (url_event))
            usuario=cur.fetchall()
            cur.execute("SELECT nombre FROM videos WHERE urlArchivo=%s", (url_event))
            nombre_arch=cur.fetchall()
            
            cur.execute("DELETE FROM videos WHERE urlArchivo=%s" , (url_event))
            conn.commit()
            

        return {
            'statusCode': 200,
            'headers': { 'Access-Control-Allow-Origin' : '*' },
            'body':json.dumps({"usuarioSubio": usuario, "nombre" : nombre_arch})
        }
        
    except pymysql.MySQLError as e:
        return {
            'statusCode': 200,
            'headers': { 'Access-Control-Allow-Origin' : '*' },
            'body':json.dumps({'accesoConcedido': 0})
        }
    
