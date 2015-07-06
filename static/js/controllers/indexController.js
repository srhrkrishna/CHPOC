openstackApp.controller('indexController', ['$scope', '$modal', 'openstackService', 'videoService','jsonService','jsonFolderService', function ($scope, $modal, openstackService, videoService,jsonService,jsonFolderService) {

    var modalInstance = null;

    $scope.apiCall = openstackService;

    $scope.showLogin = function () {
        modalInstance = $modal.open({
            templateUrl: 'html/login.html',
            controller: 'loginController',
            backdrop: 'static',
            keyboard: false
        });
    };



    $scope.currentUser = "";

    $scope.$on("loginSuccess", function (event, args) {
        if (args.username) {
            $scope.currentUser = args.username;
        }
//        videoService.getVideos(function(data){
//            $scope.links = data;
//        });
        jsonService.login(function(data){
            $scope.folders = data;
        });



    });
    
    $scope.downloadFile = function(link) {
        if ($scope.apiCall.isDownloading) {
            return false;
        }
        openstackService.request(link);
    }

    $scope.viewMetadata = function(name) {
        //openstackService.metadata();
        $modal.open({
            templateUrl: 'html/metadata.html',
            controller: 'metadataController',
            backdrop: 'static',
            keyboard: false,
            size: 'lg',
            resolve: {
                fileInfo: function() { return name; }
            }
        });
    }   

    $scope.viewVideo = function(name) {
        //openstackService.metadata();
        $modal.open({
            templateUrl: 'html/videoplay.html',
            controller: 'videoController',
            backdrop: 'static',
            keyboard: false,
            size: 'lg',
            resolve: {
                fileInfo: function() { return name; }
            }
        });
    } 

    //$scope.links = [{ name: "File Name 1", url: "#" }, { name: "File Name 2", url: "#" }];

    $scope.tableShow = true;

    $scope.showBackButton = false;

   $scope.showFolderVideos = false;


    $scope.showTable = function() {

        $scope.showBackButton = false;

        $scope.showFolderVideos = false;

        $scope.tableShow = true;



    }


    $scope.getFolderForVideos = function (videoName) {


        jsonFolderService.getFolderVideos(function(data){

          //  $scope.videos = data; // get data from json

            $scope.tableShow = false;

            $scope.showBackButton = true;

            $scope.showFolderVideos = true;


            $scope.videos = data;

            $scope.folderName =  App_Constants.folderName + '/';

            $scope.downloadFolderName =  App_Constants.folderName + '___';

            $scope.viewVideoFolderName =  App_Constants.folderName + '___';


            App_Constants.folderName = "";

        /*   angular.forEach(data, function(item){


                if(item.name === videoName){
                    var text=[];
                    text.push(item);
                    $scope.videos = text;


                }

            })*/

        },videoName);




    }




}]);
