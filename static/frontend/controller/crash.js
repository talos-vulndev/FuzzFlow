'use strict';

angular.module('frontApp')
    .controller('CrashManagerCtrl',
function ($scope, $rootScope, $interval, config, JobAPI, CrashAPI, MiscAPI) {

    $scope.initCrashes = function(){
        JobAPI.list().then(function(data){
            $scope.jobs = data
            CrashAPI.list().then(function(data){
                $scope.crashes = data;
            })
        })
    };

     $scope.getJobName = function(crash){
        for(var i = 0; i < $scope.jobs.length; i++){
            if($scope.jobs[i].id === crash.job_id){
                return $scope.jobs[i].name;
            }
        }
     }

     $scope.getStaticURL = function(rel){
        return "http://" + config.server + '/' + rel;
     }

     $scope.getFileName = function(rel){
        var i;
        for(i = rel.length; i > 0 ; i--){
            if(rel[i] === '/'){
                break
            }
        }
        return rel.substring(i + 1 , rel.length);
     }

     $scope.formatDateTime = function(timeString){
        return moment(timeString).format('YYYY-MM-DD h:mm:ss A');
     };

     $scope.toggleShowCrashOutputModal = function(crash){
        $scope.selectedCrash = crash;
        MiscAPI.download($scope.getStaticURL(crash.dbg_file)).then(function(data){
            $scope.selectedCrash.dbg_file_output = data;
            $('#crashOutputModal').modal('show');
        }, function(){

        })
     }

     $scope.initCrashes();
     $rootScope.crashManagerTimer = $interval($scope.initCrashes, config.refreshTime);
});
