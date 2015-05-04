openstackApp.controller('metadataController', ['$scope', '$http', '$modalInstance', 'fileInfo', function($scope, $http, $modalInstance, fileInfo) {

	var baseUrl = App_Constants.url + '/video/metadata/', url;

	$scope.closePopup = function(){
		$modalInstance.dismiss('cancel');
	};

	$scope.metadatas = [];

	$scope.loadMetadata = function() {
		url = baseUrl + fileInfo;
		$http.get(url).
	  		success(function(data, status) {
	  			$scope.metadatas = data;
	  		}).error(function(data, status) {

	  		});
	}


}]);