/**read all documents from db dealerships */

const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

async function main(params) {
      const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY })
      const cloudant = CloudantV1.newInstance({
          authenticator: authenticator
      });
      cloudant.setServiceUrl(params.COUCH_URL);
     
      try {
        let docList = await cloudant.postAllDocs({
            db: 'dealerships',
            includeDocs: true
        });
        return { "docs": docList.result.rows };
        } catch (error) {
          return { error: error.description };
      }
}