/*=======应用列表数据======*/
APP_EDIT_LIST_URL = 'app_edit';///////编辑
APP_DELETE_LIST_URL = 'app_delete';///////删除
/*=======应用分类======*/
APP_CLASSIFY_URL = 'app_classify';///////应用分类
/*=======推荐应用列表======*/
RECOMMEND_EDIT_LIST_URL = 'recommend_edit';///////编辑
RECOMMEND_DELETE_LIST_URL = 'recommend_delete';///////删除
RECOMMEND_BUILD_LIST_URL ='recommend_build';/////拖动排序
/*=======直播列表数据======*/
LIVE_EDIT_LIST_URL = 'live_edit';/////编辑
LIVE_DELETE_LIST_URL = 'live_delete';/////删除
LIVE_BUILD_LIST_URL ='live_build';/////拖动排序
/*=======直播分类======*/
LIVE_CLASSIFY_URL = 'live_classify';
/*=======直播配图数据======*/
PIC_LIST_URL='live_pic';
LIVE_PIC_UPLOAD = 'live_pic_upload';
//////////////////////////////
var console=console||{log:function(){return;}};
if(!app){
    app = angular.module('myApp', []);
};
app.directive('ngFocus', ['$parse', function($parse) {
  return function(scope, element, attr) {
    var fn = $parse(attr['ngFocus']);
    element.bind('focus', function(event) {
      scope.$apply(function() {
        fn(scope, {$event:event});
      });
    });
  }
}]);
 
