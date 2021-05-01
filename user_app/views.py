from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import boto3
from django.conf import settings
from traceback import print_exc
import json 

def list_images(request):
    s3 = boto3.resource('s3', 
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key= settings.AWS_SECRET_ACCESS_KEY,
        aws_session_token=settings.AWS_SESSION_TOKEN
    )
    my_bucket = s3.Bucket(
        settings.AWS_BUCKET_NAME
    )

    obj = [{'thumb':file.key, 'name':file.key.split("/")[1]} for file in my_bucket.objects.filter(Prefix=settings.AWS_THUMBS_DIR+"/")]
    bucket_url = f'https://{settings.AWS_BUCKET_NAME}.s3.amazonaws.com/'
        
    return render(request, 'browse_images.html', {
        'images':obj,
        'bucket_url':bucket_url
    })

def request_process(request):
    if request.method != 'POST':
        return HttpResponse(status=405)

    data = json.loads(request.body)
    source_files = data['source-file-names']
    processor = data['image-processor-type']
    print(source_files, processor)
    for begin in range(0, len(source_files), 10):
        end = min(len(source_files), begin+10)
        messages = [
            {
                'Id':str(i), 
                'MessageBody':json.dumps(
                    {
                        'filename':str(image),
                        'destination':str(processor)+str(image),
                        'process':str(processor),
                    }
                )
            } for i, image in enumerate(source_files)
        ]
    sqs = boto3.resource('sqs', 
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key= settings.AWS_SECRET_ACCESS_KEY,
        aws_session_token=settings.AWS_SESSION_TOKEN,
        region_name=settings.AWS_DEFAULT_REGION
    )
    # Get the queue. This returns an SQS.Queue instance
    try:
        queue = sqs.get_queue_by_name(QueueName=settings.AWS_QUEUE_NAME)
        queue.send_messages(Entries=messages)
        return HttpResponse(status=202)
    except:
        print_exc()
        print("Queue does not exist")
        return HttpResponse(status=500)




    
def request_upload(request):
    s3 = boto3.client('s3', 
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key= settings.AWS_SECRET_ACCESS_KEY,
        aws_session_token=settings.AWS_SESSION_TOKEN,
        region_name=settings.AWS_DEFAULT_REGION
    )
    data = s3.generate_presigned_post(
        settings.AWS_BUCKET_NAME, 
        '${filename}',
        Fields={"acl": "public-read", "success_action_status":'201'},
        Conditions=[{'acl':"public-read"}],
        ExpiresIn=300
    )
    return JsonResponse(
        {
            'url':data['url'],
            'fields':data['fields']
        }
    )