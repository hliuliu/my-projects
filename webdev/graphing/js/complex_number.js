


function ComplexNum (re,im) {
  this.re = re;
  this.im = im;

  this.add = function (that) {
    // Assume that is a ComplexNum
    return new ComplexNum(this.re+that.re, this.im+that.im);
  }

  this.multiply = function (that) {
    return new ComplexNum(this.re*that.re-this.im*that.im, this.re*that.im+this.im*that.re);
  }

  this.squared = function () {
    return this.multiply(this);
  }

  this.conjugate = function () {
    return new ComplexNum(this.re, -this.im);
  }

  this.plot = function (pgrid) {
    pgrid.fillPixel(this.re,this.im);
  }

  this.norm = function () {
    return Math.sqrt(this.re*this.re + this.im*this.im);
  }

}


function JuliaFn(c) {
  return function (z) {
    return z.squared().add(c);
  };
}


function MandelbrotPlot(plotGrid, maxiter=50, eps=0.001) {

  var convergeFn = function (c) {
    var f = JuliaFn(c);
    var z = new ComplexNum(0,0);
    var converge = z.norm()<=2;
    var w =z;
    for (var i=0;converge && i<maxiter;i++) {
      w = f(w);
      converge = w.norm()<=2;
    }

    return converge;
  };

  var c = new ComplexNum(0,0);
  for (c.re=plotGrid.xleft;c.re<=plotGrid.xright;c.re+=eps) {
    for (c.im = plotGrid.ybot; c.im <= plotGrid.ytop; c.im+=eps) {
      if (convergeFn(c)) {
        c.plot(plotGrid);
      }
    }
  }


}



function JuliaPlot(c, plotGrid, maxiter=10, eps =0.001) {
  var f = JuliaFn(c);
  var R = (1+Math.sqrt(1+4*c.norm()))/2;
  var z = new ComplexNum(0,0);
  for (z.re=plotGrid.xleft;z.re<=plotGrid.xright;z.re+=eps) {
    for (z.im = plotGrid.ybot; z.im <= plotGrid.ytop; z.im+=eps) {
      var converge = z.norm()<=R;
      var w =z;
      for (var i=0;converge && i<maxiter;i++) {
        w = f(w);
        converge = w.norm()<=R;
      }
      if (converge) {
        z.plot(plotGrid);
      }
    }
  }
}

// function JuliaPlot(c, plotGrid, maxiter=20) {
//   var f = JuliaFn(c);
//   var R = (1+Math.sqrt(1+4*c.norm()))/2;
//   var z = new ComplexNum(0,0);
//   console.log(R);
//   logs= [];
//
//   var convergeFn = function (x,y) {
//     var z = new ComplexNum(x,y);
//     var converge = z.norm()<=R;
//     var w =z;
//     for (var i=0;converge && i<maxiter;i++) {
//       w = f(w);
//       converge = w.norm()<=R;
//     }
//     // if (converge) {
//     //   z.plot(plotGrid);
//     // }
//     logs.push(w.norm());
//     return converge;
//   };
//
//   plotGrid.fillConditionalPixels(convergeFn);
//
//   console.log(logs);
//
// }
