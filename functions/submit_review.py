import sys
import ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def main(dict):
    authenticator = IAMAuthenticator("I2FZtaRcoeyM21st6oTL2K1o3zTczcaU34vuaH02Q7UN")
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url("https://apikey-v2-f2ochbg76t4zjcekhh01vzna530y9mgrl5szm6dnpij:869e59c26af6924b09a494ed1d8cc9ed@7b6506a4-4a9f-4b55-ba38-0c4bd4bdb915-bluemix.cloudantnosqldb.appdomain.cloud")
    response = service.post_document(db='reviews', document=dict["review"]).get_result()
    try:
        result = {
            'headers': {'Content-Type':'application/json'},
            'body': {'data': response}
        }
        return result
    except:
        return {
            'statusCode': 404,
            'message': 'Something went wrong'
        }
