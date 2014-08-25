var ploneModule;

ploneModule.factory('reportTreeService', function($q, $http) {

  var getTreeData = function(path) {
    console.log('getTreeData(' + path + ')');
    var deferred = $q.defer();
    $http({
      method: 'GET',
      url: '++api++v1/folder_children',
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
    $scope.location = $location;
    $scope.folders = [];
    var path = $scope.location.path();
    console.log("PATH: " + path);
    reportTreeService.getTreeData(path).then(function(data) {
      $scope.folders = data;

      $scope.my_tree_handler = function(branch) {
        console.log('my_tree_handler(' + branch + ')');
        $scope.output = "You selected: " + branch.label;
        if (branch.label == 'Nachrichten') {
          reportTreeService.getTreeData('/news').then(function(data) {
            branch.children = data;
          });
        }
        if (branch.label == 'Termine') {
          reportTreeService.getTreeData('/events').then(function(data) {
            branch.children = data;
          });
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
