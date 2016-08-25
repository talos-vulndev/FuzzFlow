'use strict';

var server_ip = '172.28.128.3';


angular
.module('frontApp', [
'ngRoute',
'ngTagsInput',
'file-model',
])
.value('config', {
    server: server_ip,
    baseURL: "http://" + server_ip + "/api",
    refreshTime: 5000   // Timer to update info from server
})
.config(function ($routeProvider) {
    $routeProvider
    .when('/', {
        templateUrl: 'view/overview.htm',
        controller: 'OverviewCtrl',
        title: "Overview",
    })
    .when('/node', {
        templateUrl: 'view/node.htm',
        controller: 'NodeManagerCtrl',
        title: "Node Manager",
    })
    .when('/crash', {
        templateUrl: 'view/crash.htm',
        controller: 'CrashManagerCtrl',
        title: "Crash Manager",
    })
    .when('/job', {
        templateUrl: 'view/job.htm',
        controller: 'JobManagerCtrl',
        title: "Job Manager",
    })
    .when('/err', {
        templateUrl: 'view/err.htm',
        controller: 'ErrLogCtrl',
        title: "Error Log",
    })
    .when('/config', {
        templateUrl: 'view/config.htm',
        controller: 'ConfigManagerCtrl',
        title: "Configuration",
    })
    .otherwise({
        redirectTo: '/'
    });
})
.run(['$location', '$rootScope', '$interval',
    function($location, $rootScope, $interval) {
    $rootScope.navActiveLink = function(path){
        return ($location.$$path === path) ? 'active' : '';
    }
    $rootScope.$on('$routeChangeSuccess', function (event, current, previous) {
        $interval.cancel($rootScope.nodeManagerTimer);
        $interval.cancel($rootScope.overviewTimer);
        $interval.cancel($rootScope.jobManagerTimer);
        $interval.cancel($rootScope.crashManagerTimer);
        $interval.cancel($rootScope.errLogTimer);

        if (current.hasOwnProperty('$$route')) {
            $rootScope.title = current.$$route.title;
        }
    });

}]);
