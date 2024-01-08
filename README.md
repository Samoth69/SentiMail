# <p align="center">SentiMail</p>
  
L'expert de la détection de mail malveillant
    

## 🛠️ Install     
```bash
TO DO
```


# API Documentation

## Authentication
- Generate a new API key
- Use the API key in the header of your request:
  - Key: `Authorization`
  - Value: `Token <API_KEY>`

## Submit email
```http
POST /api/submit/
```
### Request:

Content-Type: multipart/form-data
Body:
  - Key: `file`
  - Value: `<mail_file>`
  
### Response:
| Code | Description                |
| :-------- | :------------------------- |
| `200`   | **OK**    |
| `400`  | **Bad Request**   |
| `401`| **Unauthorized** |
| `500`| **Internal Server Error** |

### Request sample:
```bash
curl --location 'http://<ip>/api/submit/' \
--header 'Authorization: Token <API_KEY>' \
--form 'file=@"</path/mail_file>"'
```

### Response sample (200 OK):
```json
{
    "uuid": "1574c5a7-2860-4659-a538-6210d074fb3d"
}
```

## Get email analysis
```http
GET /api/analysis/<uuid>/
```

### Response:
| Code | Description                |
| :-------- | :------------------------- |
| `200`   | **OK**    |
| `400`  | **Bad Request**   |
| `401`| **Unauthorized** |
| `404`| **Not Found** |
| `500`| **Internal Server Error** |

### Request sample:
```bash
curl --location 'http://<ip>/api/analysis/1574c5a7-2860-4659-a538-6210d074fb3d' \
--header 'Authorization: Token 27cdb16b2189fdc09f008fd901f54306f155697a'
```

### Response sample (200 OK):
```json
{
    "uuid": "1574c5a7-2860-4659-a538-6210d074fb3d",
    "created_at": "2023-12-14T10:41:45.989923Z",
    "user": "anonymous",
    "isReady": false,
    "responseMetadataIp": "IP is not malicious",
    "responseMetadataDomain": "Mail is not malicious",
    "responseMetadataSPF": "SPF record is valid"
}
```

## Update email analysis
```http
PATCH /api/analysis/<uuid>/
```

### Response:
| Code | Description                |
| :-------- | :------------------------- |
| `200`   | **OK**    |
| `400`  | **Bad Request**   |
| `401`| **Unauthorized** |
| `404`| **Not Found** |
| `500`| **Internal Server Error** |

### Request sample:
```bash
curl --location --request PATCH 'http://<ip>/api/analysis/0b3cf9d0-fcb3-4bf6-9a29-33abcaab4826/' \
--header 'Content-Type: application/json' \
--header 'Authorization: Token 27cdb16b2189fdc09f008fd901f54306f155697a' \
--data '{
    "responseMetadataIp": "IP not found in database",
    "responseMetadataDomain": "Mail is not malicious",
    "responseMetadataSPF": "SPF record is invalid"
}'
```

### Response sample (200 OK):
```json
{
    "uuid": "0b3cf9d0-fcb3-4bf6-9a29-33abcaab4826",
    "created_at": "2023-12-14T10:41:45.989923Z",
    "user": "anonymous",
    "isReady": false,
    "responseMetadataIp": "IP not found in database",
    "responseMetadataDomain": "Mail is not malicious",
    "responseMetadataSPF": "SPF record is invalid"
}
```


        
## 🙇 Author
#### Thomas Genin
#### Nicola Piemontese
#### Valentin Tournier
#### Thomas Violent

        