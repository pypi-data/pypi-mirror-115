# Usage
  > json_config_file_path = "/path/to/file/json"  
  > client = ApiClient(json_config_file_path)   
  > data = client.make_request('example1')   
  >  

# JSON Format
```yaml
{  
  "name": "api endpoints",  
  "description": "hello",  
  "config": {    
    "example1": {  
      "method": "GET",  
      "url": "https://gorest.co.in/public/v1/users",  
      "header": {  
        "Content-Type": "application/json"  
      },  
      "parameters": {  
        "hello": "world"  
      },  
      "save_response": false  
    }  
  }  
}  
