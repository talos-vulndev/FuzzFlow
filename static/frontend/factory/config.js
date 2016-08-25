'use strict';

angular.module('frontApp')
    .factory('ConfigAPI',
function (config, $http, $q) {
    var create = function(data){
        var deferred = $q.defer();
        $http.post(config.baseURL + '/config', data)
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
        $http.post(config.baseURL + '/config/' + id, data)
        .success(function(data, status){
            deferred.resolve(data);
        })
        .error(function(error, status){
            deferred.reject(error);
        })
        return deferred.promise;
    }
    var list = function(){
        var deferred = $q.defer();
        $http.get(config.baseURL + '/config')
        .success(function(data, status){
            deferred.resolve(data);
        })
        .error(function(error, status){
            deferred.reject(error);
        })
        return deferred.promise;
    }
    var read = function(id){
        var deferred = $q.defer();
        $http.get(config.baseURL + '/config/' + id)
        .success(function(data, status){
            deferred.resolve(data);
        })
        .error(function(error, status){
            deferred.reject(error);
        })
        return deferred.promise;
    }
    var read_by_host_id = function(id){
        var deferred = $q.defer();
        $http.get(config.baseURL + '/config/' + id + '?host=1')
        .success(function(data, status){
            deferred.resolve(data, status);
        })
        .error(function(error, status){
            deferred.reject(error, status);
        })
        return deferred.promise;
    }
    return {
        create: create,
        update: update,
        list: list,
        read: read,
        read_by_host_id: read_by_host_id
    }
});
