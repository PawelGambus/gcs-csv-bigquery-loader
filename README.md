# ☁️ Recruitment Task – Cloud Function + BigQuery

This repository presents my solution to a recruitment task, which involved building an automated data pipeline based on Google Cloud Platform (GCP).

---

## 📝 Task Description

Log in to the Google Cloud Platform console and select the project `alterdata-rekrutacja-46`, where you have full permissions.

**Task**:
- Create your own bucket in Google Cloud Storage.
- Write a Cloud Function (v1) that:
  - is triggered when a `.csv` file is uploaded,
  - automatically creates a corresponding table in BigQuery using schema autodetection (`autodetect=True`).

---

## 🚀 My Approach

### ✅ Region Selection and Resource Configuration

- I selected the `europe-central2 (Warsaw)` region due to its low cost and physical proximity.
- The bucket and the Cloud Function were both deployed in the same region.
- I disabled replication to avoid unnecessary costs.
- The bucket name is random but clearly indicates its purpose.

### ✅ Cloud Function – Trigger and Configuration

- I used the trigger `google.cloud.storage.object.v1.finalized`, which activates when a file is created in the bucket.
- I verified that uploading a CSV file correctly triggers the function.
- I configured minimal resources and limited concurrency to a single execution due to the expected low workload.

### ✅ BigQuery Handling

- I created a dataset.
- I used `autodetect=True` and additional configuration:
  ```python
  job_config = bigquery.LoadJobConfig(
      autodetect=True,
      column_name_character_map="V2",
      skip_leading_rows=1,
      source_format=bigquery.SourceFormat.CSV,
  )
  ```
- I applied automatic cleaning of column names (`column_name_character_map="V2"`).
- I removed invalid characters from table names and shortened them if necessary.
- If table name conflicts occurred, I appended incremental numbers (`tablename_2`, `tablename_3`, ...).
- I validated that the uploaded file is a proper CSV and not located in an unsupported folder.

### 🧹 Validation and Cleanup

- I implemented validation of the CSV headers.
- I ensured the function handles missing data, incorrect formats, and missing schemas gracefully.
- I kept the environment clean by manually removing test files and tables.

---

## 🧪 Technologies and Tools

- Google Cloud Storage
- Google Cloud Functions (Python, v1)
- BigQuery + CLI (`bq`)
- Python client for BigQuery

---

## 🧑‍💻 Author

Pawel Gambus  
[LinkedIn](https://www.linkedin.com/in/pawel-gambus)
