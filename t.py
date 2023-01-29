import ctypes
import json


so_file = "./convolution.so"

convolution = ctypes.CDLL(so_file)
convolution.convolution.restype = ctypes.POINTER(ctypes.c_int)


def sendResp(statusCode, body):
    return {
        'statusCode': statusCode,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            'data': body
        }),
        "isBase64Encoded": False
    }

def main():
    a = [1, 3, 5, 6]
    b = [3, 5, 6, 7]
    if len(a) != len(b):
        print(sendResp(400, "arrays should have the same size"))
        return

    inputArraySize = len(a)
    resSize = inputArraySize*2-1
    a_arr = (ctypes.c_int * len(a))(*a)
    b_arr = (ctypes.c_int * len(b))(*b)
    tmp = convolution.convolution(a_arr, b_arr, inputArraySize)
    res = tmp[0:resSize]
    print(sendResp(200, res))

main()