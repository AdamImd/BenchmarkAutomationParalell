#include <stdio.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>
#include <math.h>
#include "./config.h"

int main() {
    int integerDimension = DIMENSION;
    double precision = PRECISION;

    // Initialize random seed
    srand(time(NULL));
    
    double (*array)[integerDimension];
    array = malloc(integerDimension * sizeof(*array));
    printf("Dimension: %d \n", integerDimension);
    printf("Precision: %f \n", precision);

    for (int i = 0; i < integerDimension; i++) {
        for (int j = 0; j < integerDimension; j++) {
            // Random value between 0 and 100
            array[i][j] = (double)rand() / (double)RAND_MAX * 100;
        }
    }
    
    int precisionCount = 0;

    while (1) {
        double result = 0.0;
        // average 4 numbers around it
        #pragma omp parallel for reduction(+:precisionCount)
        for (int i = 1; i < integerDimension - 1; i++) {
            for (int j = 1; j < integerDimension - 1; j++) {
                result = (array[i-1][j] + array[i+1][j] + array[i][j-1] + array[i][j+1]) / 4;
                //Check if the result is within the precision
                if (fabs(result - array[i][j]) < precision)
                    precisionCount++;
                array[i][j] = result;
            }
        }
        printf("Precision count: %d/%d \n", precisionCount, (integerDimension - 2) * (integerDimension - 2));
        if (precisionCount == (integerDimension - 2) * (integerDimension - 2)) {
            break;
        }
        precisionCount = 0;
    }
    printf("Result: %f \n", array[integerDimension/2][integerDimension/2]);

}