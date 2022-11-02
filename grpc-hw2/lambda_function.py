import json
import re
import boto3
import hashlib


def lambda_handler(event, context):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('cs441-hw2-aw')

    try:
        timestamp = event["queryStringParameters"]["timestamp"]
        dT = event["queryStringParameters"]["dT"]
        getValue = event["queryStringParameters"]["getX"]
        logFile = event["queryStringParameters"]["logFile"]
    except:
        timestamp = event["timestamp"]
        dT = event["dT"]
        getValue = event["getX"]
        logFile = event["logFile"]

    logs = []
    s3_object = s3.Object('cs441-hw2-aw', 'LogsFromEC2/'+logFile)

    logs = s3_object.get()['Body'].read().splitlines()

    isPresent = check_message_presence(timestamp, logs)
    (hash_code, matched_logs) = get_matched_logs(timestamp, dT, logs)

    if (getValue == "checkIfPresent" and isPresent):
        return {
            'statusCode': 200,
            'body': json.dumps({'isPresent': "The timestamp is present in the logs",
                                'MD5': str(hash_code)})
        }

    elif (getValue == "checkIfPresent" and not isPresent):
        return {
            'statusCode': 404,
            'body': json.dumps({'isPresent': "The timestamp is not present in the logs",
                                'MD5': str(hash_code)})
        }

    elif (getValue == "matchedLogs" and isPresent):
        return {
            'statusCode': 200,
            'body': json.dumps({'isPresent': "The timestamp is present in the logs",
                                'MD5': str(hash_code),
                                'matched_logs': matched_logs})
        }

    elif (not isPresent and getValue == "matchedLogs"):
        return {
            'statusCode': 404,
            'body': json.dumps({'isPresent': "The timestamp is not present in the logs and no logs were matched.",
                                'MD5': str(hash_code),
                                'matched_logs': matched_logs})
        }
    else:
        return {
            'statusCode': 400,
            'body': 'Bad request! Please format the parameters correctly.'
        }


# Function to convert timestamp from log into a numerical value
def get_timestamp(log):
    logTime = log.split(' ')[0].split(":")
    seconds = logTime[2].split(".")

    unixTime = (int(logTime[0]) * 60 * 60 + int(logTime[1]) *
                60 + int(seconds[0]))*1000 + int(seconds[1])
    return unixTime

# Function to match pattern of a log.


def match_pattern(log):
    pattern = log.split(" ")[-1]
    return re.search("([a-c][e-g][0-3]|[A-Z][5-9][f-w]){5,15}", pattern)

# Function in O(logn) to search for logs and return the pattern matched logs.


def binary_search(timestamp, dT, logs):

    timestamp = get_timestamp(timestamp)
    delta = get_timestamp(dT)
    right_limit = timestamp + delta
    left_limit = timestamp - delta

    left = 0
    right = len(logs)-1
    mid = (left+right)//2
    flag = False
    matched_logs = []

    # Binary search to search the given timestamp and get the closest one
    while left <= right:
        mid_timestamp = get_timestamp(logs[mid].decode('utf-8'))
        if timestamp > mid_timestamp:
            left = mid + 1
        elif timestamp < mid_timestamp:
            right = mid - 1

        if left_limit <= mid_timestamp <= right_limit:
            flag = True
            break
        mid = (left+right)//2

    hash_code = ""

    # Traversing the whole range of logs where timestamp was found using the left and right limits.
    if flag:
        hash_code = hashlib.md5(logs[mid]).digest()
        goLeft = goRight = mid

        while goLeft >= 2 and get_timestamp(logs[goLeft].decode('utf-8')) > left_limit:
            goLeft -= 1
            # print(True) if match_pattern(logs[goLeft]) else print(False)
            if match_pattern(logs[goLeft].decode('utf-8')):
                matched_logs.append(logs[goLeft].decode('utf-8'))

        while goRight < len(logs) and get_timestamp(logs[goRight].decode('utf-8')) < right_limit:
            # print(True) if match_pattern(logs[goRight]) else print(False)
            if match_pattern(logs[goRight].decode('utf-8')):
                matched_logs.append(logs[goRight].decode('utf-8'))
            goRight += 1

    return (flag, hash_code, matched_logs)

# Function to check if timestamp present is in the range of logfile


def check_message_presence(timestamp, logs):
    timestamp = get_timestamp(timestamp)
    if get_timestamp(logs[0].decode('utf-8')) < timestamp < get_timestamp(logs[len(logs)-1].decode('utf-8')):
        return True
    return False

# Function to get the hashcode and all pattern matched logs


def get_matched_logs(timestamp, dT, logs):
    (_, hash_code, matched_logs) = binary_search(timestamp, dT, logs)
    return (hash_code, matched_logs)


Pattern = "([a-c][e-g][0-3]|[A-Z][5-9][f-w]){5,15}"
