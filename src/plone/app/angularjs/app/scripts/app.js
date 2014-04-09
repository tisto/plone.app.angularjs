var ploneModule = angular.module('ploneApp', ['ngRoute', 'ngSanitize']);

ploneModule.config(['$routeProvider',
  function($routeProvider) {
    'use strict';
    $routeProvider
    .when('/:objecttraversal*', {
        controller: 'ObjectPathController',
        templateUrl: 'page.html'
      }
    ).otherwise({
      redirectTo: '/'
    });
  }
]);

ploneModule.controller('ObjectPathController',
  ['$scope', '$routeParams', '$http', '$sce',
    function($scope, $routeParams, $http, $sce) {
      'use strict';
      $http({
        url: '@@angularjs-object-traversal',
        method: 'GET',
        params: {'object-traversal-path': $routeParams.objecttraversal},
      }).success(function(data, status, headers, config) {
        $scope.page = data;
        $scope.deliberatelyTrustDangerousSnippet = function() {
          return $sce.trustAsHtml($scope.snippet);
        };
      });
    }
  ]
);
