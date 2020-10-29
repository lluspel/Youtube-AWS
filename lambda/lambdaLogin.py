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
            
            intento = -1
            cur.execute("SELECT usuario FROM usuarios WHERE usuario='" +
                event['queryStringParameters']['usuario']+
                "' AND pwd='" + event['queryStringParameters']['pwd']+
                "' AND habilitado = 1")
            conn.commit()
            for row in cur:
                cur.execute("UPDATE usuarios SET intento = 3 WHERE usuario='"
                        + event['queryStringParameters']['usuario']+
                        "' AND habilitado = 1")
                conn.commit()
                return {'statusCode': 200,
                    'headers': { 'Access-Control-Allow-Origin' : '*' },
                    'body':json.dumps({ 'accesoConcedido' :  1 })}
            
            cur.execute("SELECT intento FROM usuarios WHERE usuario='"+
            event['queryStringParameters']['usuario']+
            "' AND habilitado = 1")
            conn.commit()
            for row in cur:
                intento = int(row[0]) -1
            if (intento == 0 ):
                cur.execute("UPDATE usuarios SET habilitado = 0 WHERE usuario = '"
                    + event['queryStringParameters']['usuario']+
                    "' AND habilitado = 1")
                conn.commit()
                return {'statusCode': 200,
                    'headers': { 'Access-Control-Allow-Origin' : '*' },
                    'body':json.dumps({ 'accesoConcedido' :  -1 })} 
                    # Deshabilitacion de la cuenta
            if (intento > 0):
                cur.execute("UPDATE usuarios SET intento = "+ str(intento) +" WHERE usuario='"
                        + event['queryStringParameters']['usuario']+
                        "' AND habilitado = 1")
                conn.commit()
                return {'statusCode': 200,
                    'headers': { 'Access-Control-Allow-Origin' : '*' },
                    'body':json.dumps({ 'accesoConcedido' :  -2 })}
                    # Un intento menos
    except pymysql.MySQLError as e:
        print (e)
        sys.exit()
    
    return {'statusCode': 200,
            'headers': { 'Access-Control-Allow-Origin' : '*' },
            'body':json.dumps({ 'accesoConcedido' :  0 })}
    
