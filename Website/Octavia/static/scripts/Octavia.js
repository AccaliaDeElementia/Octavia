(function($win, $) {
    var baseUrl="http://localhost:5000",
    origOctavia = $win.Octavia,
    norm = function(element){
        elem = $(element);
        if (elem.length > 0){
            return elem;
        }
        return $("body");
    },
    subscribe = function(that, func, name){
        if (typeof func === 'function'){
            $("body").bind(name, func);
        }
        return that;
    },
    runcomplete =function(that, element, name, request, extraData){
        var elem = norm(element);
        request.complete(function(request){
            var data = JSON.parse(request.responseText);
            elem.trigger(name, [data, extraData]);
        });
        return that;
    },
    Octavia = {
        "playback": {
            "subscribe": function(func){
                return subscribe(this, func, 'playback_status');
            },
            "update": function(element) {
                return runcomplete(this, element, 'playback_status', $.get(baseUrl + '/playback'));
            },
            "play": function(element) {
                return runcomplete(this, element, 'playback_status',
                    $.post(baseUrl+'/playback',
                        JSON.stringify({playback:'play'})
                    ));
            },
            "pause": function(element) {
                return runcomplete(this, element, 'playback_status',
                    $.post(baseUrl+'/playback',
                        JSON.stringify({playback:'pause'})
                    ));
            },
            "stop": function(element) {
                return runcomplete(this, element, 'playback_status',
                    $.post(baseUrl+'/playback',
                        JSON.stringify({playback:'stop'})
                    ));
            },
            "single": function(element, active) {
                return runcomplete(this, element, 'playback_status',
                    $.post(baseUrl+'/playback',
                        JSON.stringify({single: active})
                   ));
            },
            "shuffle": function(element, active) {
                return runcomplete(this, element, 'playback_status',
                    $.post(baseUrl+'/playback',
                        JSON.stringify({random: active})
                   ));
            },
            "repeat": function(element, active) {
                return runcomplete(this, element, 'playback_status',
                    $.post(baseUrl+'/playback',
                        JSON.stringify({repeat: active})
                   ));
            },
            "consume": function(element, active) {
                return runcomplete(this, element, 'playback_status',
                    $.post(baseUrl+'/playback',
                        JSON.stringify({consume: active})
                   ));
            }
        },
        "queue": {
            "status": {
                "subscribe": function(func){
                    return subscribe(this, func, 'queue_status');
                },
                "update": function(element) {
                    return runcomplete(this, element, 'queue_status',
                        $.get(baseUrl+'/queue/current')
                    );
                },
                "first": function(element) {
                    return runcomplete(this, element, 'queue_status',
                        $.post(baseUrl+'/queue/first')
                    );
                },
                "prev": function(element) {
                    return runcomplete(this, element, 'queue_status',
                        $.post(baseUrl+'/queue/prev')
                    );
                },
                "next": function(element) {
                    return runcomplete(this, element, 'queue_status',
                        $.post(baseUrl+'/queue/next')
                    );
                },
                "last": function(element) {
                    return runcomplete(this, element, 'queue_status',
                        $.post(baseUrl+'/queue/last')
                    );
                },
                "go": function(element, id) {
                    return runcomplete(this, element, 'queue_status',
                        $.post(baseUrl+'/queue/go/'+id)
                    );
                }
            },
            "list": {
                "subscribe": function(func){
                    return subscribe(this, func, 'queue_list');
                },
                "update": function(element){
                    return runcomplete(this, element, 'queue_list',
                        $.get(baseUrl+'/queue/')
                    );
                },
                "remove": function(element, id) {
                    return runcomplete (this, element, 'queue_list',
                        $.post(baseUrl+'/queue/remove',JSON.stringify([{"id":id}]))
                    );
                },
                "add": function(element, path) {
                    return runcomplete (this, element, 'queue_list',
                        $.ajax({
                            "url": baseUrl+'/queue/add', 
                            "data": JSON.stringify([{'file':path}]),
                            "type": 'PUT'
                            })
                    );
                },
                "replace": function(element, path) {
                    return runcomplete (this, element, 'queue_list',
                        $.post(baseUrl+'/queue/add', JSON.stringify([{'file':path}]))
                    );
                }
            }
        },
        "library": {
            "subscribe": function (func){
                return subscribe(this, func, 'library_update');
            },
            "update": function(element, path){
                return runcomplete(this, element, 'library_update',
                    $.get(baseUrl+'/library/list/' + path),
                    path
                );
            }
        }
    };
    $win.Octavia = Octavia;
})(window,jQuery);