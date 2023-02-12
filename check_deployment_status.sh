
dep_name=$1
for i in {1..10}; do
    kubectl rollout status deployment/$dep_name --timeout=1s
    if [[ "$?" -eq 0 ]]; then
        kubectl get deployments/$dep_name
        exit 0
    fi
done
exit 1