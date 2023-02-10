if [[ $(eksctl get cluster --name=capstone-cluster) ]]
then
    echo "cluster already exists"
else
    echo "no such cluster.. creating one..."
    eksctl create cluster --name capstone-cluster --region $AWS_DEFAULT_REGION --nodegroup-name capstone-ng --node-type t3.small --nodes-min 2 --nodes-max 2 --managed
fi