if [[ $(kubectl get deployment capstone) ]]
then
    echo "deployment already exists"
else
    echo "creating deployment"
    kubectl create deployment capstone --image=divyavan/capstone:latest
    sleep 10
fi
if [[ $(kubectl get svc capstone-service) ]]
then
    echo "service already exists"
else
    echo "creating service"
    kubectl expose deployment capstone --name=capstone-service --type=NodePort --port=5000 --target-port=5000
fi