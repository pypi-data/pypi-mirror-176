from __fluig_services_base.interfaces.dataset import DatasetQueryParams
from fluig_services.dataset import Dataset


def main():

    instace = Dataset(
        wsdl_url="http://fluig.redeoba.com.br/webdesk/ECMDatasetService?wsdl"
    )
    response = instace.get_dataset(
        company_id="01",
        password="op40789Fwjkl32$$%1",
        user_name="integracaofluig@redeoba.com.br",
        dataset_name="dts_hierarquiaRM_MFX",
        constraints=[
            DatasetQueryParams(field_name="CHAPA", value="03100981", type="MUST")
        ],
        order=[],
        fields=[],
    )

    return print(response)


if __name__ == "__main__":
    main()
