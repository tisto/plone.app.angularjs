var ploneModule = angular.module('ploneApp', ['ngRoute']);

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

ploneModule.controller('ObjectPathController', ['$scope', '$routeParams',
  function($scope, $routeParams) {
    'use strict';
    $scope.page = {
      'route': $routeParams.objecttraversal,
      'id': 'doc1',
      'title': 'My first document',
      'text': 'This is my first document'
    };
  }
]);
