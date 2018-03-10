var oAjax2 = null;
try {
  oAjax2 = new XMLHttpRequest();
} catch (e) {
  oAjax2 = new ActiveXObject("Microsoft.XMLHTTP");
};
oAjax2.open('get','/api/getmycollection', true);
oAjax2.setRequestHeader("Content-type", "application/json");
oAjax2.send(null);
oAjax2.onreadystatechange = function () {
  if (oAjax2.readyState === 4) {
    var data = oAjax2.responseText;
    var container=document.getElementsByClassName("scontainer")[0];
    var collection=document.getElementsByClassName("collection");
    var booknum=document.getElementsByClassName("booknum");
    var finally_data = eval("(" + data + ")");
    if (finally_data.length>1) {
      for (i = 0; i < finally_data.length; i++) {
        container.innerHTML = '<div class="collection" ><span class="booknum">' + finally_data[i][0] + '</span>\n' +
          '<img class="simg" src="../img/my_collection_img1.png">\n' +
          '</div>';
        collection[i] = collection[i - 1] + "1.77333rm";
      }
    }
      if (finally_data.length===1){
        booknum[0].innerHTML=finally_data[0][0];
      }
    }
  };

