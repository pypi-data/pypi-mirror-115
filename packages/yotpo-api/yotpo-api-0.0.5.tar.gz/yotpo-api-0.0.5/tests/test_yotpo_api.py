from yotpo_api import YotpoClient

client = YotpoClient()


def test_auth():
    assert client._auth()


def test_review_creation():
    assert client.create_review(
        {
            "product_title": "product_title",
            "product_url": "https://www.sephora.com/something",
            "display_name": "John Doe",
            "email": "jone.doe@gmail.com",
            "review_content": "the fragrance is good, even thou the texture got worse, anyway, still great value.",
            "review_title": "great value",
            "review_score": 5,
        }
    )


def test_get_reviews():
    assert len(client.get_reviews()) > 0
