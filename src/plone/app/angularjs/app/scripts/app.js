var ploneModule = angular.module(
  'ploneApp',
  [
    'ngAnimate',
    'ngRoute',
    'ngSanitize',
    'ui.bootstrap'
  ]
);

// Route Configuration
ploneModule.config(['$routeProvider', '$locationProvider',
  function($routeProvider, $locationProvider) {
    'use strict';
    $locationProvider.html5Mode(true);
    $locationProvider.hashPrefix('!');
    $routeProvider.when('/contact-info', {
      controller: 'ContactInfoFormController',
      templateUrl: '++theme++plone.app.angularjs/contact-info.tpl.html'
    }).when('/:objecttraversal*', {
      controller: 'ObjectPathController',
      templateUrl: '++theme++plone.app.angularjs/page.tpl.html'
    }).otherwise({
      redirectTo: 'front-page'
    });
  }
]);

ploneModule.controller('ObjectPathController',
  ['$scope', '$routeParams', '$http', '$sce',
    function($scope, $routeParams, $http, $sce) {
      'use strict';
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


ploneModule.controller('ContactInfoFormController',
  ['$scope',
    function($scope) {
      'use strict';
      $scope.form = {
        'fullname': '',
        'email': '',
        'text': ''
      };
      $scope.submit = function (isValid) {
        if(!isValid) return;

        console.log($scope.form);
        // clear form
        $scope.form = {
          'fullname': '',
          'email': '',
          'text': ''
        };
      };
    }
  ]
);
