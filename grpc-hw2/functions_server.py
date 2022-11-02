from concurrent import futures
import logging
import grpc
import boto3
import json
import log_functions_pb2_grpc
import log_functions_pb2
import re


class Invoke_Functions(log_functions_pb2_grpc.Invoke_Functions):
    def check_message_presence(self, request, context):
        presence = False

        inputDict = {
            "timestamp": request.timestamp,
            "dT": request.dT,
            "logFile": request.logFile,
            "getX": request.getX,
        }

        logging.info("Client request received")
        logging.info("Calling the lambda function")

        try:
            response = self.callLambdaFunction(inputDict)
            print(response)
            if json.loads(response["body"])["isPresent"]:
                presence = True

            return log_functions_pb2.TimeStampPresence(
                message=presence, statusCode=response["statusCode"]
            )
        except:
            print("An error has occured while calling the lambda function.")
            logging.error("Call to lambda function failed")

    def get_matched_logs(self, request, context):
        inputDict = {
            "timestamp": request.timestamp,
            "dT": request.dT,
            "logFile": request.logFile,
            "getX": request.getX,
        }
        logging.info("Client request received")
        logging.info("Calling the lambda function")

        try:
            response = self.callLambdaFunction(inputDict)
            matched_logs = json.loads(response["body"])["matched_logs"]
            print(matched_logs)

            logging.info("Sending the response back to client")
            return log_functions_pb2.MatchedLogs(
                logs=matched_logs, statusCode=response["statusCode"]
            )
        except:
            print("An error has occured while calling the lambda function.")
            logging.error("Call to lambda function failed")

    def callLambdaFunction(self, inputDict):
        lambda_client = boto3.client("lambda")
        lambda_payload = inputDict
        response = lambda_client.invoke(
            FunctionName="arn:aws:lambda:us-east-2:542585412033:function:AnalyzeLogFile",
            InvocationType="RequestResponse",
            Payload=json.dumps(lambda_payload),
        )
        return json.load(response["Payload"])


def serve():
    port = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    log_functions_pb2_grpc.add_Invoke_FunctionsServicer_to_server(
        Invoke_Functions(), server
    )
    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()
