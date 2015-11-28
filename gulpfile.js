const gulp = require('gulp')
const babel = require('gulp-babel')
const gulpFilter = require('gulp-filter')

gulp.task('default', () => {
  const filter = gulpFilter('**/*.js', {restore: true})
  return gulp.src('src/**/*')
      .pipe(filter)
      .pipe(babel({ presets: ['es2015'] }))
      .pipe(filter.restore)
      .pipe(gulp.dest('dist'))
})
