import time
def stream(response):
    for chunk in response:
        if isinstance(chunk, bytes):
            text = chunk.decode('utf-8')
        else:
            text = str(chunk)
        
        for char in text:
            yield char
            time.sleep(0.007)