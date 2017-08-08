kubectl create configmap redis-conf --from-file=redis.conf;
kubectl create -f deployments/redis01.yaml;
kubectl create -f deployments/redis02.yaml;
kubectl create -f services/redis01.yaml;
kubectl create -f services/redis02.yaml;

kubectl create configmap twemproxy-conf --from-file=twemproxy.yml;
kubectl create -f deployments/twemproxy.yaml;
kubectl create -f services/twemproxy.yaml;
