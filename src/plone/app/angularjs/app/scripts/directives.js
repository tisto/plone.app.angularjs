'use strict';
var ploneModule;

ploneModule.controller('NavigationController',
  function($scope) {
    $scope.items = [
      {
        id: 'front-page',
        title: 'Front page',
        url: '#/front-page'
      },
      {
        id: 'news',
        title: 'News',
        url: '#/news'
      },
      {
        id: 'events',
        title: 'Events',
        url: '#/events'
      },
      {
        id: 'doc1',
        title: 'Document 1',
        url: '#/folder1/doc1'
      }
    ]
  }
);

ploneModule.directive('navigationDirective',
  function() {
    return {
      templateUrl: 'navigation.tpl.html',
      controller: 'NavigationController'
    };
  }
);

