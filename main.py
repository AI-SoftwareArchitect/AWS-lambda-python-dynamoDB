import json
import boto3
from botocore.exceptions import ClientError

# DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('UserVisits')  # DynamoDB tablosu

def lambda_handler(event, context):
    try:
        # JSON body parse et (API Gateway proxy entegrasyonunda body string gelir)
        body = json.loads(event.get("body") or "{}")
        name = body.get("name", "Dünya")

        # DynamoDB'ye kullanıcı ziyaret sayısını arttır
        visit_count = update_visit_count(name)

        response = {
            "message": f"Merhaba, {name}! AWS Lambda ile gelişmiş serverless API.",
            "visitCount": visit_count
        }

        return {
            "statusCode": 200,
            "body": json.dumps(response),
            "headers": {
                "Content-Type": "application/json"
            }
        }

    except json.JSONDecodeError:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Geçersiz JSON"}),
            "headers": {"Content-Type": "application/json"}
        }
    except ClientError as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Veritabanı hatası", "details": str(e)}),
            "headers": {"Content-Type": "application/json"}
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Bilinmeyen hata", "details": str(e)}),
            "headers": {"Content-Type": "application/json"}
        }

def update_visit_count(name: str) -> int:
    """
    DynamoDB'deki kullanıcı ziyaret sayısını arttırır ve günceller.
    """
    response = table.update_item(
        Key={"UserName": name},
        UpdateExpression="ADD VisitCount :inc",
        ExpressionAttributeValues={":inc": 1},
        ReturnValues="UPDATED_NEW"
    )
    return int(response['Attributes']['VisitCount'])
