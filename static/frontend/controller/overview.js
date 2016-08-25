'use strict';

angular.module('frontApp')
    .controller('OverviewCtrl',
function ($scope, $rootScope, $interval, $location, StatusAPI, config) {
    $scope.initOverview = function() {
        StatusAPI.read().then(function(data){
            $scope.status = data;
            console.log($scope.status);
        })
    };

    $scope.formatDateTime = function(timeString){
        return moment(timeString).format('YYYY-MM-DD h:mm:ss A');
    };

    $scope.initOverview();
    $rootScope.overviewTimer = $interval($scope.initOverview, config.refreshTime);
});
