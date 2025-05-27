// Graphical password registration and login
const images = document.querySelectorAll('.graph-img');
let pattern = [];
images.forEach(img => {
  img.addEventListener('click', () => {
    img.classList.toggle('opacity-50');
    const id = img.dataset.id;
    if (pattern.includes(id)) {
      pattern = pattern.filter(i => i !== id);
    } else {
      pattern.push(id);
    }
    document.getElementById('pattern-input').value = pattern.join(',');
  });
});