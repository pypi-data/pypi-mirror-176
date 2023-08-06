# webserver
This is the webserver for the Hubspot data extraction ETL "pipeline". Its purpose is to receive POST requests from the Zapier integration with the exported report download link.

## .env file
The .env file must have the following variables:
  - **CHROME_USER_DATA_DIR** and **CHROME_PROFILE_FOLDER**: Google Chrome stuffs;
  - **HUBSPOT_LOGIN_EMAIL**: Gmail address used in the "Sign in with Google" page;
  - **DOWNLOADS_FOLDER**: absolute path to the downloads folder;
  - **BIGQUERY_TABLE_ID**: target BQ table.
