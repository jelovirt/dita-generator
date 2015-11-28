requirejs.config({
  baseUrl: '/js/lib',
  paths: {
    app: '../app',
    rx: 'https://cdnjs.cloudflare.com/ajax/libs/rxjs/4.0.7/rx.lite.min'
  }
});

requirejs(['app/main'])