# CS-Sender
scrapy extension for spider monitor web framework cralwer-studio


## Install
```
pip install cs-sender
```

## Usage 
Config following settings to settings.py of scrapy project
```
CS_BACKEND = http://localhost:8000
CS_API_TOKEN = '6452c52c4acee2044fe9d953467e6e45be1f367c'
EXTENSIONS = {
    'cs_sender.ScrapyMonitor': 802
}
```


## Parameter

- CS_BACKEND
    - description: Ip address of crawler-studio
    - default: http://localhost:8000
-------- 
- CS_API_TOKEN
    - description: The token of crawler-studio API
    - default: ''
-------- 
- CS_ENABLE_SEND_ERR_LOG
  - description: Whether send error log to crawler-studio
  - default: True
-------- 
- CS_ERR_LOG_BUFFER_SIZE
    - description: If error log buffer size larger than CS_ERR_LOG_BUFFER_SIZE, 
      it will be sent to crawler-studio as a batch immediately, and the error log buffer will be empty
    - default: 500
    - pre-condition: CS_ENABLE_SEND_ERR_LOG set to True
-------- 
- CS_ERR_LOG_SEND_FREQ
    - description: The error logs will be sent to crawler-studio as a batch for every CS_ERR_LOG_SEND_FREQ seconds
    - default: 20 seconds
    - pre-condition: CS_ENABLE_SEND_ERR_LOG set to True
-------- 

