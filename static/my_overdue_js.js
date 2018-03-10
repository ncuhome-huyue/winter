
var oAjax0 = null;
try {
  oAjax0 = new XMLHttpRequest();
} catch (e) {
  oAjax0 = new ActiveXObject("Microsoft.XMLHTTP");
};
oAjax0.open('get','/api/getyuqi', true);
oAjax0.setRequestHeader("Content-type", "application/json");
oAjax0.send(null);
oAjax0.onreadystatechange = function () {
  if (oAjax0.readyState === 4) {
    var list = document.getElementsByClassName("container")[0];
    var jud_color=document.getElementsByClassName('state');
    var data = oAjax0.responseText;
    var finally_data = eval("(" + data + ")");
    var olist=document.getElementsByClassName("list");
    for (var i=0;i<finally_data.data.length;i++){
      list.innerHTML+='<div class="list"></div><span class="book_name">'+finally_data.data[i][0]+'</span><span class="over_due">'
        +finally_data.data[i][1]+'</span><span class="give_price">'+finally_data.data[i][2]+'</span> <span class="school">'+finally_data.data[i][3]+'</span><span class="state">'
        +finally_data.data[i][4]+'</span></div>';

      if (finally_data.data[i][4]==='已处理'){
        jud_color[i].style.color='rgba(2,199,132,0.7)'
      }
      else {
        jud_color[i].style.color='rgba(255,192,23,0.7)'
      }
    }
  }
};
