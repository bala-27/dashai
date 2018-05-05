# Deploy OCP Collector - View your new Dashboard

Select Collectors from the left Dashai Menu - then choose OpenShift:

![](../images/Screenshot_2018-03-18_15.00.12.png)

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

![](../images/Screenshot_2018-03-18_17.21.48.png)

You can select also each node in your cluster to view specific node data

![](../images/Screenshot_2018-03-18_17.22.25.png)

Ok - you have your OpenShift cluster being monitored with dashai,

You will want to move you Prometheus POD to utilize Persistent Storage
This will ensure when your POD restarts you data will be maintained and available

You can go ahead and provision some storage for your POD
In our example we have Gluster configured in our Cluster

![](../images/Screenshot2018-05-04 23.33.19.png)

Now let's update the deployment config's to attach our new storage

    oc volume dc/prometheus --add --name=prom-k8s -m /etc/prometheus -t configmap --configmap-name=prom-k8s

Feel free to customize your dashboard and play with the timeline...
