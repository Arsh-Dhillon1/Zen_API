# Zen Journal API 🧘

A FastAPI-based journal API deployed on AWS using a private EC2 instance and Amazon RDS MySQL.

The project started as a simple FastAPI application using SQLite and was later migrated to a cloud-based AWS architecture.

---

## 🏗️ Current Architecture

```text
                         AWS VPC
                            │
             ┌──────────────┴──────────────┐
             │                             │
        Public Subnet                 Private Subnet
             │                             │
      ┌──────────────┐              ┌──────────────┐
      │ Bastion Host │───── SSH ───▶│  Zen API EC2 │
      └──────────────┘              │   FastAPI    │
                                    │ Uvicorn :8000│
                                    └──────┬───────┘
                                           │
                                      MySQL :3306
                                           │
                                           ▼
                                    ┌──────────────┐
                                    │  Amazon RDS  │
                                    │    MySQL     │
                                    └──────────────┘
```

### Current AWS Components

- Amazon VPC
- Public subnet containing the Bastion Host
- Private subnet containing the Zen API EC2 instance
- Amazon RDS MySQL for persistent database storage
- Security Groups controlling communication between components
- SSH access through the Bastion Host

> **Note:** An Application Load Balancer has not been implemented yet.

---

## 🚀 Features

The API currently supports:

- Create journal entries
- Retrieve all journal entries
- Retrieve a journal entry by ID
- Update journal entries
- Delete journal entries
- Mood categorization
- Persistent storage using MySQL

### Supported Moods

- `happy`
- `calm`
- `sad`
- `angry`
- `anxious`
- `grateful`
- `excited`
- `neutral`

---

## 🛠️ Tech Stack

| Category | Technologies |
|---|---|
| Backend | Python, FastAPI, Pydantic |
| ORM | SQLAlchemy |
| Server | Uvicorn |
| Database | SQLite → MySQL |
| Cloud | Amazon EC2, Amazon RDS |
| Networking | Amazon VPC, Subnets, Security Groups |
| Access | Bastion Host, SSH |

---

## 📁 Project Structure

```text
Zen_API/
└── app/
    ├── main.py
    ├── database.py
    └── venv/
```

### `main.py`

Contains the FastAPI application, API endpoints, Pydantic models, and SQLAlchemy database models.

### `database.py`

Handles the SQLAlchemy engine, database sessions, and database configuration.

---

## 🗄️ Database

The application originally used SQLite and was later migrated to MySQL on Amazon RDS.

The database contains:

- `users`
- `journals`

The relationship between the tables is:

```text
users
  │
  │ 1
  │
  │ *
journals
```

Each journal entry references a user through the `user_id` foreign key.

---

## 🔄 SQLite → MySQL Migration

The application's persistence layer was migrated from SQLite to Amazon RDS MySQL.

The migration involved:

1. Creating the RDS MySQL database
2. Connecting the private EC2 instance to RDS
3. Updating the application's database configuration
4. Creating the required tables in RDS
5. Migrating existing application data

The original SQLite database was preserved as the source database.

---

## ☁️ AWS Deployment

### VPC

The application is deployed inside an AWS VPC with separate public and private subnets.

```text
VPC
├── Public Subnet
│   └── Bastion Host
│
└── Private Subnet
    ├── Zen API EC2
    └── RDS MySQL
```

### Bastion Host

The Bastion Host is located in the public subnet and provides SSH access to the private Zen API EC2 instance.

```text
Developer Laptop
       │
       │ SSH
       ▼
Bastion Host
       │
       │ SSH
       ▼
Private Zen API EC2
```

### Zen API EC2

The FastAPI application runs on an EC2 instance inside the private subnet.

The application listens on port `8000`.

The EC2 instance does not have a public IPv4 address.

### Amazon RDS

Amazon RDS MySQL provides persistent database storage.

The database is accessible from the Zen API EC2 instance through MySQL port `3306`.

Database credentials are provided through the `DATABASE_URL` environment variable.

---

## 🔐 Security

- Application EC2 is deployed in a private subnet
- RDS is not publicly exposed
- Bastion Host is used for SSH access
- Security Groups control traffic between components
- Database credentials are stored using environment variables
- Private keys and credentials are not committed to Git

---

## ▶️ Running the API

Activate the virtual environment:

```bash
source venv/bin/activate
```

Start the application:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

FastAPI Swagger documentation is available at:

```text
/docs
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/journals` | Get all journals |
| `GET` | `/journals/{journal_id}` | Get a journal |
| `POST` | `/journals` | Create a journal |
| `PUT` | `/journals/{journal_id}` | Update a journal |
| `DELETE` | `/journals/{journal_id}` | Delete a journal |

### Example Request

```json
{
    "content": "I am staying consistent with my engineering journey",
    "mood": "happy"
}
```

---

## 📚 What I Learned

- Building REST APIs with FastAPI
- Pydantic data validation
- SQLAlchemy ORM
- Relational database design
- Foreign keys
- SQLite → MySQL migration
- AWS VPC networking
- Public vs private subnets
- Bastion Host architecture
- EC2 deployment
- Amazon RDS
- Security Groups
- Environment-based configuration
- SSH access to private infrastructure
- Separation of application and database layers