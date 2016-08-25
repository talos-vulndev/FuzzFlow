'use strict';

angular.module('frontApp')
    .controller('ErrLogCtrl',
function ($scope, $rootScope, $interval, MiscAPI, config) {
    $scope.initLog = function() {
        MiscAPI.log().then(function(data){
            $scope.log = data.log;
            console.log($scope.log);
        })
    };


    $scope.initLog();
    $rootScope.errLogTimer = $interval($scope.initLog, config.refreshTime);
});
