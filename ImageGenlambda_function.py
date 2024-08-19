import json
import boto3
import base64
import datetime

bedrock = boto3.client('bedrock-runtime')
s3 = boto3.client('s3')

def gen_image(input_prompt) :
    
    body = {
        "text_prompts" : [
            {
                "text" : input_prompt
            }
                        ],
            "cfg_scale" : 7 
            }

    #Simply put, the CFG scale (classifier-free guidance scale) or 
    #guidance scale is a parameter that controls how much the image generation process follows the text prompt. 
    #The higher the value, the more the image sticks to a given text input.
    
    response = bedrock.invoke_model(body=json.dumps(body),modelId="stability.stable-diffusion-xl-v1")
    response_byte = json.loads(response['body'].read())
    response_base64 = response_byte['artifacts'][0]['base64']
    response_final = base64.b64decode(response_base64)
    return response_final
    
    #print(response_final)


def save_image_s3(s3_bucket,s3_key,generated_image) :
    
    try :
        s3.put_object (Bucket = s3_bucket, Key = s3_key, Body = generated_image)
        print ("Image saved to S3")
    except Exception as e:
        print ("Error in writing to S3")


def lambda_handler(event, context):
    input_prompt = event['prompt']
    print(input_prompt)
    
    generated_image = gen_image(input_prompt)
    
    if generated_image :
        current_time = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
        s3_key = f'ImageGen/{current_time}.png'
        s3_bucket = 'awss3lecture'
        
        save_image_s3(s3_bucket,s3_key,generated_image )
    else:
        print ("No Image was generated")
    
    
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
