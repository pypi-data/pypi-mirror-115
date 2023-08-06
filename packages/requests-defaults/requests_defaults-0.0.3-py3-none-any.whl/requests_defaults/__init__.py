__version__ = "0.1.0"

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry  # pylint: disable=import-error
from requests_toolbelt import sessions

default_retry_strategy = Retry(
    total=3,
    status_forcelist=[429, 500, 502, 503, 504],
    method_whitelist=["HEAD", "GET", "OPTIONS"],
)


class Session(sessions.BaseUrlSession):
    """
    Requests with sane defaults
    """

    def __init__(
        self,
        raise_for_status=True,
        timeout=5,
        retry_strategy=default_retry_strategy,
        headers=None,
        **kwargs,
    ):
        super().__init__(**kwargs)

        if headers:
            self.headers.update(headers)

        adapter_kwargs = {}
        if retry_strategy:
            adapter_kwargs["max_retries"] = retry_strategy

        adapter_kwargs["timeout"] = timeout
        adapter = TimeoutHTTPAdapter(**adapter_kwargs)
        self.mount("http://", adapter)
        self.mount("https://", adapter)

        if raise_for_status:
            assert_status_hook = (
                lambda response, *args, **kwargs: response.raise_for_status()
            )
            self.hooks["response"] = [assert_status_hook]


class TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.timeout = kwargs.pop("timeout")
        super().__init__(*args, **kwargs)

    # pylint: disable=arguments-differ
    def send(self, request, **kwargs):
        kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)
