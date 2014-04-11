var ploneModule;

ploneModule.controller('NavigationController',
  function($scope, $http) {
    'use strict';
    var url = '@@angularjs-top-navigation';
    $http.get(url).success(function(data) {
      $scope.items = data;
    });
  }
);

ploneModule.directive('navigationDirective',
  function() {
    'use strict';
    return {
      templateUrl: 'navigation.tpl.html',
      controller: 'NavigationController'
    };
  }
);

ploneModule.controller('NavigationPortletController',
  function($scope, $http) {
    'use strict';
    var url = '@@angularjs-portlet-navigation';
    $http.get(url).success(function(data) {
      $scope.items = data;
    });
  }
);

ploneModule.directive('navigationPortletDirective',
  function() {
    'use strict';
    return {
      templateUrl: 'navigation-portlet.tpl.html',
      controller: 'NavigationPortletController'
    };
  }
);
