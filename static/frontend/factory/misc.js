'use strict';

angular.module('frontApp')
    .factory('MiscAPI',
function (config, $http, $q) {
    var upload = function(file, template){
        var deferred = $q.defer();
        var fd = new FormData();
        fd.append('file', file);
        $http.post(config.baseURL + '/upload', fd,
        {
            transformRequest: angular.identity,
            headers: {'Content-Type': undefined}
        })
        .success(function(data){
            if(angular.isDefined(template)){
                for(var k in template){
                    if(template[k] === '<upload_path>')
                        template[k] = data.upload_path
                }
                deferred.resolve(template);
            }
            else{
                deferred.resolve(data);
            }

        })
        .error(function(error){
            deferred.reject(error);
        });
        return deferred.promise;
    };
    var download = function(url){
        var deferred = $q.defer();
        console.log(url);
        $http({
            url: url,
            method: 'GET',
            transformResponse: [function (data) {
                return data;
            }]
        })
        .success(function(data){
            deferred.resolve(data);
        })
        .error(function(error){
            deferred.reject(error);
        });
        return deferred.promise;
    }
    var log= function(){
        var deferred = $q.defer();
        $http.get(config.baseURL + '/log')
        .success(function(data, status){
            deferred.resolve(data);
        })
        .error(function(error, status){
            deferred.reject(error);
        })
        return deferred.promise;
    }

    return {
        upload: upload,
        download: download,
        log: log
    }
});
