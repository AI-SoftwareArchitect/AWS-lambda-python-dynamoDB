# Serverless AWS Lambda Python API

Basit ve gelişmiş özelliklere sahip AWS Lambda fonksiyonu.

## Özellikler
- JSON input/output
- Hata yönetimi
- DynamoDB ile kullanıcı ziyaret sayısı takibi
- API Gateway proxy entegrasyonu

## Kullanım
1. DynamoDB tablosu oluştur:
```bash
aws dynamodb create-table \
  --table-name UserVisits \
  --attribute-definitions AttributeName=UserName,AttributeType=S \
  --key-schema AttributeName=UserName,KeyType=HASH \
  --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5
