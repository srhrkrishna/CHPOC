openstackApp.service('loginService', ['$http', function ($http) {

	var url = App_Constants.url + '/user/login', loginUtil = {};


	loginUtil.login = function(success, error, info) {
		$http.post(url, info).
	  		success(function(data, status, headers, config) {
	  			App_Constants.auth = headers()['x-a12n'];
	  			success(true);
	  		}).error(function(data, status) {
	  			error();
	  		});
  	}

    return loginUtil;

}]);

openstackApp.service('jsonService', ['$http', function ($http) {

    var url = App_Constants.url + '/list/?' + new Date(), videoSrvc = {};

    videoSrvc.login = function(success, error) {
        $http.get(url).
            success(function(data, status, headers, config) {
                success(data);
            }).
            error(function(data, status, headers, config) {
                alert("error");
            });
    }
    return videoSrvc;

}]);


openstackApp.service('jsonFolderService', ['$http', function ($http) {




    var url = App_Constants.url + '/list/?' + new Date() , folderVideoSrvc = {};

    folderVideoSrvc.getFolderVideos = function(success,folderName, error) {


        App_Constants.folderName = folderName;


        $http.get(url).
            success(function(data, status, headers, config) {
                success(data);
            }).
            error(function(data, status, headers, config) {
                alert("error");
                alert(data);
                alert(status);
                alert(headers);

            });
    }
    return folderVideoSrvc;

}]);

openstackApp.factory('authTokenFactory', ['$q', function ($q) {

    var token = 'token';

    return {
        request: function (config) {
        	config.headers['x-a12n'] = App_Constants.auth;
            if(App_Constants.folderName.length > 0){
                config.headers['x-pseudo-folder'] = App_Constants.folderName;
            }
            return config || $q.when(config);
        },
        response: function (response) {
            return response || $q.when(response);
        }
    };
} ]);

openstackApp.config(['$httpProvider', function ($httpProvider) {
    $httpProvider.interceptors.push('authTokenFactory');
}]);

