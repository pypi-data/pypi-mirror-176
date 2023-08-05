from typing import Optional

from src.pip_fluigio.__fluig_services_base.interfaces.dataset import \
    DatasetQueryParams


class DatasetParams(DatasetQueryParams):
    field_name: Optional[str]
    value: Optional[str]
    type: str
