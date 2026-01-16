# 🔴 Real-Time Clickstream Analytics Platform

This project implements a **real-time clickstream data processing pipeline** using **Azure Event Hubs**, **PySpark Structured Streaming**, and **Delta Lake**.  
It follows the **Medallion Architecture (Bronze–Silver–Gold)** to ingest, process, and aggregate continuous user interaction events into analytics-ready datasets.

The pipeline is designed to be **low-latency, scalable, and production-oriented**, closely reflecting real-world streaming data platforms.

---

## 🏗️ Architecture Overview
Clickstream Generator (Python)
↓
Azure Event Hubs
↓
Spark Structured Streaming
↓
Bronze → Silver → Gold (Delta Lake on ADLS Gen2)


### Medallion Layers

#### 🥉 Bronze — Raw Streaming Ingestion
- Consumes clickstream events from **Azure Event Hubs**
- Enforces schema using `from_json`
- Captures ingestion metadata:
  - Event Hub enqueue time
  - Spark ingestion timestamp
- Writes append-only raw events to **Delta Lake**
- Uses checkpointing for fault tolerance and exactly-once processing

---

#### 🥈 Silver — Cleansed & Enriched Streaming Data
- Applies real-time transformations on Bronze data
- Standardizes browser values and extracts domain from URLs
- Filters invalid or incomplete events
- Flattens nested product arrays into a normalized structure
- Produces a clean, analytics-ready streaming dataset
- Maintains schema consistency for downstream aggregations

---

#### 🥇 Gold — Session-Level Analytics (Stateful Streaming)
- Builds **session-based aggregates** using event-time processing
- Uses watermarks to handle late-arriving events and control state growth
- Computes key session metrics:
  - Session start and end time
  - Total events per session
  - Unique page views
  - Add-to-cart and purchase counts
  - Total purchase value
  - Products and categories viewed
- Performs **merge-based upserts** into Delta tables using `foreachBatch`
- Ensures idempotent and scalable aggregation updates

---

## 📊 Key Analytics Outputs

### Session Insights
- User session duration and engagement
- Conversion-related metrics (add-to-cart, purchases)
- Product and category interaction tracking

These datasets can be directly consumed by BI tools or downstream analytics workloads.

---

## 🔄 Streaming & Incremental Processing Design

- **Structured Streaming** ensures continuous, low-latency data ingestion
- **Event-time watermarks** enable correct handling of late data
- **Checkpointing** guarantees fault tolerance and restart safety
- **Delta Lake MERGE operations** ensure exactly-once updates for aggregated data
- No destructive overwrites — all layers are built for incremental processing

---

## 🛠️ Tech Stack

| Category | Tools |
|--------|------|
| **Cloud Platform** | Azure |
| **Messaging** | Azure Event Hubs |
| **Data Processing** | Apache Spark (Structured Streaming), Databricks |
| **Storage** | Azure Data Lake Storage Gen2 |
| **Table Format** | Delta Lake |
| **Language** | Python, SQL |

---

## ✅ Engineering Highlights
- Real-time ingestion with Azure Event Hubs
- Event-time–aware streaming transformations
- Stateful session aggregation using watermarks
- Medallion Architecture (Bronze–Silver–Gold)
- Production-grade checkpointing and fault tolerance
- Analytics-ready Delta Lake tables

---

## 📌 Why This Project Matters
This project demonstrates **real-world streaming data engineering practices**, including:
- Designing low-latency ingestion pipelines
- Handling late and out-of-order events
- Building scalable stateful aggregations
- Applying clean data contracts between Medallion layers

It closely mirrors how **production clickstream analytics platforms** are built in modern cloud environments.

---

## 🚀 Future Enhancements
- Add real-time dashboards (Power BI / Azure Synapse / Databricks SQL)
- Implement user-level and product-level rolling aggregations
- Introduce data quality metrics and monitoring
- Extend to multi-region Event Hub ingestion

---

