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

openstackApp.factory('authTokenFactory', ['$q', function ($q) {

    var token = 'token';

    return {
        request: function (config) {
        	config.headers['x-a12n'] = App_Constants.auth;
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

