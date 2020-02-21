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

//All files in css folder
let cssSources1 = {
    watchFolder: [
        
        'iahx/static/less/bootstrap.less',       
        'iahx/static/less/advanced.less',
        'iahx/static/less/chart.less',
        'iahx/static/less/decs.locator.less',
        'iahx/static/less/jquery.cluetip.less',
        'iahx/static/less/jquery.fancybox.1.3.4.less',
        'iahx/static/less/layout.less',
        'iahx/static/less/print.less',
        'iahx/static/less/related.less',
        'iahx/static/less/scielo.portal.custom.less',
        'iahx/static/less/scielo.portal.less',
        'iahx/static/less/scielo.print.less',
        'iahx/static/less/selectize.bootstrap3.less',
        'iahx/static/less/skin.less',
        'iahx/static/less/styles.less'

        ],
    output: 'iahx/static/css'
};

// file in css/ui-lightness folder
let cssSources2 = {
    watchFolder: [
        
        'iahx/static/less/jquery.ui.1.10.1.custom.less'

        ],
    output: 'iahx/static/css/ui-lightness'
};

// file in css/mobile folder
let cssSources3 = {
    watchFolder: [
        
        'iahx/static/less/style.mobile.less'

        ],
    output: 'iahx/static/css/mobile'
};

function processUiCustom() {
    return src("iahx/static/less/jquery.ui.1.10.1.custom.less")
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
            rename({ suffix: ".min" })
        )
        .pipe(
            sourceMaps.write(".")
        )
        .pipe(
            rename("jquery.ui.1.10.1.custom.min.css")
        )
        .pipe(
            dest("iahx/static/css/ui-lightness")
        )
        .pipe(
            connect.reload()
        );
}

function processStyleMobile() {
    return src("iahx/static/less/style.mobile.less")
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
            rename({ suffix: ".min" })
        )
        .pipe(
            sourceMaps.write(".")
        )
        .pipe(
            rename("style.min.css")
        )
        .pipe(
            dest("iahx/static/css/mobile")
        )
        .pipe(
            connect.reload()
        );
}


function processCSS() {
    return src(cssSources1.watchFolder)
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
            rename({ suffix: ".min" })
        )
        .pipe(
            sourceMaps.write(".")
        )
        .pipe(
            dest(cssSources1.output)
        )
        .pipe(
            connect.reload()
        );
}



// file in js/ folder
let jsSources = {
    scieloSearchContent: [
        //'./js/plugins/slick.js',
        //'./js/plugins.js',
        //'./js/vd-ep.js',
        './iahx/static/js/main.js'
        ],
    
    watcher: [
        //'./js/plugins.js',
        //'./js/vd-ep.js',
        './iahx/static/js/main.js'
        ],

    output: './js'
};

function proccessJs() {
    return src(jsSources.scieloSearchContent)
            .pipe(
                sourceMaps.init()
            )
            /*
            .pipe(
                concat("vd-ep.min.js")
            )
            */
            .pipe(
                uglify()
            )
            .pipe(
                sourceMaps.write('.')
            )
            .pipe(
                dest(jsSources.output)
            )
            .pipe(
                connect.reload()
            );
}



// Watchers
function watchCSSProcess() {
    return watch(cssSources1.watchFolder,processCSS);
}
function watchUiCustom() {
    return watch(cssSources2.watchFolder, processUiCustom);
}
function watchStyleMobile() {
    return watch(cssSources3.watchFolder, processStyleMobile);
}



exports.watch = series(
    processCSS,
    processStyleMobile,
    processUiCustom,
    proccessJs,

    parallel(
        watchCSSProcess,
        watchUiCustom,
        watchStyleMobile
    )
);



exports.default = series(
    processCSS,
    //processStyleMobile,
    //processUiCustom,
    proccessJs
);