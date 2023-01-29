provider "aws" {
  region = "us-east-1"
}

resource "aws_api_gateway_rest_api" "example" {
  name        = "tf-lambda-getway"
  description = "Getway for lambda"
}

output "base_url" {
  value = "${aws_api_gateway_deployment.example.invoke_url}"
}

resource "aws_iam_role" "iam_for_lambda_tf" {
  name = "iam_for_lambda_tf"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_lambda_function" "convolution" {
  depends_on = [
#    data.archive_file.zip_code,
  ]

  # If the file is not in the current working directory you will need to include a
  # path.module in the filename.
  filename      = "function.zip"
  function_name = "convolution"
  role          = aws_iam_role.iam_for_lambda_tf.arn
  handler       = "main.lambda_handler"

  # The filebase64sha256() function is available in Terraform 0.11.12 and later
  # For Terraform 0.11.11 and earlier, use the base64sha256() function and the file() function:
  # source_code_hash = "${base64sha256(file("lambda_function_payload.zip"))}"
  source_code_hash = filebase64sha256("function.zip")

  runtime = "python3.8"

  environment {
    variables = {
      foo = "bar"
    }
  }
}

resource "aws_api_gateway_resource" "function" {
  rest_api_id = "${aws_api_gateway_rest_api.example.id}"
  parent_id   = "${aws_api_gateway_rest_api.example.root_resource_id}"
  path_part   = "{proxy+}"
}

resource "aws_api_gateway_method" "convolution" {
  rest_api_id   = "${aws_api_gateway_rest_api.example.id}"
  resource_id   = "${aws_api_gateway_resource.function.id}"
  http_method   = "ANY"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "lambda" {
  rest_api_id             = "${aws_api_gateway_rest_api.example.id}"
  resource_id             = "${aws_api_gateway_method.convolution.resource_id}"
  http_method             = "${aws_api_gateway_method.convolution.http_method}"
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.convolution.invoke_arn
}

resource "aws_api_gateway_deployment" "example" {
  depends_on = [
    aws_api_gateway_integration.lambda,
  ]

  rest_api_id = "${aws_api_gateway_rest_api.example.id}"
  stage_name  = "v1"
}

resource "aws_lambda_permission" "apigw" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.convolution.function_name}"
  principal     = "apigateway.amazonaws.com"

  # The /*/* portion grants access from any method on any resource
  # within the API Gateway "REST API".
  source_arn = "${aws_api_gateway_rest_api.example.execution_arn}/*/*"
}