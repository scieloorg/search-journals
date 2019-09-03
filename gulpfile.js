const {src, dest, watch, series, parallel} = require('gulp');
const less          = require('gulp-less');
const cleanCSS      = require('gulp-clean-css');
const uglify        = require('gulp-uglify');
const sourceMaps    = require('gulp-sourcemaps');
const connect       = require('gulp-connect');
const gutil         = require('gulp-util');
const rename        = require('gulp-rename');
const concat        = require('gulp-concat');
const minifyCSS     = require('gulp-minify-css');

// Creating webserver with live-reload
function webserver() {
    return connect.server({
        name: 'SciELO-Seach-App',
        port: 8000,
        livereload: true,
        open: {
            browser: 'chrome' // if not working OS X browser: 'Google Chrome'
        }
    });
}

//Process CSS
let cssSources = {
    watchFolder: [
        
        'iahx/static/less/advanced.less',
        'iahx/static/less/chart.less',
        'iahx/static/less/decs-locator.less',
        'iahx/static/less/jquery.cluetip.less',
        'iahx/static/less/jquery.fancybox.less',
        'iahx/static/less/layout.less',
        'iahx/static/less/print.less',
        'iahx/static/less/related.less',
        'iahx/static/less/scielo-portal-custom.less',
        'iahx/static/less/scielo-portal.min.less',
        'iahx/static/less/scielo-print.less',
        'iahx/static/less/selectize.bootstrap3.less',
        'iahx/static/less/skin.less',
        'iahx/static/less/styles.less'

        ],
    output: 'iahx/static/css'
};

function processBootstrap() {
    return src("node_modules/bootstrap/less/bootstrap.less")
            .pipe(
                sourceMaps.init()
            )
            .pipe(
                less().on('error', function(err){
                    gutil.log(err);
                    this.emit('end');
                }))
            .pipe(
                cleanCSS()
            )
            .pipe(
                minifyCSS()
            )
            .pipe(
                sourceMaps.write(".")
            )
            .pipe(
                rename("bootstrap.min.css")
            )
            .pipe(
                dest("iahx/static/css")
            )
            .pipe(
                connect.reload()
            );
}

function processUiCustom() {
    return src("iahx/static/less/jquery-ui-1.10.1.custom.less")
            .pipe(
                sourceMaps.init()
            )
            .pipe(
                less().on('error', function(err){
                    gutil.log(err);
                    this.emit('end');
                }))
            .pipe(
                cleanCSS()
            )
            .pipe(
                minifyCSS()
            )
            .pipe(
                sourceMaps.write(".")
            )
            .pipe(
                rename("jquery-ui-1.10.1.custom.min.css")
            )
            .pipe(
                dest("iahx/static/css/ui-lightness")
            )
            .pipe(
                connect.reload()
            );
}

function processStyleMobile() {
    return src("iahx/static/less/style-mobile.less")
            .pipe(
                sourceMaps.init()
            )
            .pipe(
                less().on('error', function(err){
                    gutil.log(err);
                    this.emit('end');
                }))
            .pipe(
                cleanCSS()
            )
            .pipe(
                minifyCSS()
            )
            .pipe(
                sourceMaps.write(".")
            )
            .pipe(
                rename("style.css")
            )
            .pipe(
                dest("iahx/static/css/mobile")
            )
            .pipe(
                connect.reload()
            );
}

function processCSS() {
    return src(cssSources.watchFolder)
            .pipe(
                sourceMaps.init()
            )
            .pipe(
                less().on('error', function(err){
                    gutil.log(err);
                    this.emit('end');
                }))
            .pipe(
                cleanCSS()
            )
            .pipe(
                minifyCSS()
            )
            .pipe(
                sourceMaps.write(".")
            )
            .pipe(
                dest(cssSources.output)
            )
            .pipe(
                connect.reload()
            );
}

// Watchers
function watchCSSProcess() {
    return watch(cssSources.watchFolder,processCSS);
}

exports.watchCSSProcess = series(processBootstrap, processUiCustom, processStyleMobile, processCSS, watchCSSProcess);
exports.default = series(processBootstrap, processUiCustom, processStyleMobile, processCSS);