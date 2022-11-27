import boto3
import json
from io import BytesIO
from PIL import Image, ImageOps  #PIL requires a package called pillow with an ARN for the region
import os 
import uuid
from datetime import datetime

s3 = boto3.client('s3')
size = int(os.environ.get('THUMBNAIL_SIZE')) #defined in environment variables in template file
dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('IMAGEDATA_TABLE') 

def s3_thumbnail_generator(event, context):


    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    img_size = event['Records'][0]['s3']['object']['size']


    if (not key.endswith("_thumbnail.png")):  #only items not ending with "_thumbnail.png" are taken since we give the particular tail to processed image 

        image = get_s3_image(bucket, key)

        thumbnail = image_to_thumbnail(image)

        thumbnail_key = new_filename(key)

        url = upload_to_s3(bucket=bucket, key=thumbnail_key, image=thumbnail, img_size=img_size)

        return url

def get_s3_image(bucket, key):

    response = s3.get_object(Bucket=bucket, Key=key) #retireves image
    imagecontent = response['Body'].read() 

    file = BytesIO(imagecontent) #access the image

    img = Image.open(file) #create the image

    return img


def image_to_thumbnail(image):

    return ImageOps.fit(image, (size,size), Image.ANTIALIAS) #resized image


def new_filename(key):

    key_split = key.rsplit('.', 1)   #splits the string from the right and adds a "." separator 
    return key_split[0] + "_thumbnail.png" #renamed thumbnail from original



def s3_save_thumbnail_url_to_dynamodb(url_path, img_size):

    to_int = round((float(img_size*0.53)/1000), 2)  #rounds the output value to two decimal characters 
    table = dynamodb.Table(table_name) #takes the table from dynamodb in aws
    response = table.put_item(

        Item = {

            'id': str(uuid.uuid4()), #generates a random large id 
            'url': str(url_path),
            'approxReducedSize': str(to_int) + str('KB'),        #fills the table with id and attributes for the primary key
            'createdAt': str(datetime.now()),
            'updatedAt': str(datetime.now())
        }
    )


    return {
        'statusCode': 200,
        'headers': {'Content-type':'application/json'},
        'body': json.dumps(response)
    }
    
    
def s3_get_thumbnail_urls(event, context):

    
    table = dynamodb.Table(table_name)
    response = table.scan()
    data = response['Items']

  
    while 'LastEvaluatedKey' in response:        #loops through values in response
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(data)
    }

def s3_get_item(event, context):

    table = dynamodb.Table(table_name)
    response = table.get_item(Key={

        'id': event['pathParameters']['id']
    })

    item = response['Item']

    return {
        'statusCode': 200,
        'headers': {'Content-type':'application/json',
                    'Access-Control-Allow-Origin':'*'},   #allows anyone to access the image and it is available via the internet
        'body': json.dumps(item),
        'isBase64Encoded': False,

    }


def s3_delete_item(event, context):

    item_id = event['pathParameters']['id']

 
    response = {
        "statusCode": 500,
        "body": f"An error occured while deleting post {item_id}"
    }

    table = dynamodb.Table(table_name)

    response = table.delete_item(Key={
        'id': item_id
    })
    all_good_response = {
        "deleted": True,
        "itemDeletedId": item_id
    }


    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        response = {
            "statusCode": 200,
            'headers': {'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*'},
            'body': json.dumps(all_good_response),
        }
        
    return response


def upload_to_s3(bucket, key, image, img_size):

    out_thumbnail = BytesIO()                     

    image.save(out_thumbnail, 'PNG')
    out_thumbnail.seek(0)


    response = s3.put_object(           #item details, permissions and configurations

        ACL = 'public-read',
        Body = out_thumbnail,
        Bucket = bucket,
        ContentType = 'image/png',
        Key = key
    )

    print(response)

    url = '{}/{}/{}'.format(s3.meta.endpoint_url, bucket, key)

    s3_save_thumbnail_url_to_dynamodb(url_path=url, img_size=img_size)   #saves the url of the image to dynamodb table

    return url