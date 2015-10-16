var openstackApp = angular.module('openstackApp', ['ui.bootstrap']);

var App_Constants = { "url": "http://localhost", "auth": "","JSON_URL":"folderandcount.json",folderName:"" };

openstackApp.config(function ($locationProvider) {
    $locationProvider.html5Mode(true);
});
