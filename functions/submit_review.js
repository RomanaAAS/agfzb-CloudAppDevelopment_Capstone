/**submit a new review to db */

 const {CloudantV1} = require('@ibm-cloud/cloudant');
 const {IamAuthenticator} = require('ibm-cloud-sdk-core');
 
 const DB_NAME='reviews';
 
 async function main(params) {
     
     try {
 
     const authenticator = new IamAuthenticator({apikey: IAM_API_KEY});
     const cloudant = CloudantV1.newInstance({authenticator: authenticator});
     cloudant.setServiceUrl(COUCH_URL);
    
 
         let req = await cloudant.postDocument({
             db: DB_NAME,
             document: params
         });
         return  req.result;
 
     } catch (error) {
         return {
             error: error.description
         };
     }
 }