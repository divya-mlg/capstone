
dep_name=$1
echo "Current deployment status of $dep_name before entering wait loop:"
kubectl get deployments/$dep-name -o wide
for i in {1..10}; do
    kubectl rollout status deployment/$dep_name --timeout=1s
    if [[ "$?" -eq 0 ]]; then
        kubectl get deployments/$dep_name -o wide
        exit 0
    fi
done
exit 1