from django.shortcuts import render, redirect
from django.http import HttpResponse
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
    if request.method == 'POST':
        source_file = request.POST.get('source-file-name')
        destination_file = request.POST.get('destination-file-name')
        processor = request.POST.get('image-processor-type')
        print(source_file, destination_file, processor)
        mbody = {
            'filename':source_file,
            'destination':destination_file,
            'process': processor
        }
        sqs = boto3.resource('sqs', 
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key= settings.AWS_SECRET_ACCESS_KEY,
            aws_session_token=settings.AWS_SESSION_TOKEN
        )
        # Get the queue. This returns an SQS.Queue instance
        try:
            queue = sqs.get_queue_by_name(QueueName=settings.AWS_QUEUE_NAME)
            queue.send_message(MessageBody=json.dumps(mbody))
        except:
            print_exc()
            print("Queue does not exist")

    return redirect('browse')