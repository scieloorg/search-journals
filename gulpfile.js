const { src, dest, watch, series, parallel } = require('gulp');
const less = require('gulp-less');
const cleanCSS = require('gulp-clean-css');
const uglify = require('gulp-uglify');
const sourceMaps = require('gulp-sourcemaps');
const connect = require('gulp-connect');
const gutil = require('gulp-util');
const rename = require('gulp-rename');
const concat = require('gulp-concat');
const minifyCSS = require('gulp-minify-css');


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


//Core

//All files in css folder

let cssSources = {
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
let cssSourcesUI = {
    watchFolder: [

        'iahx/static/less/jquery.ui.1.10.1.custom.less'

    ],
    output: 'iahx/static/css/ui-lightness'
};

// file in css/mobile folder
let cssSourcesMobile = {
    watchFolder: [

        'iahx/static/less/style.mobile.less'

    ],
    output: 'iahx/static/css/mobile'
};


// RevEnf

//All files in revenf css folder
let cssSourcesRevEnf = {
    watchFolder: [

        'iahx-sites/revenf/static/less/bootstrap.less',
        'iahx-sites/revenf/static/less/advanced.less',
        'iahx-sites/revenf/static/less/chart.less',
        'iahx-sites/revenf/static/less/decs.locator.less',
        'iahx-sites/revenf/static/less/jquery.cluetip.less',
        'iahx-sites/revenf/static/less/jquery.fancybox.1.3.4.less',
        'iahx-sites/revenf/static/less/layout.less',
        'iahx-sites/revenf/static/less/print.less',
        'iahx-sites/revenf/static/less/related.less',
        'iahx-sites/revenf/static/less/scielo.portal.custom.less',
        'iahx-sites/revenf/static/less/scielo.portal.less',
        'iahx-sites/revenf/static/less/scielo.print.less',
        'iahx-sites/revenf/static/less/selectize.bootstrap3.less',
        'iahx-sites/revenf/static/less/skin.less',
        'iahx-sites/revenf/static/less/styles.less'

    ],
    output: 'iahx-sites/revenf/static/css'
};

// file in rev enf css/ui-lightness folder
let cssSourcesUIRevEnf = {
    watchFolder: [

        'iahx-sites/revenf/static/less/jquery.ui.1.10.1.custom.less'

    ],
    output: 'iahx-sites/revenf/static/css/ui-lightness'
};

// file in rev enf css/mobile folder
let cssSourcesMobileRevEnf = {
    watchFolder: [

        'iahx-sites/revenf/static/less/style.mobile.less'

    ],
    output: 'iahx-sites/revenf/static/css/mobile'
};


// ScieloOrg

//All files in scieloorg css folder
let cssSourcesScieloOrg = {
    watchFolder: [

        'iahx-sites/scieloorg/static/less/bootstrap.less',
        'iahx-sites/scieloorg/static/less/advanced.less',
        'iahx-sites/scieloorg/static/less/chart.less',
        'iahx-sites/scieloorg/static/less/decs.locator.less',
        'iahx-sites/scieloorg/static/less/jquery.cluetip.less',
        'iahx-sites/scieloorg/static/less/jquery.fancybox.1.3.4.less',
        'iahx-sites/scieloorg/static/less/layout.less',
        'iahx-sites/scieloorg/static/less/print.less',
        'iahx-sites/scieloorg/static/less/related.less',
        'iahx-sites/scieloorg/static/less/scielo.portal.custom.less',
        'iahx-sites/scieloorg/static/less/scielo.portal.less',
        'iahx-sites/scieloorg/static/less/scielo.print.less',
        'iahx-sites/scieloorg/static/less/selectize.bootstrap3.less',
        'iahx-sites/scieloorg/static/less/skin.less',
        'iahx-sites/scieloorg/static/less/styles.less'

    ],
    output: 'iahx-sites/scieloorg/static/css'
};

// file in rev enf css/ui-lightness folder
let cssSourcesUIScieloOrg = {
    watchFolder: [

        'iahx-sites/scieloorg/static/less/jquery.ui.1.10.1.custom.less'

    ],
    output: 'iahx-sites/scieloorg/static/css/ui-lightness'
};

// file in rev enf css/mobile folder
let cssSourcesMobileScieloOrg = {
    watchFolder: [

        'iahx-sites/scieloorg/static/less/style.mobile.less'

    ],
    output: 'iahx-sites/scieloorg/static/css/mobile'
};



// Process

// Core
function processUiCustom() {
    return src("iahx/static/less/jquery.ui.1.10.1.custom.less")
        .pipe(
            sourceMaps.init()
        )
        .pipe(
            less().on('error', function(err) {
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
            less().on('error', function(err) {
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
    return src(cssSources.watchFolder)
        .pipe(
            sourceMaps.init()
        )
        .pipe(
            less().on('error', function(err) {
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
            dest(cssSources.output)
        )
        .pipe(
            connect.reload()
        );
}

// RevEnf
function processUiCustomRevEnf() {
    return src("iahx-sites/revenf/static/less/jquery.ui.1.10.1.custom.less")
        .pipe(
            sourceMaps.init()
        )
        .pipe(
            less().on('error', function(err) {
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
            dest("iahx-sites/revenf/static/css/ui-lightness")
        )
        .pipe(
            connect.reload()
        );
}

function processStyleMobileRevEnf() {
    return src("iahx-sites/revenf/static/less/style.mobile.less")
        .pipe(
            sourceMaps.init()
        )
        .pipe(
            less().on('error', function(err) {
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
            dest("iahx-sites/revenf/static/css/mobile")
        )
        .pipe(
            connect.reload()
        );
}

function processCSSRevEnf() {
    return src(cssSourcesRevEnf.watchFolder)
        .pipe(
            sourceMaps.init()
        )
        .pipe(
            less().on('error', function(err) {
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
            dest(cssSourcesRevEnf.output)
        )
        .pipe(
            connect.reload()
        );
}


// ScieloOrg
function processUiCustomScieloOrg() {
    return src("iahx-sites/scieloorg/static/less/jquery.ui.1.10.1.custom.less")
        .pipe(
            sourceMaps.init()
        )
        .pipe(
            less().on('error', function(err) {
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
            dest("iahx-sites/scieloorg/static/css/ui-lightness")
        )
        .pipe(
            connect.reload()
        );
}

function processStyleMobileScieloOrg() {
    return src("iahx-sites/scieloorg/static/less/style.mobile.less")
        .pipe(
            sourceMaps.init()
        )
        .pipe(
            less().on('error', function(err) {
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
            dest("iahx-sites/scieloorg/static/css/mobile")
        )
        .pipe(
            connect.reload()
        );
}

function processCSSScieloOrg() {
    return src(cssSourcesScieloOrg.watchFolder)
        .pipe(
            sourceMaps.init()
        )
        .pipe(
            less().on('error', function(err) {
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
            dest(cssSourcesScieloOrg.output)
        )
        .pipe(
            connect.reload()
        );
}



// Watchers

//Core
function watchCSSProcess() {
    return watch(cssSources.watchFolder, processCSS);
}

function watchUiCustom() {
    return watch(cssSourcesUI.watchFolder, processUiCustom);
}

function watchStyleMobile() {
    return watch(cssSourcesMobile.watchFolder, processStyleMobile);
}

// RevEnf
function watchCSSProcessRevEnf() {
    return watch(cssSourcesRevEnf.watchFolder, processCSS);
}

function watchUiCustomRevEnf() {
    return watch(cssSourcesUIRevEnf.watchFolder, processUiCustom);
}

function watchStyleMobileRevEnf() {
    return watch(cssSourcesMobileRevEnf.watchFolder, processStyleMobile);
}

// ScieloOrg
function watchCSSProcessScieloOrg() {
    return watch(cssSourcesScieloOrg.watchFolder, processCSS);
}

function watchUiCustomScieloOrg() {
    return watch(cssSourcesUIScieloOrg.watchFolder, processUiCustom);
}

function watchStyleMobileScieloOrg() {
    return watch(cssSourcesMobileScieloOrg.watchFolder, processStyleMobile);
}


exports.watch = series(
    processCSS,
    processStyleMobile,
    processUiCustom,

    processCSSRevEnf,
    processStyleMobileRevEnf,
    processUiCustomRevEnf,

    processCSSScieloOrg,
    processStyleMobileScieloOrg,
    processUiCustomScieloOrg,

    parallel(
        watchCSSProcess,
        watchUiCustom,
        watchStyleMobile,

        watchCSSProcessRevEnf,
        watchUiCustomRevEnf,
        watchStyleMobileRevEnf,

        watchCSSProcessScieloOrg,
        watchUiCustomScieloOrg,
        watchStyleMobileScieloOrg
    )
);

exports.default = series(
    processCSS,
    processStyleMobile,
    processUiCustom,

    processCSSRevEnf,
    processStyleMobileRevEnf,
    processUiCustomRevEnf,

    processCSSScieloOrg,
    processStyleMobileScieloOrg,
    processUiCustomScieloOrg
);