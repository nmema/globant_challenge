# Globant's Data Engineer Challenge

## Architecture

<p align="center">
  <img src="/docs/images/architecture.png"/>
</p>

## Process

1. I used a Amazon RDS for Postgresql to create the tables used in the challenge.
2. I created the secrets such as the database parameters using AWS Secrets Manager.
3. Once a development was ready to test it out, I created and image using `docker build -t <tag> .` and uploaded it to ECR. [This guide](https://docs.aws.amazon.com/AmazonECR/latest/userguide/docker-push-ecr-image.html) was helpful to achieve it.
4. I used ECS to launch Fargate, creating a Task Definition and the running a service on a cluster.
5. If everything worked correctly, I commited the changes to the repo.
6. Repeated step 3 to 5.

## TODO
- Add an API Token to restric access.
- Add tests.
- Use Python CDK to automate deployment.
- Use Github Actions for CI.
- My original idea was to save an CSV file into S3, then Lambda function would be triggered passing the S3 URL to the API & upload the file to the database. It would be a nice to have.
