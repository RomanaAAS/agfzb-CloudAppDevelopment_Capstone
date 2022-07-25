/**read dealerships, choose a state */

const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');
const DB_NAME = "dealerships";

async function main(params) {
    try{
      const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY });
      const cloudant = CloudantV1.newInstance({authenticator: authenticator});
      cloudant.setServiceUrl(params.COUCH_URL);
      
      var state = params.state;
      selector = {'st': state};
      
      if (params.id!=null){
            selector['id'] = parseInt(params.id);
      }
      
      let dbList = await cloudant.postFind({
          db: DB_NAME,
          selector: selector
      });
      return dbList.result;
      
    } catch (error) {
      return { error: error.description };
      }
}

