# Wikipedia Annotator Platform

Platform for helping people make datasets for NLP translation by using Wikipedia article summaries from it's API.

## Features

- Buillt a REST API using Django REST Framework.
- Swagger implemented OpenAPI3 for API documentation.
- Containerized application(services) using Docker.
- Implement frontend using ReactJS with ChakraUI.
- Created djnago permission groups of Manager and Annoator
- Only Manager can create Projects and import summary from WikipediaAPI.
- Add Languages on the fly which are supported by React transliterate.
- Assign annotator to project.
- User can only see projects assigned to them or created by them.
- Onl yManagers can perform project status change.
- Update and save sentence translations.
- Ability to create multiple projects.
- Implemented React-Transliterate.
- Intuitive UI for user to understand Topic of project and language to be annotated.

## Built With

- [Django REST Framework](https://www.django-rest-framework.org)
- [PotgreSQL as RDS](https://www.postgresql.org)
- [ReactJS in Typescript](https://reactjs.org)
- [ChakraUI](https://chakra-ui.com)

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [docker-compose](https://docs.docker.com/compose/install/)

## Installation and Usage

1. Clone this repository and change directory.

```bash
git https://github.com/Biswal21/WikiAnnotator.git
cd WikiAnnotator
```

2. Run the following command to **build** and **run** all the containers for the first time.

```bash
docker-compose up --build
```

3. Run the following command to **run** all the containers for subsequent times.

```bash
docker-compose up
```

## Deployed server and fronted

5. Visit django-admin at
   development: `localhost:8000/admin/` production: `https://wiki-annot.fly.dev/admin/`
6. Visit frontend at
   - Developement: `localhost:3000` 
   - Production: [production](https://main--gentle-caramel-659bd7.netlify.app/)
7. Visit API documentation at
   - Development `localhost:8000/docs`
   - Production: [production docs](https://wiki-annot.fly.dev/docs/)
8. Visit Server Admin
   - Development: `localhost:8000/admin/`
   - Production: `[production admin](https://wiki-annot.fly.dev/admin/) 

## Note

- Admin user with username as **_admin_** and password as **_admin_** is created.

### Note for Production Credentials

- Check `admin` credentials in **google form response** last question's answer.
- Check `annotator` credentials in **google form response** last question's answer.
- Check `manager` credentials in **google form response** last question's answer.
