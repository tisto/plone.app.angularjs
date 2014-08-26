var ploneModule;

ploneModule.factory('reportTreeService', function($q, $http) {

  var getTreeData = function(path) {
    if (path == '/front-page') {
      path = null;
    }
    var deferred = $q.defer();
    $http({
      method: 'GET',
      url: '++api++v1/navigation_tree',
      params: {
        path: path
      }
    }).then(function (response) {
      deferred.resolve(response.data);
    });
    return deferred.promise;
  };

  return {
      getTreeData: getTreeData
  };

});


ploneModule.controller('NavigationPortletController',
  function($scope, $location, reportTreeService) {
    'use strict';
    //$scope.location = $location;
    $scope.folders = [];
    var path = $scope.location.path();
    reportTreeService.getTreeData(path).then(function(data) {
      $scope.folders = data;
      $scope.my_tree_handler = function(branch) {
        //console.log(branch.expanded);
        branch.expanded = true;
        $location.path(branch.url);
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
