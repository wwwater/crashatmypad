'use strict';

var gulp        = require('gulp');
var source      = require('vinyl-source-stream');
var rename      = require('gulp-rename');
var uglify      = require('gulp-uglify');
var browserify  = require('browserify');
var glob        = require('glob');
var es          = require('event-stream');
var scss        = require('gulp-sass');
var concat      = require('gulp-concat');
var cleanCSS    = require('gulp-clean-css');
var browserSync = require('browser-sync').create();
var exec        = require('child_process').exec;
var clean       = require('gulp-clean');
var runSequence = require('run-sequence');
var eslint      = require('gulp-eslint');

gulp.task('eslint', function() {
    return gulp.src(['./crashatmypad/static/js/*.js'])
        .pipe(eslint())
        .pipe(eslint.format())
        .pipe(eslint.failAfterError());
});

gulp.task('browserify', ['eslint'], function(done) {
    return glob('./crashatmypad/static/js/*.js', function(err, files) {
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
    });
});

gulp.task('uglify', ['browserify'], function() {
    return gulp.src(['./crashatmypad/static/tmp/*.js'])
        .pipe(uglify())
        .pipe(gulp.dest('./crashatmypad/static/dist'));
});

gulp.task( 'clean:tmp', ['uglify'], function() {
    return gulp.src('./crashatmypad/static/tmp', { read: false })
        .pipe(clean());
});

gulp.task('js', ['clean:tmp']);

gulp.task('scss', function() {
    return gulp.src(['./crashatmypad/static/css/*.scss'])
        .pipe(scss({"bundleExec": true}))
        .pipe(cleanCSS())
        .pipe(concat('style.min.css'))
        .pipe(gulp.dest('./crashatmypad/static/dist'));
});

gulp.task( 'clean:dist', function() {
    return gulp.src('./crashatmypad/static/dist', { read: false })
        .pipe(clean());
});

gulp.task('build', function() {
    runSequence(
        'clean:dist',
        ['js', 'scss']
    );
});


// ----------------------------------------------------------------------------
// tasks for local development

gulp.task('scss-watch', ['scss'], function () { browserSync.reload(); });
gulp.task('js-watch', ['js'], function () { browserSync.reload(); });

gulp.task('serve', function() {

    exec('gunicorn -b 0.0.0.0:8000 --reload --access-logfile - "crashatmypad.app:create_app()"');

    browserSync.init({
        proxy: "127.0.0.1:8000"
    });

    gulp.watch("./crashatmypad/templates/*.html").on('change', function () { browserSync.reload(); });
    gulp.watch("./crashatmypad/static/scss/*.scss", ['scss-watch']);
    gulp.watch('./crashatmypad/static/js/*.js', ['js-watch']);
});


gulp.task('default', function() {
    runSequence(
        'clean:dist',
        ['js', 'scss'],
        'serve'
    );
});