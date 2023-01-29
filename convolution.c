#include <stdio.h>

int * convolution(int a[], int b[], int inputArraySize)
{
    int resArrayLength = inputArraySize*2-1;
    static int resArr[sizeof(a)/sizeof(int)*2-1];

    for (int i = 0; i < inputArraySize; i++)
    {
        int aPointer = 0;
        int bPointer = i;
        int res = 0;
        for (int j = 0; j <= i; j++){
            bPointer = i - j;
            res = res + (b[bPointer] * a[aPointer]);
            aPointer = aPointer + 1;
        }
        resArr[i] = res;
    }


    for(int i = 0; i<inputArraySize/2; i++){
       int temp = a[i];
       a[i] = a[inputArraySize-i-1];
       a[inputArraySize-i-1] = temp;
    }
    for(int i = 0; i<inputArraySize/2; i++){
       int temp = b[i];
       b[i] = b[inputArraySize-i-1];
       b[inputArraySize-i-1] = temp;
    }

    for (int i = 0; i < inputArraySize-1; i++)
    {
        int aPointer = 0;
        int bPointer = i;
        int res = 0;
        for (int j = 0; j <= i; j++){
            bPointer = i - j;
            res = res + (b[bPointer] * a[aPointer]);
            aPointer = aPointer + 1;
        }
        resArr[resArrayLength-1-i] = res;
    }

    return resArr;
}