app.directive('ngBlur', ['$parse', function($parse) {
  return function(scope, element, attr) {
    var fn = $parse(attr['ngBlur']);
    element.bind('blur', function(event) {
      scope.$apply(function() {
        fn(scope, {$event:event});
      });
    });
  }
}]);
app.directive("uploadUploadify", function() {
    return {
        require: '?ngModel',
        restrict: 'A',
        link: function ($scope, element, attrs, ngModel,$rootScope) {
            var opts = angular.extend({}, $scope.$eval(attrs.nlUploadify));
            element.uploadify({
                'method'   : 'post',
                'auto': true,
                'swf': opts.swf || 'static/js/uploadify.swf',
                'uploader': opts.uploader || LIVE_PIC_UPLOAD,//图片上传方法
                'fileTypeDesc' : 'Image Files (.JPG,.JPEG,.GIF,.PNG,.BMP)', //出现在上传对话框中的文件类型描述
                'fileTypeExts' : '*.jpg;*.jpeg;*.gif;*.png;*.bmp', //控制可上传文件的扩展名，启用本项时需同时声明fileDesc
                'fileSizeLimit' : 1024*5+'KB', //控制上传文件的大小，单位byte

                'buttonText': opts.buttonText || '上传文件',
                'width': opts.width || '100%',
                'height': opts.height || 36,
                'onUploadSuccess': function (file, data, response) {
                    if (ngModel) {
                        if (data !==1) {
                            var picData = [];
                            data = JSON.parse(data);
                            
                            $scope.$apply(function() {
                                ngModel.$setViewValue(data.url);
                                if($scope.app){
                                    $scope.app.url = 'http://www/uploads'+$scope.app.urls;
                                    $scope.app.logo = 'static/uploads/'+$scope.app.logos;
                                    if($scope.app.info){
                                        if($scope.app.info.pic){
                                            var pics = 'static/uploads/'+ $scope.app.info.pics;
                                            $scope.app.info.pic.push(pics);
                                        }else{
                                            var pics = 'static/uploads/'+ $scope.app.info.pics;
                                            picData.push(pics);
                                            $scope.app.info.pic = picData;    
                                        };
                                        
                                    };
                                };
                                if($scope.history){
                                    $scope.history.url = 'http://www/uploads'+$scope.history.urls;
                                };
                                if($scope.picture.pics){
                                    $scope.picture.pic = $scope.picture.pics;
                                };
                            });
                            
                        };
                    };
                }
            });
        }
    };
});
app.directive('myDatepicker', function() {
    return {
        restrict: 'A',
        require : '?ngModel',
        link: function (scope, element, attrs, ngModel) {
          ngModel.$render = function() {
                element.val(ngModel.$viewValue || '');
          };
          if (ngModel ) {
            element.bind('focus blur change', function () {
              scope.$apply(function() {
                ngModel.$setViewValue(element.val());
              });
            });
          };
        }
    };
});
app.run(function($rootScope) {

    $rootScope.tipBoxHide =function(){
        $rootScope.tipBox = "hide";
    };

    $rootScope.closeAll = function(){
        $rootScope.popupBox = 'hide';
        $rootScope.historyBox = 'hide';
        $rootScope.tipBox = 'hide';
        $rootScope.allBox = 'hide';
        $rootScope.classifyBox = 'hide';
        $rootScope.listBox = 'hide';
        $rootScope.infoBox = 'hide';
        $rootScope.passwdBox = "hide";
        
    };
});
/////////账户管理
var confirmpasswd;
app.directive('newpassword', function() {
  return {
    restrict: 'CEA',
    require: 'ngModel',
    link: function(scope, elm, attrs, ctrl) {
         ctrl.$parsers.unshift(function(viewValue) {
            var newpasswd = /^[\@A-Za-z0-9\!\#\$\%\^\&\*\.\~\-\_]{6,12}$/;
            if (viewValue.match(newpasswd)) {
                  confirmpasswd = viewValue;
                  ctrl.$setValidity('newpasswd', true);
                  return viewValue;
            } else {
                  ctrl.$setValidity('newpasswd', false);
                  return undefined;
            }
      });
    }
  };
})
app.directive('confirmpassword', function() {
  return {
    restrict: 'CEA',
    require: 'ngModel',
    link: function(scope, elm, attrs, ctrl) {
      ctrl.$parsers.unshift(function(viewValue) {
        if (confirmpasswd == viewValue) {
          ctrl.$setValidity('confirmpasswd', true);
          return viewValue;
        } else {
          ctrl.$setValidity('confirmpasswd', false);
          return undefined;
        }
      });
    }
  };
})
if(!Array.indexOf)//////ie不支持数组的indexof方法
{
    Array.prototype.indexOf = function(obj)
    {              
        for(var i=0; i<this.length; i++)
        {
            if(this[i]==obj)
            {
                return i;
            }
        }
        return -1;
    }
};
pictureData =[];
overall = function($scope,$http,$rootScope,$filter){
    $scope.picData = pictureData;
    //////个人信息
    infoShow = function(){
        this._click = function(){
            $rootScope.infoBox = "show";
            $rootScope.allBox = "show";
            $http({
                url: "./info?action=get",
                method: "GET"
           }).success(function (data, status, headers, config) {
               if(data.status==200){
                   $scope.info = data.Result;
                }
                else if(data.status==500){
                    $rootScope.tipBox = "show";
                    $rootScope.allClose = "show";
                    $rootScope.tipText="请求失败，请重试。"; 
                }
            }).error(function (data, status, headers, config) {
                console.log(data);
           });    
        };
    };
    //////////
    $scope.myToken=/^[a-zA-Z\d]{1,64}$/;
    $scope.submitInfo = function(){
        if($scope.infoForm.$invalid){
            $rootScope.tipBox = "show";
            $rootScope.tipText="请填写正确信息。";
            $rootScope.tipClose = 'show';
        }
        else{
            var token = $scope.info.Token;
            var appid = $scope.info.AppID;
            var secret = $scope.info.Secret;
            
            $http({
            url: "./info?action=set&"+"token="+token+"&appid="+appid+"&secret="+secret,
            method: "GET"
           }).success(function (data, status, headers, config) {
                if(data.status==200){
                    $rootScope.tipBox = "show";
                    $rootScope.infoBox="hide";
                    $rootScope.tipText="恭喜您，提交成功！"; 
                    $rootScope.allClose = "show";
                }
                else if(data.status==500){
                    $rootScope.tipBox = "show";
                    $rootScope.tipText="您填写的信息有误"; 
                    $rootScope.tipClose = "show";
                }
                
            }).error(function (data, status, headers, config) {
                console.log(data);
           });    
      };
    };
    ///////修改密码
    passwdShow = function(){
        this._click = function(){
            $rootScope.passwdBox = "show";
            $rootScope.allBox = "show";
        };
    };
    $scope.myPasswd=/^[\@A-Za-z0-9\!\#\$\%\^\&\*\.\~\-\_]{6,12}$/;
    $scope.submitPasswd = function(){
            if($scope.passwdForm.$invalid){
                $rootScope.tipBox = "show";
                $rootScope.tipText="请填写正确信息。";
                $rootScope.tipClose = 'show';
            }
            else{
                var old = $scope.passwd.old;
                var newpasswd = $scope.passwd.news;
                $http({
                url: "./info",
                method: "POST",
                data:{passwd:old,newpasswd:newpasswd}
               }).success(function (data, status, headers, config) {
                    if(data.status==200){
                        $rootScope.tipBox = "show";
                        $rootScope.passwdBox="hide";
                        $rootScope.tipText="恭喜您，提交成功！"; 
                        $rootScope.allClose = "show";
                        /////初始化
                        $scope.passwordForm.$setPristine();
                        $scope.passwd = {
                            old:"",
                            news:"",
                            confirms:""
                        };     
                    }
                    else if(data.status==403){
                        $rootScope.tipBox = "show";
                        $rootScope.tipText="您填写的信息有误"; 
                        $rootScope.tipClose = "show";
                    }
                    
                }).error(function (data, status, headers, config) {
                    console.log(data);
               });    
                
          };
    };
    //////////导航菜单
    $scope.navData = [
        {name:'安全退出',url:'logout',icon:'exit'},
        {name:'首页',url:'index.html',icon:'home'},
        {name:'应用管理',url:'javascript:void(0);',icon:'app',
            subnav:[
                {name:'应用列表',url:'index.html'},
                {name:'应用推荐',url:'recommend.html'}
            ]
        },
        {name:'直播配图',url:'picture.html',icon:'image'},
        {name:'直播管理',url:'live.html',icon:'live'},
        {name:'账户管理',url:'javascript:void(0);',icon:'user',
            subnav:[
                {name:'个人信息',url:'javascript:void(0);',object:new infoShow()},
                {name:'修改密码',url:'javascript:void(0);',object:new passwdShow()}
            ]
        }
    ];
    /*================主要内容开始=============*/
    classifyAppType ='all';/////应用分类
    classifyPicType ='';///////配图分类
    classifyLiveType ='';//////直播分类
    
    $scope.listData = listData;
    ////应用列表分页
    ctrlApp = function(){
            ///////翻页
            var sortingOrder = 'score';
            $scope.sortingOrder = sortingOrder;
            $scope._reverses = false;
            $scope.filteredItems = [];
            $scope.groupedItems = [];
            $scope.itemsPerPage = 3;
            $scope.pagedItems = [];
            $scope.currentPage = 0;
            var searchMatch = function (haystack, needle) {
                if (!needle) {
                    return true;
                };
                return haystack.toLowerCase().indexOf(needle.toLowerCase()) !== -1;
            };
        
            // init the filtered items
            $scope.searchs = function () {
                $scope.filteredItems = $filter('filter')($scope.listData, function (list) {
                    //for(var attr in list) {
                        if (searchMatch(list.name, $scope.query))
                            return true;
                    //};
                    return false;
                });
                // take care of the sorting order
                if ($scope.sortingOrder !== '') {
                    $scope.filteredItems = $filter('orderBy')($scope.filteredItems, $scope.sortingOrder, $scope._reverses);
                };
                $scope.currentPage = 0;
                // now group by pages
                $scope.groupToPages();
            };
            // calculate page in place
            $scope.groupToPages = function () {
                $scope.pagedItems = [];
                
                for (var i = 0; i < $scope.filteredItems.length; i++) {
                    if (i % $scope.itemsPerPage === 0) {
                        $scope.pagedItems[Math.floor(i / $scope.itemsPerPage)] = [ $scope.filteredItems[i] ];
                    } else {
                        $scope.pagedItems[Math.floor(i / $scope.itemsPerPage)].push($scope.filteredItems[i]);
                    };
                };
            };
            
            $scope.prevPage = function () {
                if ($scope.currentPage > 0) {
                    $scope.currentPage--;
                };
            };
            
            $scope.nextPage = function () {
                if ($scope.currentPage < $scope.pagedItems.length - 1) {
                    $scope.currentPage++;
                };
            };
            
            $scope.setPage = function () {
                if(this.page){
                    $scope.currentPage = this.page-1;
                };
            };
            $scope.searchnull = function(){
                $scope.query.length <= 0 ? $scope.searchs() : null;
            };
            // functions have been describe process the data for display
            $scope.searchs();
        
            // change sorting order
            $scope.sort_by = function(newSortingOrder) {
                if ($scope.sortingOrder == newSortingOrder){
                    $scope._reverses = !$scope._reverses;
                }else{
                    $scope.sortingOrder = newSortingOrder;
                };
                if($scope._reverses){
                    $scope._reverse = 'icon-up';
                }else{
                    $scope._reverse = 'icon-down';
                };
            };    
        };
        ctrlApp();
        ctrlApp.$inject = ['$scope', '$filter'];

    ///////////////////////查看详情
    $scope.slideText = "查看详情";
    $scope.viewDetails = function(){
        this.details = !this.details;
        if(this.details){
            this.slideText = "收起详情";
        }    
        else{
            this.slideText = "查看详情";
        }
    };
    ///////增加信息
    $scope.addList = function(){
        $rootScope.popupBox ='show';
        $rootScope.allBox = 'show';
        $rootScope.app = {history:[]};
        $rootScope.types = 'add';
        $rootScope._top = 56;
    };
    
    ////编辑信息
    $scope.updateList = function(index){
        $rootScope.app = this.list;
        $rootScope.popupBox ='show';
        $rootScope.allBox = 'show';
        var _scrollTop = document.body.scrollTop || document.documentElement.scrollTop
        $rootScope._top = 40+_scrollTop;
        $rootScope.types = 'update';
        $rootScope.num = index;
    };
    /////删除信息
    $scope.deleteShow = function(){
        this.deleteBox = 'show';
    };
    $scope.deleteList = function(index){
        $scope.pagedItems[$scope.currentPage].splice(index,1);
        this.deleteBox = 'hide';    
        var myKey = this.list.name;
        var myData = this.list;
        requestApp(myKey,'delete','');
    };
    $scope.deleteBoxHide = function(){
        this.deleteBox = 'hide';    
    };
    //////保存应用数据
    requestApp = function(myKey,updateType,submitData){
        var appUrl='';
        if(classifyAppType=='all'){
            switch(updateType){
                case 'edit':
                appUrl = APP_EDIT_LIST_URL;
                break;
                case 'delete':
                appUrl = APP_DELETE_LIST_URL;
                break;
            };
        }else{
            switch(updateType){
                case 'edit':
                appUrl = RECOMMEND_EDIT_LIST_URL;
                break;
                case 'delete':
                appUrl = RECOMMEND_DELETE_LIST_URL;
                break;
                case 'build':
                appUrl = RECOMMEND_BUILD_LIST_URL;
                break;
            };
        };
        //////请求提交数据
        var submitData = angular.toJson(submitData);
        console.log(submitData);
        //////
        $rootScope.popupBox = 'hide';
        $rootScope.historyBox = 'hide';
        $rootScope.allBox = 'show';
        $rootScope.listBox = 'hide';

        $http({
            url: appUrl,
            method: "POST",
            data: {classify:classifyAppType,key:myKey,data:submitData}
           }).success(function (data, status, headers, config) {
            if(data.status==200){
                $rootScope.tipBox = "show";
                $rootScope.tipText="恭喜您，提交成功！"; 
                $rootScope.tipClose = 'hide';
                $rootScope.allClose = 'show';
            }
            else if(data.status==500){
                $rootScope.tipBox = "show";
                $rootScope.tipText="提交失败，请重试。";
                $rootScope.tipClose = 'show';
                $rootScope.allClose = 'hide';
            }
            
            }).error(function (data, status, headers, config) {
                console.log(status);
           });
    };
/*};
appList = function($scope,$http,$rootScope){*/
    ////提交信息 
    $scope.submitApp = function(types,num){
        if($scope.appForm.$invalid){
            $rootScope.tipBox = 'show';
            $rootScope.tipClose = 'show';
            $rootScope.allClose = 'hide';
            $rootScope.tipText = '您输入的信息有误！';
        }else{
            $scope.master= {};
            $scope.master = angular.copy($scope.app);
            switch(types){
                case 'add':
                $scope.listData.push($scope.master);
                ctrlApp();
                break;
                
                case 'update':
                $scope.listData[num]=$scope.master;
                break;
            };
            ///////
            var myKey = $scope.master.name;
            var submitData = angular.toJson($scope.master);
            console.log(submitData);
            ///////
            $http({
                url: APP_EDIT_LIST_URL,
                method: "POST",
                data: {key:myKey,classify:classifyAppType,data:submitData}
               }).success(function (data, status, headers, config) {
                if(data.status==200){
                    $rootScope.tipBox = "show";
                    $rootScope.tipText="恭喜您，提交成功！"; 
                    $rootScope.tipClose = 'hide';
                    $rootScope.allClose = 'show';
                    $rootScope.popupBox="hide";
                    ///////////// 初始化
                    $scope.appForm.$setPristine();
                    $scope.app = {};
                }
                else if(data.status==500){
                    $rootScope.tipBox = "show";
                    $rootScope.tipClose = 'show';
                    $rootScope.allClose = 'hide';
                    $rootScope.tipText="提交失败，请重试。";
                }
                
            }).error(function (data, status, headers, config) {
                console.log(status);
           });    
        };
    };
/*};
appHistory = function($scope,$http,$rootScope){*/
    ///////增加历史版本
    $scope.addHistory = function(index){
        $rootScope.historyBox ='show';
        $rootScope.allBox = 'show';
        $rootScope.history = {};
        
        $rootScope.hisTypes ='add';
        $rootScope.pareNum =index;    
    };
    ///////编辑历史版本
    $scope.updateHistory = function(pare,index){
        $rootScope.history = this.items;
        $rootScope.historyBox ='show';
        $rootScope.allBox = 'show';
        $rootScope.hisTypes ='update';
        $rootScope.pareNum =pare;
        $rootScope.num =index;
    };
    ////提交历史版本
    $scope.submitHistory = function(hisTypes,pareNum,num){
        if($scope.historyForm.$invalid){
            $rootScope.tipBox = 'show';
            $rootScope.tipClose = 'show';
            $rootScope.allClose = 'hide';
            $rootScope.tipText = '您输入的信息有误！';
        }else{
            $scope.master= {};
            $scope.master = angular.copy($scope.history);
            switch(hisTypes){
                case 'add':
                $scope.pagedItems[$scope.currentPage][pareNum].history.push($scope.master);
                break;
                
                case 'update':
                $scope.pagedItems[$scope.currentPage][pareNum].history[num]=$scope.master;
                break;
            };
            var myKey = $scope.pagedItems[$scope.currentPage][pareNum].name;
            var submitData = angular.toJson($scope.pagedItems[$scope.currentPage][pareNum]);
            console.log(submitData);
            ///////
            $http({
                url: APP_EDIT_LIST_URL,
                method: "POST",
                data: {key:myKey,classify:classifyAppType,data:submitData}
               }).success(function (data, status, headers, config) {
                if(data.status==200){
                    $rootScope.tipBox = "show";
                    $rootScope.tipText="恭喜您，提交成功！"; 
                    $rootScope.tipClose = 'hide';
                    $rootScope.allClose = 'show';
                    $rootScope.popupBox="hide";
                    ///////////// 初始化
                    $scope.historyForm.$setPristine();
                    $scope.history = {};
                }
                else if(data.status==500){
                    $rootScope.tipBox = "show";
                    $rootScope.tipText="提交失败，请重试。";
                    $rootScope.tipClose = 'show';
                    $rootScope.allClose = 'hide';
                }
                
            }).error(function (data, status, headers, config) {
                console.log(status);
           });    
        };
    };
    /////删除历史信息
    $scope.deleteHistory = function(pare,index){
        this.list.history.splice(index,1);
        var myKey = this.list.name;
        var myData = this.list;
        requestApp(myKey,'edit',myData);
    };
    ////////保存拖动排序
    $scope.buildList = function(){
        var myData = [];
        for(var i=0; i<$scope.pagedItems.length; i++){
            for(var j =0; j<$scope.pagedItems[i].length; j++){
                myData.push($scope.pagedItems[i][j]);    
            };
        };
        requestApp('','build',myData);
    };
    
    ///////从列表中增加信息
    var temporaryData = [];
    $scope.chooseData= listData;
    $scope.addForList = function(){
        var listId =[];
        for(var j=0; j<$scope.listData.length; j++){
            listId.push($scope.listData[j].name);
        };
        /////去重
        $scope.chooseData = [];
        for(var i=0; i<listData.length; i++){
            if (listId.indexOf(listData[i].name) <0) {
                $scope.chooseData.push(listData[i]);
            };
        };
        $rootScope.allBox = 'show';
        $rootScope.listBox = 'show';    
        $rootScope.app = {};
        $rootScope.types = 'add';
        var num = $scope.chooseData.length;
        if(num<12){
            $rootScope._topCh = 150-num*5;
        }
        else if(num>=12){
            $rootScope._topCh = 60;
        };
        temporaryData = [];
        for(var k=0; k<$scope.chooseData.length; k++){
            temporaryData.push('1');
            $scope.chooseData[k].appName=false;
        };
    };
    ////选择列表
    $scope.appChoose = function(index){
        this.list.appName = !this.list.appName;
        if(this.list.appName){
            temporaryData[index]=this.list;
        }else{
            temporaryData[index]='1';
        };
    };
    /////提交列表
    $scope.submitChoose = function(){
        //console.log(temporaryData);
        var submitData = [];
        for(var i=0; i<temporaryData.length; i++){
            if(temporaryData[i]!=='1'){
                $scope.listData.push(temporaryData[i]);
                submitData.push(temporaryData[i]);
            };
        };
        ctrlApp();
        //$scope.listData = $scope.listData.concat(temporaryData);
        //$('#nameList i').attr('class','');
        $scope.chooseForm.$setPristine();
        $scope.searchString={};
        
        requestApp('','edit',submitData);
    };
    //////分类管理
    $scope.classifyList = function(){ 
        classifyAppType = this.classify.id;
        var content = eval(classifyAppType);
        $scope.listData = content;
        ctrlApp();
    };
    $scope.classifyData = [
        {name:'影音',id:'video'},
        {name:'游戏',id:'game'},
        {name:'教育',id:'education'},
        {name:'生活',id:'life'},
        {name:'网络',id:'network'},
        {name:'其它',id:'other'}
    ];
    $scope.manageClassify = function(){
        $rootScope.classifyBox = 'show';
        $rootScope.allBox = 'show';
    };
    ///////保存分类数据
    $scope.saveClassify = function(save){
        var submitClassifyData = angular.toJson($scope.classifyData);
        console.log(submitClassifyData);
        //////
        $http({
            url: APP_CLASSIFY_URL,
            method: "POST",
            data: {data:submitClassifyData}
           }).success(function (data, status, headers, config) {
            if(data.status==200){
                if(save=='drag'){
                    $rootScope.tipBox = "show";
                    $rootScope.tipText="恭喜您，提交成功！"; 
                    $rootScope.tipClose = 'hide';
                    $rootScope.allClose = 'show';
                };
            }
            else if(data.status==500){
                $rootScope.tipBox = "show";
                $rootScope.tipText="提交失败，请重试。";
                $rootScope.tipClose = 'show';
                $rootScope.allClose = 'hide';
            }
            
        }).error(function (data, status, headers, config) {
            console.log(status);
       });        
    };
    /////删除分类
    $scope.deleteClassify = function(index){
        $scope.classifyData.splice(index,1);
        $scope.saveClassify();
    };
    ////直播分页
    ctrlLive = function(){
            ///////翻页
            var sortingOrder = 'score';
            $scope.sortingOrder = sortingOrder;
            $scope._reverses = false;
            $scope.filteredItems = [];
            $scope.groupedItems = [];
            $scope.itemsPerPage = 3;
            $scope.pagedItems = [];
            $scope.currentPage = 0;
            var searchMatch = function (haystack, needle) {
                if (!needle) {
                    return true;
                };
                return haystack.toLowerCase().indexOf(needle.toLowerCase()) !== -1;
            };
        
            // init the filtered items
            $scope.searchs = function () {
                $scope.filteredItems = $filter('filter')($scope.liveData, function (lives) {
                    for(var attr in lives) {
                        if (searchMatch(lives[attr], $scope.query))
                            return true;
                    };
                    return false;
                });
                // take care of the sorting order
                if ($scope.sortingOrder !== '') {
                    $scope.filteredItems = $filter('orderBy')($scope.filteredItems, $scope.sortingOrder, $scope._reverses);
                };
                $scope.currentPage = 0;
                // now group by pages
                $scope.groupToPages();
            };
            // calculate page in place
            $scope.groupToPages = function () {
                $scope.pagedItems = [];
                
                for (var i = 0; i < $scope.filteredItems.length; i++) {
                    if (i % $scope.itemsPerPage === 0) {
                        $scope.pagedItems[Math.floor(i / $scope.itemsPerPage)] = [ $scope.filteredItems[i] ];
                    } else {
                        $scope.pagedItems[Math.floor(i / $scope.itemsPerPage)].push($scope.filteredItems[i]);
                    };
                };
            };
            
            $scope.prevPage = function () {
                if ($scope.currentPage > 0) {
                    $scope.currentPage--;
                };
            };
            
            $scope.nextPage = function () {
                if ($scope.currentPage < $scope.pagedItems.length - 1) {
                    $scope.currentPage++;
                };
            };
            
            $scope.setPage = function () {
                if(this.page){
                     $scope.currentPage = this.page-1;
                };
            };
        
            // functions have been describe process the data for display
            $scope.searchs();
        
        };
    /////////////////////////////直播管理//////////////////////////////
    $scope.classifyLive = function(){ 
        classifyLiveType = this.classify.id
        var content = eval(classifyLiveType);
        $scope.liveData = content;
        for(var i=0; i<$scope.liveData.length; i++){
            $scope.liveData[i].drags='chapter';
            for(var j=0; j<$scope.liveData[i].list.length; j++){
                $scope.liveData[i].list[j].drags='lecture';
            };
        };
        ctrlLive();
    };
    $scope.classifyLiveData = [
        {name:'大陆',id:'land'},
        {name:'央视',id:'cctv'},
        {name:'地方台',id:'local'},
        {name:'其它',id:'other'},
        {name:'其它',id:'other'},
        {name:'其它',id:'other'},
        {name:'其它',id:'other'},
        {name:'其它',id:'other'},
        {name:'其它其它其它其它其它其它',id:'other'},
        {name:'其它',id:'other'},
        {name:'其它',id:'other'},
        {name:'其它',id:'other'},
        {name:'其它',id:'other'},
        {name:'其它',id:'other'},
        {name:'其它',id:'other'},
        {name:'其它',id:'other'},
        {name:'其它',id:'other'},
        {name:'其它',id:'other'},
        {name:'其它',id:'other'},
        {name:'其它',id:'other'},
        {name:'其它',id:'other'},
        {name:'其它',id:'other'},
        {name:'其它',id:'other'},
        {name:'其它',id:'other'},
        {name:'其它',id:'other'}
    ];
    ///////保存分类数据
    $scope.saveClassifyLive = function(save){
        var submitClassifyData = angular.toJson($scope.classifyLiveData);
        console.log(submitClassifyData);
        //////
        $http({
            url: LIVE_CLASSIFY_URL,
            method: "POST",
            data: {data:submitClassifyData}
           }).success(function (data, status, headers, config) {
            if(data.status==200){
                if(save=='drag'){
                    $rootScope.tipBox = "show";
                    $rootScope.tipText="恭喜您，提交成功！"; 
                    $rootScope.tipClose = 'hide';
                    $rootScope.allClose = 'show';
                };
            }
            else if(data.status==500){
                $rootScope.tipBox = "show";
                $rootScope.tipText="提交失败，请重试。";
                $rootScope.tipClose = 'show';
                $rootScope.allClose = 'hide';
            }
            
        }).error(function (data, status, headers, config) {
            console.log(status);
       });        
    };
    /////删除分类
    $scope.deleteClassifyLive = function(index){
        $scope.classifyLiveData.splice(index,1);
        $scope.saveClassifyLive();
    };
    
    //////////直播列表管理///////////
    ////保存数据
    $scope.saveLive = function(myKey,updateType,submitData){
        var appUrl='';
        switch(updateType){
            case 'edit':
            appUrl = LIVE_EDIT_LIST_URL;
            break;
            case 'delete':
            appUrl = LIVE_DELETE_LIST_URL;
            break;
            case 'build':
            appUrl = LIVE_BUILD_LIST_URL;
            break;
        };
        var submitData = angular.toJson(submitData);
        console.log(submitData);
        //////
        $http({
            url: appUrl,
            method: "POST",
            data: {key:myKey,classify:classifyLiveType,data:submitData}
           }).success(function (data, status, headers, config) {
            if(data.status==200){
                if(updateType=='build'){
                    $rootScope.allBox = "show";
                    $rootScope.tipBox = "show";
                    $rootScope.tipText="恭喜您，提交成功！"; 
                    $rootScope.allClose = 'show';
                };
            }
            else if(data.status==500){
                $rootScope.allBox = "show";
                $rootScope.tipBox = "show";
                $rootScope.tipText="提交失败，请重试。";
                $rootScope.allClose = 'show';
            }
            
        }).error(function (data, status, headers, config) {
            console.log(status);
       });        
    };
    $scope.updateLive = function(){
        var myKey = this.lives.name;
        var submitData = this.lives;
        $scope.saveLive(myKey,'edit',submitData);    
    };
    ////////保存拖动排序
    $scope.buildLive = function(){
        var myData = [];
        for(var i=0; i<$scope.pagedItems.length; i++){
            for(var j =0; j<$scope.pagedItems[i].length; j++){
                myData.push($scope.pagedItems[i][j]);    
            };
        };
        $scope.saveLive('','build',myData);
    };
    ///增加一个台
    $scope.addLive = function(){
        var thisType = $scope.liveData[0].types;
        $scope.liveData.splice(0,0,{state:true,types:thisType,list:[]});
        ctrlLive();
    };
    /////删除台
    $scope.deleteLive = function(index){
        $scope.pagedItems[$scope.currentPage].splice(index,1);
        this.deleteBox = 'hide';
        var myKey = this.lives.name;
        $scope.saveLive(myKey,'delete','');
    };
    ////频道分类选择
    $scope.liveChoose = function(index){
        var myType = this.lives.types;
        var liveValue = eval(myType);
        var moveData = $scope.liveData[index];
        liveValue.push(moveData);
        $scope.liveData.splice(index,1);
        ctrlLive();
        
        var myKey = this.lives.name;
        $scope.saveLive(myKey,'delete','');//////保存当前删除数据
        
        var submitData = angular.toJson(moveData);
        console.log(submitData);
        //////保存移动数据
        $http({
            url: LIVE_EDIT_LIST_URL,
            method: "POST",
            data: {key:myKey,classify:myType,data:submitData}
           }).success(function (data, status, headers, config) {
            if(data.status==200){
                $rootScope.allBox='show';
                $rootScope.tipBox = "show";
                $rootScope.tipText="恭喜你，数据移动成功";
                $rootScope.allClose = 'show';
            };
            
        }).error(function (data, status, headers, config) {
            console.log(status);
       });
    };
    /////查看源
    $scope.viewText = "查看源";
    $scope.viewSource = function(){
        this.source = !this.source;
        if(this.source){
            this.viewText = "收起源";
        }    
        else{
            this.viewText = "查看源";
        };
    };
    ////台开关
    $scope.turnLive = function(){
        if(this.lives.state){
            this.lives.state =false;
            this.source =false;
            this.viewText = "查看源";
        }else{
            this.lives.state =true;
        };
        var myKey = this.lives.name;
        var myData = this.lives;
        $scope.saveLive(myKey,'edit',myData);
    };
    ////源开关
    $scope.turnSource = function(){
        this.videos.state = !this.videos.state;
        var myKey = this.lives.name;
        var myData = this.lives;
        $scope.saveLive(myKey,'edit',myData);
    };
    ////增加视频源
    $scope.addSource = function(index){
        this.lives.list.push({state:true});    
    };
    ////删除视频源
    $scope.deleteSource = function(pare,index){
        this.lives.list.splice(index,1);
        var myKey = this.lives.name;
        var myData = this.lives;
        $scope.saveLive(myKey,'edit',myData);
    };
    ////////////////拖动
    $scope.chaptersOptions = {
      accept: function(data, sourceItemScope, targetScope, destIndex) {
        return (data.drags == 'chapter'); // only accept chapter
      }
      
    };
    $scope.lecturesOptions = {
      accept: function(data, sourceItemScope, targetScope, destIndex) {
        return (data.drags == 'lecture'); // only accept lecture
      }
    };
    
//	$scope.picData = [];
};
//////
getData = function($scope,$http){
    $http({
        url: PIC_LIST_URL + "?data=starting",
        method: "GET"
    }).success(function (data, status, headers, config) {
        if(data.status==200){
			pictureData = data.picData;
            $scope.picData = data.picData;
        }
        else if(data.status==500){
            $rootScope.tipBox = "show";
            $rootScope.tipText="提交失败，请重试。";
            $rootScope.tipClose = 'show';
            $rootScope.allClose = 'hide';
        }
    }).error(function (data, status, headers, config) {
        console.log(status);
    });
    $scope.classifyPic = function(){ 
        classifyPicType = this.classify.id;
        $http({
                url: PIC_LIST_URL+'?data=' + classifyPicType,
                method: "GET"
               }).success(function (data, status, headers, config) {
                if(data.status==200){
                    $scope.picData = data.picData;
                }
                else if(data.status==500){
                    $rootScope.tipBox = "show";
                    $rootScope.tipText="提交失败，请重试。";
                    $rootScope.tipClose = 'show';
                    $rootScope.allClose = 'hide';
                };
                
            }).error(function (data, status, headers, config) {
                console.log(status);
           });    
    };
	//////////直播配图//////////
    ////分类管理
    $scope.classifyPicData = [
        {
            name:'启动页',id:'starting'
        },
        {
            name:'加载页',id:'loading'    
        }
    ];
    ////配图开关
    $scope.turnPic = function(){
        this.list.state = !this.list.state;
        $scope.savePic();
    };
    ///////增加信息
    $scope.addPicture = function(){
        $rootScope.popupBox ='show';
        $rootScope.allBox = 'show';
        $rootScope.types = 'add';  
        $rootScope.picture = {weight:1,pic:''};  
    };
    ////编辑信息
    $scope.updatePicture = function(index){
        $rootScope.popupBox ='show';
        $rootScope.allBox = 'show';
        $rootScope.types = 'update';  
        $rootScope.num = index;
        $rootScope.picture = this.list;  
    };
    /////删除信息
    $scope.deletePic = function(index){
        $scope.picData.splice(index,1);
        $scope.savePic();
    };
    $scope.weightData=[
            {value:1},
            {value:2},
            {value:3},
            {value:4},
            {value:5},
            {value:6},
            {value:7},
            {value:8},
            {value:9}
        ];
    $scope.submitPic = function(picTypes,index){
        if($scope.picForm.$invalid){
            $rootScope.tipBox = 'show';
            $rootScope.tipClose = 'show';
            $rootScope.allClose = 'hide';
            $rootScope.tipText = '请上传图片！';
        }else{
            $scope.master= {};
            $scope.master = angular.copy($scope.picture);
            switch(picTypes){
                case 'add':
                $scope.picData.push($scope.master);
                break;
                
                case 'update':
                $scope.picData[index]=$scope.master;
                break;
                
            };
            var submitPicData = angular.toJson($scope.picData);
            console.log(submitPicData);
            ///////
            $http({
                url: PIC_LIST_URL,
                method: "POST",
                data: {key:classifyPicType,data:submitPicData}
               }).success(function (data, status, headers, config) {
                if(data.status==200){
                    $rootScope.tipBox = "show";
                    $rootScope.tipText="恭喜您，提交成功！"; 
                    $rootScope.tipClose = 'hide';
                    $rootScope.allClose = 'show';
                    $rootScope.popupBox="hide";
                    ///////////// 初始化
                    $scope.picForm.$setPristine();
                    $scope.picture = {};
                }
                else if(data.status==500){
                    $rootScope.tipBox = "show";
                    $rootScope.tipText="提交失败，请重试。";
                    $rootScope.tipClose = 'show';
                    $rootScope.allClose = 'hide';
                };
                
            }).error(function (data, status, headers, config) {
                console.log(status);
           });    
        };
    };
    $scope.savePic = function(){
        var submitPicData = angular.toJson($scope.picData);
        console.log(submitPicData);
        ///////
        $http({
            url: PIC_LIST_URL,
            method: "POST",
            data: {key:classifyPicType,data:submitPicData}
           }).success(function (data, status, headers, config) {
             if(data.status==500){
                $rootScope.tipBox = "show";
                $rootScope.tipText="提交失败，请重试。";
                $rootScope.allClose = 'show';
            };
            
        }).error(function (data, status, headers, config) {
            console.log(status);
       });        
    };
};
angular.element(document).ready(function(){
    ////二级菜单
    $('#nav>li').hover(function(){
        $(this).children('ol').stop(true,true).slideDown();
    },function(){
        $(this).children('ol').stop(true,true).slideUp();
    });    
    //////应用列表详情
    $.msclick(".infoBox","ul.tab li",".con","on");
    var number = $('.picShow').length;
    for(var i=0; i<number; i++){
        $.picShow("#show"+i);
    };
    $(document).on('click','.submit,.rebuild,ul.tabs li,#search,.pages a',function(){
        $.msclick(".infoBox","ul.tab li",".con","on");
        var number = $('.picShow').length;
        for(var i=0; i<number; i++){
            $.picShow("#show"+i);
        };
    });
    //////直播配图查看大图
    $(document).on('click','.viewPic',function(){
        $('#all').css('display','block');
        $('#popupBox').fadeIn();
        var active = $(this).attr('myIndex')*1;
        $.picShow("#showPic",active);
        $('#close,#all').click(function(){
            $('#all').css('display','none');
            $('#popupBox').fadeOut();    
        });
    });
    ////应用分类
    $('ul.tabs li:first-child').trigger('click').attr('class','on');
    
    $(document).on('click','ul.tabs li',function(){
        $(this).addClass('on').siblings().removeClass('on');
        ////////自动计算长度
        var oneScreen = $('.classifyTab').width()-400;
        var ulWidth = 0;
        $('.classifyTab ul.tabs li').each(function(index, element) {
            ulWidth += $(this).width()+20;////20内边距
        });
        $('.classifyTab ul.tabs').css('width',ulWidth);
        var scrollLeft=0;
        $(this).prevAll().each(function(index, element) {
            scrollLeft += $(this).width()+20;////20内边距
        });
        var num = parseInt(scrollLeft/oneScreen,10);
        $('.classifyTab ul.tabs').animate({'margin-left':oneScreen*num*-1},300);
    });
});