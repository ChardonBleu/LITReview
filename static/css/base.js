/*jslint es6*/
/*global document window*/

"use strict";

 window.onscroll = function() {scrollFunction()};

/**
 * resize logo image --> resize height navbar
 * @param  None
 */
 function scrollFunction() {
 if (document.body.scrollTop > 50 || document.documentElement.scrollTop > 50) {
     document.getElementById("logo").style.width = "50px";
 } else {
     document.getElementById("logo").style.width = "100px";
 }
 }