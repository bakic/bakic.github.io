document.querySelectorAll('.prose pre').forEach(function (pre) {
  var btn = document.createElement('button');
  btn.type = 'button';
  btn.className = 'copy';
  btn.textContent = 'Copy';
  btn.addEventListener('click', function () {
    var code = pre.querySelector('code');
    navigator.clipboard.writeText(code ? code.innerText : pre.innerText).then(function () {
      btn.textContent = 'Copied';
      setTimeout(function () { btn.textContent = 'Copy'; }, 1500);
    });
  });
  pre.appendChild(btn);
});
