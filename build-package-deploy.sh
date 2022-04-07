
# variables
S3_DATA_BUCKET=devices-bucket-1234
S3_BUILD_BUCKET=build-bucket-1234
STACK_NAME=devices-stack

# validate
sam validate --template template.yaml

aws cloudformation validate-template --template-body file://template.yaml

# build
sam build --template template.yaml

# package
sam package --output-template-file packaged.yaml --s3-bucket $S3_BUILD_BUCKET

# deploy
sam deploy --template-file packaged.yaml --stack-name devices-stack --capabilities CAPABILITY_IAM --debug

# cleaning up
aws s3 rm s3://$S3_DATA_BUCKET/data.csv # and any other objects

aws cloudformation delete-stack --stack-name $STACK_NAME
