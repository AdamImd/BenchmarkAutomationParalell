#include "config.h"
#include "kernels.h"
#include <math.h>


double single(double array[][DIMENSION], int integerDimension, double precision, int precisionCount){
    double result = 0.0;
    for (int i = 1; i < integerDimension - 1; i++) {
        for (int j = 1; j < integerDimension - 1; j++) {
            result = (array[i-1][j] + array[i+1][j] + array[i][j-1] + array[i][j+1]) / 4;
            if (fabs(result - array[i][j]) < precision)
                precisionCount++;
            array[i][j] = result;
        }
    }
    return precisionCount;
}

double naive_parallel(double array[][DIMENSION], int integerDimension, double precision, int precisionCount){
    double result = 0.0;
    #pragma omp parallel for reduction(+:precisionCount)
    for (int i = 1; i < integerDimension - 1; i++) {
        for (int j = 1; j < integerDimension - 1; j++) {
            result = (array[i-1][j] + array[i+1][j] + array[i][j-1] + array[i][j+1]) / 4;
            if (fabs(result - array[i][j]) < precision)
                precisionCount++;
            array[i][j] = result;
        }
    }
    return precisionCount;
}