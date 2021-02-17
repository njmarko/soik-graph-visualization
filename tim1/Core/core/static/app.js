function isTopLevelNode(node) {
  return node.parents.length === 0;
}

function createNode(parentNode, node) {
  $('#jstree').jstree().create_node(parentNode.id ,  {'id' : node.id, 'text' : node.name}, 'last');
}

function populateNodeChildren(node, nodes) {
  node.children.forEach(childID => {
    const childNode = nodes.get(parseInt(childID));
    createNode(node, childNode);
  })
}

function getNodeContent(graphNode) {
  const contentDiv = $('<div></div>');
  for (const [attr, value] of Object.entries(graphNode.attributes)) {
   const attributeParagraph = $(`<p><b>${attr}:</b> ${decodeEntities(value)}</p>`);
   contentDiv.append(attributeParagraph);
  }
  return contentDiv;
}

// https://stackoverflow.com/questions/5796718/html-entity-decode
// http://jsfiddle.net/LYteC/4/
var decodeEntities = (function() {
  // this prevents any overhead from creating the object each time
  var element = document.createElement('div');

  function decodeHTMLEntities (str) {
    if(str && typeof str === 'string') {
      // strip script/html tags
      str = str.replace(/<script[^>]*>([\S\s]*?)<\/script>/gmi, '');
      str = str.replace(/<\/?\w(?:[^"'>]|"[^"]*"|'[^']*')*>/gmi, '');
      element.innerHTML = str;
      str = element.textContent;
      element.textContent = '';
    }

    return str;
  }

  return decodeHTMLEntities;
})();

let globalNodes = []

function generateTreeView(nodes) {
  globalNodes = nodes;
  let treeNodes = []
  // Find only top level nodes i.e. the nodes that have no parent
  for (const [_id, node] of nodes.entries()) {
    if (isTopLevelNode(node)) {
      treeNodes.push({
        'id': node.id,
        'text': node.name
      });
    }
  }
  // If there is no such nodes display all the nodes as top level
  if (treeNodes.length === 0) {
    treeNodes = [...nodes.values()];
  }

  // Create tree view and connect event handlers
  $('#jstree')
  .on('select_node.jstree', function (_event, data) {
    const node = nodes.get(parseInt(data.node.id));
    // Populate node children only once
    if (data.node.children.length === 0) {
      populateNodeChildren(node, nodes);
    }
    const customEvent = new CustomEvent('core_vertex_selected', {bubbles: true, detail: node});
    const dispatcher = document.getElementsByTagName('svg')[0];
    dispatcher.dispatchEvent(customEvent); 
  })
  // https://jsfiddle.net/doug99collins/rpkbpxsk/3/
  .bind('dblclick.jstree', function (event) {
    const tree = $(this).jstree();
    const treeNode = tree.get_node(event.target);
    const graphNode = nodes.get(parseInt(treeNode.id));
    const modalContent = getNodeContent(graphNode);
    $('#vertexInfoContent').empty();
    $('#vertexInfoContent').append(modalContent);
    $('#vertexInfoModal').modal('show');
  })
  .jstree({
    'core': {
      'check_callback' : true,
      'data': treeNodes,
      'themes': {
        'name': 'proton',
        'responsive': true
      }
    }
  });
}

function dispatchVertexSelectedEvent(node) {
  const customEvent = new CustomEvent('core_vertex_selected', {bubbles: true, detail: node});
  const dispatcher = document.getElementsByTagName('svg')[0];
  dispatcher.dispatchEvent(customEvent);
}

$('#treeEventDispatcher').on('plugin_vertex_selected', event => {
  $("#jstree").jstree().deselect_all(true);
  const nodeId = event.originalEvent.detail.toString();
  if($('#jstree').jstree(true).get_node(nodeId)) {
    $('#jstree').jstree('select_node', nodeId);
  } else {
    const node = globalNodes.get(parseInt(nodeId));
    dispatchVertexSelectedEvent(node);
  }
});

$('#jstree').slimScroll({
  height: '800px',
  width: '800px'
});

window.onload = async function(){
  await sleep(400);
  cloneContent();
  var contentUpdateManager = setInterval(refreshMinimap, 500);
  function refreshMinimap(){
    document.querySelector("#minimap-content").remove();
    cloneContent();
  }

};
//document.querySelector("#main-visualization").onclick = refreshMinimap;

function cloneContent(){
  let svgs = document.getElementsByTagName("svg");
  let svgClone = svgs[0].cloneNode(true);
  svgClone.setAttribute("id", "minimap-content");

  document.querySelector("#minimap").appendChild(svgClone);

  document.querySelector("#minimap-content").onclick = function (event) { 
    let parent = event.target.parentElement;
    
    let id = parent.getAttribute("id");
    if(id !== null){
      if(id.startsWith('vertex_')){
        const correctedId = id.replace('vertex_', '');
          const customEvent = new CustomEvent('plugin_vertex_selected', {bubbles: true, detail: correctedId});
          const dispatcher = document.getElementById('treeEventDispatcher');
          dispatcher.dispatchEvent(customEvent); 
      }
    }
    
 }
  
  let nodes = document.getElementsByClassName("node");
  
  let nodesX = [];
  let nodesY = [];
  
  for(var i = 0; i < nodes.length;i++){
      let translateValues = nodes[i].getAttribute("transform").replace("translate(", "").replace(")", "").split(',');
      
      let x = parseFloat(translateValues[0]);
      let y = parseFloat(translateValues[1]);

      nodesX.push(x);
      nodesY.push(y);
  }

  let moveX = 10000;
  let moveY = 3000;
  let scale = 0.03;


  let minX = Math.min.apply(Math, nodesX);
  let minY = Math.min.apply(Math, nodesY);

  let maxX = Math.max.apply(Math, nodesX);
  let maxY = Math.max.apply(Math, nodesY);

  
  moveY = minY >= 0 ? -minY + 1000: Math.abs(minY) + 500;
  moveX = minX >= 0 ? -minX + 1000 : Math.abs(minX) + 500;

  d3.select("#minimap-content g").attr("transform", "scale(" + scale + ") translate(" + moveX + ", " + moveY + ")");


}


function sleep(ms){
  return new Promise(resolve => setTimeout(resolve, ms));
}
