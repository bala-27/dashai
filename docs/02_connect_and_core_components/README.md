# Connect to DashAI - WebUI / Connect Cluster and Deploy Core Components

Click on the route you exposed earlier - that will open the Dashai configurator:

![](../images/Screenshot_2018-02-12_14.14.01.png)

This will load the main page - Login:

![](../images/Screenshot_2018-03-18_14.49.40.png)

Connect to your Cluster:

You can use your id and password (make sure to add the OpenShift URL)

You can also use the token we used above to login via OC client - **Easiest / Quickest!**

![](../images/Screenshot_2018-03-18_14.49.53.png)

Now make sure to set the proper project (the project you just created "dashai")

![](../images/Screenshot_2018-03-18_14.52.54.png)

You cam also select the project from the left menu - "Set Project"

![](../images/Screenshot_2018-03-18_14.55.30.png)

Now its time to deploy base components (Influxdb and Grafana containers)

Choose "Deploy Base Components" from the left menu

![](../images/Screenshot_2018-03-18_14.57.08.png)

Wait for the results to display

![](../images/Screenshot_2018-03-18_14.58.08.png)

You can see the new Builds inside your OpenShift project from the WebUI:

![](../images/Screenshot_2018-02-12_14.28.04.png)

Here are your new PODs coming online

![](../images/Screenshot_2018-02-12_14.28.14.png)

You should have a new grafana route also:

![](../images/Screenshot2018-04-2422.42.43.png)

Your base components are now deployed...

You will want to move you Influxdb and Grafana PODs to utilize Persistent Storage
This will ensure when your POD restarts you data will be maintained and available

You can go ahead and provision some storage for your PODs
In our example we have Gluster configured in our Cluster

![](../images/Screenshot2018-05-04-23.18.44.png)

![](../images/Screenshot2018-05-04-23.19.27.png)

![](../images/Screenshot2018-05-04-23.20.38.png)

![](../images/Screenshot2018-05-04-23.29.30.png)

Now let's update the deployment config's to attach our new storage

    oc volume dc/dashai-influxdb --add --overwrite --name=dashai-influxdb-volume-1 --type=persistentVolumeClaim --claim-name=influxpv

    oc volume dc/grafana --add --overwrite --name=grafana-var-lib --type=persistentVolumeClaim --claim-name=grafanapv --mount-path=/var/lib/grafana
