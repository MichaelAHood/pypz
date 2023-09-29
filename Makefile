serve:
	FLASK_APP=pypz/server.py poetry run flask run --debug

create:
	curl -X POST http://localhost:5000/create_resources \
		-H "Content-Type: application/json" \
		-d '{"processor_name": "data","zip_file_path": "lambdas/function.zip","handler": "function.lambda_handler"}'

delete:
	curl -X POST http://localhost:5000/delete_resources \
		-H "Content-Type: application/json" \
		-d '{"processor_name": "data"}'


createb:
	aws --endpoint-url=http://localhost:4566 s3 mb "s3://data" --region us-east-1 --profile localstack

removeb:
	aws --endpoint-url=http://localhost:4566 s3 rb "s3://data" --region us-east-1 --profile localstack

listb:
	aws --endpoint-url=http://localhost:4566 s3 ls --region us-east-1 --profile localstack

package:
	zip lambdas/function.zip lambdas/function.py