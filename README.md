# Hackathon Platform

Platform for organisers and participants to host and participate in hackathons.

## Features

- Buillt a REST API using Django REST Framework.
- Swagger implemented OpenAPI3 for API documentation.
- Containerized application(services) using Docker.
- Created djnago permission groups of Organisers and Participants.
- Only Organiser can create a hackathon.
- Organiser can view all the projects submitted for a hackathon.
- Organiser can view all the participants registered for a hackathon.
- Hackathon can specify the type of submit( file, image or link)
- Particapants can register for a hackathon.
- Particiapnts can submit their projects for a hackathon.
- Particapants can view all the hackathons they have registered for.
- Particapants can view all submissions of hackathons they have registered for.

## Built With

- [Django REST Framework](https://www.django-rest-framework.org)
- [PotgreSQL as RDS](https://www.postgresql.org)

## Database Design
![Database schema](https://raw.githubusercontent.com/Biswal21/Hackathon-portal/main/readme-asset/Hackathon%20Portal.png)

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [docker-compose](https://docs.docker.com/compose/install/)

## Installation and Usage
1. Clone this repository and change directory.

```bash
git https://github.com/Biswal21/Hackathon-portal.git
cd Hackathon-portal
```

2. Run the following command to **build** and **run** all the containers for the first time.

```bash
docker-compose up --build
```

3. Run the following command to **run** all the containers for subsequent times.

```bash
docker-compose up
```

## 


4. Visit API documentation at
   - Development `localhost:8000/docs`
   - Production: [production docs](https://hack-port.fly.dev/docs/)
5. Visit Server Admin
   - Development: `localhost:8000/admin/`
   - Production: `[production admin](https://hack-port.fly.dev/admin/) 

## Note

- Admin user with username as **_admin_** and password as **_admin_** is created.

### Note for Production Credentials

- Check `admin` credentials in **google form response** last question's answer.
- Check `organiser` credentials in **google form response** last question's answer.
- Check `participant` credentials in **google form response** last question's answer.
