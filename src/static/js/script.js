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
    const cartMiniValue = document.getElementById('cartValue')
    // Obtém o elemento de contador de quantidade
    // const quantityCounter = document.querySelectorAll('.quantity-counter');

    try {
      const response = await fetch('/produto/add-to-cart', {
        method: 'POST',
        body: new URLSearchParams(formData) // Converte os dados do formulário para URLSearchParams
      });

      if (response.ok) {
        const data = await response.json();

        // Log de sucesso no console
        console.log(`Produto ${productId} adicionado ao carrinho`, data);

        let totalQuantity = 0;
        for(const productId in data) {
          console.log(data.quantity)
          totalQuantity += data.quantity
        }
        
        console.log(totalQuantity)
        // Atualiza a quantidade exibida
        let currentQuantity = data.quantity;

        // Muda o botão para indicar adição ao carrinho
        cartMiniValue.innerText = `${data.total}`
        button.style.backgroundColor = 'green';
        button.innerText = `Adicionado ao carrinho (${currentQuantity})`;
        setTimeout(() => {
          button.style.backgroundColor = 'rgb(37 99 235 / var(--tw-bg-opacity))';
          button.innerText = 'Adicionar ao carrinho';
        }, 5000); // Reseta após 2 segundos
      } else {
        // Lida com erro na resposta do servidor
        console.error('Erro ao adicionar produto ao carrinho');
        // Volta o botão ao estado original
        button.style.backgroundColor = 'red';
        button.innerText = 'Erro ao adicionar';
        setTimeout(() => {
          button.style.backgroundColor = 'rgb(37 99 235 / var(--tw-bg-opacity))';
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
        button.style.backgroundColor = 'rgb(37 99 235 / var(--tw-bg-opacity))';
        button.innerText = 'Adicionar ao carrinho';
      }, 2000); // Reseta após 2 segundos
    }
  });

});

const buyButton = document.getElementById('buy-button');
console.log('capturado')

buyButton.addEventListener('click', async function (event) {
  event.preventDefault(); // Previne a ação padrão do botão

  // Seleciona todos os itens do carrinho
  const cartItems = document.querySelectorAll('.cart-item');
  let totalPrice = 0;

  let teste = updateSubtotal();

  // Calcula o preço total somando o preço de cada item multiplicado pela sua quantidade
  // cartItems.forEach(item => {
  //   const price = parseFloat(item.querySelector('.item-price').textContent);
  //   const quantity = parseInt(item.querySelector('.item-quantity').textContent);
  //   totalPrice += price * quantity;
  // });

  // Cria um FormData para enviar o preço total
  const formData = new FormData();
  formData.append('total_price', teste);

  try {
    const response = await fetch('/produto/carrinho/comprar', {
      method: 'POST',
      body: new URLSearchParams(formData)
    });

    if (response.ok) {
      const data = await response.json();
      console.log('Compra realizada com sucesso:', data);

      // Mostra uma mensagem de sucesso ou redireciona o usuário
      alert('Compra realizada com sucesso!');
      window.location.href = '/produto/carrinho'; // Redireciona para a página do carrinho
    } else {
      console.error('Erro ao realizar a compra');
      alert('Erro ao realizar a compra, por favor tente novamente.');
    }
  } catch (error) {
    console.error('Erro de rede ao realizar a compra:', error);
    alert('Erro de rede, por favor tente novamente.');
  }
});

// Tornar a função scrollToContent globalmente acessível
window.scrollToContent = function () {
  document.querySelector('.content').scrollIntoView({ behavior: 'smooth' });
};

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
  return subtotal.toFixed(2);
}

// Inicializar o subtotal ao carregar a página
updateSubtotal();
