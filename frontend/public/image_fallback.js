document.addEventListener('error', function (event) {
  const image = event.target;
  if (image instanceof HTMLImageElement && !image.dataset.fallbackApplied) {
    image.dataset.fallbackApplied = 'true';
    image.src = '/placeholder.svg';
  }
}, true);
