name := "hello-scaloid-sbt"

import android.Keys._
android.Plugin.androidBuild

javacOptions ++= Seq("-source", "1.8", "-target", "1.8")
scalaVersion := "2.11.7"
scalacOptions in Compile += "-feature"

updateCheck in Android := {} // disable update check
proguardCache in Android ++= Seq("org.scaloid")

proguardSettings

ProguardKeys.options in Proguard ++= Seq("-dontnote", "-dontwarn", "-ignorewarnings")

ProguardKeys.options in Proguard += ProguardOptions.keepMain("some.MainClass")

ProguardKeys.merge in Proguard := true

proguardOptions in Android ++= Seq(
  "-dontobfuscate"
  ,"-dontoptimize"
  ,"-keepattributes Signature"
  ,"-printseeds target/sbt-seeds.txt"
  ,"-printusage target/sbt-usage.txt"
  ,"-dontwarn scala.collection.**" // required from Scala 2.11.4
  ,"-dontwarn org.scaloid.**" // this can be omitted if current Android Build target is android-16
  ,"-dontnote org.apache.http.**"
  ,"-dontnote android.net.http.**"
  ,"-dontwarn org.apache.**"
  ,"-keep public class org.apache.poi.** {*;}"
  ,"-keep class org.apache.http.**"
  ,"-keep interface org.apache.http.**"
//  ,"-libraryjars " + apacheDirectory + "poi/poi-3.9.jar"
//  ,"-libraryjars " + apacheDirectory + "poi-ooxml-3.9.jar"
//  ,"-libraryjars " + apacheDirectory + "poi-ooxml-schemas-3.9.jar"
)

libraryDependencies += "org.scaloid" %% "scaloid" % "4.2"
libraryDependencies ++= Seq(
  "org.apache.poi" % "poi" % "3.9"
, "org.apache.poi" % "poi-ooxml" % "3.9"
)

run <<= run in Android
install <<= install in Android

// Tests //////////////////////////////

libraryDependencies ++= Seq(
  "org.apache.maven" % "maven-ant-tasks" % "2.1.3" % "test",
  "org.robolectric" % "robolectric" % "3.0" % "test",
  "junit" % "junit" % "4.12" % "test",
  "com.novocode" % "junit-interface" % "0.11" % "test"
)

// without this, @Config throws an exception,
unmanagedClasspath in Test ++= (bootClasspath in Android).value