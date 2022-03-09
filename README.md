# Insights Data Provider

Copyright © Bentley Systems, Incorporated. All rights reserved.

[iTwin.js](http://www.itwinjs.org) is an open source platform for creating, querying, modifying, and displaying Infrastructure Digital Twins. To learn more about the iTwin Platform and its APIs, visit the [iTwin developer portal](https://developer.bentley.com/).

## About this Repository

This repository contains a python tool to fetch iModel insights data through reporting APIs and save results in a csv file.

Visit the [Insights API](https://developer.bentley.com/apis/insights/) for more documentation on the insights service.

## Setup


  ### Create Agent Client Application

  - [Register an Agent Application](https://developer.bentley.com/register/)
  - Give your agent application a name.
  - Choose "Service" application type.
    - Select `Visualization` and `Reporting & Insights` API associations
    - Save `Client ID`, `Client Secret`, `Client email` and `Scopes` (Be sure to save the secret somewhere safe - it is only shown once)
  - Add `{client_id}@apps.imsoidc.bentley.com` as a project participant of your project.

  > Allow some time after registering the agent application. The identity profile of the agent is being created in the background and can take between 5 and 10 minutes
  > Make sure you have `View/Configure` RBAC permissions under `Insights and Reporting` category in your project role.

  ### Environment Variables

  ```
  # Authorization
  CLIENT_ID=
  CLIENT_SECRET=
  SCOPE="insights:read insights:modify"
  GRANT_TYPE='client_credentials'
  TOKEN_URL=https://ims.bentley.com/connect/token

  # Data Source
  BASE_URL=https://api.bentley.com/insights/reporting/odata/
  REPORT_ID=
  ```

## Usage

```
python data.py -o [OutputCSVFile]
```

## Report Configuration

You can choose to either use [Insights API](https://developer.bentley.com/apis/insights/) or [Grouping-Mapping-Widget](https://www.npmjs.com/package/@itwin/grouping-mapping-widget) UI to modify report content.

To use grouping-mapping-widget, you need to setup local environment:
  1. Create a SPA client app similar to [agent](#create-agent-client-application) but choose `SPA` instead of `Service` application type.
  2. Clone and build itwin viewer
      ```
      git clone https://github.com/Guillar1/itwin-viewer-sample-dev.git
      ```
  3. Copy client_id, redirect_url and scopes from step 1 into .env file.

> You need to run [extraction](https://developer.bentley.com/apis/insights/operations/run-extraction/) after modifying grouping and mappings.


## Visualize [Sample Report](https://www.itwinjs.org/sandboxes/HelenZhou/ReportingAPI)
