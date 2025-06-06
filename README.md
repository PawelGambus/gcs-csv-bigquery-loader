# ☁️ GCP Cloud Function – CSV Loader

This repository contains my solution for a Task of a recruitment challenge focused on building an automated ingestion pipeline using Google Cloud Platform.

---

## 📝 Task Description

Log in to the Google Cloud Platform console and locate the project: `*****`.  
You have full permissions in this project.

### Task 1

- Create your own bucket in Google Cloud Storage with any name.
- Implement a **Cloud Function (v1)** in GCP that:
  - is triggered by the upload of any `.csv` file into the bucket,
  - automatically creates a corresponding table in BigQuery based on the schema inferred from the file (`autodetect=True`).

---

## 🚀 My Implementation Details

### ✅ Region and Resource Setup

- I selected the region `europe-central2 (Warsaw)` for its low cost and physical proximity to the company.
- Both the Cloud Function and the bucket are located in the same region to avoid cross-region data transfer costs.
- I disabled multi-region replication to reduce unnecessary costs.

### ✅ Cloud Function – Trigger and Architecture

- I used the trigger: `google.cloud.storage.object.v1.finalized`  
  → Activated on finalizing a file upload (based on [GCP docs](https://cloud.google.com/functions/docs/calling/storage)).
- I confirmed that uploading a file indeed triggers the function.
- I configured the function with minimal resources and set **max concurrency to 1**, assuming low traffic.

### ✅ Dataset and BigQuery Table Handling

- Created dataset using CLI
- Used native Google Cloud Python SDK instead of pandas, to simplify integration and avoid additional dependencies.
- Verified table existence using [BigQuery's table check pattern](https://cloud.google.com/bigquery/docs/samples/bigquery-table-exists).
- Cleaned and validated table names to meet [BigQuery naming restrictions](https://cloud.google.com/bigquery/docs/tables).
- Automatically incremented table names if duplicates existed (e.g., `table_2`, `table_3`).
- Skipped files that are not CSV or located in other folders.

### ✅ Data Loading Config

- I used the following `LoadJobConfig`:
  ```python
  job_config = bigquery.LoadJobConfig(
      autodetect=True,
      column_name_character_map="V2",
      skip_leading_rows=1,
      source_format=bigquery.SourceFormat.CSV,
  )
  ```
  - `column_name_character_map="V2"`: automatically fixes problematic headers for BigQuery compatibility.
  - Based on [this official reference](https://cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.job.LoadJobConfig#google_cloud_bigquery_job_LoadJobConfig_column_name_character_map).

### 🧹 Validations and Improvements

- Verified that uploaded file is truly a `.csv`.
- Sanitized table names and checked for invalid characters or excessive length.
- Ensured headers are valid and CSV format is consistent.
- If a table with the same name already exists, a suffix is added.
- Logging is done inside the Cloud Function using `print()`, though ideally this would be sent to structured logs.

---

## 🔒 Access & Permissions

- After testing, I disabled **public access** to the bucket.
- Missing permission `roles/pubsub.publisher` was added during debugging.

---

## 🧪 Technologies Used

- Google Cloud Storage
- Google Cloud Functions (Python v1)
- BigQuery + CLI (`bq`)
- Python BigQuery SDK

---

## 🧑‍💻 Author

Pawel Gambus  
[LinkedIn](https://www.linkedin.com/in/pawel-gambus)
