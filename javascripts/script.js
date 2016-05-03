var colorArray = ["#819090","#708284","#536870",
"#475B62","#E9FCFF","#FF5F9A",
"#738A05","#259286","#2176C7",
"#595AB7","#C61C6F","#D11C24",
"#BD3613","#A57706","#5E6B90",
"#EAE3CB","#DDACE2","#63A1F7",
"#434090","#E06E6E","#F1A7A2",
"#A2F1A7","#D67DA9","#10971B"];

var width = "100%",
height = 800,
shiftKey;

var svg = d3.select("#graph")
.attr("tabindex", 1)
.on("keydown.brush", keydown)
.on("keyup.brush", keyup)
.each(function() { this.focus(); })
.append("svg")
.attr("width", width)
.attr("height", height);

svg.append("defs").append("marker")
.attr("id", "arrowhead")
.attr("refX", 15) /*must be smarter way to calculate shift*/
.attr("refY", 2)	
.attr("fill","gray")
.attr("markerWidth", 6)
.attr("markerHeight", 4)
.attr("orient", "auto")
.append("path")
	.attr("d", "M 0,0 V 4 L6,2 Z"); //this is actual shape for arrowhead


var link = svg.append("g")
.attr("class", "link")
.attr("marker-end", "url(#arrowhead)")
.selectAll("line");

var node = svg.append("g")
.attr("class", "node")
.selectAll("circle");

var text = svg.selectAll("text")
.append("text");

var intentDiv = d3.select("body").append("div")	
.attr("class", "permissionInfo")	
.style("opacity", 0);

var pathInfo = d3.select("body").append("div")	
.attr("class", "pathInfo")	
.style("opacity", 0);	

var toolImage = svg.selectAll("image"); 

var offSet = 30;
var nodeRadius = 30;
var bubbleRadius = 10;
let bubbleOffSet = (nodeRadius+bubbleRadius)/Math.sqrt(2);	

let lineOffSet = 35;
let curvedLevel = [-100,100][Math.floor(Math.random()*2)];

d3.json("graph.json", function(error, graph) {

	graph.links.forEach(function(d) {
		d.source = graph.nodes[d.source];
		d.target = graph.nodes[d.target];
	});

	node =node.data(graph.nodes).enter().append("circle")
	.attr("r", nodeRadius)
	.attr("cx", function(d) { return d.x; })
	.attr("cy", function(d) { return d.y; })
	.attr("fill", function(d){return randomColor();})
	.style("stroke-width", 1)
	.style("opacity", 1)
	

	.on("mouseover", function(d) {		

		var permissions = d.usesPermissions
		var temp = "[User Permissions]</br>"
		for (var i = 0; i < permissions.length; i++) {					
			temp = temp + permissions[i] + "<br/>"							
		}

		intentDiv.transition()			
		.style("opacity", .9);

		intentDiv .html(temp)
		.style("left", (d3.event.pageX + 10) + "px")		
		.style("top", (d3.event.pageY) + "px");	

	})

	.on("mouseout", function(d) {

		intentDiv.transition()			
		.style("opacity", 0);

	})

	.on("mousedown", function(d) {
		if (!d.selected) { // Don't deselect on shift-drag.
			if (!shiftKey) node.classed("selected", function(p) { 
				return p.selected = d === p;});

				else d3.select(this).classed("selected", d.selected = true);

			}

		})

	.on("mouseup", function(d) {
		if (d.selected && shiftKey) d3.select(this).classed("selected", d.selected = false);
		
	})
	.call(d3.behavior.drag()
		.on("drag", function(d) { nudge(d3.event.dx, d3.event.dy); }));


link = link.data(graph.links).enter().append("path")
.attr('stroke-width', 3)
.attr('stroke-dasharray',function(d){

	if (d.dataFlow){
		return "5 5";
	}else{
		return "";
	}	

})
.style("stroke", function(d){

	if (d.dataFlow){
		return "green";
	}else{
		return "gray";
	}
})
.attr("d", function(d) {
    return draw_curve(d.source.x, d.source.y, d.target.x, d.target.y, curvedLevel);
 })
.attr("fill","transparent")
.attr("x1", function(d) { return d.source.x})
.attr("y1", function(d) { return d.source.y})
.attr("x2", function(d) { return d.target.x})
.attr("y2", function(d) { return d.target.y});

text = text.data(graph.nodes).enter().append("text")
.attr("x", function (d) { return d.x; })
.attr("y", function (d) { return d.y; })
.text( function (d) { return d.Name; })
.attr("font-family", "sans-serif")
.attr("font-size", "20px")
.attr("fill", "black");

toolImage = toolImage.data(graph.links).enter().append("image")
.attr("x", function(d) { return ((d.source.x - d.target.x)/2 + d.target.x); })
.attr("y", function(d) { return ((d.source.y - d.target.y)/2 + d.target.y); })
.attr("xlink:href",function(d) {

	if(d.description != "None"){

		if (d.dataFlow){
			return "./image/dataFlow.png"
		}else{
			return "./image/"+d.byTool+".png"	
		}
	}

	
})
.attr('width', 40)
.attr('height', 40)
.on("mouseover", function(d) {
	
	if(d.description != "None"){

	var fromComponent = d.fromComponent
	var toComponent = d.toComponent
	var intent = d.byIntent

	var temp = "- From : " + fromComponent + "</br>";
	temp = temp + "- To : " + toComponent + "</br>";
	temp = temp + "- Intent : " + intent + "</br>";
	temp = temp + "- Description : " + d.description + "</br>";
	f
		pathInfo.transition()		
			.duration(200)		
			.style("opacity", .9);

		pathInfo.html(temp)
			.style("width","500px")
			.style("left", (d3.event.pageX) + "px")		
			.style("top", (d3.event.pageY + 20) + "px");	
	}

})
.on("mouseout", function(d) {

	pathInfo.transition()		
		.duration(500)		
		.style("opacity", 0);

});

});

