# AWS Production Migration Strategy (Call Center Context)

This document outlines the transition from the local CrewAI + RAG prototype to a production-grade, secure Enterprise Architecture on AWS.

## Executive Summary
The goal is to move from a local Python environment using Gemini and ChromaDB to a scalable, secure, and compliant architecture utilizing AWS serverless and managed services. This transition ensures data privacy, high availability, and the ability to process millions of compliance logs.

---

## 🏗️ Technical Component Migration

### 1. Compute: AWS Fargate
- **Local**: Python scripts running on local machines.
- **Production**: Deploy the CrewAI application as containerized microservices on **AWS Fargate** (Serverless Containers).
- **Why**: Fargate removes the need to manage EC2 instances while providing isolated, long-running environments for agent tasks.

### 2. Orchestration: AWS Step Functions
- **Strategy**: While CrewAI manages internal agent collaboration, **AWS Step Functions** should be used for the high-level workflow orchestration (e.g., triggering the audit, handling retries, and integrating with external Call Center APIs).
- **Implementation**: Keep CrewAI for the "intelligence" layer and use Step Functions to manage the end-to-end business process.

### 3. Vector Database: Amazon Aurora PostgreSQL (with pgvector)
- **Local**: ChromaDB.
- **Production**: Migrate to **Amazon Aurora PostgreSQL with pgvector extension**.
- **Justification**: 
  - **Scale**: Aurora is optimized for handling **millions of embeddings** with high-performance indexing.
  - **Enterprise Grade**: Provides multi-AZ reliability, automated backups, and unified storage with traditional metadata, avoiding the complexity of syncing a standalone vector store with a primary database.

### 4. LLM Layer: AWS Bedrock (Claude 3.5 Sonnet)
- **Local**: Google Gemini (LiteLLM).
- **Production**: Switch to **AWS Bedrock** utilizing **Claude 3.5 Sonnet**.
- **Compliance**: Bedrock ensures that data processing stays within the AWS ecosystem, providing the SOC, ISO, and HIPAA compliance required for financial and secure call center operations.

### 5. Security & Compliance
- **Secrets Management**: Use **AWS Secrets Manager** to store API keys and database credentials securely.
- **Identity & Access Management (IAM)**:
  - Assign **IAM Roles** to Fargate tasks with narrow permissions.
  - Specifically ensure `bedrock:InvokeModel` permissions are strictly controlled.
- **Data Privacy**: By using Bedrock with VPC Endpoints, **data remains within the VPC**, ensuring PII (Personally Identifiable Information) never traverses the public internet—a critical requirement for Call Center compliance audits.

### 6. CI/CD Pipeline: AWS CodePipeline
- **Flow**: Source (GitHub/CodeCommit) → Build (CodeBuild - containerizing the app) → Deploy (ECS/Fargate).
- **Quality Gates**: Automate unit tests and agent logic validation before deployment.

---

## 📈 Next Steps
1. Dockerize the current Python application.
2. Provision Infrastructure using Terraform or AWS CDK.
3. Configure VPC and Security Groups for database and compute isolation.
