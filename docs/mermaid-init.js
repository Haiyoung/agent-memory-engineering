// Mermaid 渲染
(function() {
  if (typeof mermaid === 'undefined') {
    console.error('Mermaid not loaded');
    return;
  }
  mermaid.initialize({ startOnLoad: false, theme: 'default' });

  var blocks = document.querySelectorAll('pre > code.language-mermaid');
  console.log('Found ' + blocks.length + ' mermaid blocks');

  blocks.forEach(function(codeEl, i) {
    var src = codeEl.textContent.trim();
    var container = document.createElement('div');
    container.className = 'mermaid';
    container.id = 'mermaid-diagram-' + i;
    codeEl.parentNode.replaceWith(container);

    mermaid.render('mermaid-svg-' + i, src).then(function(r) {
      container.innerHTML = r.svg;
    }).catch(function(err) {
      container.textContent = '[Mermaid error: ' + err.message + ']';
    });
  });
})();
