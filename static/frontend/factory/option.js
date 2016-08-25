'use strict';

angular.module('frontApp')
    .factory('OptionAPI',
function (config, $http, $q) {
    var list = function(){
        var deferred = $q.defer();
        $http.get(config.baseURL + '/option')
        .success(function(data, status){
            deferred.resolve(data);
        })
        .error(function(error, status){
            deferred.reject(error);
        })
        return deferred.promise;
    }
    var type = function(){
        var deferred = $q.defer();
        $http.get(config.baseURL + '/option?type=1')
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
        $http.get(config.baseURL + '/option/' + id + '?delete=1')
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
        $http.post(config.baseURL + '/option/' + id, data)
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
        $http.post(config.baseURL + '/option', data)
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
        type: type,
        remove: remove,
        update: update,
        create: create
    }
});
