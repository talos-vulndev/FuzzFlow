'use strict';

angular.module('frontApp')
    .controller('ConfigManagerCtrl',
function ($scope, ArchAPI, PlatformAPI, EngineAPI, TargetAPI, ScriptAPI, OptionAPI) {

    /**
    *   Architecture Configuration
    */
    $scope.listArch = function(){
        ArchAPI.list().then(function(data){
            $scope.arches = data;
        });
    };
    $scope.toggleArchConfig = function(arch){
        arch.configMode = !arch.configMode;
    };
    $scope.removeArch = function(arch){
        ArchAPI.remove(arch.id).then(function(){
            $scope.listArch();
        });
    };
    $scope.updateArch = function(arch){
        ArchAPI.update(arch.id, arch).then(function(){
            $scope.listArch();
            $scope.newArchName = null;
        }, function(){
            $.notify("invalid name.", "error");
        });
    };
    $scope.createArch = function(name){
        ArchAPI.create({
            name: name
        }).then(function(){
            $scope.listArch();
            $scope.newArchName = null;
        }, function(){
            $.notify("invalid input.", "error");
        });
    };

    /**
    *   Platform Configuration
    */
    $scope.listPlatform = function(){
        PlatformAPI.list().then(function(data){
            $scope.platforms = data;
        });
    }
    $scope.togglePlatformConfig = function(plat){
        plat.configMode = !plat.configMode;
    };
    $scope.removePlatform = function(plat){
        PlatformAPI.remove(plat.id).then(function(){
            $scope.listPlatform();
        });
    };
    $scope.updatePlatform = function(plat){
        PlatformAPI.update(plat.id, plat).then(function(){
            $scope.listPlatform();
            $scope.newPlatformName = null;
        }, function(){
            $.notify("invalid input.", "error");
        });
    };
    $scope.createPlatform = function(name){
        PlatformAPI.create({
            name: name
        }).then(function(){
            $scope.listPlatform();
            $scope.newPlatformName = null;
        }, function(){
            $.notify("invalid input.", "error");
        });
    };

    /**
    *   Engine Configuration
    */
    $scope.getEnginePlatform = function(engine){
        for(var i = 0; i < $scope.platforms.length; i++){
            if(engine.platform_id === $scope.platforms[i].id){
                return $scope.platforms[i].name;
            };
        };
    };
    $scope.getEngineArch = function(engine){
        for(var i = 0; i < $scope.arches.length; i++){
            if(engine.arch_id === $scope.arches[i].id){
                return $scope.arches[i].name;
            };
        };
    };
    $scope.listEngine = function(){
        EngineAPI.list().then(function(data){
            $scope.engines = data;
            $scope.engines.forEach(function(engine){
                for(var i = 0; i < $scope.platforms.length; i++){
                    if(engine.platform_id === $scope.platforms[i].id){
                        engine.platform = $scope.platforms[i];
                        break;
                    };
                };
                for(var i = 0; i < $scope.arches.length; i++){
                    if(engine.arch_id === $scope.arches[i].id){
                        engine.arch = $scope.arches[i];
                        break;
                    };
                };
                engine.option_tags = [];
                engine.options.forEach(function(opt){
                    engine.option_tags.push({
                        text: opt.name,
                        option: opt
                    })
                })
            })
        });
    };
    $scope.toggleEngineConfig = function(engine){
        engine.configMode = !engine.configMode;
    };
    $scope.removeEngine = function(engine){
        EngineAPI.remove(engine.id).then(function(){
            $scope.listEngine();
        });
    };
    $scope.updateEngine = function(engine){
        var options = [];
        engine.option_tags.forEach(function(tag){
            options.push(tag.option.id);
        })
        EngineAPI.update(engine.id, {
            name: engine.name,
            path: engine.path,
            platform_id: engine.platform.id,
            arch_id: engine.arch.id,
            options: options
        }).then(function(){
            $scope.listEngine();
            $scope.newEngine= null;
        }, function(){
            $.notify("invalid input.", "error");
        });
    };
    $scope.createEngine = function(engine){
        var options = [];
        engine.option_tags.forEach(function(tag){
            options.push(tag.option.id);
        })
        console.log(options);
        if(angular.isDefined(engine) && angular.isDefined(engine.platform)){
            EngineAPI.create({
                name: engine.name,
                path: engine.path,
                platform_id: engine.platform.id,
                arch_id: engine.arch.id,
                options: options
            }).then(function(){
                $scope.listEngine();
                $scope.newEngine = null;
            }, function(){
                $.notify("invalid input.", "error");
            });
        }
        else{
            $.notify("invalid input.", "error");
        };
    };


    /**
    *   Target Configuration
    */
    $scope.getTargetPlatform = function(target){
        for(var i = 0; i < $scope.platforms.length; i++){
            if(target.platform_id === $scope.platforms[i].id){
                return $scope.platforms[i].name;
            };
        };
    };
    $scope.getTargetArch = function(target){
        for(var i = 0; i < $scope.arches.length; i++){
            if(target.arch_id === $scope.arches[i].id){
                return $scope.arches[i].name;
            };
        };
    };
    $scope.listTarget = function(){
        TargetAPI.list().then(function(data){
            $scope.targets = data;
            $scope.targets.forEach(function(target){
                for(var i = 0; i < $scope.platforms.length; i++){
                    if(target.platform_id === $scope.platforms[i].id){
                        target.platform = $scope.platforms[i];
                        break;
                    };
                };
                for(var i = 0; i < $scope.arches.length; i++){
                    if(target.arch_id === $scope.arches[i].id){
                        target.arch = $scope.arches[i];
                        break;
                    };
                };
            })

        });
    }
    $scope.toggleTargetConfig = function(target){
        target.configMode = !target.configMode;
    };
    $scope.removeTarget= function(target){
        TargetAPI.remove(target.id).then(function(){
            $scope.listTarget();
        });
    };
    $scope.updateTarget = function(target){
        TargetAPI.update(target.id, {
            name: target.name,
            path: target.path,
            arch_id: target.arch.id,
            platform_id: target.platform.id
        }).then(function(){
            $scope.listTarget();
        }, function(){
            $.notify("invalid input.", "error");
        });
    };
    $scope.createTarget = function(newTarget){
        if(angular.isDefined(newTarget)){
            TargetAPI.create({
                name: newTarget.name,
                path: newTarget.path,
                arch_id: newTarget.arch.id,
                platform_id: newTarget.platform.id,
            }).then(function(){
                $scope.listTarget();
                $scope.newTarget = null;
            }, function(){
                $.notify("invalid input.", "error");
            });
        }
        else{
            $.notify("invalid input.", "error");
        };

    };

    /**
    *   Script Configuration
    */
    $scope.listScript = function(){
        ScriptAPI.list().then(function(data){
            $scope.scripts = data;
        });
    };

    $scope.toggleScriptConfig = function(script){
        script.configMode = !script.configMode;
    };

    $scope.removeScript = function(script){
        ScriptAPI.remove(script.id).then(function(){
            $scope.listScript();
        });
    };

    $scope.updateScript = function(script){
        ScriptAPI.update(script.id, script).then(function(){
            $scope.listScript();
        }, function(){
            $.notify("invalid input.", "error");
        });
    };

    $scope.createScript = function(sc){
        ScriptAPI.create({
            name: sc.name,
            script: sc.script
        }).then(function(){
            $scope.listScript();
        }, function(){
            $.notify("invalid input.", "error");
        });
    };


    /**
    *   Option Configuration
    */
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

    $scope.getOptionType = function(opt){
        if(angular.isDefined($scope.option_types)){
            for(var i = 0; i < $scope.option_types.length; i++){
                if(opt.type_id === $scope.option_types[i].id){
                    return $scope.option_types[i].name;
                };
            };
        };
    };

    $scope.toggleOptionConfig = function(opt){
        opt.configMode = !opt.configMode;
    };

    $scope.removeOption = function(opt){
        OptionAPI.remove(opt.id).then(function(){
            $scope.listOption();
        });
    };

    $scope.updateOption = function(opt){
        OptionAPI.update(opt.id, {
            name: opt.name,
            option_type_id: opt.type.id
        }).then(function(){
            $scope.listOption();
        }, function(){
            $.notify("invalid input.", "error");
        });
    };

    $scope.createOption = function(opt){
        if(angular.isDefined(opt) && angular.isDefined(opt  .type)){
            OptionAPI.create({
                name: opt.name,
                option_type_id: opt.type.id
            }).then(function(){
                $scope.listOption();
            }, function(){
                $.notify("invalid input.", "error");
            });
        }
        else{
            $.notify("invalid input.", "error");
        };
    };

    $scope.queryOptionTags = function(q){
        var result = [];
        $scope.options.forEach(function(opt){
            if(opt.name.startsWith(q)){
                result.push(
                    {
                        text: opt.name,
                        option: opt,
                    }
                );
            }
        });
        return result;
    };

    $scope.activateTab = function(tabid){
        $('.tabs-left > li').removeClass('active');
        $(tabid + 'Nav').addClass('active');
        $('.tab-pane').removeClass('active');
        $(tabid + 'Tab').addClass('active');
        $scope.initNodes();
    }


    $scope.initNodes = function() {
            $scope.listArch();
            $scope.listPlatform();
            $scope.listEngine();
            $scope.listTarget();
            $scope.listScript();
            $scope.listOption();
    };

    $scope.initNodes();
});
