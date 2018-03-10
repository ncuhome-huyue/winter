var determine_button=document.getElementsByClassName('determine_button')[0];
var login_button=document.getElementsByClassName("login_button")[0];
var username_input=document.getElementsByClassName("username")[0];
var password_input=document.getElementsByClassName("password")[0];
username_input.onclick=function () {
  var username=document.getElementsByClassName("username_hr")[0];
  username.color='#76d1b2';
};

password_input.onclick=function () {
  var password=document.getElementsByClassName("password_hr")[0];
  password.color='#76d1b2'
};


login_button.onclick=function () {
  var hidden_area=document.getElementsByClassName("hidden_area")[0];
  hidden_area.style.display='block';

};

determine_button.onclick=function () {
    var verification_code = document.getElementsByClassName('check_yanzheng')[0].value;
    var username = document.getElementsByClassName('username')[0].value;
    var password = document.getElementsByClassName('password')[0].value;
    var data = {
      "username": username,
      "password": password,
      "yanzheng": verification_code
    };
    var final_data = JSON.stringify(data);
    var oAjax = null;
    try {
      oAjax = new XMLHttpRequest();
    } catch (e) {
      oAjax = new ActiveXObject("Microsoft.XMLHTTP");
    };
    oAjax.open('post', 'http://127.0.0.1:5000/api/login', true);
    oAjax.setRequestHeader("Content-type", "application/json");
    oAjax.send(final_data);
    oAjax.onreadystatechange = function () {
      if (oAjax.readyState === 4) {
        var data = oAjax.responseText;
        var finally_data=eval("("+data+")");
        if (finally_data.status==='success'){
          window.location.href='mypage.html';
          window.localStorage.setItem("name",finally_data.name)
        }
        if (finally_data.status==='error'){
          var hidden_area=document.getElementsByClassName("hidden_area")[1];
          hidden_area.style.display='block';
          setTimeout(function () {
            var hidden_area=document.getElementsByClassName("hidden_area")[1];
            hidden_area.style.display='none';
          },1000)
        }
      }
    }
  };
