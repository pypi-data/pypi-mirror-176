// Calculate the route cost given a cost matrix
float route_cost(float **cost_matrix, int *route, int n){
    float cost = 0;
    for (int i = 0; i < n; i++){
        cost += cost_matrix[route[i]][route[(i+1)%n]];
    }
    return cost;
};