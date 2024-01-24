# <p align="center">SentiMail</p>
  
The expert in malicious email detection

**=> Voir le dossier docs pour avoir la documentation du projet.**

build-push-check-action : https://forge.cpe.granux.fr/thomas.violent/build-push-check-action

## 📝 Table of Contents

- [Features](#features)
- [Tech Stack](#tech_stack)
- [Getting Started](#getting_started)
- [API Documentation](#api_documentation)
- [Authors](#authors)

# Features <a name = "features"></a>
SentiMail performs three types of analyses on the email:

### Metadata Analysis
- Analysis of the sender's IP
- Analysis of the sender's domain
- Analysis of the sender domain's SPF
### Email Content Analysis
- Link analysis
- Spelling analysis
- Keyword analysis
- Typo-squatting analysis
- Unusual characters analysis
### Attachments Analysis
- Analysis of attachment hashes
- Analysis of attachment file types
  
For more informations about the technical specifications, please refer to the [technical specifications](docs/specifications_techniques.md).
For more informations about the security plan, please refer to the [security plan](docs/plan_securisation.md).
# Tech Stack <a name = "tech_stack"></a>

## Backend
- <a href="https://www.djangoproject.com/" target="_blank" rel="noreferrer"> <img src="https://cdn.worldvectorlogo.com/logos/django.svg" alt="django" width="40" height="40"/> Django</a>
- <a href="https://www.django-rest-framework.org/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/encode/django-rest-framework/master/docs_theme/img/favicon.ico" alt="django-rest-framework" width="40" height="40"/> Django REST Framework</a>
- <a href="https://www.rabbitmq.com" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/rabbitmq/rabbitmq-icon.svg" alt="rabbitMQ" width="40" height="40"/> RabbitMQ</a>
- <a href="https://www.postgresql.org/" target="_blank" rel="noreferrer"> <img src="https://www.postgresql.org/media/img/about/press/elephant.png" alt="postgresql" width="40" height="40"/> PostgreSQL</a>
- <a href="https://min.io/" target="_blank" rel="noreferrer"> <img src="https://min.io/resources/img/logo.svg" alt="minio" width="40" height="40"/> Minio</a>

## Infrastructure
- <a href="https://www.docker.com/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/docker/docker-original-wordmark.svg" alt="docker" width="40" height="40"/> Docker </a> 
- <a href="https://kubernetes.io" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/kubernetes/kubernetes-icon.svg" alt="kubernetes" width="40" height="40"/> Kubernetes</a>
- <a href="https://traefik.io/traefik/" target="_blank" rel="noreferrer"> <img src="https://docs.traefik.io/assets/img/traefik.logo.png" alt="traefik" width="40" height="40"/> Traefik</a>
- <a href="https://crowdsec.net/" target="_blank" rel="noreferrer"> <img src="https://github.com/crowdsecurity/crowdsec-docs/raw/main/crowdsec-docs/static/img/crowdsec_no_txt.png" alt="crowdsec" width="40" height="40"/> CrowdSec</a>
- <a href="https://www.sonarqube.org/" target="_blank" rel="noreferrer"> <img src="https://assets-eu-01.kc-usercontent.com/c35a8dfe-3d03-0143-a0b9-1c34c7b9b595/12e3974b-220d-4cde-8f17-2ff9fa9d9c27/SonarQube_Logo.svg" alt="sonarqube" width="40" height="40"/> SonarQube</a>
- <a href="https://goharbor.io/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/goharbor/harbor/main/docs/img/harbor_logo.png" alt="harbor" width="40" height="40"/> Harbor</a>







# Getting Started <a name = "getting_started"></a>
## 🛠️ Run locally 
- Clone the repository
- Copy the `sample.env` file to `.env` and fill in the variables
- Run `docker compose up -d --build`
- Open `http://localhost:8000` in your browser


# API Documentation <a name = "api_documentation"></a>

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

## Get email analysis for authenticated user

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

## Get email analysis for anonymous user
```http
GET /api/result/<uuid>/
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
curl --location 'http://<ip>/api/result/1574c5a7-2860-4659-a538-6210d074fb3d' \
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


        
## 🙇 Author <a name = "authors"></a> 
#### Thomas Genin
#### Nicola Piemontese
#### Valentin Tournier
#### Thomas Violent

        