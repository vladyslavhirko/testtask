## Requirements
1. [AWS cli](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
2. [Terraform](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli)
3. [gcc](https://gcc.gnu.org/install/)
4. [python3](https://www.python.org/downloads/)
5. [zip for linux](https://www.tecmint.com/install-zip-and-unzip-in-linux/) or [zip for mac](https://formulae.brew.sh/formula/zip)

## How to use
1. Install all tools from the `Requirements` section
2. Login to the AWS account using AWS cli tool. `aws configure`
   - Pass account creds (access key, secret key), region should be `us-east-1`
3. Initialize terraform. `terraform init`. This command will install all requirement modules and create terraform data.
4. C and Python code already exists. But for using C function as shared object in the python you should create *.so file. ` gcc -shared -o convolution.so -fPIC convolution.c`
5. Next need to put .so file and python script into archive: `zip function.zip main.py convolution.so`. Both of the files should be in one directory. 
Generated archive should be in the root directory. 
6. For applying terraform configuration - type `terraform apply`.

## Terraform config
Terraform config should create AWS lambda function and API getway. 
API getway will be setuped as trigger for lambda function. 
After success configuration applying, terraform will print link which call lambda function,
`base_url = "https://2gdb5iwctg.execute-api.us-east-1.amazonaws.com/v1"` for using API add `/function` path at the end of the URL and pass query params `?a=1,2,3&b=3,4,5`.
Example: `https://2gdb5iwctg.execute-api.us-east-1.amazonaws.com/v1/a?a=2,5,9&b=2,3,4`.
After changing code or resource config in terraform for applying changes use `terraform apply` command.

## Note
C function for calculating convolution already generated and exists as .so 
files in directories `so_linux_generated` and `so_macos_generated`. 
For local usage both of them can be used, depend's on your system, 
but for using shared object file in lambda, please use file from `so_linux_generated`.
For using locally .py file and .so file should be in one directory.

## Problems 
1. Generating .so file depends on the system. 
gcc compiler doesn't provide possibility to generate .so 
file in one OS for another OS. If ypu try to generate .so file using 
macos it shouldn't work with lambda.

- How to solve this? We can create docker container with `ubuntu` image, 
copy C file into the container, generate .so file there 
and throw file to the local machine. This solution will work independent on the OS.

2. Convolution algorithm works only with integers (1, 15, 23 etc) and 
doesn't work with double numbers.

- How to solve this? Just change C function for working with double numbers instead of integers.

3. Convolution algorithm works with arrays with the same length.
If you try to pass arrays with different length. You'll have 400 bad request.

- How to solve this? Need to change algorithm. Or just generate using chatGTP :)

4. According to the task, link should be in `https://[host]/[stage]/function?a=123&b=234` format.
But if you try to use another pass part, for example `test` instead of `function`, convolution will work.

- How to solve this? Need to check API getway configuration, and check how it can be fixed.
For now api getway has `AWS-PROXY` type. I suppose that instead of proxy can be used another getway type.

## How to make this better
Instead of .zip archive and running all commands locally we can use CI. 
Terraform can work with files from remote git repositories. So.
We can create 2 repository, 
first for python and C code and second for terraform config.
CI on first repos will generate .so file, and create zip archive. 
After that pipeline will create container with terraform config and call  `terraform apply` command, 
which will take code from the repos and push to the lambda.
Also in aws console we can create tests for each lambda function, tests will improve code quality.
Also, now .so file and python script should be in one directory, it's not good idea, so it will
be good to separate these files and create separate directory for .so file, for example `lib`.