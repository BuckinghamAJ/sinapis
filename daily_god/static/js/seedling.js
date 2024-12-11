function expandCard(card) {
    const truncatedContent = card.querySelector('.truncated-content');
    const fullContent = card.querySelector('.full-content');
    const truncatedText = truncatedContent.textContent.trim().replace(/"/g, '');
    
    if (truncatedText && truncatedText.endsWith('…')) {
       // card.style.position = 'absolute';
        card.style.zIndex = '10';
        card.classList.remove('w-80','h-80')
        card.classList.add('hover:shadow-gold-glow', 'h-96', 'w-96', 'overflow-auto');
        truncatedContent.classList.add('hidden');
        fullContent.classList.remove('hidden');
    }
}

function shrinkCard(card) {
    card.style.position = '';
    card.style.zIndex = '';
    card.classList.remove('hover:shadow-gold-glow', 'h-96', 'w-96', 'overflow-auto');
    card.classList.add('w-80','h-80')
    card.querySelector('.truncated-content').classList.remove('hidden');
    card.querySelector('.full-content').classList.add('hidden');
}