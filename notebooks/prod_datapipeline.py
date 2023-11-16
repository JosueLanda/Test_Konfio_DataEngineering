import warnings
from datetime import date
from delta import DeltaTable
import pyspark.sql.types as T
import pyspark.sql.functions as F
from pyspark.sql import SparkSession
from tools_datapipeline.extractor.scraper_world_population import ScrapperWorldPopulation
warnings.filterwarnings("ignore")

def extract_process(process_type:str)->None:
    
    columns_name = ["id_population"
     ,"country"
     ,"count_population"
     ,"yearly_change"
     ,"net_change"
     ,"density"
     ,"land_area"
     ,"migrants"
     ,"fert_rate"
     ,"med_age"
     ,"urban_pop"
     ,"world_share"
    ]

    mode_write = "overwrite"
    if process_type == 'INCREMENTAL':
        mode_write = "append"

    scraper = ScrapperWorldPopulation("https://www.worldometers.info/world-population/population-by-country/",spark)
    df_spark = scraper.extract_data_from_source()
    df_spark = df_spark.withColumn("ingestion_date",F.current_date())
    
    for old_name,new_name in zip(df_spark.columns,columns_name):
        df_spark = df_spark.withColumnRenamed(old_name,new_name)
    
    df_spark.write.partitionBy("ingestion_date").format("delta").mode(mode_write).save("bronze_layer/")

def transform_process(process_type:str)->DataFrame:

    columns_drop = ["ingestion_date"]
    if process_type == 'INCREMENTAL':
        
        today_value = date.today()
        df_spark = spark.read.format("delta") \
               .option("partitionFilters", f"ingestion_date == '{today_value}'") \
               .load("bronze_layer/")
    else:
        
        df_spark = spark.read.format("delta").load("bronze_layer/")
    
    df_spark = df_spark.withColumn("yearly_change",F.regexp_replace(F.col("yearly_change")," %",""))
    df_spark = df_spark.withColumn("urban_pop",F.regexp_replace(F.col("urban_pop")," %",""))
    df_spark = df_spark.withColumn("world_share",F.regexp_replace(F.col("world_share")," %",""))
    df_spark = df_spark.withColumn("yearly_change",F.col("yearly_change").cast(T.FloatType()))
    df_spark = df_spark.withColumn("urban_pop",F.col("urban_pop").cast(T.FloatType()))
    df_spark = df_spark.withColumn("world_share",F.col("world_share").cast(T.FloatType()))
    df_spark = df_spark.withColumn("country",F.lower(F.col("country")))
    df_spark = df_spark.dropDuplicates(["id_population"])
    df_spark = df_spark.orderBy(F.col("id_population").asc())
    df_spark = df_spark.drop(*columns_drop)

    return df_spark

def load_process(df_spark:DataFrame)->None:
    
    df_spark = df_spark.withColumn("processing_date",F.current_date())
    df_spark.write.partitionBy("processing_date").format("delta").mode("overwrite").save("silver_layer/")

if __name__ =="__main__":

    spark = SparkSession.builder \
        .appName("Engine") \
        .config("spark.jars.packages", "io.delta:delta-core_2.12:2.4.0") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .getOrCreate()

    extract_process('INCREMENTAL')
    df_spark = transform_process("INCREMENTAL")
    load_process(df_spark)