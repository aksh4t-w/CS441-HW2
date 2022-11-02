# CS441 Homework-2
## University of Illinois at Chicago
## Akshat Wagadre
## UIN - 654098103

## Introduction:
* In this homework, an AWS Lambda function is created which performs operations on a log file. This lambda function is called using two different clients:
1) gRPC Client: Built using python. It has two parts, the gRPC client and the gRPC server. 
The client makes requests to the server and the server performs the lambda call and returns the response back to the client.
2) REST Client: Built using scala. It performs API calls as GET requests to the lambda function via an API gateway created in AWS. The API gateway sends back
the response to the client.
* Apart from these, an EC2 instance is created in AWS which runs the log generator program. This program copies the logs to an S3 bucket which can later be 
accessed by the lambda function.

Demonstration of the project can be found here: https://youtu.be/o7ksl5x3D2g

## Prerequisites
* Java: JDK 11.0
* SBT
* Python
* AWS-CLI

## Instructions to run the project.
### 1) Clone the project to your local machine.
### 2) Input parameters for the clients:
```
1) timestamp: The timestamp you need to search for. Eg: timestamp="22:08:42.640".
2) dT: The time interval in which logs are to be searched and matched. Eg: dT="00:00:10.000".
3) logFile: Name of the logfile in the bucket. Eg: logFile="logfile.log".
4) getX: Type of operation you want to perform i.e. "checkIfPresent" or "matchedLogs". Eg. getX="matchedLogs",
```


### 3) Running the gRPC client present in the grpc-hw2 directory.
* Install the dependencies from requirements.txt file: 
`pip install -r requirements. txt`
* Run the functions_server.py and client.py files in two different terminals.
* Open the client file to modify parameters as required.

### 4) Running the REST client.
* Define the input parameters in LambdaFunction.conf.
* To run the client use: `sbt clean compile run`
* Example of the GET request made: 
https://cgqrxm8291.execute-api.us-east-2.amazonaws.com/test/check_log_presence?timestamp=15:08:42.640&dT=00:00:10.000&logFile=logfile.log&getX=matchedLogs

### 5) (Optional) Instructions for EC2 instance:
* Adding write permissions to a directory in EC2: `sudo chmod ugo+rwx LogFileGenerator`
* Transferring files to the EC2 instance using:
`scp -i <key-pair> -r "PathToProjectDirectory\LogFileGenerator\*" ec2-user@<EC2-IP>:<PathToCopyFilesToOnEC2>`
* Installing sbt on the EC2 instance:
```
curl -L https://www.scala-sbt.org/sbt-rpm.repo > sbt-rpm.repo
sudo mv sbt-rpm.repo /etc/yum.repos.d/
sudo yum install sbt
```