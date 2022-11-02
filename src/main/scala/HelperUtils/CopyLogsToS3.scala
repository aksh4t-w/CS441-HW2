package HelperUtils

import com.amazonaws.AmazonServiceException
import com.amazonaws.regions.Regions
import com.amazonaws.services.s3.{AmazonS3, AmazonS3ClientBuilder}
import com.typesafe.config.{Config, ConfigFactory}

import java.io.File

object CopyLogsToS3 {
  val s3_config: Config = ConfigFactory.load("LambdaFunction.conf")

  val bucket = s3_config.getString("LambdaFunction.Bucket")
  val S3_Path = s3_config.getString("LambdaFunction.EC2_Path")
  val path = s3_config.getString("LambdaFunction.File_Path")


  val s3: AmazonS3 = AmazonS3ClientBuilder.standard.withRegion(Regions.US_EAST_2).build

  try s3.putObject(bucket, S3_Path, new File(path))
  catch {
    case e: AmazonServiceException =>
      System.err.println(e)
      System.exit(1)
  }
}
