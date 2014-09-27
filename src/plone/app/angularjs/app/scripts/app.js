var ploneModule = angular.module(
  'ploneApp',
  [
    'ngAnimate',
    'ngRoute',
    'ngSanitize',
    'ui.bootstrap',
    'angularBootstrapNavTree',
    //'ngMockE2E'
  ]
);

// Route Configuration
ploneModule.config(['$routeProvider', '$locationProvider',
  function($routeProvider, $locationProvider) {
    'use strict';
    $locationProvider.html5Mode(true);
    $locationProvider.hashPrefix('!');
    $routeProvider.when('/:objecttraversal*', {
      controller: 'ObjectPathController',
      templateUrl: 'page.tpl.html'
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
        url: '++api++v1/traversal',
        method: 'GET',
        params: {'path': $routeParams.objecttraversal.replace('index.html/', '')},
      }).success(function(data) {
        $scope.page = data;
        $scope.deliberatelyTrustDangerousSnippet = function() {
          return $sce.trustAsHtml($scope.snippet);
        };
      });
    }
  ]
);
