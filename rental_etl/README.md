# Airflow: Zing Chart Crawler

## Introduction

This is a sample project to get acquainted with Apache Airflow and use it to crawl data from Zing's Chart rankings.

## Installation

Before getting started, you'll need to install the following software and libraries:

- Docker
- Python 3.x

## Directory Structure

    dags/: Contains DAGs.
    scripts/: Contains scripts related to data crawling.
    data/: Where the crawled data is stored.

## Usage

1. Setup docker:
   ```shell
   docker compose up
   ```

2. Create .venv for test code:

   To be able to run a test to check whether the function runs successfully or not before creating a test DAG on Airflow.

   ```
   
   ```
