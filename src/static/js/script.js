document.addEventListener('DOMContentLoaded', function () {

  const dropzone = document.getElementById('dropzone');
  const fileInput = document.getElementById('imagem');

  // Desaparecimento e Remoção de Mensagens Flash
  setTimeout(function () {
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(function (message) {
      message.style.transition = 'opacity 0.5s ease-out'; // Efeito de transição
      message.style.opacity = '0'; // Efeito de desvanecimento
      setTimeout(function () {
        message.remove(); // Remove do DOM
      }, 500); // Espera a transição de desvanecimento terminar
    });
  }, 5000); // 5000 milissegundos = 5 segundos

  // Função para Rolar Suavemente para o Conteúdo
  function scrollToContent() {
    document.querySelector('.content').scrollIntoView({ behavior: 'smooth' });
  }

  // Aplica Máscara de Formatação ao Campo de Preço
  var precoInput = document.getElementById('preco');
  precoInput.addEventListener('input', function () {
    var precoValue = precoInput.value.replace(/\D/g, '');
    precoInput.value = VMasker.toMoney(precoValue, { precision: 2, separator: ',', delimiter: '.', unit: 'R$ ', zeroCents: false });
  });

  // Clique na área de dropzone abre o seletor de arquivo
  dropzone.addEventListener('click', () => {
      fileInput.click();
  });

  // Quando o arquivo é selecionado através do seletor de arquivo
  fileInput.addEventListener('change', () => {
      handleFiles(fileInput.files);
  });

  // Quando os arquivos são arrastados para o dropzone
  dropzone.addEventListener('dragover', (event) => {
      event.preventDefault();
      dropzone.classList.add('dragover');
  });

  dropzone.addEventListener('dragleave', () => {
      dropzone.classList.remove('dragover');
  });

  dropzone.addEventListener('drop', (event) => {
      event.preventDefault();
      dropzone.classList.remove('dragover');
      const files = event.dataTransfer.files;
      fileInput.files = files; // Atualiza o input com os arquivos arrastados
      handleFiles(files);
  });

  // Função para lidar com arquivos selecionados ou arrastados
  function handleFiles(files) {
      if (files.length) {
          const file = files[0];
          // Atualiza a visualização do dropzone com o nome do arquivo
          dropzone.innerHTML = `<span class="text-gray-500">Arquivo selecionado: ${file.name}</span>`;
      }
  }

  const stars = document.querySelectorAll('.star');

  stars.forEach(star => {
    star.addEventListener('click', function() {
      const value = parseInt(this.getAttribute('data-value'));

      // Marca as estrelas conforme o valor clicado
      stars.forEach((s, index) => {
        if (index < value) {
          s.classList.add('active');
        } else {
          s.classList.remove('active');
        }
      });

      document.getElementById('rating-value').value = value;
    });
  });

});

// Tornar a função scrollToContent globalmente acessível
window.scrollToContent = function() {
  document.querySelector('.content').scrollIntoView({ behavior: 'smooth' });
};
