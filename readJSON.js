const fs = require('fs');
var obj = require('./NGSCOutput/g_24_2.gexf.json');
//node
var nodeObj = obj.gexf.graph.nodes.node
var i;
for (i = 0; i < nodeOjb.length; i++) {
  text += cars[i] + "<br>";
}
console.log(nodeObj)
/*for (i in nodeObj) {
  console.log(i)
  x = ;
  console.log(x);
}*/
//var sMyString = fs.readFileSync('./NGSCOutput/g_24_2.gexf.json').toString();
