# oms-api-tests
This repository contains automated tests and a CI/CD pipeline for validating the Order Management System (OMS) used in an e-commerce platform. The OMS enables customers to place and track orders while allowing administrators to manage order statuses through a RESTful API built with FastAPI and MongoDB.


## Test Reports

Test reports are generated in JUnit XML format and stored as CI artifacts (e.g., `results.xml`).



## Known Issues

- The PATCH `/orders/{order_id}` endpoint test has been temporarily skipped due to time constraints.
- Functionality will be finalized and tested in a future revision.