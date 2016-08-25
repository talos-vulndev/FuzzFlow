'use strict';

angular.module('frontApp')
    .controller('NodeManagerCtrl',
function ($scope, $rootScope, ArchAPI, PlatformAPI, HostAPI, EngineAPI, TargetAPI, ConfigAPI, config, $interval) {
    $scope.listHost = function(){
        HostAPI.list().then(function(data){
            $scope.result = data;
            $scope.nodes = $scope.result.hosts;
        })
    }
    $scope.initNodes = function() {
        if(angular.isUndefined($scope.arches)){
            ArchAPI.list().then(function(data){
                $scope.arches = data;
                if(angular.isUndefined($scope.platforms)){
                    PlatformAPI.list().then(function(data){
                        $scope.platforms = data;
                        $scope.listHost();
                    });
                };
            });
        }
        else{
            $scope.listHost();
        };

//        if(angular.isUndefined($scope.engines)){
//            EngineAPI.list().then(function(data){
//                $scope.engines = data;
//
//            });
//        };
//        if(angular.isUndefined($scope.targets)){
//            TargetAPI.list().then(function(data){
//                $scope.targets = data;
//            });
//        };
    };
    $scope.formatDateTime = function(timeString){
        return moment(timeString).format('YYYY-MM-DD h:mm:ss A');
    };
    $scope.getPlatformName = function(node){
        for(var i = 0; i < $scope.platforms.length; i++){
            if($scope.platforms[i].id === node.platform_id){
                return $scope.platforms[i].name;
            }
        }
    };
    $scope.getArchName = function(node){
        for(var i = 0; i < $scope.arches.length; i++){
            if($scope.arches[i].id === node.arch_id){
                return $scope.arches[i].name;
            }
        }
    };
    $scope.uptime= function(node){
        if(angular.isDefined($scope.result)){
            var serverMoment = moment($scope.result.serverTime)
            var updateMoment = moment(node.updated_at)
            var duration = moment.duration(serverMoment.diff(updateMoment));
            return duration.format("HH:mm")
        }
    }
//    $scope.setSelectedNode = function(node){
//        $scope.selectedNode = node;
//        ConfigAPI.read_by_host_id($scope.selectedNode.id)
//        .then(
//            function(data){
//                $scope.selectedNode.config = data;
//                for(var i = 0; i < $scope.platforms.length; i++){
//                    if($scope.platforms[i].id == data.platform_id){
//                        $scope.selectedNode.platform = $scope.platforms[i];
//                        break;
//                    };
//                };
//                for(var i = 0; i < $scope.arches.length; i++){
//                    if($scope.arches[i].id == data.arch_id){
//                        $scope.selectedNode.arch = $scope.arches[i];
//                        break;
//                    };
//                };
//                $scope.selectedNode.engine_tags = [];
//                $scope.selectedNode.config.engines.forEach(function(engine){
//                    $scope.selectedNode.engine_tags.push({
//                        text: engine.name,
//                        engine: engine,
//                    });
//                });
//                $scope.selectedNode.target_tags = [];
//                $scope.selectedNode.config.targets.forEach(function(target){
//                    $scope.selectedNode.target_tags.push({
//                        text: target.name,
//                        target: target,
//                    });
//                });
//                $('#nodeConfigModal').modal('show');
//            },
//            function(err){
//                $scope.selectedNode.engine_tags = [];
//                $scope.selectedNode.target_tags = [];
//                $('#nodeConfigModal').modal('show');
//            }
//        );
//    }
//
//    $scope.shortenName = function(name){
//        if(angular.isDefined(name)){
//            if (name.length > 25){
//                return name.substring(0, 22) + '...'
//            }
//            else{
//                return name;
//            };
//        }
//    }
//    $scope.saveNodeConfig = function(){
//        var node = $scope.selectedNode;
//        var engines = [];
//        for(var i = 0; i < node.engine_tags.length; i++){
//            engines.push(node.engine_tags[i].engine.id);
//        };
//        var targets = [];
//        for(var i = 0; i < node.target_tags.length; i++){
//            targets.push(node.target_tags[i].target.id);
//        };
//
//        ConfigAPI.update($scope.selectedNode.config.id, {
//            host_id: node.id,
//            platform_id: node.platform.id,
//            arch_id: node.arch.id,
//            engines: engines,
//            targets: targets
//        }).then(function(data){
//            $.notify("Config updated successfully.", "success");
//            $('#nodeConfigModal').modal('hide');
//        }, function(fail){
//            $.notify("Config failed.", "error");
//        });
//    }
//
//    $scope.addNodeConfig = function(){
//        var node = $scope.selectedNode;
//        var engines = [];
//        for(var i = 0; i < node.engine_tags.length; i++){
//            engines.push(node.engine_tags[i].engine.id);
//        };
//        var targets = [];
//        for(var i = 0; i < node.target_tags.length; i++){
//            targets.push(node.target_tags[i].target.id);
//        };
//
//        ConfigAPI.create({
//            host_id: node.id,
//            platform_id: node.platform.id,
//            arch_id: node.arch.id,
//            engines: engines,
//            targets: targets
//        }).then(function(data){
//            $.notify("Config added successfully.", "success");
//            $('#nodeConfigModal').modal('hide');
//        }, function(fail){
//            $.notify("Config failed.", "error");
//        });
//    }
//
//    $scope.queryEngineTags = function(q){
//        var result = [];
//        $scope.engines.forEach(function(engine){
//            if(engine.name.startsWith(q)){
//                result.push(
//                    {
//                        text: engine.name,
//                        engine: engine,
//                    }
//                );
//            }
//        });
//        return result;
//    };
//    $scope.queryTargetTags = function(q){
//        var result = [];
//        $scope.targets.forEach(function(target){
//            if(target.name.startsWith(q)){
//                result.push(
//                    {
//                        text: target.name,
//                        target: target,
//                    }
//                );
//            }
//        });
//        return result;
//    };

    $scope.initNodes();
    $rootScope.nodeManagerTimer = $interval($scope.initNodes, config.refreshTime);
});
