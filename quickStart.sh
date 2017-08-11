# Start the redis-node pods
kubectl create -f deployments/redis-node.yaml;
kubectl create -f services/redis-node.yaml;

# And start the twemproxy pods
kubectl create -f deployments/twemproxy.yaml;
kubectl create -f services/twemproxy.yaml;
