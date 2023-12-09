[![install](https://github.com/nogibjj/IDS706_Fall2023_Final_Team_Project/actions/workflows/install.yml/badge.svg)](https://github.com/nogibjj/IDS706_Fall2023_Final_Team_Project/actions/workflows/install.yml)
[![lint](https://github.com/nogibjj/IDS706_Fall2023_Final_Team_Project/actions/workflows/lint.yml/badge.svg)](https://github.com/nogibjj/IDS706_Fall2023_Final_Team_Project/actions/workflows/lint.yml)
[![format](https://github.com/nogibjj/IDS706_Fall2023_Final_Team_Project/actions/workflows/format.yml/badge.svg)](https://github.com/nogibjj/IDS706_Fall2023_Final_Team_Project/actions/workflows/format.yml)
[![test](https://github.com/nogibjj/IDS706_Fall2023_Final_Team_Project/actions/workflows/test.yml/badge.svg)](https://github.com/nogibjj/IDS706_Fall2023_Final_Team_Project/actions/workflows/test.yml)
# IDS706 Fall 2023 Final Project

Team members: Yuchen Zhang (yz674) Xuesen Wen (xw202) Yuhan Xue (yz167) Rui Chen (rc381) Junhan Xu (jx139)

Repository for IDS706-Data Engineering Systems Fall 2023 Final Project.

This project includes the following:
- ``Data Engineering Pipeline``: The main part of this project. ``eda-bank-loan-default-risk-analysis`` is a Jupyter Notebook that contains the whole process of Extracting, Transforming and Loading data for analysis, which applies multiple EDA methods to analyze the bank load data and comes up with useful conclusions. Due to the volumn of dataset and the large amount of computation, the notebook is deployed and run on ``Azure Databricks`` platform for the best performance.

- ``Microservice``: The interface between the users and data pipeline mentioned above, implemented in ``app.py``. It is built with ``FastAPI``, which provides simple APIs that users can visit using ``HTTP`` requests, hiding all the underlying details of interacting with ``SQL database``. The microservice is deployed on ``Azure App Service``, which provides the auto-scaling feature that enhances the availability of the application.

- ``Container Configuration``: ``Dockerfile`` contains the process of building a ``Docker`` container that is compatible with the runtime environement for the microservice mentioned above. Note that it is crutial to include ``driver.sh`` in the container, as ``msodbcsql18`` driver needs to be installed separately for the microservice to interact with ``Azure SQL database``.

- ``Load test``: ``Locust`` library is used for load testing the microservice deployed on ``Azure``. It has fantastic features of customizing the load and visulize performance results over time.

- ``Continuous Integration and Continuous Delivery (CI/CD)``

- ``GitHub Configurations``

- ``Infrastructure as Code (IaC)``

## Architectural Diagram
![](<img/Architectural Diagram.jpg>)

## Data Engineering Pipeline: Bank Loan Default Risk Analysis
In this pipeline, we demonstrate a case study, giving us an idea of applying EDA in a real business scenario, based on ``loan-defaulter`` dataset from ``Kaggle``. The pipeline is included in ``eda-bank-loan-default-risk-analysis.ipynb``, making use of ``Pandas`` library to load and manipulate the data. The notebook is deployed on ``Azure Databricks``, and the datasets can be directly loaded from ``Databricks File System``. The notebook includes several steps:
- ``Load Data``: Import the csv dataset files, check the dimensions and columns
- ``Data cleaning and manupulation``: Inspect the dataset, remove or interpolate invalid or missing values
    - For example, we remove some of the columns by checking if they have low correlation between them
    ![](img/pipeline_0.png)
- ``Data Analysis``: Apply multiple EDA methods to analyse the data, giving out reasonable inferences, here are some examples:
    - Analysing if owning a car is related to loan repayment status: Clients who own a car are half in number of the clients who dont own a car. But based on the percentage of deault, there is no correlation between owning a car and loan repayment as in both cases the default percentage is almost same. ![](img/pipeline_1.png)
    - Analysing housing type based on loan repayment status: Majority of people live in House/apartment; People living in office apartments have lowest default rate; People living with parents (~11.5%) and living in rented apartments(>12%) have higher probability of defaulting ![](img/pipeline_2.png)
    - Checking loan repayment status based on Organization type: Organizations with highest percent of loans not repaid are Transport: type 3 (16%), Industry: type 13 (13.5%), Industry: type 8 (12.5%) and Restaurant (less than 12%). Self employed people have relative high defaulting rate, and thus should be avoided to be approved for loan or provide loan with higher interest rate to mitigate the risk of defaulting.![](img/pipeline_3.png)

## Microservice: FastAPI application
``FastAPI`` library enables us to easily build microservice that provides users with APIs that can be reached via HTTP requests. In this project, we created a ``uvicorn`` microservice that interfaces with the data engineering pipeline; specifically, our users can use the API to query the ``Azure SQL database``. The microservice is containerized with ``Dockerfile``, stored on ``Docker Hub`` and deployed on ``Azure App Service``. It has several steps:
- ``ODBC Driver Installation``: included in ``driver.sh``. ``ODBC Driver`` is a necessary component for the microservice to interact with ``Azure SQL database``.
- ``Data Preparation``: included in ``data_prepare.py``. It reads datasets from ``Azure Blob Storage`` to ``pandas dataframe``, then makes use of ``SQLAlchemy`` and ``pyodbc`` to write the data to ``Azure SQL databse``.
- ``Azure App Service``: users can reach out to the service via the public domain provided by ``Azure App Service`` and get the results of SQL queries, for example, this route simply returns all the rows in the database:![](img/fastapi_1.png)
- ``Load Test``: Note that ``Azure App Service`` automatically scale up based on the amount of user requests. We use ``locust`` to simulate concurrent user requests to apply load test to the microservice. It turns out that the result of load test is restricted by the performance of ``Azure VM`` - the VM has ``4 vCPUs`` and ``16GB`` RAMs, and we enabled ``multi-core mode`` of ``locust``, but the peak ``RPS (requests per second)`` is around ``2000``. We can tell that the bottlenect was not on ``Azure App Service`` but was on ``Azure VM`` because the ``CPU percentage`` and ``memory percentage`` of the application is quite low when the load test is running, as shown below:
![](img/fastapi_2.png)![](img/fastapi_3.png)

## Miscellaneous
- ``Infrastructure as Code (IaC)``: We make use of ``Azure Resource Manager (ARM)`` templates to deploy the ``Azure App``. Specifically, we added customized template to ``Azure Portal``: 
```json
{
    "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
    "contentVersion": "1.0.0.0",
    "parameters": {
        "name": {
            "type": "string"
        },
        "location": {
            "type": "string"
        }
    },
    "resources": [
        {
            "type": "Microsoft.Web/sites",
            "apiVersion": "2018-11-01",
            "name": "[parameters('name')]",
            "location": "[parameters('location')]",
            "kind": "app",
            "properties": {
                "serverFarmId": "[resourceId('Microsoft.Web/serverfarms', parameters('name'))]"
            }
        },
        {
            "type": "Microsoft.Web/serverfarms",
            "apiVersion": "2018-02-01",
            "name": "[parameters('name')]",
            "location": "[parameters('location')]",
            "sku": {
                "name": "F1",
                "capacity": 1
            }
        }
    ]
}
```
![](img/mis_1.png)
- ``Continuous Integration and Continuous Delivery (CI/CD)``: enabled by ``GitHub Actions`` defined in ``.github/workflows``
- ``GitHub Configurations``: enabled in ``.devcontainer`` configurations for ``GitHub Codespaces``, making the local version of project completely reproducible
- ``Quantitative Assessment``: see the ``Load Test`` part of ``Microservice`` content above