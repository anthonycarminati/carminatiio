# eb_deploy_dev.sh
#! /bin/bash

# SET ENVIRONMENT VARIABLES
SHA1=$1
ENV=prod
APPLICATION_NAME=carminatiio
EB_BUCKET=anthonycarminati-carminatiio
# DOCKERRUN_FILE=$SHA1-Dockerrun.aws.json
DOCKERRUN_FILE=Dockerrun.aws.json
echo "Environment Variables have been set successfully"

# DEPLOY IMAGE TO DOCKERHUB
docker push anthonycarminati/carminatiio:$SHA1
echo "Image successfully deployed to DockerHub"

# CREATE DOCKERRUN FILE AND PUSH TO S3
sed "s/<TAG>/$SHA1/" < Dockerrun.aws.json.template > $DOCKERRUN_FILE
echo "DockerRun file successfully created"

aws s3 cp $DOCKERRUN_FILE s3://$EB_BUCKET/$ENV/$DOCKERRUN_FILE
echo "DockerRun file successfully pushed to S3"

# CREATE EB APPLICATION VERSION
aws elasticbeanstalk create-application-version --application-name $APPLICATION_NAME --version-label $SHA1 --source-bundle S3Bucket=$EB_BUCKET,S3Key=$DOCKERRUN_FILE
echo "EB application version successfully created"

# UPDATE ELASTIC BEANSTALK ENVIRONMENT TO LATEST VERSION
aws elasticbeanstalk update-environment --environment-name $ENV --version-label $SHA1
echo "EB environment successfully set to latest version"
