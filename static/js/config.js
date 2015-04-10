var openstackApp = angular.module('openstackApp', ['ui.bootstrap']);

openstackApp.config(function ($locationProvider) {
    $locationProvider.html5Mode(true);
});