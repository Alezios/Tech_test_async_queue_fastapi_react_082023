#### Installation:

- No python version specified nor lib versions specified
- Missing lib `requests`
- Preferably use markdown with backquotes or triple backquotes to describe procedure, example:

```bash
docker run -d -it -p 5000:5000 quay.io/codait/max-image-caption-generator
docker run -d -p 5672:5672 rabbitmq:3-management

cd backend/
python3 -m venv algoregtest
source algoregtest/bin/activate
pip install fastapi python-multipart pika uvicorn requests

uvicorn main:app --reload
```

#### Usage:

- On the first run the consumer doesn't find the queue, a first image must be created
- A configuration file at the project root could be better than hardcoding the values
- Not a lot of comments or logs (for a tech test more logs could be better, but that's a personal opinion)

#### Invalid file type/extension

As you mentioned the difference is in the form-data image value. I used https://algoreg.requestcatcher.com/ on my side to see the difference.

Yours is:

```

<headers that are correct>

--------------------------d8b371448a440d5b
Content-Disposition: form-data; name="image"; filename="apple-touch-icon.png"

?PNG

<Some binary data>
```

Expected is:

```
<headers that are correct>

--------------------------d8b371448a440d5b
Content-Disposition: form-data; name="image"; filename="apple-touch-icon.png"
Content-Type: image/png

?PNG

<Some binary data>
```

The correct code is therefore:

```
path = str(body)[2:-1]
files = {
    'image': (path, open(path, 'rb'), 'image/png'), # This adds the content-type **in** the form-data value (not in the headers)
}
maxCaptionGeneratorResponse = requests.post(self.CODAIT_MAX_CAPTION_GENERATOR_URL, files=files,)
```
