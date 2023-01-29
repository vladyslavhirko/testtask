import json

def createResp(statusCode, body):
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

def lambda_handler(event, context):
    a_str = event["queryStringParameters"]["a"]
    b_str = event["queryStringParameters"]["b"]
    a_arr_str = a_str.split(',')
    b_arr_str = b_str.split(',')
    a = []
    b = []
    try:
        a = list(map(int, a_arr_str))
        b = list(map(int, b_arr_str))
    except:
        return createResp(400, "array should contain only integer values")

    if len(a) != len(b):
        return createResp(400, "arrays should have the same size")
    if len(a) == 0 or len(b) == 0:
        return createResp(400, "inpuit arrays should contains at least of 1 element")

    inputArraySize = len(a)
    resSize = inputArraySize*2-1
    a_arr = (ctypes.c_int * len(a))(*a)
    b_arr = (ctypes.c_int * len(b))(*b)
    tmp = convolution.convolution(a_arr, b_arr, inputArraySize)
    res = tmp[0:resSize]
    return createResp(200, res)
    # return createResp(200, res)