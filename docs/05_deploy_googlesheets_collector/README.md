# Deploy Google Sheets Collector

Let's first prepare our data file that will feed the dashai collector

Download this example file and upload into into you google account

[https://github.com/dashai/dashai/blob/master/docs/Dashai%20Sample%20-%20Sheet.xlsx)

---

![](../images/Screenshot2018-04-2617.29.13.png)

We figured NHL hockey stats we appropriate to stick to our Canadian roots

The first tab in the sheet is where dashai will pull data from, make sure you maintain the format of the document. The "Section" comes in handy later, it will allow you to graph that entire dataset in a single section of the dashboard. (not having to add each row for example)

![](../images/Screenshot2018-04-2617.47.03.png)

The "Prep Sheet" is handy when preparing your data, since dashai will pick up any data you put into the first sheet "Arctiq - Dashboard" it is recommended to prepare your data in another tab and then paste it into the main sheet to start the data connection and limit data fields you don't want. You can also use other other cells in any tab to feed a cell in the main sheet. An example of a useful service to feed a good sheet is Zapier:

[https://zapier.com/apps/google-sheets/integrations](https://zapier.com/apps/google-sheets/integrations)

For now we would recommend just starting with the sample sheet to test the integration then add you own data and customize your dashboard to fit your needs.

---

Here is an example of the working integration:

![](../images/Screenshot2018-04-2618.31.50.png)

---

Ok now that our google sheet is ready - Let's go ahead and deploy the sheets collector

Click on the left menu again - Choose "Collectors" from the menu

You are going to select the "Google Sheets" collector

![](../images/Screenshot2018-04-2817.30.44.png)

Go ahead and select "Deploy" - You will be prompted for the information soon"

![](../images/Screenshot_2018-03-18_17.34.47.png)

Wait for the status page to display:

![](../images/Screenshot_2018-02-12_14.58.53.png)

You will be prompted for some required information that will enable connectivity to your sheet

Click the link "Click Here To Authorize DashAi"

![](../images/Screenshot_2018-03-18_17.36.01.png)

You will be prompted to login to you google account where your sheet lives

Enter you google account email address:

![](../images/Screenshot_2018-02-12_14.55.50.png)

Input your password:

![](../images/Screenshot_2018-02-12_14.57.00.png)

Allow DashAi to access your sheet (this token is only be available for a short time)

![](../images/Screenshot_2018-02-12_14.57.14.png)

Copy the token that is displayed and paste to the "Google Auth Code" box

Also paste in the URL to you google sheet (the sheet we prepared at the top of this doc)

![](../images/Screenshot_2018-03-18_17.36.01.png)

![](../images/Screenshot_2018-03-18_17.37.10.png)

Click "Submit"

You can monitor the "dashai-sheets" build in the same OpenShift project via WebUI

![](../images/Screenshot_2018-02-12_15.00.16.png)

You will see your google-sheets POD come online

![](../images/Screenshot_2018-02-12_15.02.18.png)

Select your "Dashboards" from the left hand Dashai menu

![](../images/Screenshot_2018-03-18_17.41.02.png)

You can see your new Dashboard "all the data is coming from your google sheet"

![](../images/Screenshot2018-04-2423.31.49.png)

Let's make sure it's working and collecting new data, go to your google sheet

We love the Leafs, so let's up their Stanley Cups to "50"

![](../images/Screenshot2018-04-2423.34.06.png)

Flip back to your dashboard and see the change (wow that was fast)

![](../images/Screenshot2018-04-2423.34.41.png)

Ok back to reality...

![](../images/Screenshot2018-04-2423.36.20.png)

You can see the data point drop right away

![](../images/Screenshot2018-04-2423.36.33.png)

Ok, so now it's your turn to collect you own data and start showing off you Dashboard
