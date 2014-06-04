var console=console||{log:function(){return;}};
app = angular.module('myApp', []);
login = function($scope,$http,$rootScope){
    $scope.userName=/^[a-zA-Z][a-zA-Z\d\w\-]{3,12}$/;
    $scope.userPasswd=/^[a-zA-Z\d\w\-\@]{4,12}$/;
    $scope.popupHide = function(){
        $scope.popup = "hide";
    };
    $scope.logon = function(){
        if($scope.loginForm.$invalid){
            $scope.tipBox = "show";
            $scope.tipText = "用户名或密码有误！";
        }
        else{
            var userName = $scope.user.name;
            var userWord = $scope.user.passwd;
            $scope.loading = "show";
            $http({
                url: "./login.html",
                method: "POST",
                data: {user:userName,passwd:userWord}
           }).success(function (data, status, headers, config) {
                $scope.loading = "hide";
                if(data.status==200){
                    $scope.tipBox = "show";
                    $scope.tipText = "登录成功！";
                    window.location.href="index.html";
                }
                else if(data.status==403){
                    $scope.tipBox = "show";
                    $scope.tipText = "用户名或密码有误！";
                }
            }).error(function (data, status, headers, config) {
                $scope.loading = "hide";
                console.log(data);
           });
       }    
    };
    $scope.enterLogon = function (event) {
        event = event || window.event;
        var KeyCode = event.which?event.which:event.keyCode;
        if (KeyCode == 13) {
            $scope.logon();
        }
    };
    $scope.closeAll = function(){
        $scope.tipBox = 'hide';
    };
};
