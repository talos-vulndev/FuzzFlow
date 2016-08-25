'use strict';

angular.module('frontApp')
    .factory('HostAPI',
function (config, $http, $q) {
    var list = function(){
        var deferred = $q.defer();
        $http.get(config.baseURL + '/host')
        .success(function(data, status){
            deferred.resolve(data);
        })
        .error(function(error, status){
            deferred.reject(error);
        })
        return deferred.promise;
    }
    return {
        list: list
    }
});
