var gulp = require('gulp'),
    del = require('del'),
    prefix = require('gulp-prefix');


gulp.task('clean', function(cb) {
    del(['src/plone/app/angularjs/app'], cb)
});


gulp.task('move', ['clean'], function(){
  gulp.src('app/**/*.*', { base: './' })
  .pipe(gulp.dest('src/plone/app/angularjs'));
});


gulp.task('prefix', function(){
  var prefixUrl = "++theme++plone.app.angularjs/";
  gulp.src('app/index.html')
    .pipe(prefix(prefixUrl, null, true))
    .pipe(gulp.dest('src/plone/app/angularjs/app'));
});

gulp.task('default', ['move'], function() {
    gulp.start('prefix');
});
