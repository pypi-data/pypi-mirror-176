from typing import List, Tuple


class ApiConfig:
    def get_base_url(self) -> str:
        return "/"

    def get_structured_identity_prefix(self) -> str:
        pass

    def get_add_schema(self) -> dict:
        pass

    def get_edit_schema(self) -> dict:
        pass


class AppConfig:
    def __init__(self, api_configs: List[ApiConfig]):
        self.api_configs = api_configs

    def get_app_name(self) -> str:
        pass

    def get_version(self) -> str:
        pass

    def get_enterprise_id(self) -> str:
        return "17869"

    def get_min_page_size(self) -> int:
        return 10

    def get_max_page_size(self) -> int:
        return 100

    def get_default_page_size(self) -> int:
        return 20

    def get_swagger_api_version(self) -> str:
        return "1.0.0"

    def get_config_file(self) -> str:
        pass

    def get_apis(self) -> List[ApiConfig]:
        return self.api_configs

    def get_api_by_url(self, url: str) -> ApiConfig:
        for api in self.get_apis():
            if url.startswith(api.get_base_url()):
                return api

        return self.get_apis()[0]

    def exists_api_by_url(self, url: str) -> bool:
        for api in self.get_apis():
            if url.startswith(api.get_base_url()):
                return True

        return True

    def get_logging_info_by_url(self, url: str) -> Tuple[str, str]:
        api = self.get_api_by_url(url)
        return api.get_structured_identity_prefix(), self.get_enterprise_id()
