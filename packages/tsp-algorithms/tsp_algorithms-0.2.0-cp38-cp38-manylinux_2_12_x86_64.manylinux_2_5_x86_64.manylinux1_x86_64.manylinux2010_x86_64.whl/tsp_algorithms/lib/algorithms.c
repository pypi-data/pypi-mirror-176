#include <stdlib.h>

#include "./include/metrics.h"
#include "./include/algorithms.h"

// Generate a route using the nearest neighbor algorithm
int *nearest_neighbors(float **cost_matrix, int n){
    int *route = (int *)malloc(n * sizeof(int));
    int *current_route = (int *)malloc(n * sizeof(int));
    int *visited = (int *)malloc(n * sizeof(int));

    float path_fitness = 1000000000;
    for (int starting_node = 0; starting_node < n; starting_node++){
        for (int i = 0; i < n; i++){
            visited[i] = 0;
        }
        int current_node = starting_node;
        for (int i = 0; i < n; i++){
            current_route[i] = current_node;
            visited[current_node] = 1;
            float min_cost = 1000000000;
            int min_node = -1;
            for (int j = 0; j < n; j++){
                if (visited[j] == 0 && cost_matrix[current_node][j] < min_cost){
                    min_cost = cost_matrix[current_node][j];
                    min_node = j;
                }
            }
            current_node = min_node;
        }
        float current_fitness = route_cost(cost_matrix, current_route, n);
        if (current_fitness < path_fitness){
            path_fitness = current_fitness;
            for (int i = 0; i < n; i++){
                route[i] = current_route[i];
            }
        }
    }
    return route;
};

// Run the two opt algorithm on a route
int *two_opt(float **cost_matrix, int *route, int n){
    int *route_list = (int *)malloc(n * sizeof(int));
    int *best_route = (int *)malloc(n * sizeof(int));
    for (int i = 0; i < n; i++){
        route_list[i] = route[i];
        best_route[i] = route[i];
    }
    int improved = 1;
    while (improved){
        improved = 0;
        for (int i = 0; i < n - 1; i++){
            for (int j = i + 1; j < n; j++){
                if (j - i == 1){
                    continue; // changes nothing, skip then
                }
                int *new_route = (int *)malloc(n * sizeof(int));
                for (int k = 0; k < n; k++){
                    new_route[k] = route_list[k];
                }
                int *temp = (int *)malloc((j - i) * sizeof(int));
                for (int k = 0; k < j - i; k++){
                    temp[k] = route_list[i + k];
                }
                for (int k = 0; k < j - i; k++){
                    new_route[i + k] = temp[j - i - k - 1];
                }
                float fit = route_cost(cost_matrix, new_route, n);
                float best_fit = route_cost(cost_matrix, best_route, n);
                if (fit < best_fit){
                    for (int k = 0; k < n; k++){
                        best_route[k] = new_route[k];
                    }
                    improved = 1;
                }
            }
        }
        for (int i = 0; i < n; i++){
            route_list[i] = best_route[i];
        }
    }
    return best_route;
};
