var ploneModule = angular.module(
  'ploneApp', ['ngRoute', 'ngSanitize', 'ngAnimate', 'ui.bootstrap']
);

ploneModule.config(['$routeProvider',
  function($routeProvider) {
    'use strict';
    $routeProvider.when('/:objecttraversal*', {
      controller: 'ObjectPathController',
      templateUrl: 'page.html'
    }).otherwise({
      redirectTo: '/front-page'
    });
  }
]);

ploneModule.controller('ObjectPathController',
  ['$scope', '$routeParams', '$http', '$sce',
    function($scope, $routeParams, $http, $sce) {
      'use strict';
      if ($routeParams.objecttraversal.match('/edit$')) {
        alert("edit");
      }
      $http({
        url: '@@angularjs-object-traversal',
        method: 'GET',
        params: {'object-traversal-path': $routeParams.objecttraversal},
      }).success(function(data) {
        $scope.page = data;
        $scope.deliberatelyTrustDangerousSnippet = function() {
          return $sce.trustAsHtml($scope.snippet);
        };
      });
    }
  ]
);
