# Healthcare Mining

1. We will use Docker to run an instance of Solr. Install docker from https://www.docker.com/products/docker-desktop.

2. Once docker is up and running, go into `SolrFiles` folder and run the following command:`docker-compose up`. This will download an image of Solr from DockerHub and might take couple of minutes. When completed, open up http://localhost:8983/solr/#/ and you should be able to see Solr's interface. 

3. Install Node Package Manager (NPM) and Solr-Node if not already installed:
      `pip install npm` 
      `npm install solr-node`
      
4. CD into `SolrFiles/app` and run `start.js` using `node start.js`. 
`start.js` is the file which is used for insertion and deletion of the records into Solr's db. Look for comments inside the file to perform insertion and deletion. 

5. Run `backend/flsk.py` and then goto http://localhost:5000. 
         

