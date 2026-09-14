# Zen Journal API 🧘

A production-oriented backend project built with **FastAPI**, **SQLAlchemy**, **Amazon EC2**, and **Amazon RDS**.

The project started as a simple FastAPI application using SQLite and was later deployed to AWS with a private EC2 instance and a managed MySQL database on Amazon RDS.

---

## 🏗️ Current Architecture

```text
                    AWS VPC
              ┌─────────────────┐
              │                 │
Internet ──→  │ Bastion Host    │
              │ Public Subnet   │
              │                 │
              └────────┬────────┘
                       │ SSH
                       ▼
              ┌─────────────────┐
              │   Zen API EC2   │
              │  Private Subnet │
              │                 │
              │ FastAPI         │
              │ Uvicorn :8000   │
              └────────┬────────┘
                       │
                       │ MySQL :3306
                       ▼
              ┌─────────────────┐
              │   Amazon RDS    │
              │    MySQL        │
              │  Private Subnet │
              └─────────────────┘
Current AWS components
Amazon VPC
Public subnet containing the bastion host
Private subnet containing the Zen API EC2 instance
Amazon RDS MySQL for persistent database storage
Security Groups controlling communication between components
SSH Agent Forwarding / SSH access through Bastion

Note: An Application Load Balancer has not been implemented yet.

🚀 Features

The API currently supports:

Create journal entries
Retrieve all journal entries
Retrieve a journal entry by ID
Update journal entries
Delete journal entries
Mood categorization
Persistent storage using MySQL

Supported moods:

happy
calm
sad
angry
anxious
grateful
excited
neutral
🛠️ Technology Stack
Application
Python
FastAPI
Uvicorn
Pydantic
SQLAlchemy
Database
SQLite — original development database
MySQL — production database
Amazon RDS
Cloud / Infrastructure
Amazon EC2
Amazon VPC
Public and Private Subnets
Bastion Host
Security Groups
Amazon RDS
📁 Project Structure
Zen_API/
│
└── app/
    │
    ├── main.py
    ├── database.py
    └── venv/
main.py

Contains:

FastAPI application
Pydantic request models
SQLAlchemy models
API endpoints
Journal CRUD operations
database.py

Responsible for:

Reading the database connection URL
Creating the SQLAlchemy engine
Creating database sessions
Defining the SQLAlchemy declarative base
🗄️ Database

The application originally used SQLite during development.

The original database contained:

users
journals

The application was later configured to use Amazon RDS MySQL.

The database relationship is:

users
  │
  │ 1
  │
  │
  │ *
journals

Each journal entry contains a user_id foreign key referencing the users table.

🔄 SQLite → MySQL Migration

The project demonstrates moving the application's persistence layer from SQLite to Amazon RDS MySQL.

The migration process involved:

Creating the RDS MySQL database.
Configuring the private EC2 instance to communicate with RDS.
Updating the application's database configuration.
Using SQLAlchemy to create the required tables in RDS.
Migrating the existing application data into the new database.

The original SQLite database was preserved as the source database.

☁️ AWS Deployment
1. VPC

The application runs inside an AWS VPC.

The infrastructure separates public-facing infrastructure from private application/database infrastructure.

VPC
│
├── Public Subnet
│   └── Bastion Host
│
└── Private Subnet
    ├── Zen API EC2
    └── RDS
2. Bastion Host

The bastion host is located in a public subnet and provides SSH access into the private network.

The private Zen API server does not require a public IPv4 address.

Access follows:

Developer Laptop
       │
       │ SSH
       ▼
Bastion Host
       │
       │ SSH
       ▼
Private Zen API EC2
3. Private Zen API Server

The FastAPI application runs on an EC2 instance inside a private subnet.

Uvicorn runs the application on:

0.0.0.0:8000

The EC2 instance is not directly exposed to the public Internet.

4. Amazon RDS

The application uses Amazon RDS MySQL as its persistent database.

The RDS instance is placed inside the VPC and is accessible by the Zen API server through the MySQL port:

3306

The database is protected using a dedicated security group.

The application connects using an environment variable:

DATABASE_URL

This keeps database credentials out of the source code.

🔐 Security

The architecture follows a basic defense-in-depth approach.

EC2

The Zen API server is located in a private subnet and does not require a public IP address.

Bastion

SSH access is performed through a dedicated bastion host.

RDS

RDS is not exposed directly to the Internet.

Only the application server should be able to communicate with the database on:

TCP 3306
Credentials

Database credentials are supplied through environment variables rather than being hardcoded into the application.

Example:

export DATABASE_URL="mysql+pymysql://..."

Never commit database passwords, private keys, or other secrets to Git.

▶️ Running the API

Activate the virtual environment:

source venv/bin/activate

Start Uvicorn:

uvicorn main:app --host 0.0.0.0 --port 8000

The application will then listen on:

http://0.0.0.0:8000

FastAPI's interactive Swagger documentation is available at:

/docs
🔌 API Endpoints
Get all journals
GET /journals
Get a journal
GET /journals/{journal_id}
Create a journal
POST /journals

Example request:

{
  "content": "Today I remained consistent with my goals.",
  "mood": "happy"
}
Update a journal
PUT /journals/{journal_id}
Delete a journal
DELETE /journals/{journal_id}
🧪 Example

A journal entry:

{
  "content": "I am staying consistent with my engineering journey",
  "mood": "happy"
}

is persisted in MySQL through:

FastAPI
   ↓
SQLAlchemy
   ↓
MySQL
   ↓
Amazon RDS
📚 What This Project Demonstrates

This project goes beyond basic CRUD by demonstrating several backend and cloud concepts:

REST API development with FastAPI
Pydantic data validation
SQLAlchemy ORM
Relational database design
Foreign keys
SQLite → MySQL migration
AWS VPC networking
Public vs private subnets
Bastion host architecture
EC2 deployment
Amazon RDS
Security Groups
Environment-based configuration
SSH access to private infrastructure
Separation of application and database layers
🔮 Future Improvements

The current architecture can be extended further.

Planned improvements include:

 Application Load Balancer
 HTTPS using ACM
 Public API access through the Load Balancer
 Multiple API EC2 instances
 Auto Scaling
 Proper user creation/authentication
 Better database migration tooling
 Docker containerization
 CI/CD pipeline
 CloudWatch monitoring and logging
 Production-grade process management
 Infrastructure as Code

A future architecture could look like:

                    Internet
                       │
                       ▼
                ┌──────────────┐
                │     ALB      │
                │ Public       │
                └──────┬───────┘
                       │
             ┌─────────┴─────────┐
             ▼                   ▼
       ┌───────────┐       ┌───────────┐
       │ Zen API   │       │ Zen API   │
       │ EC2       │       │ EC2       │
       │ Private   │       │ Private   │
       └─────┬─────┘       └─────┬─────┘
             │                   │
             └─────────┬─────────┘
                       ▼
                 ┌───────────┐
                 │ RDS MySQL │
                 │ Private   │
                 └───────────┘