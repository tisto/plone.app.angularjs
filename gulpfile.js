var gulp = require('gulp'),
    del = require('del'),
    prefix = require('gulp-prefix'),
    replace = require('gulp-replace'),
    htmlReplace = require('gulp-html-replace'),
    browserSync = require('browser-sync');


// CLEAN
gulp.task('clean', function(cb) {
  del(['src/plone/app/angularjs/app/*.*'], cb)
});


// TEMPLATES
gulp.task('templates', function(){
  gulp.src('app/*.tpl.html')
  .pipe(gulp.dest('src/plone/app/angularjs/app'));
});

// BOWER_COMPOMENTS
gulp.task('bower', function(){
  gulp.src('app/bower_components/**/*.*')
  .pipe(gulp.dest('src/plone/app/angularjs/app/bower_components'));
});


// PREFIX
gulp.task('index-html', function(){
  var prefixUrl = "++theme++plone.app.angularjs/";
  gulp.src('app/*.html')
    .pipe(prefix(prefixUrl, null, true))
    .pipe(htmlReplace({
        'mock': ''
    }))
    .pipe(gulp.dest('src/plone/app/angularjs/app'));
});

// SCRIPTS
gulp.task('scripts', function(){
  gulp.src('app/scripts/**/*.js')
    .pipe(replace("templateUrl: '", "templateUrl: '++theme++plone.app.angularjs/"))
    .pipe(gulp.dest('src/plone/app/angularjs/app/scripts/'));
});


// STYPES
gulp.task('styles', function(){
  gulp.src('app/styles/*.css')
    .pipe(gulp.dest('src/plone/app/angularjs/app/styles/'));
});


// BROWSER SYNC
gulp.task('browser-sync', function() {
  browserSync({
    server: {
      baseDir: "./app/"
    }
  });
});


// DEFAULT
gulp.task('default', ['bower', 'templates', 'index-html', 'scripts', 'styles']);
