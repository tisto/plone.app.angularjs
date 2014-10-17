var ploneModule;

angular.module('e2e-mocks', ['ngMockE2E']).run(function($httpBackend) {

  var site_structure = [
    {
      id: 'front-page',
      title: 'Welcome to Plone',
      description: 'Congratulations! You have successfully installed Plone.',
      text: '<p>Front-page content</p>',
      path: 'front-page',
      portal_type: 'document',
      children: []
    },
    {
      id: 'news',
      title: 'News',
      description: 'Site News',
      text: '<p>Site news content</p>',
      path: 'news',
      portal_type: 'folder',
      children: []
    },
    {
      id: 'events',
      title: 'Events',
      description: 'Site Events',
      text: '<p>Site events content</p>',
      path: 'events',
      portal_type: 'folder',
      children: []
    },
    {
      id: 'Members',
      title: 'Members',
      description: 'Site Members',
      text: '<p>Site Members content</p>',
      path: 'Members',
      portal_type: 'folder',
      children: []
    }
  ];


  // -- TOP NAVIGATION -------------------------------------------------------
  var top_navigation = [
    {
      id: 'news',
      title: 'News',
      description: 'News',
      path: '/news'
    },
    {
      id: 'events',
      title: 'Events',
      description: 'Events',
      path: '/events'
    }
  ];
  var re = new RegExp('\\+\\+api\\+\\+v1/top_navigation');
  $httpBackend.whenGET(re).respond(top_navigation);


  // --- PORTLET NAVIGATION --------------------------------------------------
  var portlet_navigation_re = new RegExp('\\+\\+api\\+\\+v1/portlet_navigation');
  $httpBackend.whenGET(portlet_navigation_re).respond(site_structure);


  // --- TRAVERSAL -----------------------------------------------------------
  angular.forEach(site_structure, function(value, key) {
    var traversal = {
      'route': value.path,
      'id': value.id,
      'title': value.title,
      'description': value.description,
      'text': '<p>Lorem Ipsum</p>'
    };
    var traversal_re = new RegExp('\\+\\+api\\+\\+v1/traversal\\?path=' + value.path);
    $httpBackend.whenGET(traversal_re).respond(traversal);

  });


  // --- PASS THROUGH TEMPLATES ----------------------------------------------
  var templates_re = new RegExp('.*.tpl.html$');
  $httpBackend.whenGET(templates_re).passThrough();

});

ploneModule.requires.push('e2e-mocks');

