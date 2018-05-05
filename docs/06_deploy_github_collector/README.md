# Deploy Github Collector

Start by clicking on the left menu and selecting Collectors

Choose "Github Collector" - Hit "Deploy"

![](../images/Screenshot2018-04-2815.11.38.png)

Go ahead and click "Deploy"  again

![](../images/Screenshot2018-04-2815.11.46.png)

In this section we need you to provide the Github repo's you want to collect data from

![](../images/Screenshot2018-04-2817.03.56.png)

Below is an example a few different repo's you can use for testing:

    dashai/dashai, openshift/origin, kubernetes/kubernetes, prometheus/prometheus, ansible/ansible, tensorflow/tensorflow

You can use your own, make sure to follow the formatting (no , after the last repo)

---

You don't need a API token for public repo's, but Github will rate limit the data collection calls. If you use an API token you won't have that limitation.

For any Private Repo you will need an API token.

Here is an example of how to create an API token inside your Github account:

Under "Settings" (top right drop down), then "Developer Settings" (bottom left menu)

![](../images/Screenshot2018-04-2816.30.52.png)

Create a new "Personal Access Token" - Provide "repo" permission

![](../images/Screenshot2018-04-2816.32.25.png)

Copy the token, you will use it to deploy the "Github Collector"

![](../images/Screenshot2018-04-2816.33.21.png)

Enter the repo's and your token and click "Submit"

![](../images/Screenshot2018-04-2815.13.48.png)

Wait for the status screen to display

![](../images/Screenshot2018-04-2815.17.41.png)

You can flip over to your OpenShift project and see a new build and POD coming up

![](../images/Screenshot2018-04-2816.39.08.png)

If you go into the deployment config and look at the "Environment" tab you will see the repo's and API key

![](../images/Screenshot2018-04-2815.40.10.png)

If you ever want to add more repo's, you can add them at the end of the last entry

When you hit saw this will cause you new POD to redeploy and start collecting the new data

Go ahead and click on the "Dashboard" on the left side and "Launch" your Dashboard

![](../images/Screenshot2018-04-2816.35.34.png)

We have loaded some default graphs for you (feel free to customize)

![](../images/Screenshot-2018-05-05-12.10.16.png)
