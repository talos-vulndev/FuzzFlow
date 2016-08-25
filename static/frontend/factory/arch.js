'use strict';

angular.module('frontApp')
    .factory('ArchAPI',
function (config, $http, $q) {
    var list = function(){
        var deferred = $q.defer();
        $http.get(config.baseURL + '/arch')
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
        $http.get(config.baseURL + '/arch/' + id + '?delete=1')
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
        $http.post(config.baseURL + '/arch/' + id, data)
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
        $http.post(config.baseURL + '/arch', data)
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
