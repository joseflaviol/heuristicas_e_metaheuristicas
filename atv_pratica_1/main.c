#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {

    if (argc < 2) {
        printf("No file name was provided.\n");
        exit(0);
    }

    int i;
    int number_of_items;
    int knapsack_capacity;
    int *weights;
    int *values;

    FILE *file = fopen(argv[1], "r");

    if (file == NULL) {
        printf("file not found\n");
        return 0;
    } 

    fscanf(file, "%d %d", &number_of_items, &knapsack_capacity);

    weights = (int *) malloc(sizeof(int) * number_of_items);
    values = (int *) malloc(sizeof(int) * number_of_items);

    for (i = 0; i < number_of_items; i++) {
        fscanf(file, "%d %d", &values[i], &weights[i]);
    }

    fclose(file);

    for (i = 0; i < number_of_items; i++) {
        printf("%d %d\n", values[i], weights[i]);
    }

    return 0;

}