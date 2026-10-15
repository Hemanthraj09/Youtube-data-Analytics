"""
One-time conversion of the raw 5.5 GB CSV into Parquet for the Spark pipeline.

- Explicit schema (no inferSchema pass over 5.5 GB)
- multiLine + escape: descriptions contain newlines and doubled quotes
- Dates parsed to proper types; thumbnail_url dropped (unused)
- description replaced by its length: the text is most of the file's bytes
  and the pipeline only uses its length

Run with the spark-env Python:  ~/spark-env/venv/Scripts/python.exe spark_prepare.py
"""
import time
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, StringType, LongType

from spark_session import get_spark, RAW_CSV, PARQUET_PATH

SCHEMA = StructType([
    StructField("title", StringType()),
    StructField("channel_name", StringType()),
    StructField("daily_rank", LongType()),
    StructField("daily_movement", LongType()),
    StructField("weekly_movement", LongType()),
    StructField("snapshot_date", StringType()),
    StructField("country", StringType()),
    StructField("view_count", LongType()),
    StructField("like_count", LongType()),
    StructField("comment_count", LongType()),
    StructField("description", StringType()),
    StructField("thumbnail_url", StringType()),
    StructField("video_id", StringType()),
    StructField("channel_id", StringType()),
    StructField("video_tags", StringType()),
    StructField("kind", StringType()),
    StructField("publish_date", StringType()),
    StructField("langauge", StringType()),
])

if __name__ == "__main__":
    t0 = time.time()
    spark = get_spark("yt_prepare")

    raw = spark.read.csv(
        str(RAW_CSV), header=True, schema=SCHEMA,
        multiLine=True, escape='"', encoding="UTF-8", mode="PERMISSIVE",
    )

    df = (
        raw.drop("thumbnail_url")
        .withColumn("description_len", F.coalesce(F.length("description"), F.lit(0)))
        .drop("description")
        .withColumn("snapshot_date", F.to_date("snapshot_date"))
        .withColumn("publish_ts", F.to_timestamp("publish_date", "yyyy-MM-dd HH:mm:ssXXX"))
        .drop("publish_date")
    )

    # multiLine reading is single-threaded; spread rows out before writing
    df.repartition(48).write.mode("overwrite").parquet(str(PARQUET_PATH))

    out = spark.read.parquet(str(PARQUET_PATH))
    print(f"Rows written: {out.count():,}")
    null_counts = out.select([F.sum(F.col(c).isNull().cast("int")).alias(c) for c in out.columns]).first().asDict()
    print("Null counts:", {k: v for k, v in null_counts.items() if v})
    print(f"Done in {time.time() - t0:,.0f}s")
    spark.stop()
