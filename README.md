## Prerequisites

Make sure to have downloaded all dependencies (fastapi, python-mutlipart, python-pika, uvicorn, sqlite3)
It is necessary for the docker images 'rabbitmq:3-management' and 'quay.io/codait/max-image-caption-generator:latest' to run as localhost containers, respectively on port 5672:5672 and 5000:5000.

## Download

Download the archive and unzip it at the location of your choice. Please make sure the location allows non-admin users and programs to make directories

## Test and run the project

go to 'backend/' and run the command 'uvicorn main:app --reload'

WARNING (To the attention of Romaric Mourgues): Because of the delay I suffered while trying to make the max-caption-generator work (see email) I couldn't find enough time to do the frontend. Only the backend upload endpoint works partly. Sadly, since the caption (and thus keywords) generator doesn't work, i couldn't provide a search endpoint relying upon it either.

Once the application startup is complete, the API should be listening for request on localhost port 8000. You may test it by running
'curl -F "image=@<path_to_your_desired_image>" -X POST http://localhost:8000/image/upload'
from another terminal

## What happens

### On startup

First, upon startup, the API will initialize an IImageRepository (SQLiteDatabase) and an ICaptionGenerator (RabbitMQCaptionGeneratorService). When SQLiteDatabase is initialized, it will create a 'db_images.db' file database if absent. This file shall be located in 'backend/DAL/db/', which will also be created if absent.
RabbitMQCaptionGeneratorService starts two instances, a rabbitMQ producer, and a rabbitMQ consumer, both establishing a connection with rabbitMQ server running on localhost, on the standard port (5672). They'll declare the 'images_captioning' queue.
The RabbitMQCaptionGeneratorConsumer consumer also has his 'start_consuming()' function be run on a separate Thread upon startup, so it may keep on waiting messages while the rest of the application works.

### On curl post command

The API should convert the sent file to an Image model class, also verifying if the file is an actual image. Then it should try to register the Image as a file in a directory '/backend/DAL/db/images' (creating the directories if they're absent). Once done, it will save the path to the newly registered image in the sqlite3 database.

The API will then try to ask max-caption-generator to create a caption and keywords for the same Image. Through dependency injection, Image will ask RabbitMQCaptionGeneratorService to generate a caption. The service will use its producer (RabbitMQCaptionGeneratorProducer) to dispatch the image path as a message, to the rabbitMQ server 'images_captioning' queue.
The consumer, still running in a separate thread, will consume the message and try to handle it. By handling, I mean opening a stream object to the image using 'open(<path>, 'rb')' and send it as an HTTP POST request to the max-caption-generator API running in a container (http://localhost:5000/model/predict)
Unfortunately, the project stops there, as I cannot find any solution to the response '{"message": "Invalid file type/extension. Please provide an image in JPEG or PNG format."}' that I get. No matter how many different syntax I try for the request.


### Reminder of the subject
## Advanced search in images

### Synopsis

Google Drive and Apple Photos provides a way to search images using keywords, for instance search "dog" and find all your pictures of your dog.

In this technical test we will create a backend to upload images, generate keywords for them in a async queue, then expose a search endpoint.

### Subject

1. The development must be in **python** using **FastApi**.
2. You will provide a README.md containing description of how to run your project.
3. You will note the time used for this project but there is no strict time limit.
4. Finally the code will be accessible from your Github with the license you prefer (MIT, AGPL, etc). In this specific test you can have two folders `frontend/` and `backend/`

Your focus will be:
- Create a **FastApi** python server
- Use a small database (or directly store in JSON files, use what you prefer) to store the keywords of the files
- Implementing a MQ (message queue service) using **RabbitMQ** with docker `docker run -d -p 5672:5672 rabbitmq:3-management` and https://github.com/pika/pika (normalement le username/password sera guest:guest, un exemple de emiter/consumer de job est présent ici: https://github.com/pika/pika#example)
- Use the caption generator from https://hub.docker.com/r/codait/max-image-caption-generator (as described in #use-the-model you just have to call it as an external API on port 5000)
- Do some frontend from an existing code base

### Work to do (backend)

1. Install/run/test the libraries mentioned above
2. Create two endpoints: upload a file, and search file
3. The upload endpoint must: store the file, add it to the database, then create a rabbitmq job (the job will only contain the database id)
4. Create a rabbitmq job listener that will handle any incomming job, call the max-image-caption-generator, wait for reply and update the database object.
5. Create a search file endpoint. If no search term is provided, return everything the most recent first. Or use the search term to select corresponding images. Also includes pagination and limits.

### Work to do (frontend)

1. Download and open the attached ZIP (https://gist.github.com/RomaricMourgues/789394db37760a0e21bd36b1fa4fca89/raw/19fb1a98d33cdb72d7dcd0552083e35cd0217c34/frontend.zip) that contains an initial code base in React, note: this project uses **typescript**, **tailwind**, and React **hooks**.
2. Run a `yarn install` then `yarn start` you should see a basic search bar
3. Implement the two functions in `src/features/photo-library/api-client/api-client.ts`, the `search` function must retrieve from python server a `list of strings`. The upload function must just upload the file to the backend.
4. When uploading a file, you can edit the `src/views/index.tsx` to call `await search("")` just after `await upload(file)` to refresh the list of displayed items.

### What is expected

We want to test your ability to implement and learn new technologies together and create a clean application.
Here you will explore the message queues and see their advantage for async jobs, do not hesitate to read some documentation about MQ advantages and use cases.
Finaly the technical test is a fullstack test and we expect a fully working frontend and backend all together.

### To continue... (not included in the technical test)

- There is some little improvements to do, for instance, if we already started a search in the search bar, uploading a file should clear this search bar too if we refresh the list of files.
- There is no rules in backend or frontend to refuse non-image files, wich could lead to some bugs.
- The frontend could be improved to support drag and drop images, sho something when there is no photos etc
- We could also upload files to a S3 service like Minio
- I don't talk about creating a documentation of the REST endpoints, but of course in real life it should exists
- Adding some tests is always great, though it could be difficult as we must have a max-caption-generator running for the tests.
