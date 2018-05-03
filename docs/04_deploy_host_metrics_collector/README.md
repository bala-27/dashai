# Deploy OpenShift Collector & View Your New Dashboard

Select Collectors from the left Dashai Menu - then choose OpenShift:

![](../images/Screenshot2018-04-2817.30.07.png)

This step will deploy the OpenShift components and collector:

![](../images/Screenshot_2018-03-18_15.05.42.png)

Wait for the status page to display:

![](../images/Screenshot_2018-03-18_15.06.18.png)

You can monitor the new POD builds via the OpenShift WebUI - Let the deployment finish

Click on the Dashboards link on the left hand side

You will see your new Dashboard "DashAi OpenShift 3.x Monitoring" - Click "Launch"

![](../images/Screenshot_2018-03-18_17.20.49.png)

This will launch the Grafana WebUi

Login into the Grafana WebUI - (admin - dashai) - (*You can change the password if you like)*

![](../images/Screenshot_2018-03-18_17.21.26.png)

You will see your main OpenShift Cluster Dashboard (We loaded some baseline metrics for you)

You can select also each node in your cluster to view specific node data

![](../images/Screenshot_2018-03-18_17.22.29.png)

![](../images/Screenshot_2018-03-18_17.22.28.png)

Ok - you have your OpenShift cluster being monitored with DashAI,

Feel free to customize your dashboard and play with the timeline...
