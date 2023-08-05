from scamadviser_client.base_api import BaseAPI
from scamadviser_client.request import Request
from scamadviser_client.schema.feed_params import DownloadParams, ListParams


class FeedAPI(BaseAPI):
    host: str = "api.scamadviser.cloud/v2/trust/feed"

    @Request(method="get", path="list")
    def list(self, params: dict = {}):
        params["apikey"] = self.apikey
        return ListParams(**params).dict()

    @Request(method="get", path="download")
    def download(self, params: dict = {}):
        params["apikey"] = self.apikey
        return DownloadParams(**params).dict()
