'use strict';

angular.module('frontApp')
    .controller('JobManagerCtrl',
function ($scope, $rootScope, JobAPI, TargetAPI, EngineAPI, OptionAPI, HostAPI, MiscAPI, $q, config, $interval) {

     $scope.shortenName = function(name){
        if(angular.isDefined(name)){
            if (name.length > 25){
                return name.substring(0, 22) + '...'
            }
            else{
                return name;
            };
        }
    }

    $scope.toggleJobModal = function(){

        $scope.newJob = {};
        $('#addJobModal').modal('show');

    }

    $scope.listJob = function(){
        JobAPI.list().then(function(data){
            console.log(data);
            $scope.jobs = data;
        })
    };

    $scope.getOptionType = function(opt){
        if(angular.isDefined($scope.option_types)){
            for(var i = 0; i < $scope.option_types.length; i++){
                if(opt.type_id === $scope.option_types[i].id){
                    return $scope.option_types[i].name;
                };
            };
        };
    };

    $scope.getOptionById = function(id){
        if(angular.isDefined($scope.options)){
            for(var i = 0; i < $scope.options.length; i++){
                if($scope.options[i].id === id){
                    return $scope.options[i];
                }
            }
        }
    }

    $scope.listOption = function(){
        OptionAPI.list().then(function(data){
            $scope.options = data;
            OptionAPI.type().then(function(data){
                $scope.option_types = data;
                $scope.options.forEach(function(option){
                    for(var i = 0; i < $scope.option_types.length; i++){
                        if(option.type_id === $scope.option_types[i].id){
                            option.type = $scope.option_types[i];
                            break;
                        };
                    };
                });
            });
        });
    };

    $scope.get_state_id_by_name = function(name){
        for(var i = 0 ; i < $scope.states.length; i++){
            if($scope.states[i].name === name)
                return $scope.states[i].id;
        }
        return -1;
    }

    $scope.createJob = function(job){
        if(angular.isDefined(job.nodeCount)
        && angular.isDefined(job.target)
        && angular.isDefined(job.name)
        && angular.isDefined(job.engine)){

            var state_id = $scope.get_state_id_by_name('Queued');
            var promises = [];
            var options = [];
            job.engine.options.forEach(function(opt){
                switch($scope.getOptionType(opt)){
                    case 'FIELD':
                        var val = angular.isDefined(opt.value)? opt.value.toString() : '';
                        promises.push({
                            id: opt.id,
                            value: val
                        });
                        break;
                    case 'CHECKBOX':
                        var val = angular.isDefined(opt.value)? opt.value.toString() : 'false';
                        promises.push({
                            id: opt.id,
                            value: val
                        });
                        break;
                    case 'LIST':
                        var lst = [];
                        if(angular.isDefined(opt.list)){
                            opt.list.forEach(function(tag){
                                lst.push(tag.text);
                            })
                        }
                        promises.push({
                            id: opt.id,
                            value: lst.toString()
                        });
                        break;
                    case 'FILE':
                        if(angular.isDefined(opt.value)){
                            promises.push(MiscAPI.upload(opt.value, {
                                id: opt.id,
                                value: '<upload_path>'
                            }))
                        }
                        else{
                            promises.push({
                                id: opt.id,
                                value: ''
                            });
                        }
                        break;
                }
            })
            $q.all(promises).then(function(result){
                options = result

                if(state_id === -1){
                    $.notify("invalid input.", "error");
                    return;
                }

                promises = [];
                for(var i = 0; i< job.nodeCount; i++){
                    promises.push(JobAPI.create({
                        name: job.name + '_' + (i+1),
                        target_id: job.target.id,
                        engine_id: job.engine.id,
                        state_id: state_id,
                        options: options
                    }));
                }

                $q.all(promises).then(function(){
                    $scope.listJob();
                    $('#addJobModal').modal('hide');
                }, function(){
                    $.notify("invalid input.", "error");
                    $('#addJobModal').modal('hide');
                });
            }, function(){
                $.notify("invalid input.", "error");
                $('#addJobModal').modal('hide');
            })
        }
        else{
            $.notify("invalid input.", "error");
        };
    }

    $scope.getTargetName = function(job){
        for(var i = 0; i < $scope.targets.length; i++){
            if($scope.targets[i].id === job.target_id){
                return $scope.targets[i].name;
            }
        }

    }

    $scope.getHostName = function(job){
        for(var i = 0; i < $scope.hosts.length; i++){
            if($scope.hosts[i].id === job.host_id){
                return $scope.hosts[i].name + '(id=' + $scope.hosts[i].id + ')';
            }
        }
        return "<Unassigned>"
    }

    $scope.getEngineName = function(job){
        for(var i = 0; i < $scope.engines.length; i++){
            if($scope.engines[i].id === job.engine_id){
                return $scope.engines[i].name;
            }
        }
    }

    $scope.getStateName = function(job){
        for(var i = 0; i < $scope.states.length; i++){
            if($scope.states[i].id === job.state_id){
                return $scope.states[i].name;
            }
        }
    }

    $scope.formatDateTime = function(timeString){
        return moment(timeString).format('YYYY-MM-DD h:mm:ss A');
    };

    $scope.initJobs = function(){
        if(angular.isUndefined($scope.options)){
            $scope.listOption();
        }
        HostAPI.list().then(function(data){
            $scope.hosts = data.hosts;
            JobAPI.state().then(function(data){
                $scope.states = data;
                EngineAPI.list().then(function(data){
                    $scope.engines = data;
                    TargetAPI.list().then(function(data){
                        $scope.targets= data;
                        $scope.listJob();
                    });
                });
            })
        })


        $scope.nodeCountRange = [];
        for(var i = 1 ; i <= 100; i++){
            $scope.nodeCountRange.push(i);
        }
    }

    $scope.toggleShowJobOutputModal = function(job){
        $scope.selectedJob = job;
        $('#jobOutputModal').modal('show');
    }

    $scope.formatJobOutput = function(output){
        if (angular.isDefined(output) && output.length > 0 && output !== 'None'){
            return atob(output)
        }
        return "<No Output>"
    }

    $scope.repeatJob = function(job){
        var state_id = $scope.get_state_id_by_name('Queued');
        JobAPI.update(job.id, {
            state_id : state_id
        }).then(function(){
            $scope.listJob();
        })
    }

    $scope.removeJob = function(job){
        JobAPI.remove(job.id).then(function(){
            $scope.listJob();
        })
    }

    $scope.initJobs();
    $rootScope.jobManagerTimer = $interval($scope.initJobs, config.refreshTime);
});
