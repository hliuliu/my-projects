

function SubCanvas(xl, yl, width, height, canvas) {
  // subcanvas within a canvas
  // (xl,yl) is the top left corner relative to the original canvas

  this.xl = xl;
  this.yl = yl;
  this.width = width;
  this.height = height;
  this.canvas = canvas;
  this.context = canvas.getContext('2d');

  this.inBounds = function(x,y) {
    return x>=0 && y>=0 && x<this.width && y<this.height;
  };

  this.toCanvasCoords = function(x,y) {
    return [x+this.xl,y+this.yl];
  };

  this.fromCanvasCoords = function(x,y) {
    return [x-this.xl, y-this.yl];
  };

  this.fillPixel = function(x,y) {
    cp = this.toCanvasCoords(x,y);
    x= cp[0];
    y= cp[1];
    this.context.fillRect(x,y,1,1);
  };

  this.fillConditionalPixels = function (condfn) {
    // for each valid pixel (x,y), fill it iff condfn(x,y) -> true
    // console.log(this.width);
    // console.log(this.height);
    for (var i =0; i<this.width; i++) {
      for (var j = 0; j<this.height; j++) {
        if (condfn(i,j)) {
          this.fillPixel(i,j);
        }
      }
    }
  }

  this.fillAllPixels = () => { this.fillConditionalPixels((x,y) => {return true;}); };

  this.setFillColor =  function(colorString) {
    this.context.fillStyle = colorString;
  }

  this.getFillColor = function() {
    return this.context.fillStyle;
  }

  this.drawLine = function(x1,y1,x2,y2) {
    var converted = [];
    [[x1,y1], [x2,y2]].forEach(
      function(pts) {
        converted.push.apply(converted,
          this.toCanvasCoords.apply(this, pts)
        );
      }
    );
    var context= this.context;
    converted.reverse();
    context.moveTo(converted.pop(), converted.pop());
    context.lineTo(converted.pop(), converted.pop());
    context.stroke();
  }


}



function SubCanvasByMargin(marginX,marginY,canvas) {
  return new SubCanvas(marginX,marginY, canvas.width-marginX*2, canvas.height-marginY*2, canvas);
}
