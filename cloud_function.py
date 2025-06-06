import unicodedata
from google.cloud import bigquery
from pathlib import Path

project = "alterdata-rekrutacja-46"
bucket = "zadanie1-rekrutacja-46"
dataset = "csv_dataset"
client = bigquery.Client(f"{project}")

def table_exists(project_name, dataset_name, table_name, client):
    table_id = f"{project_name}.{dataset_name}.{table_name}"
    try:
        client.get_table(table_id)
    except Exception as e:
        return False
    return True

def transform_file_path(path):
    allowed_char_categories = ["Lu", "Ll", "Lt", "Lm", "Lo", "Mn", "Mc", "Me", "Nl", "Nd", "No", "Pc", "Pd", "Zs"]
    new_path = path.replace("/", "_")
    new_path = new_path.replace(".", "_")

    new_path = [char for char in new_path if unicodedata.category(char) in allowed_char_categories]
    return "".join(new_path)

def trim_table_name_length(name):
    while len(name.encode("UTF-8")) > 1024:
        name = name[1:]
    return name

def generate_new_suffix(name):
    split_name = name.split("_")
    try:
        num_suffix = int(split_name[-1])
    except Exception as e:
        return f"{name}_1"
    num_suffix += 1
    new_name = "_".join(split_name[:-1])
    return f"{new_name}_{str(num_suffix)}"

def generate_table_name(project, dataset, client, file_name):
    table_name = transform_file_path(file_name)
    table_name = trim_table_name_length(table_name)
    while table_exists(project, dataset, table_name, client):
        table_name = generate_new_suffix(table_name)
        table_name = trim_table_name_length(table_name)
    return table_name


def load_new_file(event, context, client=client, project=project, bucket=bucket, dataset=dataset):
    file_name = event["name"]
    
    if file_name.split(".")[-1] != "csv" :
        return 

    table_name = generate_table_name(project, dataset, client, file_name)
    uri = f"gs://{bucket}/{file_name}"
    table_id = f"{project}.{dataset}.{table_name}"


    job_config = bigquery.LoadJobConfig(
        autodetect=True,
        column_name_character_map="V2",
        skip_leading_rows=1,
        source_format=bigquery.SourceFormat.CSV,
    )

    load_job = client.load_table_from_uri(
        uri, table_id, job_config=job_config
    )

    load_job.result()
    destination_table = client.get_table(table_id)
    print(f"Loaded {str(destination_table.num_rows)} rows into table {table_name}.")