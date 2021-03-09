# micro-captcha

A simple microservice which provides CAPTCHA verification trough http protocol.  

Provides two endpoints:   
- **GET  /captcha**  
  Return a JSON object containing a captcha identifier, under key `id`, and the captcha image, under key `image`, encoded in **base64**.
  Image format is `png`.
- **POST /captcha**  
  Accept a JSON object payload containing a provided captcha identifier, under key `id`, and a solution provided for the captcha, under key `answer`.  
  Return a `200` HTTP status code if the verification succeeded, or a meaningful `4xx` HTTP status with a JSON object as the payload, 
  containing a key `detail` which value is the error message. 

Once the application run, you can find the auto generated documentation with detailed examples by opening `http://localhost:8000/docs` url with a modern browser.

#### Why base64 encoding?

The main reason is to save an HTTP call, which would be necessary to load the image if an url was provided.  
Even tough the size of the string is slightly larger, about 30% larger than the image, it seems still convenient against the extra HTTP call 
and furthermore, base64 encoded images are natively supported by almost any modern browser 
and can be easily decoded by other consumers, mobile applications included.

### Requirements

Any recent version of docker and docker-compose installed.  
Internally two container are created: python 3.8 for a [fastapi](https://fastapi.tiangolo.com) application and redis 6 for persisted storage.

### How to run

1. Clone the repository:  
   `git clone https://github.com/simone6021/micro-captcha`
2. Launch from a shell:  
   `docker-compose up`

### Run tests

1. Clone the repository:  
   `git clone https://github.com/simone6021/micro-captcha`
2. Launch from a shell:  
   `docker-compose -f docker-compose.yml -f docker-compose-tests.yml run --rm app`

Application docker image support setting a non-empty value to `TEST` argument during docker build to include testing dependencies.
   
### Try it yourself

1. Run the app, see [How to Run](#how-to-run).
   
2. Request a CAPTCHA via the GET endpoint.  
   curl example: `curl localhost:8000/captcha`

3. Decode the base64 encoded image.  
   Example for a UNIX-like system with base64 utility installed: `echo "content_of_image_key" | base64 -d > captcha.png`

4. Solve the captcha then send the answer, along with the captcha identifier provided, to the POST endpoint:
   curl example: `curl -X POST -H "Content-Type: application/json" -d '{"captcha_id": "captcha_id_value", "answer": "answer_value"}' localhost:8000/captcha`

Please note that you can try this application using the auto generated documentation, just open a browser and visit the URL `http://localhost:8000/docs`

### TODO

- [ ] Add API rate limit, e.g. throttling.
- [ ] 100% tests coverage, current is 98%.
- [ ] Improve the captcha image: make it looks nicer and/or (slightly) more readable.
- [ ] Implement audio captcha.
- [ ] Use direct redis connection and client, via `aioredis`, instead of [fastapi-cache](https://github.com/comeuplater/fastapi_cache) because support for other types of cache backends is probably not needed anymore.
- [ ] Docker secret management? Environment variable should be sufficient.
