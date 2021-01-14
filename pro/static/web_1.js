window.onload=initAll;

function initAll() {
	var inp=document.getElementById('inp');
	inp.addEventListener('keydown',f1);
	// var b1=document.getElementById('b1');
	// b1.onclick=f2;
}


function f1(e) {
	console.log(e.target.value);
	var url='/search_word?wd='+e.target.value.toString();
	console.log(url);
	var d=document.getElementById('sugg');
	var s=''
	var res = new XMLHttpRequest();
  	res.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
    	var p=JSON.parse(this.responseText);
    	for (var k in p){
    		s+='<option value="'+p[k].toString()+'"/>';
    		console.log(p[k]);
    		d.innerHTML=s;
    	}
 
    }
  };
  res.open("GET", url, true);
  res.send();
}

// function f2() {
// 	var inp=document.getElementById('inp').value;
// 	var url='/save_word?wd='+inp;
// 	console.log(url);
// 	var res = new XMLHttpRequest();
//   	res.onreadystatechange = function() {
//     if (this.readyState == 4 && this.status == 200) {
//     	var p=this.responseText;
//     	console.log(p);
//  		document.getElementById('hh1').innerHTML=p;
//     }
//   };
//   res.open("GET", url, true);
//   res.send();
// }