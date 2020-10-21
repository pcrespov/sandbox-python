# swagger_client.DefaultApi

All URIs are relative to *https://virtserver.swaggerhub.com/pcrespov/test-simple/1.0.0*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_project**](DefaultApi.md#add_project) | **POST** /projects | adds a new project
[**projects_get**](DefaultApi.md#projects_get) | **GET** /projects | searches projects


# **add_project**
> add_project(project_item=project_item)

adds a new project

Adds an new project to the database

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DefaultApi()
project_item = swagger_client.ProjectItem() # ProjectItem | Project item to add (optional)

try:
    # adds a new project
    api_instance.add_project(project_item=project_item)
except ApiException as e:
    print("Exception when calling DefaultApi->add_project: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_item** | [**ProjectItem**](ProjectItem.md)| Project item to add | [optional] 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **projects_get**
> list[ProjectItem] projects_get(search_string=search_string)

searches projects

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DefaultApi()
search_string = 'search_string_example' # str | pass an options search string to filter project names (optional)

try:
    # searches projects
    api_response = api_instance.projects_get(search_string=search_string)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->projects_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **search_string** | **str**| pass an options search string to filter project names | [optional] 

### Return type

[**list[ProjectItem]**](ProjectItem.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

