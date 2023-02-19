import os
import re
import time
import networkx as nx

from collections import defaultdict
from hashlib import sha256
from itertools import product
from pathlib import PurePath

from pyspark.sql import SparkSession
from pyspark.sql import functions as fns
from pyspark.sql.types import StringType, StructType, StructField, LongType, BooleanType, ArrayType

FUNC_TPL_TABLE = ""
SAVE_DIR = ""
SLOT_TIME_CSV = ""

BLACK_SET = {'src', 'external', 'third_party', '3rdparty', 'extern', 'common', 'tests',
             'thirdparty', 'modules', 'third-part', 'deps', 'source', 'components', 'extra'}

EXTERN_FLAG = {'external', 'third_party', '3rdparty', 'extern',
               'components', 'third-party', 'thirdparty', 'deps'}


def parse_func_src(func_src):
    def replacer(match):
        s = match.group(0)
        if s.startswith('/'):
            return ""
        else:
            return s
    pattern = re.compile(
        r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
        re.DOTALL | re.MULTILINE
    )
    func_src = re.sub(pattern, replacer, func_src)
    func_src = "".join([c for c in func_src.splitlines(True) if c.strip()])
    func_src = func_src.strip()
    if func_src.count("\n") <= 6:
        return None
    # normalize code
    func_src = re.sub(r"[\n\r\t\{\}\s]", "", func_src)
    func_id = sha256(func_src.encode()).hexdigest()
    return func_id


def parse_tpl_list(tpl_list):
    tpl_slot_time = list()
    seg_count = defaultdict(int)
    tpl_name_id = defaultdict(list)
    for tpl in tpl_list:
        tpl_id = tpl.tpl_uuid
        tpl_name = tpl.tpl_name
        slot_time = tpl.func_info.commit_time
        file_path = PurePath(tpl.func_info.file_path.lower())
        extern_flag = False
        seg_set = set()
        for seg in file_path.parent.parts + (file_path.stem,):
            if seg in EXTERN_FLAG:
                extern_flag = True
            if seg in BLACK_SET or seg == tpl_name:
                continue
            seg_set.add(seg)
        for seg in seg_set:
            seg_count[seg] += 1
        if not extern_flag:
            tpl_info = (tpl_id, slot_time)
            tpl_name_id[tpl_name].append(tpl_info)
            tpl_slot_time.append(tpl_info)
    # resolve the function path
    if len(seg_count):
        lower_count = 1 if len(tpl_list) <= 3 else 2
        seg_sort = sorted(seg_count.items(), reverse=True, key=lambda x: x[1])
        for seg, count in seg_sort:
            if count < lower_count:
                break
            if seg in tpl_name_id:
                origin_tpl = sorted(tpl_name_id[seg], key=lambda x: x[1])[0]
                return (origin_tpl[0], 0)
    if len(tpl_slot_time):
        origin_tpl = sorted(tpl_slot_time, key=lambda x: x[1])[0]
        return origin_tpl
    return None


def resolve_origin_tpl(tpl_list):
    # handle eponymous tpl
    origin_tpl = parse_tpl_list(tpl_list)
    return origin_tpl


def resolve_tpl_pair(tpl_list):
    tpl_set = set(tpl_list)
    reuse_set = tpl_set & reuse_count.keys()
    reused_set = tpl_set & reused_count.keys()
    tpl_pair_set = set()
    for tpl_s, tpl_x in product(reuse_set, reused_set):
        if tpl_s == tpl_x:
            continue
        tpl_pair = (tpl_s, tpl_x) if tpl_s < tpl_x else (tpl_x, tpl_s)
        tpl_pair_set.add(tpl_pair)
    if len(tpl_pair_set):
        return list(tpl_pair_set)
    return None


