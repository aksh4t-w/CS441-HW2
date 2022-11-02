import grpc
import time
import logging
import log_functions_pb2_grpc
import log_functions_pb2


def run():
    print("Will try to search the logs ...")
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = log_functions_pb2_grpc.Invoke_FunctionsStub(channel)

        # response = stub.SayHello(log_functions_pb2.HelloRequest(name="you"))
        # print("Greeter client received: " + response.message)

        logging.info("Calling gRPC server for checking timestamp...")
        response1 = stub.check_message_presence(
            log_functions_pb2.TimeStampRequest(
                timestamp="22:08:42.640",
                dT="00:00:30.000",
                logFile="logfile.log",
                getX="checkIfPresent",
            )
        )
        print("Status Code: " + str(response1.statusCode))
        print("Time stamp presence: " + str(response1.message))

        logging.info("Calling gRPC server for getting pattern matched logs...")
        response2 = stub.get_matched_logs(
            log_functions_pb2.TimeStampRequest(
                timestamp="22:08:42.640",
                dT="00:00:10.000",
                logFile="logfile.log",
                getX="matchedLogs",
            )
        )
        print("Status Code: " + str(response2.statusCode))
        print("Logs which matched the given pattern: " + str(response2.logs))


if __name__ == "__main__":
    logging.basicConfig()
    run()
