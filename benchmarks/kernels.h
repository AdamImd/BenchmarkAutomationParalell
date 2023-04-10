#ifndef KERNLES_H
#define KERNLES_H

#include "config.h"

double naive_parallel(double array[][DIMENSION], int integerDimension, double precision, int precisionCount);
double single(double array[][DIMENSION], int integerDimension, double precision, int precisionCount);


#endif