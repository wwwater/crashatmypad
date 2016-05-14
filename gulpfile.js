'use strict';

var gulp       = require('gulp');
var source     = require('vinyl-source-stream');
var rename     = require('gulp-rename');
var uglify     = require('gulp-uglify');
var browserify = require('browserify');
var glob       = require('glob');
var es         = require('event-stream');
var scss       = require('gulp-sass');
var concat     = require('gulp-concat');
var cleanCSS   = require('gulp-clean-css');
var browserSync = require('browser-sync').create();

gulp.task('browserify', function(done) {
    glob('./crashatmypad/static/js/*.js', function(err, files) {
        if(err) done(err);

        var tasks = files.map(function(entry) {
            return browserify({ entries: [entry] })
                .bundle()
                .pipe(source(entry))
                .pipe(rename({
                    dirname: ''
                }))
                .pipe(gulp.dest('./crashatmypad/static/tmp'));
            });
        es.merge(tasks).on('end', done);
    })
});

gulp.task('uglify', function() {
    gulp.src(['./crashatmypad/static/tmp/*.js'])
        .pipe(uglify())
        .pipe(gulp.dest('./crashatmypad/static/dist'));
});

gulp.task('js', ['browserify'], function(){
    gulp.start('uglify');
});


gulp.task('scss', function() {
    gulp.src(['./crashatmypad/static/css/*.scss'])
        .pipe(scss({"bundleExec": true}))
        .pipe(cleanCSS())
        .pipe(concat('style.min.css'))
        .pipe(gulp.dest('./crashatmypad/static/dist'));
});


gulp.task('build', ['js', 'scss']);

gulp.task('js-watch', ['js'], function () { browserSync.reload(); });
gulp.task('scss-watch', ['scss'], function () { browserSync.reload(); });

gulp.task('serve', ['build'], function() {

    browserSync.init({
        proxy: "127.0.0.1:8000"
    });

    gulp.watch("./crashatmypad/templates/*.html").on('change', function () { browserSync.reload(); });
    gulp.watch("./crashatmypad/static/scss/*.scss", ['scss-watch']);
    gulp.watch('./crashatmypad/static/js/*.js', ['js-watch']);
});


gulp.task('default', ['serve']);