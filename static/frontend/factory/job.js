'use strict';

angular.module('frontApp')
    .factory('JobAPI',
function (config, $http, $q) {
    var list = function(){
        var deferred = $q.defer();
        $http.get(config.baseURL + '/job')
        .success(function(data, status){
            deferred.resolve(data);
        })
        .error(function(error, status){
            deferred.reject(error);
        })
        return deferred.promise;
    }
    var state = function(){
        var deferred = $q.defer();
        $http.get(config.baseURL + '/job?state=1')
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
        $http.get(config.baseURL + '/job/' + id + '?delete=1')
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
        $http.post(config.baseURL + '/job/' + id, data)
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
        $http.post(config.baseURL + '/job', data)
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
        state: state,
        remove: remove,
        update: update,
        create: create
    }
});
