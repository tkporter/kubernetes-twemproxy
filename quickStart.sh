kubectl create -f deployments/redis-node.yaml;
kubectl create -f services/redis-node.yaml;

kubectl create -f deployments/twemproxy.yaml;
kubectl create -f services/twemproxy.yaml;
