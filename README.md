# Selenium Test Scripts

Scripts written in python, javascript and java leveraging seleniums webdriver framework to test functionality.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 


### Installing And Running the Test

**Javascript Test**


```
cd js-webdriverIO-test
npm install
```
This will install the dependencies needed for the project. You can run the project in two different ways:
* Provide the api token in command line and it will randomly pick a host device in the Microsoft Power BI pool
* Provide the web url along with the broswer name and version and it will execute the script on that device


```
node test.js --key=<api_token>
```
or
```
node test.js --url=<webdriver_url> --browser=<browserName> --ver=<browserVersion>
```
**Python Test**

```
cd python-test
pip install -r requirements.txt
```

Similar to the Javascript project there is two ways of running this script with the same functionality as before.
* Provide the api token in command line and it will randomly pick a host device in the Microsoft Power BI pool
* Provide the web url along with the broswer name and version and it will execute the script on that device

```
python test.py --key <api_token>
```

or

```
python test.py --url <web_driver_url> --browser <browserName> --version <browserVersion>
```






