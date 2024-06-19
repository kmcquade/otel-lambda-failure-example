setup:
	echo 'Install AWS SAM'
deploy:
	sam deploy \
		--stack-name otel-failure-example \
		--no-fail-on-empty-changeset \
		--resolve-s3 \
		--capabilities CAPABILITY_IAM CAPABILITY_AUTO_EXPAND CAPABILITY_NAMED_IAM \
		--no-confirm-changeset \
		--region us-east-1
delete:
	aws cloudformation delete-stack --stack-name otel-failure-example --region us-east-1
invoke:
	sam remote invoke HelloWorldFunction --event '{}' --stack-name otel-failure-example --region us-east-1 --output text