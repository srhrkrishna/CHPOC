openstackApp.service('loginService', ['$http', function ($http) {

	var url = App_Constants.url + '/user/login', loginUtil = {};


	loginUtil.login = function(success, error) {
		$http.post(url, {}).
	  		success(function(data, status) {
	  			success(true);
	  		}).error(function(data, status) {
	  			error(false);
	  		});
  	}

    return loginUtil;


}]);