def eval_recall_threshold(tpl_s, tpl_x, reuse_num):
    func_num_x = func_count[tpl_x] if tpl_x in func_count else 0
    reuse_num_x = reuse_count[tpl_x] if tpl_x in reuse_count else 0
    reused_num_x = reused_count[tpl_x] if tpl_x in reused_count else 0
    if func_num_x - reuse_num_x <= 0 or reuse_num <= 15:
        return False
    tpl_pair = (tpl_s, tpl_x) if tpl_s < tpl_x else (
        tpl_x, tpl_s)
    if tpl_pair in func_overlap and reuse_num / func_overlap[tpl_pair] > 0.95:
        if reuse_num / reused_num_x > 0.15 or func_overlap[tpl_pair] - reuse_num <= 5:
            return True
    if reuse_num / (func_num_x - reuse_num_x) >= 0.0075 * func_num_x / reused_num_x:
        return True
    return False


def main():

    global func_count, func_overlap, reuse_count, reused_count

    spark = SparkSession \
        .builder \
        .appName("Source_Relation") \
        .config("hive.exec.dynamic.partition.mode", "nonstrict") \
        .config("hive.exec.dynamic.partition", "true") \
        .config("hive.exec.max.dynamic.partitions", 40000) \
        .config("hive.exec.max.dynamic.partitions.pernode", 10000) \
        .config("hive.exec.compress.output", "false") \
        .getOrCreate()

    spark.conf.set("spark.sql.execution.arrow.enabled", "true")

    hive_sql = f"""select tpl_uuid, func_src, func_info from {FUNC_TPL_TABLE}"""
    df = spark.sql(hive_sql)

    df = df.select(
        df.tpl_uuid,
        df.slot_uuid,
        df.file_path,
        fns.explode(df.functions).alias("func_info")
    ).na.drop()

    df = df.select(
        df.tpl_uuid,
        df.slot_uuid,
        df.file_path,
        df.func_info.src.alias("func_src"),
    )

    # parse the function source code
    parse_func_udf = fns.udf(parse_func_src, StringType())
    df_func_id = (
        df.groupBy(df.func_src)
        .agg(parse_func_udf(df.func_src).alias("func_id"))
        .na.drop()
    )
    df = df.join(df_func_id, "func_src", "left").na.drop()

    '''
    Parse the slot with origin time
    root
    |-- tpl_uuid: string (nullable = true)
    |-- func_id: string (nullable = true)
    |-- func_info: struct (nullable = true)
    |    |-- commit_time: long (nullable = true)
    |    |-- file_path: string (nullable = true)
    '''

    # parse the slot with function origin time
    df_slot_time = spark.read.options(
        header='True', inferSchema='True'
    ).csv(SLOT_TIME_CSV)

    df = df.join(df_slot_time, "slot_uuid", "left").na.drop()
    df = df.groupby(df.tpl_uuid, df.func_id).agg(
        fns.collect_list(
            fns.struct(df.commit_time, df.file_path)
        ).alias("func_info")
    )
    df = df.withColumn("func_info", fns.array_min(df.func_info))

    # function number for each tpl
    df.cache()
    func_count = df.groupby(df.tpl_uuid).agg(
        fns.count(df.func_id).alias("func_num")
    ).toPandas().set_index("tpl_uuid").to_dict(orient="dict")["func_num"]

    '''
    Resolve the origin tpl for each function
    root                                                                            
    |-- func_id: string (nullable = true)
    |-- tpl_list: array (nullable = false)
    |    |-- element: struct (containsNull = false)
    |    |    |-- tpl_uuid: string (nullable = true)
    |    |    |-- tpl_name: string (nullable = true)
    |    |    |-- func_info: struct (nullable = true)
    |    |    |    |-- commit_time: long (nullable = true)
    |    |    |    |-- file_path: string (nullable = true)
    |-- origin_tpl: struct (nullable = true)
    |    |-- tpl_uuid: string (nullable = true)
    |    |-- origin_time: long (nullable = true)
    '''

    # resolve the origin tpl for each function
    df = df.groupby(df.func_id).agg(
        fns.collect_list(
            fns.struct(df.tpl_uuid, df.tpl_name, df.func_info)
        ).alias("tpl_list")
    )
    df_func = df.withColumn("tpl_list", fns.col("tpl_list.tpl_uuid"))
    resolve_origin_udf = fns.udf(
        resolve_origin_tpl,
        StructType(
            [StructField("tpl_uuid", StringType()),
             StructField("origin_time", LongType())]
        )
    )
    df = df.withColumn(
        "origin_tpl",
        resolve_origin_udf(df.tpl_list)
    )

    # resolve the reuse relation
    df = df.select(
        df.func_id,
        fns.explode(df.tpl_list).alias("tpl"),
        df.origin_tpl
    )
    df = df.withColumn(
        "tpl",
        fns.struct(
            df.tpl.tpl_uuid.alias("tpl_uuid"),
            df.tpl.func_info.commit_time.alias("slot_time")
        )
    )
    df = df.filter(
        (df.tpl.slot_time > df.origin_tpl.origin_time) &
        (df.tpl.tpl_uuid != df.origin_tpl.tpl_uuid)
    )
    df = df.select(
        df.tpl.tpl_uuid.alias("tpl_s"),
        df.origin_tpl.tpl_uuid.alias("tpl_x"),
        df.func_id
    )
    df.cache()

    reuse_count = df.groupby(df.tpl_s.alias("tpl_uuid")).agg(
        fns.countDistinct(df.func_id).alias("reuse_num")
    ).toPandas().set_index("tpl_uuid").to_dict(orient="dict")["reuse_num"]

    reused_count = df.groupby(df.tpl_x.alias("tpl_uuid")).agg(
        fns.countDistinct(df.func_id).alias("reused_num")
    ).toPandas().set_index("tpl_uuid").to_dict(orient="dict")["reused_num"]

    df = df.groupby(df.tpl_s, df.tpl_x).agg(
        fns.count(df.func_id).alias("reuse_num")
    )

    # count number of overlap function
    resolve_pair_udf = fns.udf(
        resolve_tpl_pair,
        ArrayType(StructType(
            [StructField("tpl_s", StringType()),
             StructField("tpl_x", StringType())]
        ))
    )
    df_func = df_func.select(
        df_func.func_id,
        resolve_pair_udf(df_func.tpl_list).alias("tpl_pair_list")
    ).na.drop()
    df_func = df_func.select(
        df_func.func_id,
        fns.explode(df_func.tpl_pair_list).alias("tpl_pair")
    )
    df_func = df_func.select(
        df_func.func_id,
        df_func.tpl_pair.tpl_s.alias("tpl_s"),
        df_func.tpl_pair.tpl_x.alias("tpl_x")
    )

    func_overlap = df_func.groupBy(df_func.tpl_s, df_func.tpl_x).agg(
        fns.count(df_func.func_id).alias("overlap_num")
    ).toPandas().set_index(["tpl_s", "tpl_x"]).to_dict(orient="dict")["overlap_num"]

    # recall the results
    eval_recall_udf = fns.udf(eval_recall_threshold, BooleanType())
    df = df.filter(eval_recall_udf(df.tpl_s, df.tpl_x, df.reuse_num))
    reuse_dict = df.toPandas().set_index(
        ["tpl_s", "tpl_x"]
    ).to_dict(orient="dict")["reuse_num"]
    recall_relation = reuse_dict.keys()

    print(f"[+] Total relations by algorithm: {len(recall_relation)}")

    df_reuse = spark.createDataFrame(
        list(recall_relation),
        schema=["origin_tpl_uuid", "reuse_tpl_uuid"]
    )

    (
        df_reuse.repartition(1)
        .write.option("header", True)
        .csv(
            os.path.join(SAVE_DIR, "reuse_relation.csv"),
            mode="overwrite"
        )
    )


if __name__ == "__main__":
    main()
