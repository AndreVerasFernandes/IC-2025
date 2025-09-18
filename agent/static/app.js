const elements = {
  widget: document.querySelector('.chat-widget'),
  floatingToggle: document.querySelector('.floating-toggle'),
  headerToggle: document.querySelector('.chat-header__toggle'),
  statusText: document.querySelector('.status-text'),
  statusDot: document.querySelector('.status-dot'),
  messages: document.querySelector('.chat-messages'),
  quickReplies: document.querySelector('.quick-replies'),
  input: document.querySelector('#message-input'),
  send: document.querySelector('#send-btn'),
  attachBtn: document.querySelector('#attach-btn'),
  fileInput: document.querySelector('#file-input'),
};

// ONLINE/OFFLINE
function updateOnlineStatus() {
  const online = navigator.onLine;
  elements.statusText.textContent = online ? 'online' : 'offline';
  elements.statusDot.style.background = online ? 'var(--success)' : 'var(--error)';
  elements.statusDot.style.boxShadow = online
    ? '0 0 0 3px rgba(34,197,94,.15)'
    : '0 0 0 3px rgba(239,68,68,.15)';
}
window.addEventListener('online', updateOnlineStatus);
window.addEventListener('offline', updateOnlineStatus);
updateOnlineStatus();

// Remover toggle de header se estiver no modo página
if (elements.headerToggle) {
  elements.headerToggle.remove();
}

// QUICK REPLIES
const suggestions = [
  'Segunda via do boleto',
  'Acompanhar minha matrícula',
  'Problemas com login',
  'Mais informações sobre cursos',
];
renderQuickReplies(suggestions);
function renderQuickReplies(items) {
  elements.quickReplies.innerHTML = '';
  items.forEach(text => {
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.textContent = text;
    btn.addEventListener('click', () => {
      elements.input.value = text;
      handleSend();
    });
    elements.quickReplies.appendChild(btn);
  });
}

// INPUT behavior
elements.input.addEventListener('input', autoGrow);
elements.input.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    handleSend();
  }
});
function autoGrow() {
  elements.input.style.height = 'auto';
  elements.input.style.height = Math.min(elements.input.scrollHeight, 140) + 'px';
}

// SEND
elements.send.addEventListener('click', handleSend);
function handleSend() {
  const text = elements.input.value.trim();
  if (!text) return;
  appendMessage('user', { type: 'text', text });
  elements.input.value = '';
  autoGrow();
  callBackend(text);
}

// ATTACHMENTS
elements.attachBtn.addEventListener('click', () => elements.fileInput.click());
elements.fileInput.addEventListener('change', handleFiles);
function handleFiles(e) {
  const files = Array.from(e.target.files || []);
  if (!files.length) return;
  files.forEach(async (file) => {
    const isImage = file.type.startsWith('image/');
    const objectUrl = URL.createObjectURL(file);
    if (isImage) {
      appendMessage('user', { type: 'image', url: objectUrl, name: file.name });
    } else {
      appendMessage('user', { type: 'file', url: objectUrl, name: file.name, size: file.size });
    }
    // Você pode adaptar isso para enviar o arquivo ao backend futuramente
    appendMessage('bot', { type: 'text', text: `Recebemos o arquivo: ${file.name}` });
  });
  elements.fileInput.value = '';
}

// MESSAGES
function appendMessage(author, payload) {
  const li = document.createElement('li');
  li.className = `message ${author}`;
  const bubble = document.createElement('div');
  bubble.className = 'bubble';

  if (payload.type === 'text') {
    bubble.textContent = payload.text;
  } else if (payload.type === 'image') {
    const img = document.createElement('img');
    img.src = payload.url;
    img.alt = payload.name || 'Imagem';
    img.className = 'thumb';
    bubble.appendChild(img);
    const meta = document.createElement('div');
    meta.className = 'meta';
    meta.textContent = payload.name || 'Imagem';
    bubble.appendChild(meta);
  } else if (payload.type === 'file') {
    const link = document.createElement('a');
    link.href = payload.url;
    link.download = payload.name || 'arquivo';
    link.className = 'file-pill';
    link.innerHTML = `<svg width="16" height="16" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M14 2H6a2 2 0 0 0-2 2v16l6-3 6 3V8l-2-2z"/></svg> ${payload.name || 'arquivo'}${payload.size ? ' • ' + prettySize(payload.size) : ''}`;
    bubble.appendChild(link);
  }

  li.appendChild(bubble);
  elements.messages.appendChild(li);
  scrollToBottom();
}

function prettySize(bytes) {
  const units = ['B','KB','MB','GB'];
  let i = 0, size = bytes;
  while (size >= 1024 && i < units.length - 1) { size /= 1024; i++; }
  return `${size.toFixed(size < 10 && i > 0 ? 1 : 0)} ${units[i]}`;
}

function scrollToBottom() {
  elements.messages.scrollTop = elements.messages.scrollHeight;
}

// TYPING INDICATOR
let typingVisible = false;
function showTyping() {
  if (typingVisible) return;
  typingVisible = true;
  const li = document.createElement('li');
  li.className = 'message bot typing';
  li.dataset.typing = 'true';
  const bubble = document.createElement('div');
  bubble.className = 'bubble';
  const label = document.createElement('span');
  label.textContent = 'Digitando ';
  const dots = document.createElement('span');
  dots.className = 'dots';
  dots.innerHTML = '<span class="dot"></span><span class="dot"></span><span class="dot"></span>';
  bubble.appendChild(label);
  bubble.appendChild(dots);
  li.appendChild(bubble);
  elements.messages.appendChild(li);
  scrollToBottom();
}
function hideTyping() {
  const node = elements.messages.querySelector('li[data-typing="true"]');
  if (node) node.remove();
  typingVisible = false;
}

// BACKEND INTEGRATION
async function callBackend(userText) {
  showTyping();
  try {
    const response = await fetch('/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: userText })
    });
    const data = await response.json();
    hideTyping();

    const botResponses = data.responses || [];
    if (botResponses.length === 0) {
      appendMessage('bot', { type: 'text', text: 'Desculpe, não entendi. Pode repetir?' });
    } else {
      botResponses.forEach(reply => {
        appendMessage('bot', { type: 'text', text: reply });
      });
    }

    // Atualiza quick replies baseado na última mensagem, se desejar
    const dynamicSuggestions = suggestNext(userText);
    renderQuickReplies(dynamicSuggestions);

  } catch (error) {
    hideTyping();
    appendMessage('bot', { type: 'text', text: 'Erro ao se comunicar com o servidor.' });
    console.error(error);
  }
}

// SUGESTÕES dinâmicas simples (pode evoluir)
function suggestNext(text) {
  const t = text.toLowerCase();
  if (t.includes('boleto')) return ['Ver boleto', 'Gerar nova via'];
  if (t.includes('curso')) return ['Lista de cursos', 'Modalidades'];
  if (t.includes('matrícula')) return ['Ver status', 'Atualizar dados'];
  return ['Falar com atendente', 'Ajuda com login', 'Mais informações'];
}

// Mensagem de boas-vindas
appendMessage('bot', { type: 'text', text: 'Olá! Sou seu assistente virtual. Como posso ajudar?' });
