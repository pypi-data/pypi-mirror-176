from pip_fluigio.fluig_services.token import Token


def main():

    instance = Token(wsdl_url="https://lab.fluig.com/webdesk/ECMTokenService?wsdl")
    # response = instace.get_dataset(
    #     company_id="01",
    #     password="op40789Fwjkl32$$%1",
    #     user_name="integracaofluig@redeoba.com.br",
    #     dataset_name="dts_hierarquiaRM_MFX",
    #     constraints=[
    #         DatasetQueryParams(field_name="CHAPA", value="03100981", type="MUST")
    #     ],
    #     order=[],
    #     fields=[],
    # )

    # response = instace.get_all_available_dataset(
    #     company_id="01",
    #     password="op40789Fwjkl32$$%1",
    #     user_name="integracaofluig@redeoba.com.br",
    # )

    # return print(response)

    # response = instance.get_token_by_login(
    #     company_id="01",
    #     password="academy.aluno",
    #     user_id="academy.aluno",
    #     login="academy.aluno",
    # )

    # return print(
    #    instance.get_token_by_email(
    #        company_id="01", password="academy.aluno", email="academy.aluno@fluig.com"
    #    )
    # )

    # return print(instance.get_token(login="academy.aluno", password="academy.aluno"))

    validate = instance.validate_token(token="12df6ac7-9351-4b83-96e8-414dc3369404")

    return print(validate)


if __name__ == "__main__":
    main()
