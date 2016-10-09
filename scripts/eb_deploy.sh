# deploy.sh
#! /bin/bash

SHA1=$1
ENV=dev
APPLICATION_NAME=carminatiio

# Deploy image to Docker Hub
docker push anthonycarminati/carminatiio:$SHA1

# Create new Elastic Beanstalk version
EB_BUCKET=anthonycarminati-carminatiio
DOCKERRUN_FILE=$SHA1-Dockerrun.aws.json
sed "s/<TAG>/$SHA1/" < Dockerrun.aws.json.template > $DOCKERRUN_FILE
aws s3 cp $DOCKERRUN_FILE s3://$EB_BUCKET/$ENV/$DOCKERRUN_FILE
aws elasticbeanstalk create-application-version --application-name $APPLICATION_NAME --version-label $SHA1 --source-bundle S3Bucket=$EB_BUCKET,S3Key=$DOCKERRUN_FILE

# Update Elastic Beanstalk environment to new version
aws elasticbeanstalk update-environment --environment-name $ENV --version-label $SHA1
