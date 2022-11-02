package TestCases

import com.typesafe.config.{Config, ConfigFactory}
import org.scalatest.flatspec.AnyFlatSpec
import org.scalatest.matchers.should.Matchers
import java.util.regex.Pattern
import java.net.URLEncoder

class testEncoding extends AnyFlatSpec with Matchers {
  val configfile: Config = ConfigFactory.load()
  val lambdaConfig: Config = ConfigFactory.load("LambdaFunction")
  val FunctionURL: String = lambdaConfig.getString("LambdaFunction.FunctionURL")
  val LogFile: String = lambdaConfig.getString("LambdaFunction.LogFile")
  val timestamp: String = lambdaConfig.getString("LambdaFunction.Timestamp")
  val dT: String = lambdaConfig.getString("LambdaFunction.dT")

  val pattern = configfile.getString("randomLogGenerator.Pattern")

  behavior of "encoding for strings and pattern matching"

  it should "correctly match encoded timestamp" in {
    URLEncoder.encode(timestamp, "UTF-8") shouldBe a [String]
  }

  it should "correctly match encoded logfile name" in {
    URLEncoder.encode(LogFile, "UTF-8") shouldBe a
      [String]
  }

  it should "correctly match encoded dT (delta time)" in {
    URLEncoder.encode(dT, "UTF-8") shouldBe a
      [String]
  }

  it should "obtain the Pattern" in {
    pattern shouldBe a [String]
  }

  it should "match the pattern specified in the configuration file with test string" in {
    val test_string = "14:18:43.447 [scala-execution-context-global-149] WARN  HelperUtils.Parameters$ - BFHGTjzJL:^jN5qG6mC7mK6tae0~uGmrD+n+F|W"
    val compiled_pattern = Pattern.compile(pattern)
    val matcher = compiled_pattern.matcher(test_string)
    matcher.find() should be (true)
  }

  it should "not match the pattern specified in the configuration file with test string" in {
    val test_string = "14:19:01.711 [scala-execution-context-global-149] INFO  HelperUtils.Parameters$ - .NzRJ4vdWPrn\\Ye{fjw!|\\"
    val compiled_pattern = Pattern.compile(pattern)
    val matcher = compiled_pattern.matcher(test_string)
    matcher.find() should be(false)
  }
}