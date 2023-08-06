# The exporter
Run by the cronjob on the server, this will open an automated browser window, login and click the export link on the report page

## .env file
The .env file must have the following variables:
  - **CHROME_USER_DATA_DIR** and **CHROME_PROFILE_FOLDER**: Google Chrome user data dir and folder name. Go to the browser settings to copy;
  - **EXPORT_START_URL**: URL of the report. You end up in this page after you click on the report name on the main reports page;
  - **CHROMEDRIVER_EXECUTABLE_PATH**: absolute path to the chromedriver executable;
  - **HUBSPOT_LOGIN_EMAIL**: Gmail address used to login into hubspot. This email address must appear on the "Sign in with Google" page for the bot to be able to login and continue.