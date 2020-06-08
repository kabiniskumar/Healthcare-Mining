const solr_node = require('solr-node');
const symptoms = require('./SymToDis.json');
const threads = require('./disToThreads.json')

var client = new solr_node({
  host: '127.0.0.1',
  port: '8983',
  core: 'mycore',
  protocol: 'http'
});

//Add in a loop
symptoms.forEach((symptom) => {
  client.update(symptom, function(err, result) {
    if (err) {
      console.log(err);
      return;
    }
    console.log('Response:', result.responseHeader);
  });
});

threads.forEach((thread) => {
  client.update(thread, function(err, result) {
    if (err) {
      console.log(err);
      return;
    }
    console.log('Response:', result.responseHeader);
  });
});

// delete all
// const deleteAllQuery = '*:*'
// client.delete(deleteAllQuery, function(err, result) {
//   if (err) {
//     console.log(err);
//     return;
//   }
//   console.log('Response:', result.responseHeader);
// });