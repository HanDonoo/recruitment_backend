# Recruitment Backend

This is the backend server for the recruitment platform. It handles all business logic, data processing, and coordinates interactions with large language models (LLMs). Built with Python FastAPI, the server is containerized and deployed on AWS EC2, with Nginx used as a reverse proxy to provide secure HTTPS access.

## Technology Stack

- **Backend Framework:** Python FastAPI  
- **Deployment:** AWS EC2  
- **Reverse Proxy:** Nginx (for HTTPS and routing)  
- **Database:** (MySQL)  
- **LLM Integration:** External API or self-hosted LLM services  

## Features

- Robust REST API endpoints to serve frontend requests  
- Business logic for job posting, candidate assessment, and recommendation  
- Integration with AI LLM services for CV scoring and recommendations  
- Secure and scalable deployment with Ec2 and Nginx  
- Database interaction via ORM (e.g., SQLAlchemy)  

## Getting Started

### Prerequisites

- Python 3.10  
- AWS EC2 instance
- Nginx (for reverse proxy configuration)  

### Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/HanDonoo/recruitment_backend.git
cd recruitment_backend
pip install -r requirements.txt
```
### Running Locally

```bash
uvicorn app.main:app --reload  --port 8080 
```
