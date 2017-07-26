# Getting Started with Python on Bluemix

This is a simple demonstration on how to use the IBM Watson API to do image recognition and deploy on IBM Bluemix

This sample application is based on the IBM Bluemix Python getting started [repo](https://github.com/IBM-Bluemix/get-started-python). The essential contents of the README to help you with the deployment is reproduced from the get-started repository.

A working demo is available at the following URL: [http://imgrecognition-dizzying-duecento.mybluemix.net/](http://imgrecognition-dizzying-duecento.mybluemix.net/)

## Requirements

You'll need the following:
* [Python](https://www.python.org/download/releases/2.7/)
* [Git](https://git-scm.com/downloads)
* [Bluemix account](https://console.ng.bluemix.net/registration/)
* [Cloud Foundry CLI](https://github.com/cloudfoundry/cli#downloads)
* [Flask](http://flask.pocoo.org/)
* [Bootstrap](http://getbootstrap.com/getting-started#download)


## 1. Run the app locally

Install the dependencies listed in the [requirements.txt ![External link icon](../../icons/launch-glyph.svg "External link icon")](https://pip.readthedocs.io/en/stable/user_guide/#requirements-files) file to be able to run the app locally.

You can optionally use a [virtual environment ![External link icon](../../icons/launch-glyph.svg "External link icon")](https://packaging.python.org/installing/#creating-and-using-virtual-environments) to avoid having these dependencies clash with those of other Python projects or your operating system.

  ```
pip install -r requirements.txt
  ```

The requirements for this web application are 

* Flask==0.12.2
* cf-deployment-tracker==1.0.4
* cloudant==2.4.0
* watson_developer_cloud

To call the Image Recognition service made available by the Watson API, the commands are as follows:
 ```
from watson_developer_cloud import VisualRecognitionV3 as vr
x = vr(api_key=' key',version='version')
img = x.classify(images_url='url')
pprint.pprint(img)
 ```

Run the app.
  ```
python hello.py
  ```

View your app at: http://localhost:8000

## 2. Prepare the app for deployment

The manifest.yml includes basic information about your app, such as the name, how much memory to allocate for each instance and the route. In this manifest.yml **random-route: true** generates a random route for your app to prevent your route from colliding with others.  You can replace **random-route: true** with **host: myChosenHostName**, supplying a host name of your choice. [Learn more...](https://console.bluemix.net/docs/manageapps/depapps.html#appmanifest)
 ```
 applications:
 - name: <application_name>
   random-route: true
   memory: 128M
 ```

## 3. Deploy the app

You can use the Cloud Foundry CLI to deploy apps.

Choose your API endpoint
   ```
cf api <API-endpoint>
   ```

Replace the *API-endpoint* in the command with an API endpoint from the following list.

|URL                             |Region          |
|:-------------------------------|:---------------|
| https://api.ng.bluemix.net     | US South       |
| https://api.eu-de.bluemix.net  | Germany        |
| https://api.eu-gb.bluemix.net  | United Kingdom |
| https://api.au-syd.bluemix.net | Sydney         |

Login to your {{site.data.keyword.Bluemix_notm}} account

  ```
cf login
  ```

From within the *get-started-python* directory push your app to {{site.data.keyword.Bluemix_notm}}
  ```
cf push
  ```

This can take a minute. If there is an error in the deployment process you can use the command `cf logs <Your-App-Name> --recent` to troubleshoot.

When deployment completes you should see a message indicating that your app is running.  View your app at the URL listed in the output of the push command.  You can also issue the
  ```
cf apps
  ```
  command to view your apps status and see the URL.
