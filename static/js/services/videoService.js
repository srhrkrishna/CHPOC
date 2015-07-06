openstackApp.service('videoService', ['$http', function ($http) {

	var url = App_Constants.url + '/list/?' + new Date(), videoSrvc = {};

	videoSrvc.getVideos = function(success, error) {
		$http.get(url).
	  		success(function(data, status) {
	  			success(data);
	  		}).error(function(data, status) {

	  		});


  	}




    return videoSrvc;


}]);



