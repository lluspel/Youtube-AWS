import json
import boto3
    
    
def lambda_handler(event, context):
    
    try:
        
        usuario=event["queryStringParameters"]["usuarioSubio"]
        archivo=event["queryStringParameters"]["nombre"]
        
        bucket="calculadora12"
        
        ruta='usuarios/' + usuario + '/' + archivo
        
        s3 = boto3.resource("s3")
        s3.Object(bucket, ruta).delete()
        
        
        return {
            'statusCode': 200,
            'headers': { 'Access-Control-Allow-Origin' : '*' },
            'body':json.dumps({ 'accesoConcedido' :  str("True")})
        }
            
    except Exception as E:
        return {
            'statusCode': 200,
            'headers': { 'Access-Control-Allow-Origin' : '*' },
            'body':json.dumps({ 'accesoConcedido' :  str(E)})
        }