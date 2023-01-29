#resource "aws_api_gateway_rest_api" "example" {
#  name        = "tf-lambda-getway"
#  description = "Getway for lambda"
#}
#
#output "base_url" {
#  value = "${aws_api_gateway_deployment.example.invoke_url}"
#}