var canvas = document.getElementById('plane');
var context = canvas.getContext('2d');

var margin = 10;

var subCanvas = SubCanvasByMargin(margin,margin,canvas);


// declare cartesian coordinates boundary

var xleft = -2;
var xright = 0.75;
var ybot = -1.5;
var ytop = 1.5;


plotGrid = new PlottingWindow(xleft,xright,ybot,ytop,subCanvas);

// plot julia set for z^2-1
// jconst = new ComplexNum(-1,0);

// plot julia set for z^2+1
// jconst = new ComplexNum(1,0);

// plot julia set for z^2+0.25
// jconst = new ComplexNum(0.25,0);

// plot julia set for z^2+i
// jconst = new ComplexNum(0,1);
// console.log(jconst.norm());

// JuliaPlot(jconst,plotGrid);

MandelbrotPlot(plotGrid);

// console.log(canvas.width);


// context.moveTo(125, 125);
// context.lineTo(125, 45);
// context.stroke();
// context.fillRect(10,10,1,1); // fill in the pixel at (10,10)
