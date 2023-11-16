# graphql-dynamodb-backend and client

## Graphql API

#### Pre-requisites:

    python3.8

    pip install graphene==2.1.8 Flask==3.0.0 Flask-GraphQL==2.0.0 boto3=1.29.0

    Please replace your own AWS region, secret access key, account key id in migrate.py , schema.py

#### schema.py

    access_key_id = 'ACCESS_KEY_ID'
    secret_access_key = 'SECRET_ACCESS_KEY'
    region_name = "REGION"

#### migrate.py

    access_key_id = 'ACCESS_KEY_ID'
    secret_access_key = 'SECRET_ACCESS_KEY'
    region_name = "REGION"

#### Run API
- cd graphql-lambda
- python manage.py

    Backend url is http://localhost:5000

## Client

#### Environment
- node 18.16.0

#### Set Graphql API URL
- You can change Graphql API URL in /client/src/App.js

- Default value of API_URL is localhost:5000

            const httpLink = new HttpLink({
                uri: "http://API_URL/graphql",
            });

            const wsLink = new WebSocketLink({
                uri: "ws://API_URL/graphql",
                options: {
                    reconnect: true,
                },
            });
#### Run
- cd client
- yarn install
- npm run start
