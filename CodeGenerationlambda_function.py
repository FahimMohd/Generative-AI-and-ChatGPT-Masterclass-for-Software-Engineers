import json
import boto3
import datetime


def gen_code(message,language) :
    
    prompt_text = f""" Write code in {language} for following instruction : {message}.
    Assistant:
    """

    body = {
         "temperature" : 0.2,
        "top_p" : 0.8,
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens" : 1024,
        "messages" : [
            {
            "role" :"user",
            "content" :[{"type": "text", "text":prompt_text }],
            }
                    ]
            }    

    bedrock = boto3.client('bedrock-runtime')
    response = bedrock.invoke_model(body=json.dumps(body),modelId="anthropic.claude-3-haiku-20240307-v1:0")
    #print(response)
    response_content = response.get('body').read()
    response_text = json.loads(response_content)
    response_final = response_text["content"][0]["text"]
    #print(response_final)
    return response_final


def save_code_s3 (s3_bucket,s3_key, code) :
    
    s3 = boto3.client('s3')
    
    try :
        s3.put_object(Bucket = s3_bucket, Key = s3_key, Body = code)
        print ("Code saved to S3")
    except Exception as e:
        print("Error in writing to S3")
    
    

def lambda_handler(event, context):
    language = event['lang']
    message = event['message']
    
    generated_code = gen_code(message,language)
    
    if generated_code :
        current_time = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
        s3_key = f'CodeGen/{current_time}.txt'
        s3_bucket = 'awss3lecture'
        
        save_code_s3 (s3_bucket,s3_key,generated_code)
    else :
        print ("No code was generated")
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
