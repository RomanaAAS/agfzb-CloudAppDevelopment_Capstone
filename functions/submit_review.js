const {CloudantV1} = require('@ibm-cloud/cloudant');
const {IamAuthenticator} = require('ibm-cloud-sdk-core');

const COUCH_URL = "https://apikey-v2-f2ochbg76t4zjcekhh01vzna530y9mgrl5szm6dnpij:869e59c26af6924b09a494ed1d8cc9ed@7b6506a4-4a9f-4b55-ba38-0c4bd4bdb915-bluemix.cloudantnosqldb.appdomain.cloud";
const IAM_API_KEY = "I2FZtaRcoeyM21st6oTL2K1o3zTczcaU34vuaH02Q7UN";
const COUCH_USERNAME = "romana.leitgeb247@gmail.com";


async function main(params) {
    
    try {

    const authenticator = new IamAuthenticator({apikey: IAM_API_KEY});
    const cloudant = CloudantV1.newInstance({authenticator: authenticator});
    cloudant.setServiceUrl(COUCH_URL);
   

        let req = await cloudant.postDocument({
            db: "reviews",
            document: params
        });
        return  req.result;

    } catch (error) {
        return {
            error: error.description
        };
    }
}