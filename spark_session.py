"""
Shared SparkSession setup for the local Spark scripts.

Expects a self-contained Spark environment folder (default: ~/spark-env, override
with SPARK_ENV_DIR) holding:
  jre/            portable Java 17 runtime
  hadoop/bin/     winutils.exe + hadoop.dll (needed on Windows to write files)
  data/           Parquet copy of the dataset and other Spark outputs
Variables already set in the environment (JAVA_HOME, HADOOP_HOME) take precedence.
"""
import os
import sys
from pathlib import Path

ENV_DIR = Path(os.environ.get("SPARK_ENV_DIR", Path.home() / "spark-env"))
DATA_DIR = ENV_DIR / "data"
RAW_CSV = Path(__file__).resolve().parent / "trending_yt_videos_113_countries.csv"
PARQUET_PATH = DATA_DIR / "trending.parquet"


def _configure_env():
    if (ENV_DIR / "jre").is_dir():
        os.environ.setdefault("JAVA_HOME", str(ENV_DIR / "jre"))
    hadoop_bin = ENV_DIR / "hadoop" / "bin"
    if hadoop_bin.is_dir():
        os.environ.setdefault("HADOOP_HOME", str(ENV_DIR / "hadoop"))
        # hadoop.dll is found through PATH / java.library.path
        os.environ["PATH"] = str(hadoop_bin) + os.pathsep + os.environ.get("PATH", "")
    # Spark rejects hostnames containing underscores (e.g. "ACER_16")
    os.environ.setdefault("SPARK_LOCAL_HOSTNAME", "localhost")
    os.environ.setdefault("PYSPARK_PYTHON", sys.executable)


def get_spark(app_name, driver_memory="10g"):
    _configure_env()
    from pyspark.sql import SparkSession

    builder = (
        SparkSession.builder.master("local[*]")
        .appName(app_name)
        .config("spark.driver.memory", driver_memory)
        .config("spark.sql.shuffle.partitions", "48")
        .config("spark.ui.showConsoleProgress", "false")
        .config("spark.local.dir", str(ENV_DIR / "tmp"))
    )
    hadoop_bin = ENV_DIR / "hadoop" / "bin"
    if hadoop_bin.is_dir():
        # Forward slashes: backslashes are stripped when Spark parses Java options
        builder = builder.config("spark.driver.extraJavaOptions", f"-Djava.library.path={hadoop_bin.as_posix()}")
    spark = builder.getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")
    return spark