function nudge(dx, dy) {

	// Node circle
	node.filter(function(d) { return d.selected; })
	.attr("cx", function(d) { return d.x += dx; })
	.attr("cy", function(d) { return d.y += dy; });

	// Text for app name
	text.filter(function(d) { return d.selected; })
	.attr("x", function(d) { return d.x; })
	.attr("y", function(d) { return d.y; });

	// Link  - from point
	link.filter(function(d) { return d.source.selected; })
	.attr("d", function(d) {
	    return draw_curve(d.source.x, d.source.y, d.target.x, d.target.y, curvedLevel);
	 })

	// Link - to point 
	link.filter(function(d) { return d.target.selected; })
	.attr("d", function(d) {
	    return draw_curve(d.source.x, d.source.y, d.target.x, d.target.y, curvedLevel);
	 })

	// toolImage
	toolImage.filter(function(d) {
		if(d.source.selected || d.target.selected){
			return true;
		}
	})
	.attr("x", function(d) {
		var temp = (d.source.x - d.target.x)/2 + d.target.x;
		return temp += dx; 
	})
	.attr("y", function(d) { 
		var temp = (d.source.y - d.target.y)/2 + d.target.y;
		return  temp += dy;
	 });


//d3.event.preventDefault();
}

function keydown() {
if (!d3.event.metaKey) switch (d3.event.keyCode) {
	case 38: nudge( 0, -1); break; // UP
	case 40: nudge( 0, +1); break; // DOWN
	case 37: nudge(-1,  0); break; // LEFT
	case 39: nudge(+1,  0); break; // RIGHT
}
shiftKey = d3.event.shiftKey || d3.event.metaKey;
}

function keyup() {
shiftKey = d3.event.shiftKey || d3.event.metaKey;
}

function randomColor(){
var index = Math.floor((Math.random() * colorArray.length));
return colorArray[index];

}

function draw_curve(Ax, Ay, Bx, By, M) {

// Find midpoint J
var Jx = Ax + (Bx - Ax) / 2
var Jy = Ay + (By - Ay) / 2

// We need a and b to find theta, and we need to know the sign of each to make sure that the orientation is correct.
var a = Bx - Ax
var asign = (a < 0 ? -1 : 1)
var b = By - Ay
var bsign = (b < 0 ? -1 : 1)
var theta = Math.atan(b / a)

// Find the point that's perpendicular to J on side
var costheta = asign * Math.cos(theta)
var sintheta = asign * Math.sin(theta)

// Find c and d
var c = M * sintheta
var d = M * costheta

// Use c and d to find Kx and Ky
var Kx = Jx - c
var Ky = Jy + d

return "M" + Ax + "," + Ay +
       "Q" + Kx + "," + Ky +
       " " + Bx + "," + By
}
