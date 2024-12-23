# Veteran+

## Description

**Veteran+** is the project aimed to provide comprehensive assistance to Ukrainian war veterans.
We offer access to crucial resources such as grants, support programs, rehabilitation services, and retraining
opportunities.
Our mission is to help veterans find the information and support they need, facilitating their recovery and
reintegration into civilian life.

## Usage

### Local

1. Run setup script to install the app dependencies.

```bash
./local_setup.sh
```

2. Fill the `.env` with the valid environment variables values.
3. Run the app:

```bash
make app
```

To properly use the Amazon Bedrock chat model you need to configure your
[AWS credentials](https://docs.aws.amazon.com/sdk-for-java/v1/developer-guide/setup-credentials.html).
To use your existing AWS profile credentials set the appropriate env variable: `AWS_PROFILE=<your profile>`

### Docker

For development purposes or not you can go on with dockerized application.
```bash
docker-compose up --build
```

## Useful

### Load data into RAG

To load training data into vector store run this command:

```bash
make load_data file_name=links.txt
```

### Git hooks

To check the code before every commit yourself you may install Git hooks.
All hooks would be installed automatically while running `./local_setup.sh`.

```bash
pre-commit install
```

## Licensing

Copyright (C) Veteran+.

Licensed under the  **EUPL**  (the "License"); you may not use this file except in compliance with the License. Re-use
is permitted, although not encouraged, under the EUPL, with the exception of source files that contain a different
license.

You may obtain a copy of the License
at  [https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12](https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12).

Questions regarding the Veteran+ project, the License and any re-use should be directed
to [viacheslavlab@gmail.com](mailto:viacheslavlab@gmail.com).

## TODO

1. Model switch
2. Parameters change
3. Save history and recent chats to Postgres
4. AWS deployment template
5. Ukrainian translation
6. Add crawler
7. Add embeddings splitter
