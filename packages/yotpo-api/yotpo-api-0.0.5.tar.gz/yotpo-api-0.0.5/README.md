# yotpo API
This is a package to integrate and model the data
structure and wrap the api calls made to use the
yotpo api.

## Install
```shell
pip install yotpo-api
```
## Usage
### Authentication
To use the [yotpo api](https://apidocs.yotpo.com/reference) you need to provide
your yotpo **api key** and **api secret** either by passing them as kwargs to
the client init
```pyhton
client = YotpoClient(api_token, api_secret)
```
either by setting them as env vars named **YOTPO_API_TOKEN** and **YOTPO_API_SECRET**
so they are automatically used by the client when there kwargs are not provided.
```python
client = YotpoClient()
```
### Getting reviews
```python
client.get_reviews()
```
optionally providing the **product id** and the **from date** params.

### Creating reviews
```python
client.create_review(
        {
            "product_title": "product_title",
            "product_url": "https://www.sephora.com/something",
            "display_name": "John Doe",
            "email": "jone.dow@gmail.com",
            "review_content": "the fragrance is good, even thou the texture got worse, anyway, still great value.",
            "review_title": "great value",
            "review_score": 5,
        }
    )
```
