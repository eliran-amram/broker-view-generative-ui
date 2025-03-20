# broker_view_generative_ui_async_sdk.DefaultApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**chat_with_bot**](DefaultApi.md#chat_with_bot) | **POST** /bot/chat | Chat With Bot
[**health_check_health_check_get**](DefaultApi.md#health_check_health_check_get) | **GET** /health_check | Health Check


# **chat_with_bot**
> object chat_with_bot()

Chat With Bot

### Example


```python
import broker_view_generative_ui_async_sdk
from broker_view_generative_ui_async_sdk.rest import ApiException
from pprint import pprint

# Create an instance of the API class
my_host = "http://localhost"
api_instance = broker_view_generative_ui_async_sdk.init_api(api=broker_view_generative_ui_async_sdk.DefaultApi, host=my_host)

try:
    # Chat With Bot
    api_response = await api_instance.chat_with_bot()
    print("The response of DefaultApi->chat_with_bot:\n")
    pprint(api_response)
except Exception as e:
    print("Exception when calling DefaultApi->chat_with_bot: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **health_check_health_check_get**
> object health_check_health_check_get()

Health Check

### Example


```python
import broker_view_generative_ui_async_sdk
from broker_view_generative_ui_async_sdk.rest import ApiException
from pprint import pprint

# Create an instance of the API class
my_host = "http://localhost"
api_instance = broker_view_generative_ui_async_sdk.init_api(api=broker_view_generative_ui_async_sdk.DefaultApi, host=my_host)

try:
    # Health Check
    api_response = await api_instance.health_check_health_check_get()
    print("The response of DefaultApi->health_check_health_check_get:\n")
    pprint(api_response)
except Exception as e:
    print("Exception when calling DefaultApi->health_check_health_check_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

