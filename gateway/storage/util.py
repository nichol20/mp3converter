import pika, json, os

import pika.spec

def upload(f, fs, channel, access):
    try:
        fid = fs.put(f)
    except Exception as err:
        print(err)
        return "internal server error", 500
    
    message = {
        "video_fid": str(fid),
        "mp3_fid": None,
        "username": access["username"],
    }

    channel.queue_declare(queue=os.environ.get("VIDEO_QUEUE"))

    try:
        channel.basic_publish(
            exchange="",
            routing_key=os.environ.get("VIDEO_QUEUE"),
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            )
        )
    except Exception as err:
        print(err)
        fs.delete(fid)
        return "internal server error", 500