var ploneModule;

ploneModule.factory('reportTreeService', function($q, $http) {

  var getTreeData = function() {
    var deferred = $q.defer();
    $http.get("++api++v1/navigation_tree").then(function (response) {
      deferred.resolve(response.data);
    });
    return deferred.promise;
  };

  return {
      getTreeData: getTreeData
  };

});


ploneModule.controller('NavigationPortletController',
  function($scope, reportTreeService) {
    'use strict';
    $scope.folders = [];

    reportTreeService.getTreeData().then(function(data) {
      $scope.folders = data;

      $scope.my_tree_handler = function(branch) {
        $scope.output = "You selected: " + branch.label;
        if (branch.label == 'Nachrichten') {
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
      };
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
