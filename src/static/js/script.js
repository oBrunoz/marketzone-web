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
    star.addEventListener('click', function () {
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
// Seleciona todos os botões de adicionar ao carrinho
const addToCartButtons = document.querySelectorAll('#add-to-cart-button');

addToCartButtons.forEach(button => {
  button.addEventListener('click', async function (event) {
    event.preventDefault(); // Previne a ação padrão do formulário (recarregar a página)

    const form = button.closest('#add-to-cart-form'); // Encontra o formulário correspondente
    const productId = form.getAttribute('data-product-id'); // Obtém o ID do produto do atributo data

    // Obtém os dados do formulário
    const formData = new FormData(form);
    formData.append('product_id', productId); // Assegura que o product_id está nos dados

    // Obtém o elemento de contador de quantidade
    const quantityCounter = document.querySelectorAll('.quantity-counter');

    try {
      const response = await fetch('/produto/add-to-cart', {
        method: 'POST',
        body: new URLSearchParams(formData) // Converte os dados do formulário para URLSearchParams
      });

      if (response.ok) {
        const data = await response.json();
        // Log de sucesso no console
        console.log(`Produto ${productId} adicionado ao carrinho`, data);

        // Atualiza a quantidade exibida
        let currentQuantity = parseInt(quantityCounter.textContent.replace('Quantidade: ', '')) || 0;
        currentQuantity += 1;
        quantityCounter.textContent = `Quantidade: ${currentQuantity}`;

        // Muda o botão para indicar adição ao carrinho
        button.style.backgroundColor = 'green';
        button.innerText = `Adicionado ao carrinho (${currentQuantity})`;
      } else {
        // Lida com erro na resposta do servidor
        console.error('Erro ao adicionar produto ao carrinho');
        // Volta o botão ao estado original
        button.style.backgroundColor = 'red';
        button.innerText = 'Erro ao adicionar';
        setTimeout(() => {
          button.style.backgroundColor = 'blue';
          button.innerText = 'Adicionar ao carrinho';
        }, 2000); // Reseta após 2 segundos
      }
    } catch (error) {
      // Lida com erro na comunicação
      console.error('Erro de rede ao adicionar produto ao carrinho:', error);
      // Volta o botão ao estado original
      button.style.backgroundColor = 'red';
      button.innerText = 'Erro ao adicionar';
      setTimeout(() => {
        button.style.backgroundColor = 'blue';
        button.innerText = 'Adicionar ao carrinho';
      }, 2000); // Reseta após 2 segundos
    }
  });
});

document.querySelectorAll(".delete-from-cart-btn").forEach(button => {
  button.addEventListener("click", function (event) {
    event.preventDefault(); // Impede o comportamento padrão do botão

    const itemId = this.getAttribute("data-item-id");

    // Fazer a requisição AJAX
    fetch("/produto/carrinho/deletar", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded"
      },
      body: new URLSearchParams({ "item_id": itemId })
    })
      .then(response => response.json())
      .then(data => {
        if (data.status === "success") {
          // Atualizar a quantidade exibida ou remover o item do DOM
          const productDiv = document.querySelector(`[data-product-id="${itemId}"]`);
          const quantitySpan = document.querySelector(".quantity-counter");

          if (data.quantity > 0) {
            quantitySpan.textContent = `Quantidade: ${data.quantity}`;
          } else {
            productDiv.remove()
          }

          console.log(data.item_id, data.quantity)
        }
      })
      .catch(error => console.error("Error:", error));
  });
});

function updateSubtotal() {
  // Calcular o subtotal com base nos elementos ainda no carrinho
  let subtotal = 0;
  document.querySelectorAll("[data-product-id]").forEach(item => {
    const quantity = parseInt(item.querySelector(".quantity-counter").textContent.split(": ")[1]);
    const price = parseFloat(item.querySelector(".text-indigo-600").textContent.replace("R$", ""));
    subtotal += quantity * price;
  });

  // Atualizar o subtotal exibido
  document.getElementById("subtotal").textContent = `R$${subtotal.toFixed(2)}`;
}

// Inicializar o subtotal ao carregar a página
updateSubtotal();


// Tornar a função scrollToContent globalmente acessível
window.scrollToContent = function () {
  document.querySelector('.content').scrollIntoView({ behavior: 'smooth' });
};
