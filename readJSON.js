const fs = require('fs');
var obj = require('./NGSCOutput/g_24_2.gexf.json');
//node
var nodeObj = obj.gexf.graph.nodes.node
var edgeObj = obj.gexf.graph.edges
var i;
for (i = 0; i < nodeObj.length; i++) {
  //console.log(nodeObj[i])
  console.log(nodeObj[i]['@id'])
}