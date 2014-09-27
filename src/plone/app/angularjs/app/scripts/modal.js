var ploneModule;

ploneModule.controller('ModalInstanceCtrl', ['$scope', '$modalInstance', 'items',
  function ($scope, $modalInstance, items) {
    'use strict';
    $scope.items = items;
    $scope.selected = {
      item: $scope.items[0]
    };

    $scope.ok = function () {
      $modalInstance.close($scope.selected);
    };

    $scope.cancel = function () {
      $modalInstance.dismiss('cancel');
    };
  }
]);


ploneModule.controller('ModalDemoCtrl', ['$scope', '$modal', '$log',
  function ($scope, $modal, $log) {
    'use strict';
    $scope.items = ['item1', 'item2', 'item3'];

    $scope.open = function () {

      var modalInstance = $modal.open({
        templateUrl: 'edit.tpl.html',
        controller: 'ModalInstanceCtrl',
        resolve: {
          items: function () {
            return $scope.items;
          }
        }
      });

      modalInstance.result.then(function (selected) {
        $scope.selected = selected;
      }, function () {
        $log.info('Modal dismissed at: ' + new Date());
      });
    };
  }
]);
