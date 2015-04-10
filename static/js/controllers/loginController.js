openstackApp.controller('loginController', ['$scope', '$rootScope', '$modalInstance', function ($scope, $rootScope, $modalInstance) {

    $scope.user = {
        username: "",
        password: ""
    }

    $scope.userInfo = [{ username: "admin", password: "admin" }];

    $scope.loginFailed = false;

    $scope.signIn = function () {
        for (var i = 0; i < $scope.userInfo.length; i++) {
            if ($scope.userInfo[i].username === $scope.user.username &&
                $scope.userInfo[i].password === $scope.user.password) {
                $rootScope.$broadcast("loginSuccess", {
                    username: $scope.user.username
                });
                $modalInstance.dismiss('cancel');
                return;
            }
        }
        $scope.loginFailed = true;
    };

    $scope.cancelSignIn = function () {

    };


}]);