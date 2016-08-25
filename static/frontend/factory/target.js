'use strict';

angular.module('frontApp')
    .factory('TargetAPI',
function (config, $http, $q) {
    var list = function(){
        var deferred = $q.defer();
        $http.get(config.baseURL + '/target')
        .success(function(data, status){
            deferred.resolve(data);
        })
        .error(function(error, status){
            deferred.reject(error);
        })
        return deferred.promise;
    }
    var remove = function(id){
        var deferred = $q.defer();
        $http.get(config.baseURL + '/target/' + id + '?delete=1')
        .success(function(data, status){
            deferred.resolve(data);
        })
        .error(function(error, status){
            deferred.reject(error);
        })
        return deferred.promise;
    }
    var update = function(id, data){
        var deferred = $q.defer();
        $http.post(config.baseURL + '/target/' + id, data)
        .success(function(data, status){
            deferred.resolve(data);
        })
        .error(function(error, status){
            deferred.reject(error);
        })
        return deferred.promise;
    }
    var create = function(data){
        var deferred = $q.defer();
        $http.post(config.baseURL + '/target', data)
        .success(function(data, status){
            deferred.resolve(data);
        })
        .error(function(error, status){
            deferred.reject(error);
        })
        return deferred.promise;
    }
    return {
        list: list,
        remove: remove,
        update: update,
        create: create
    }
});
