/** read db reviews for a dealerId */

const {CloudantV1} = require('@ibm-cloud/cloudant');
const {IamAuthenticator} = require('ibm-cloud-sdk-core');

const DB_NAME='reviews';

async function main(params) {
   try {

   const authenticator = new IamAuthenticator({apikey: IAM_API_KEY});
    const cloudant = CloudantV1.newInstance({authenticator: authenticator});
    cloudant.setServiceUrl(COUCH_URL);
   
   var dealerId=parseInt(params.dealerId);

        let dbList = await cloudant.postFind({
            db: DB_NAME,
            selector:{"dealership":dealerId}
        });
        return  dbList.result;

    } catch (error) {
        return {
            error: error.description
        };
    }
}