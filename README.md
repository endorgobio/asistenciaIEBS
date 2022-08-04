# asistenciaIEBS

This project develops a tool automate the attendance control in a educational institution

* The file [Procfile](https://raw.githubusercontent.com/endorgobio/optimiserApp/master/Procfile) specifies the commands that are executed by the app on startup. You can use a Procfile to declare a variety of process types, including Your app’s web server. [details](https://devcenter.heroku.com/articles/procfile)

* The file [runtime](https://raw.githubusercontent.com/endorgobio/optimiserApp/master/runtime.txt) specifies the python version to be run.

* The file [requirements.txt](https://raw.githubusercontent.com/endorgobio/optimiserApp/master/requirements.txt) provides the dependencies to be installed

* To update the worksheets directly in googledocs the following is needed:
  * To create a Google service account (details are given here [link1](https://medium.com/@jb.ranchana/write-and-append-dataframes-to-google-sheets-in-python-f62479460cf0), [link2](https://www.analyticsvidhya.com/blog/2020/07/read-and-update-google-spreadsheets-with-python/), [link3](https://medium.com/analytics-vidhya/how-to-read-and-write-data-to-google-spreadsheet-using-python-ebf54d51a72c)
  * The library import gspread is used to access files

  
Regarding the implementation this project is a good example on how to:
* Read and write data from google drive sheets to dataframes

Regarding the app implementation in Dash, this projects is a good example for the following components:
* dcc.downloading to allow download of data 
