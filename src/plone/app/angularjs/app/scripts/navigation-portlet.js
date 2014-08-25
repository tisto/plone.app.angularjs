var ploneModule;

/*
ploneModule.controller('NavigationPortletController',
  function($scope, $http) {
    'use strict';
    var url = '++api++v1/navigation_tree';
    $http.get(url).success(function(data) {
      $scope.items = data;
    });
  }
);*/

ploneModule.directive('navigationPortletDirective',
  function() {
    'use strict';
    return {
      templateUrl: 'navigation-portlet.tpl.html',
      controller: 'NavigationPortletController'
    };
  }
);

ploneModule.controller('NavigationPortletController', function($scope, $timeout) {

  $scope.my_data = [
    {
      label: 'North America',
      children: []
    }, {
      label: 'South America',
      children: []
    }
  ];

  $scope.my_tree_handler = function(branch) {
    var _ref;
    $scope.output = "You selected: " + branch.label;
    if (branch.label == 'North America') {
      branch.children = [
        {
          label: 'Canada',
          children: ['Toronto', 'Vancouver']
        }, {
          label: 'USA',
          children: ['New York', 'Los Angeles']
        }, {
          label: 'Mexico',
          children: ['Mexico City', 'Guadalajara']
        }
      ];
    }
    if (branch.label == 'South America') {
      branch.children = [
        {
          label: 'Venezuela',
          children: ['Caracas', 'Maracaibo']
        }, {
          label: 'Brazil',
          children: ['Sao Paulo', 'Rio de Janeiro']
        }, {
          label: 'Argentina',
          children: ['Buenos Aires', 'Cordoba']
        }
      ];
    }
    if ((_ref = branch.data) !== null ? _ref.description : void 0) {
      return $scope.output += '(' + branch.data.description + ')';
    }
  };
});

