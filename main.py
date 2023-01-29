import json
import ctypes

so_file = "convolution.so"

convolution = ctypes.CDLL(so_file)
convolution.convolution.restype = ctypes.POINTER(ctypes.c_int)

def create_resp(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            'data': body
        }),
        "isBase64Encoded": False
    }

def lambda_handler(event, context):
    try:
        a_str = event["queryStringParameters"]["a"]
        b_str = event["queryStringParameters"]["b"]
    except:
        return create_resp(400, "[a] and [b] all arrays should be passed. Example: ?a=1,2,3&b=3,4,5")

    a_arr_str = a_str.split(',')
    b_arr_str = b_str.split(',')

    try:
        a = list(map(int, a_arr_str))
        b = list(map(int, b_arr_str))
    except:
        return create_resp(400, "array should contain only integer values")

    if len(a) != len(b):
        return create_resp(400, "arrays should have the same size")
    if len(a) == 0 or len(b) == 0:
        return create_resp(400, "input arrays should contains at least of 1 element")

    input_array_size = len(a)
    res_size = input_array_size*2-1
    a_arr = (ctypes.c_int * len(a))(*a)
    b_arr = (ctypes.c_int * len(b))(*b)
    tmp = convolution.convolution(a_arr, b_arr, input_array_size)
    res = tmp[0:res_size]
    return create_resp(200, res)

