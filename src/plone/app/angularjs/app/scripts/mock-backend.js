var ploneModule;

angular.module('e2e-mocks', ['ngMockE2E']).run(function($httpBackend) {

  var loremipsum = '<p>Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat volutpat. Ut wisi enim ad minim veniam, quis nostrud exerci tation ullamcorper suscipit lobortis nisl ut aliquip ex ea commodo consequat. Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto odio dignissim qui blandit praesent luptatum zzril delenit augue duis dolore te feugait nulla facilisi. Nam liber tempor cum soluta nobis eleifend option congue nihil imperdiet doming id quod mazim placerat facer possim assum. Typi non habent claritatem insitam; est usus legentis in iis qui facit eorum claritatem. Investigationes demonstraverunt lectores legere me lius quod ii legunt saepius. Claritas est etiam processus dynamicus, qui sequitur mutationem consuetudium lectorum. Mirum est notare quam littera gothica, quam nunc putamus parum claram, anteposuerit litterarum formas humanitatis per seacula quarta decima et quinta decima. Eodem modo typi, qui nunc nobis videntur parum clari, fiant sollemnes in futurum.</p>';
  var site_structure = [
    {
      id: 'front-page',
      title: 'Welcome to Plone',
      description: 'Congratulations! You have successfully installed Plone.',
      text: '<h2>Front-page content</h2>' + loremipsum,
      path: 'front-page',
      portal_type: 'document',
      children: []
    },
    {
      id: 'news',
      title: 'News',
      description: 'Site News',
      text: '<h2>Site news content</h2>' + loremipsum,
      path: 'news',
      portal_type: 'folder',
      children: []
    },
    {
      id: 'events',
      title: 'Events',
      description: 'Site Events',
      text: '<h2>Site events content</h2>' + loremipsum,
      path: 'events',
      portal_type: 'folder',
      children: []
    },
    {
      id: 'Members',
      title: 'Members',
      description: 'Site Members',
      text: '<h2>Site Members content</h2>' + loremipsum,
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
      'text': value.text
    };
    var traversal_re = new RegExp('\\+\\+api\\+\\+v1/traversal\\?path=' + value.path);
    $httpBackend.whenGET(traversal_re).respond(traversal);
  });

  var traversal = site_structure[0];
  var traversal_re = new RegExp('\\+\\+api\\+\\+v1/traversal\\?path=.*');
  $httpBackend.whenGET(traversal_re).respond(traversal);

  // --- PASS THROUGH TEMPLATES ----------------------------------------------
  var templates_re = new RegExp('.*.tpl.html$');
  $httpBackend.whenGET(templates_re).passThrough();

});

ploneModule.requires.push('e2e-mocks');

