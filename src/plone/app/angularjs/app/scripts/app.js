var ploneModule = angular.module(
  'ploneApp',
  [
    'chieffancypants.loadingBar',
    'ngAnimate',
    'ngRoute',
    'ngSanitize',
    'ui.bootstrap',
  ]
);

ploneModule.config(['$routeProvider', '$locationProvider',
  function($routeProvider, $locationProvider) {
    'use strict';
    $locationProvider.html5Mode(true);
    $locationProvider.hashPrefix('!');
    $routeProvider.when('/:objecttraversal*', {
      controller: 'ObjectPathController',
      templateUrl: 'page.html'
    }).otherwise({
      redirectTo: 'front-page'
    });
  }
]);

ploneModule.controller('ObjectPathController',
  ['$scope', '$routeParams', '$http', '$sce',
    function($scope, $routeParams, $http, $sce) {
      'use strict';
      //if ($routeParams.objecttraversal.match('/edit$')) {
      //}
      $http({
        url: '@@angularjs-object-traversal',
        method: 'GET',
        params: {'object-traversal-path': $routeParams.objecttraversal.replace('index.html/', '')},
      }).success(function(data) {
        $scope.page = data;
        $scope.deliberatelyTrustDangerousSnippet = function() {
          return $sce.trustAsHtml($scope.snippet);
        };
      });
    }
  ]
);
