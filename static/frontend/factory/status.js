'use strict';

angular.module('frontApp')
    .factory('StatusAPI',
function (config, $http, $q) {
    var read = function(){
        var deferred = $q.defer();
        $http.get(config.baseURL + '/status')
        .success(function(data, status){
            deferred.resolve(data);
        })
        .error(function(error, status){
            deferred.reject(error);
        })
        return deferred.promise;
    }
    return {
        read: read
    }
});
