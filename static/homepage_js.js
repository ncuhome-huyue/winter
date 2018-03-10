var name1=document.getElementsByClassName("name")[0];
var total_name=document.getElementsByClassName("total_name")[0];



if (window.localStorage.getItem("name")!==null){
  var name=window.localStorage.getItem("name")
}

arr_name=name.split("");
var len=arr_name.length;
name1.innerHTML=name.substring(0,len);
total_name.innerHTML=name;


var oAjax = null;
try {
  oAjax = new XMLHttpRequest();
} catch (e) {
  oAjax = new ActiveXObject("Microsoft.XMLHTTP");
};
oAjax.open('get','/api/readnum', true);
oAjax.setRequestHeader("Content-type", "application/json");
oAjax.send(null);
oAjax.onreadystatechange = function () {
  if (oAjax.readyState === 4) {
    var total_read_data = document.getElementsByClassName("total_read_data")[0];
    var data = oAjax.responseText;
    var finally_data = eval("(" + data + ")");
    total_read_data.innerHTML=finally_data.booknum;
  }
  };

var buton1=document.getElementsByClassName('my_overdue')[0];
var button2=document.getElementsByClassName('my_recommendation')[0];
buton1.onclick=function () {
  window.location.href="my_overdue.html"
};
button2.onclick=function () {
  window.location.href="my_recommand.html"
};
