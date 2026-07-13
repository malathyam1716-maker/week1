from stripe import StripeClient
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception
from utils.enums import StripeServiceEnum
from utils.exception_handling import is_retryable_exception


class StripeExtractor:
    def __init__(self, api_key: str, service_type: StripeServiceEnum | str):
        self.api_key = api_key
        self.service_type = self._normalize_service_type(service_type)

    @staticmethod
    def _normalize_service_type(service_type: StripeServiceEnum | str) -> StripeServiceEnum:
        if isinstance(service_type, StripeServiceEnum):
            return service_type

        normalized_value = (service_type or "").strip().lower()
        if normalized_value in {"customer", "customers"}:
            return StripeServiceEnum.customers
        if normalized_value in {"charge", "charges"}:
            return StripeServiceEnum.charges
        return StripeServiceEnum.customers

    @retry(
        retry=retry_if_exception(is_retryable_exception),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        stop=stop_after_attempt(5),
    )
    def __client(self, service_type: StripeServiceEnum) -> list[dict]:
        client = StripeClient(self.api_key)
        service_name = service_type.value
        service = getattr(client.v1, service_name, None)
        if service is None:
            raise AttributeError(f"Unsupported Stripe service: {service_name}")

        data = service.list().data
        return data

    def extract(self) -> list[dict]:
        raw_data = self.__client(self.service_type)
        customer_list = [c.to_dict() for c in raw_data]
        return customer_list
