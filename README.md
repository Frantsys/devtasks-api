# DevTasks API

> API REST para gerenciamento ágil de tarefas com suporte a equipes, projetos e sprints.

---

## Stack

| Componente       | Tecnologia                              |
|------------------|-----------------------------------------|
| Framework        | Python 3.11+ - Django 4.2 - DRF 3.15    |
| Autenticação     | djangorestframework-simplejwt           |
| Documentação     | drf-spectacular (Swagger/OpenAPI)       |
| Variáveis de env | python-decouple                         |
| Cache            | Redis (fallback: LocMemCache)           |
| Filtros          | django-filter                           |
| Banco de dados   | PostgreSQL (fallback: SQLite3)          |

---

## Documentação

| URL              | Descrição                  |
|------------------|----------------------------|
| `/api/docs/`     | Swagger UI                 |
| `/api/redoc/`    | ReDoc                      |
| `/api/schema/`   | OpenAPI JSON/YAML          |
| `/admin/`        | Django Admin               |

---

## Endpoints

### Autenticação

```
POST  /api/v1/auth/token/         Obter acesso + refresh token
POST  /api/v1/auth/token/refresh/ Renovar acesso token
```

### Recursos (CRUD completo)

```
GET|POST              /api/v1/users/
GET|PUT|PATCH|DELETE  /api/v1/users/{id}/
GET                   /api/v1/users/me/

GET|POST              /api/v1/teams/
GET|PUT|PATCH|DELETE  /api/v1/teams/{id}/

GET|POST              /api/v1/team-members/
GET|PUT|PATCH|DELETE  /api/v1/team-members/{id}/

GET|POST              /api/v1/tasks/
GET|PUT|PATCH|DELETE  /api/v1/tasks/{id}/

GET|POST              /api/v1/sprints/
GET|PUT|PATCH|DELETE  /api/v1/sprints/{id}/

GET|POST              /api/v1/projects/
GET|PUT|PATCH|DELETE  /api/v1/projects/{id}/
```

### Query Params de filtro

| Endpoint           | Parâmetros disponíveis                                       |
|--------------------|--------------------------------------------------------------|
| `/users/`          | `search`, `group`, `is_active`, `email`, `username`          |
| `/teams/`          | `search`, `sector`                                           |
| `/team-members/`   | `team` (UUID), `user` (UUID), `role`, `search`               |
| `/tasks/`          | `search`, `status`, `priority`, `title`                      |
| `/sprints/`        | `search`, `status`, `start_date_after`, `end_date_before`    |
| `/projects/`       | `search`, `status`, `title`                                  |

---