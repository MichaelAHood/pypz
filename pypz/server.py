from flask import Flask, request, jsonify
from pypz.components import (
    create_bucket,
    create_queue,
    create_lambda,
    delete_bucket,
    delete_queue,
    delete_lambda,
)

app = Flask(__name__)
logger = app.logger


@app.route("/create_resources", methods=["POST"])
def create_resources():
    data = request.json
    processor_name = data.get("processor_name")
    zip_file_path = data.get("zip_file_path")
    handler = data.get("handler")

    created_resources = []

    try:
        create_bucket(processor_name)
        created_resources.append(("bucket", processor_name))

        create_queue(processor_name)
        created_resources.append(("queue", processor_name))

        create_lambda(processor_name, zip_file_path, handler)
        created_resources.append(("lambda", processor_name))

        return jsonify({"status": "All resources created successfully"}), 200

    except Exception as e:
        # Rollback: Delete all created resources
        for resource_type, resource_name in reversed(created_resources):
            if resource_type == "bucket":
                _ = delete_bucket(resource_name)
            elif resource_type == "queue":
                _ = delete_queue(resource_name)
            elif resource_type == "lambda":
                _ = delete_lambda(resource_name)

        return (
            jsonify(
                {"status": f"Resource creation failed. Rolled back. Error: {str(e)}"}
            ),
            500,
        )


@app.route("/delete_resources", methods=["POST"])
def delete_resources():
    data = request.json
    processor_name = data.get("processor_name")

    resources = [
        ("bucket", processor_name, delete_bucket),
        ("queue", processor_name, delete_queue),
        ("lambda", processor_name, delete_lambda),
    ]

    failed_to_delete = []

    for resource_type, resource_name, delete_func in resources:
        try:
            delete_func(resource_name)
            print(f"Successfully deleted {resource_type}: {resource_name}")
        except Exception as e:
            print(f"Failed to delete {resource_type}: {resource_name}. Error: {str(e)}")
            failed_to_delete.append((resource_type, resource_name))

    if not failed_to_delete:
        return jsonify({"status": "All resources deleted successfully"}), 200
    else:
        return (
            jsonify(
                {
                    "status": f"Resource deletion failed for: {failed_to_delete}.",
                    "failed_resources": failed_to_delete,
                }
            ),
            500,
        )


if __name__ == "__main__":
    app.run(debug=True)
