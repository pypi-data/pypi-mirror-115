import time
from typing import Dict, List

from requests.models import Response

from cognite.well_model.client._api_client import APIClient
from cognite.well_model.client.utils._client_config import ClientConfig
from cognite.well_model.wsfe.models import (
    CdfFileLocator,
    CdfFileLocatorItems,
    PatternConfig,
    ProcessIdItems,
    ProcessState,
)


class WellLogExtractorClient:
    def __init__(
        self,
        project: str,
        api_key: str,
        environment: str,
        base_url: str = "https://wsfe.cognitedata-development.cognite.ai",
    ):
        self.project = project
        self.environment = environment
        self.api_client = APIClient(
            config=ClientConfig(
                api_key=api_key,
                project=project,
                base_url=base_url,
                # Since we're only using the APIClient to communicate with the WSFE,
                # we aren't using the client name for anything, but it is required by the APIClient.
                # As such, we can just leave it as an empty string
                client_name="wsfe-sdk",
            )
        )

    def _path(self, component):
        return f"/{self.environment}/{self.project}{component}"

    def submit(self, items: List[CdfFileLocator], write_to_wdl=False, patterns=[]) -> Dict[str, int]:
        """Submit a set of files for extraction"""
        request = CdfFileLocatorItems(
            write_to_wdl=write_to_wdl,
            patterns=PatternConfig(__root__=patterns),
            items=items,
        )

        response: Response = self.api_client.post(self._path("/fromcdf"), json=request.json())
        content: Dict[str, int] = response.json()
        return content

    def status(self, process_ids: List[int]) -> Dict[int, ProcessState]:
        """Retrieve the status of a set of items previously submitted for extraction"""
        items = ProcessIdItems(__root__=process_ids)

        response: Response = self.api_client.post(self._path("/status"), json=items.json())
        content: Dict[int, ProcessState] = response.json()
        return content

    def status_report(self, statuses: List[ProcessState]) -> Dict[str, int]:
        """Partition the set of statuses based on whether they are 'ready', 'processing', 'done' or 'error'"""
        status_types = set(s["status"] for s in statuses)
        return {state: sum(1 for s in statuses if s["status"] == state) for state in status_types}

    def wait(self, process_ids: List[int], verbose: bool = True, polling_interval: float = 180):
        """Waits until all the process ids specified in `process_ids` are either 'done' or 'error'"""
        statuses = self.status(process_ids)
        while any(s["status"] in ["ready", "processing"] for s in statuses.values()):
            time.sleep(polling_interval)
            statuses = self.status(process_ids)

        return statuses
