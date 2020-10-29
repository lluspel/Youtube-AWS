import sys
import logging
import pymysql
import json


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
    try:
        with conn.cursor() as cur:
            cur.execute("select usuario from usuarios where  usuario='" +
                event['queryStringParameters']['usuario']+
                "' and email='" + event['queryStringParameters']['email']+"'")
            conn.commit()
            for row in cur:
                print ('existe')
                return {'statusCode': 200,
                    'headers': { 'Access-Control-Allow-Origin' : '*' },
                    'body':json.dumps({ 'accesoConcedido' :  -1 })} # ya existe este usuario
                    
            cur.execute("INSERT INTO usuarios (nombreCompleto, usuario, email, pwd, recupPwd, intento, habilitado) VALUES ('"
                + event['queryStringParameters']['nombreCompleto']+"', '"
                + event['queryStringParameters']['usuario']+"', '"
                + event['queryStringParameters']['email']+"', '"
                + event['queryStringParameters']['pwd']+"', '"
                + event['queryStringParameters']['recupPwd']+"', 3, 1)")
            conn.commit()
            cur.execute("select usuario from usuarios where usuario='" +
                event['queryStringParameters']['usuario']+
                "' and email='" + event['queryStringParameters']['email']+"'")
            conn.commit()
            for row in cur:
                return {'statusCode': 200,
                    'headers': { 'Access-Control-Allow-Origin' : '*' },
                    'body':json.dumps({ 'accesoConcedido' :  1 })} # ya lo hemos creado
    except pymysql.MySQLError as e:
        print (e)
        sys.exit()

    return {'statusCode': 200,
                    'headers': { 'Access-Control-Allow-Origin' : '*' },
                    'body':json.dumps({ 'accesoConcedido' :  0 })}
