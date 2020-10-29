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
            cur.execute("SELECT usuario FROM usuarios WHERE email='" +
                event['queryStringParameters']['email']+
                "' AND recupPwd='" + event['queryStringParameters']['recupPwd']+"'")
            conn.commit()
            for row in cur:
                return {'statusCode': 200,
                    'headers': { 'Access-Control-Allow-Origin' : '*' },
                    'body':json.dumps({ 'accesoConcedido' :  1})}
    except pymysql.MySQLError as e:
        print (e)
        sys.exit()

    return {'statusCode': 200,
            'headers': { 'Access-Control-Allow-Origin' : '*' },
            'body':json.dumps({ 'accesoConcedido' :  0 })}
