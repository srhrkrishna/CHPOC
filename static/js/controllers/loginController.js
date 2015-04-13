openstackApp.controller('loginController', ['$scope', '$rootScope', '$modalInstance', 'loginService', function ($scope, $rootScope, $modalInstance, loginService) {

    $scope.user = {
        username: "",
        password: ""
    }

    $scope.userInfo = [{ username: "admin", password: "admin" }];

    $scope.loginFailed = false;

    $scope.signIn = function () {
        loginService.login(function (success) {
            $scope.loginFailed = !success;
            $rootScope.$broadcast("loginSuccess", {
                username: $scope.user.username
            });
            $modalInstance.dismiss('cancel');
        }, function (error){
            $scope.loginFailed = error;
        });
    };

    $scope.cancelSignIn = function () {

    };


}]);