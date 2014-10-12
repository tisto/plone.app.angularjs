var ploneModule;

ploneModule.run(function($httpBackend) {


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
  var portlet_navigation = [
    {
      "path": "front-page",
      "description": "",
      "children": [],
      "id": "front-page",
      "title": "Willkommen bei Plone"
    },
    {
      "path": "news",
      "description": "",
      "children": [],
      "id": "news",
      "title": "Nachrichten"
    },
    {
      "path": "events",
      "description": "",
      "children": [],
      "id": "events",
      "title": "Termine"
    },
    {
      "path": "Members",
      "description": "",
      "children": [],
      "id": "Members",
      "title": "Benutzer"
    }
  ];
  var re = new RegExp('\\+\\+api\\+\\+v1/portlet_navigation\\?path=.*');
  $httpBackend.whenGET(re).respond(portlet_navigation);


  // --- TRAVERSAL -----------------------------------------------------------
  var traversal = {
    'route': '/Plone/front-page',
    'id': 'front-page',
    'title': 'Startseite',
    'description': 'Congrats you installed Plone',
    'text': '<p>Lorem Ipsum</p>'
  };
  var re = new RegExp('\\+\\+api\\+\\+v1/traversal\\?path=.*');
  $httpBackend.whenGET(re).respond(traversal);

  // PASS THROUGH TEMPLATES
  var re = new RegExp('.*.tpl.html$');
  $httpBackend.whenGET(re).passThrough();

});
