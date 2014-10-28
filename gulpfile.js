var gulp = require('gulp'),
    del = require('del'),
    prefix = require('gulp-prefix'),
    less = require('gulp-less'),
    replace = require('gulp-replace'),
    htmlReplace = require('gulp-html-replace'),
    browserSync = require('browser-sync'),
    sourcemaps = require('gulp-sourcemaps');


// CLEAN
gulp.task('clean', function(cb) {
  del(['src/plone/app/angularjs/app/**/*.*'], cb)
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


// INDEX.HTML
gulp.task('index-html', function(){
  var prefixUrl = "++theme++plone.app.angularjs/";
  gulp.src('app/index.html')
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


// STYLES
gulp.task('styles', function(){
  gulp.src('app/styles/*.less')
    .pipe(sourcemaps.init())
    .pipe(less())
    .pipe(sourcemaps.write())
    .pipe(gulp.dest('app/styles/'))
    .pipe(gulp.dest('src/plone/app/angularjs/app/styles/'));
});


// WATCH
gulp.task('watch', function() {
  gulp.watch('app/styles/**/*.less', ['styles']);
  gulp.watch('app/scripts/**/*.js', ['scripts']);
  //gulp.watch('app/images/**/*', ['images']);
  gulp.watch('app/*.tpl.html', ['templates']);
  gulp.watch('app/index.html', ['index-html']);
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
gulp.task('default', ['clean'], function() {
  gulp.start('bower', 'templates', 'index-html', 'scripts', 'styles');
});
