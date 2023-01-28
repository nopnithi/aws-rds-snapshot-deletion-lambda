PACKAGE_DIR=./package
DEPLOYMENT_ZIP=deployment.zip
SAM_TEMPLATE_FILE=template.yaml
STACK_NAME=rds-snapshot-deletion
REGION=ap-southeast-1

build:
	pip install --target lambda/$(PACKAGE_DIR) pytz
	cd lambda/$(PACKAGE_DIR) && zip -r ../$(DEPLOYMENT_ZIP) .
	cd lambda && zip $(DEPLOYMENT_ZIP) lambda_function.py

deploy: build
	sam deploy --template-file $(SAM_TEMPLATE_FILE) \
	  --stack-name $(STACK_NAME) \
	  --parameter-overrides SnapshotNameContains="jenkins,instance-scheduler" SnapshotAgeThreshold=30 \
	  --capabilities CAPABILITY_IAM --resolve-s3
	rm -rf lambda/$(PACKAGE_DIR) && rm -rf lambda/$(DEPLOYMENT_ZIP)

destroy:
	aws cloudformation delete-stack --stack-name $(STACK_NAME) --region $(REGION)
