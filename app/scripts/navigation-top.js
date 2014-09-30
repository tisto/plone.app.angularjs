var ploneModule;

ploneModule.controller('NavigationController',
  function($scope, $http, $location) {
    'use strict';
    $scope.location = $location;
    var url = '++api++v1/top_navigation';
    $http.get(url).success(function(data) {
      $scope.items = data;
    });

    function setActiveNavigationItem() {
      $scope.activeSection = $location.path().slice(1).split('/')[0];
      $scope.activeItem = $location.path();
      $scope.path = $location.path().slice(1).split('/');
    }
    $scope.$watch('location.path()', setActiveNavigationItem);

  }
);

ploneModule.directive('navigationDirective',
  function() {
    'use strict';
    return {
      templateUrl: '++theme++plone.app.angularjs/navigation.tpl.html',
      controller: 'NavigationController'
    };
  }
);
