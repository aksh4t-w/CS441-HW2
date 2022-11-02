package RESTClientLambda

import HelperUtils.{CreateLogger}
import com.typesafe.config.{Config, ConfigFactory}
import java.net.URLEncoder

import java.util.concurrent.TimeUnit
import java.util.logging.{Level, Logger}

class RESTClient{}

// REST client which performs calls to the API gateway for our lambda function.
object RESTClient {
  val logger = CreateLogger(classOf[RESTClient])

  def main(args: Array[String]): Unit = {
    logger.info("Loading lambda config file...")
    val lambdaConfig: Config = ConfigFactory.load("LambdaFunction.conf")

    logger.info("Loading function api parameters...")
    val bucket: String = lambdaConfig.getString("LambdaFunction.Bucket")
    val FunctionURL: String = lambdaConfig.getString("LambdaFunction.FunctionURL")
    val LogFile: String = lambdaConfig.getString("LambdaFunction.LogFile")
    val timestamp: String = lambdaConfig.getString("LambdaFunction.Timestamp")
    val dT: String = lambdaConfig.getString("LambdaFunction.dT")
    val Task1: String = lambdaConfig.getString("LambdaFunction.Task1")
    val Task2: String = lambdaConfig.getString("LambdaFunction.Task2")

    // Make a request to our API gateway connected to the Lambda function.
    // String inputs are encoded in UTF-8 for parsing.
    logger.info("Making a request to the lambda function's API gateway...")

    try {
      logger.info("Making request to check if the timestamp is present in the log file.")
      val response1 = scala.io.Source.fromURL(FunctionURL + "?getX=" + URLEncoder.encode(Task1, "UTF-8") + "&timestamp=" + URLEncoder.encode(timestamp, "UTF-8") + "&dT=" + URLEncoder.encode(dT, "UTF-8") + "&logFile=" + URLEncoder.encode(LogFile, "UTF-8"))
      println("Response for task 1: " + response1.mkString)

      logger.info("Making request to check if the timestamp is present and getting the pattern matched logs in the given time interval in the log file.")
      val response2 = scala.io.Source.fromURL(FunctionURL + "?getX=" + URLEncoder.encode(Task2, "UTF-8") + "&timestamp=" + URLEncoder.encode(timestamp, "UTF-8") + "&dT=" + URLEncoder.encode(dT, "UTF-8") + "&logFile=" + URLEncoder.encode(LogFile, "UTF-8"))
      println("Response for task 2: " + response2.mkString)
    } catch
    {
      case e: java.io.FileNotFoundException => println("The timestamp is not present in the log file.")
    }
  }
}
