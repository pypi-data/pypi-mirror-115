import logging
import os
import requests
import math
import dateutil.parser
from typing import Dict, List
import datetime

class YotpoClient:
    def __init__(
        self, client_id: str = None, client_secret: str = None, token_type: str = None
    ):
        self.client_id = client_id or os.environ.get("YOTPO_API_TOKEN")
        self.client_secret = client_secret or os.environ.get("YOTPO_API_SECRET")
        self.grant_type = "client_credentials"
        self.apiurl = "https://api.yotpo.com/"
        self.access_token = None
        self.token_type = None
        self.logger = logging.getLogger("YOTPO_API")
        self.logger.setLevel(logging.DEBUG)
        if not self.access_token:
            self._auth()

    @staticmethod
    def _transform_date(date: str) -> int:
        naive_date = dateutil.parser.isoparse(date)
        return int(naive_date.replace(tzinfo=datetime.timezone.utc).timestamp())

    def _auth(self) -> str:
        response = requests.get(
            self.apiurl + "oauth/token",
            json={
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "grant_type": "client_credentials",
            },
        )
        if response.status_code == 200:
            credentials = response.json()
            self.access_token = credentials.get("access_token")
            self.token_type = credentials.get("token_type")

        return self.access_token is not None and self.token_type is not None

    def get_reviews(
        self, product_id="yotpo_site_reviews", from_date: int = 0
    ) -> List[Dict]:
        product_id="yotpo_site_reviews" if product_id is None else product_id
        from_date=0 if from_date is None else from_date
        current_page = 1
        per_page = 100
        page_count = 0
        reviews = []
        while True:
            response = requests.get(
                f"{self.apiurl}/v1/widget/{self.client_id}/products/"
                f"{product_id or 'yotpo_site_reviews' }/"
                f"reviews.json?per_page={per_page}?&page={current_page}"
            )
            if response.status_code == 200:
                response = response.json().get("response")
                pagination = response.get("pagination")
                reviews.extend(
                    list(
                        filter(
                            lambda r: self._transform_date(r.get("created_at"))
                            > from_date,
                            response.get("reviews"),
                        )
                    )
                )
                page_count = math.ceil(pagination.get("total") / per_page)
                if current_page < page_count:
                    current_page += 1
                else:
                    break
            elif response.status_code == 401:
                self._auth()
            else:
                self.logger.critical(f"yotpo API error:{response.reason}")
                break
        return reviews

    def create_review(self, review: Dict) -> bool:
        review.update({"appkey": self.client_id})
        if not review.get("sku"):
            review.update({"sku":"yotpo_site_reviews"})
        response = requests.post(
            self.apiurl + "reviews/dynamic_create",
            json=review,
        )
        return response.json().get("status", {}).get("code",0) == 200
