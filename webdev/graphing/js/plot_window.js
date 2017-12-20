

function PlottingWindow (xleft, xright, ybot, ytop, subCanvas) {

  // cartesian coordinates
  this.xleft = xleft;
  this.xright = xright;
  this.ybot = ybot;
  this.ytop = ytop;

  this.subCanvas = subCanvas; // an instance of the SubCanvas function

  this.drawAxes = function() {

    // TODO: Draw the axes onto the given subcanvas as would be seen on a cartesian plane
    //  based on the xy limits
  }

  this.cartesianToCanvasCoords = function(x,y) {
    // convert cartesian coordinates (x,y) to subcanvas coordinates
    // results are rounded to the nearest integer
    // xspan = this.xright-this.xleft+1;
    // yspan = this.ytop-this.ybot+1;
    dx = (this.xright-this.xleft)/(this.subCanvas.width -1);
    dy = (this.ytop-this.ybot)/(this.subCanvas.height - 1);
    cx = (x-this.xleft)/ dx;
    cy = (this.ytop - y)/ dy;
    cx = Math.round(cx);
    cy = Math.round(cy);
    return [cx,cy];
  }

  this.canvasToCartesianCoords = function(x,y) {
    dx = (this.xright-this.xleft)/(this.subCanvas.width -1);
    dy = (this.ytop-this.ybot)/(this.subCanvas.height - 1);
    return [this.xleft+dx*x, this.ytop-dy*y];
  }

  this.fillPixel = function (x,y) {
    cp = this.cartesianToCanvasCoords(x,y);
    this.subCanvas.fillPixel(cp[0],cp[1]);
  }

  this.fillConditionalPixels = function (condfn) {
    // for each valid pixel (x,y), fill it iff condfn(x,y) -> true
    self = this;
    this.subCanvas.fillConditionalPixels(
      function (x,y) {
        cp = self.canvasToCartesianCoords(x,y);
        // console.log([x,y]);
        // console.log(cp);
        return condfn(cp[0],cp[1]);
      }
    );
  }


}
