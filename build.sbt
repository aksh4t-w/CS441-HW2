name := "LogFileAnalysis"

version := "0.1"

scalaVersion := "3.0.2"

assembly / assemblyJarName := "logFileAnalysis-sbt-assembly-fatjar-1.0.jar"

assembly / assemblyMergeStrategy := {
  case PathList("META-INF", xs @ _*) => MergeStrategy.discard
  case x => MergeStrategy.first
}

val logbackVersion = "1.4.1"
val sfl4sVersion = "2.0.1"
val typesafeConfigVersion = "1.4.2"
val apacheCommonIOVersion = "2.11.0"
val scalacticVersion = "3.2.9"
val generexVersion = "1.0.2"
val awsjavaVersion = "1.12.90"
val awsjavas3Version = "1.12.98"

resolvers += Resolver.jcenterRepo

libraryDependencies ++= Seq(
  "ch.qos.logback" % "logback-core" % logbackVersion,
  "ch.qos.logback" % "logback-classic" % logbackVersion,
  "org.slf4j" % "slf4j-api" % sfl4sVersion,
  "com.typesafe" % "config" % typesafeConfigVersion,
  "commons-io" % "commons-io" % apacheCommonIOVersion,
  "org.scalactic" %% "scalactic" % scalacticVersion,
  "org.scalatest" %% "scalatest" % scalacticVersion % Test,
  "org.scalatest" %% "scalatest-featurespec" % scalacticVersion % Test,
  "com.typesafe" % "config" % typesafeConfigVersion,
  "com.github.mifmif" % "generex" % generexVersion,
  "com.amazonaws" % "aws-java-sdk" % awsjavaVersion,
  "com.amazonaws" % "aws-java-sdk-s3" % awsjavas3Version,
)