function expandCard(card) {
    const truncatedContent = card.querySelector('.truncated-content');
    const fullContent = card.querySelector('.full-content');
    const truncatedText = truncatedContent.textContent.trim().replace(/"/g, '');

    if (truncatedText && truncatedText.endsWith('…')) {
       // card.style.position = 'absolute';
       card.style.transform = 'scale(1.2)'; // Increase width and height by 1.1 times
       card.style.transition = 'transform 0.3s ease'; // Smooth transition
       card.style.zIndex = '10';
        card.style.overflow = 'auto';
        card.classList.add('hover:shadow-gold-glow');
        truncatedContent.classList.add('hidden');
        fullContent.classList.remove('hidden');
    }
}

function shrinkCard(card) {
    card.style.position = '';
    card.style.zIndex = '';
    card.style.transform = 'scale(1)'; // Reset scale to original size
    card.style.transition = 'transform 0.3s ease'; // Smooth transition
    card.style.overflow = ''; // Reset overflow to default
    card.classList.remove('hover:shadow-gold-glow');
    card.classList.add('w-80','h-80')
    card.querySelector('.truncated-content').classList.remove('hidden');
    card.querySelector('.full-content').classList.add('hidden');
}


function clearCommentForm() {
    document.getElementById('comment-form').value = "";
}

function setHxGetAttribute() {
    const referredPage = Alpine.store('seedling').referred_page;
    const form = document.querySelector('form[method="dialog"]');
    form.setAttribute('hx-get', `/` + referredPage);
}