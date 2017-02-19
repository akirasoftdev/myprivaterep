//Include required modules
var gulp = require("gulp"),
    babelify = require('babelify'),
    browserify = require("browserify"),
    connect = require("gulp-connect"),
    source = require("vinyl-source-stream"),
    typescript = require('gulp-typescript'),
    sourcemaps = require('gulp-sourcemaps')
;

var tsProject = typescript.createProject('tsconfig.json', {
     outFile: 'aaa.js'
});

//Default task. This will be run when no task is passed in arguments to gulp
gulp.task("default",["copyStaticFiles", "tsc", "build", "startServer"], function() {
    gulp.watch("./src/ts/*.ts", ["tsc"]);
    gulp.watch("./src/html/*.html", ["copyStaticFiles"]);
});

//Copy static files from html folder to build folder
gulp.task("copyStaticFiles", function(){
    return gulp.src("./src/html/*")
    .pipe(gulp.dest("./build"))
});

gulp.task("tsc", function() {
    var tsResult = tsProject.src()
        .pipe(tsProject())
    return tsResult.js
        .pipe(gulp.dest('temp/'))
})

//Convert ES6 ode in all js files in src/js folder and copy to
//build folder as bundle.js
gulp.task("build", function(){
    return browserify({
        entries: ["./temp/aaa.js"]
    })
    .transform(babelify.configure({
        presets : ["es2015"]
    }))
    .bundle()
    .pipe(source("application.js"))
    .pipe(gulp.dest("./build"))
    ;
});

//Start a test server with doc root at build folder and
//listening to 9001 port. Home page = http://localhost:9001
gulp.task("startServer", function(){
    connect.server({
        root : "./build",
        livereload : true,
        port : 9001
    });
});
