requirejs.config({
  baseUrl: '/js/lib',
  paths: {
    app: '../app'
  }
});

requirejs(['app/main'])