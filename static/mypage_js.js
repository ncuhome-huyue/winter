var oAjax0 = null;
try {
  oAjax0 = new XMLHttpRequest();
} catch (e) {
  oAjax0 = new ActiveXObject("Microsoft.XMLHTTP");
};
oAjax0.open('get','/api/getpercent', true);
oAjax0.setRequestHeader("Content-type", "application/json");
oAjax0.send(null);
oAjax0.onreadystatechange = function () {
  if (oAjax0.readyState === 4) {
    var total_read_data = document.getElementsByClassName("transcend_data")[0];
    var data = oAjax0.responseText;
    var finally_data = eval("(" + data + ")");
    total_read_data.innerHTML=finally_data.percent;
  }
};


var oAjax1 = null;
try {
  oAjax1= new XMLHttpRequest();
} catch (e) {
  oAjax1 = new ActiveXObject("Microsoft.XMLHTTP");
};
oAjax1.open('get','/api/readnum', true);
oAjax1.setRequestHeader("Content-type", "application/json");
oAjax1.send(null);
oAjax1.onreadystatechange = function () {
  if (oAjax1.readyState === 4) {
    var total_read_data = document.getElementsByClassName("total_data")[0];
    var data = oAjax1.responseText;
    var finally_data = eval("(" + data + ")");
    total_read_data.innerHTML=finally_data.booknum;
  }
};


var oAjax2 = null;
try {
  oAjax2 = new XMLHttpRequest();
} catch (e) {
  oAjax2 = new ActiveXObject("Microsoft.XMLHTTP");
};
oAjax2.open('get','/api/gettime', true);
oAjax2.setRequestHeader("Content-type", "application/json");
oAjax2.send(null);
oAjax2.onreadystatechange = function () {
  if (oAjax2.readyState === 4) {
    var total_read_data = document.getElementsByClassName("count_down_data")[0];
    var data = oAjax2.responseText;
    var finally_data = eval("(" + data + ")");
    total_read_data.innerHTML=finally_data.time;
  }
};

var name1=document.getElementsByClassName("name")[0];
var name2=document.getElementsByClassName("head_portrait_font")[0];



if (window.localStorage.getItem("name")!==null){
  var name=window.localStorage.getItem("name")
}

arr_name=name.split("");
var len=arr_name.length;
name2.innerHTML=name.substring(0,len);
name1.innerHTML=name;


var oAjax3 = null;
try {
  oAjax3 = new XMLHttpRequest();
} catch (e) {
  oAjax3 = new ActiveXObject("Microsoft.XMLHTTP");
};
oAjax3.open('get','/api/getnowbook', true);
oAjax3.setRequestHeader("Content-type", "application/json");
oAjax3.send(null);
oAjax3.onreadystatechange = function () {
  if (oAjax3.readyState === 4) {
    var  finall_container=document.getElementsByClassName("final_container")[0];
    var data = oAjax3.responseText;
    var finally_data = eval("(" + data + ")");
    for (var i=0;i<finally_data.data.length;i++){
      finally_container.innerHTML+='<div class="book_name_data">'+finally_data.data[i][0]+'</div><div class="deadtime_time">'+finally_data.data[i][1]+'</div> <div class="operation_data">'+finally_data.data[i][2]+'</div>';
    }
  }
};

var button=document.getElementsByClassName("middle")[0];
button.onclick=function () {
  window.location.href='homepage.html'
};
