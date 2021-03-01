# micro-captcha

A simple microservice which provides CAPTCHA verification trough http protocol.  

Provides two endpoints:   
- **GET  /captcha**  
  Return a JSON payload containing a captcha identifier and the captcha image encoded in base64.
- **POST /captcha**  
  Accept a JSON payload containing a provided captcha identifier and the user response for solving the captcha.  
  Return a 200 HTTP status code if the verification succeeded, or a 400 HTTP status with a JSON object as the payload, 
  containing a key `error` which value is the error message. 

### Requirements

Any recent version of docker installed.

### How to run

1. Clone the repository:  
   `git clone https://github.com/simone6021/micro-captcha`
2. Launch from a shell:  
   `docker build -t micro-capctha . && docker run -it -p 8000:8000 micro-capctha`
   
For development, enable live reload of application server and bind mount local sources:  
`docker build -t microcaptcha . && docker run -it -p 8000:8000 -v /your/path/to/src:/app microcaptcha uvicorn main:app --host 0.0.0.0 --port 8000 --reload`

### Run tests

Build docker image setting a non-empty value to `TEST` argument and launch pytest command.

1. Clone the repository:  
   `git clone https://github.com/simone6021/micro-captcha`
2. Launch from a shell:  
   `docker build --build-arg TESTS=1 -t micro-capctha . && docker run -p 8000:8000 micro-capctha pytest`
   
### Try it yourself

1. Run the app, see **How to run**
   
2. Request a CAPTCHA via the GET endpoint.  
   curl example: `curl localhost:8000/captcha`

3. Decode the base64 encoded image.  
   Example for a UNIX-like system with base64 utility installed: `echo "content_of_image_key" | base64 -d > captcha.png`

4. Solve the captcha then send the answer, along with the captcha identifier provided, to the POST endpoint:
   curl example: `curl -X POST -H "Content-Type: application/json" -d '{"captcha_id": "captcha_id_value", "answer": "answer_value"}' localhost:8000/captcha`

Please note that you can try this application using the auto generated documentation, just open a browser and visit the URL `http://localhost:8000/docs`
