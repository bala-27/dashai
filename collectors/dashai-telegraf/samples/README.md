# Description
This sample can be used to deploy the telegraph 1.7.2 agent on every note carrying label `telegraf-agent=true`. As this agent requires access to the underlying host operating system, it is run in the `privileged` SCC. 

Sample setup; 

- Switch to the `dashai` project

```
oc project dashai
```

- Ensure pods can run in the `privileged` SCC

```
oc adm policy add-scc-to-user privileged -z default
```

- Create the configmap and daemonset

```
oc create -f telegraf-configmap.yml
oc create -f telegraf-daemonset.yml
```

- Label nodes

```
oc label nodes telegraf-agent=true
```