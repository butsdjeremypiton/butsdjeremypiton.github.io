document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.feature-card').forEach(card => {
        const openBtn = card.querySelector('.open-details-btn');
        const closeBtn = card.querySelector('.close-details-btn');
        const details = card.querySelector('.project-details');

        if (!openBtn || !closeBtn || !details) return;

        openBtn.addEventListener('click', () => {
            details.classList.add('opened');
            document.body.classList.add('modal-open');
        });

        closeBtn.addEventListener('click', () => {
            details.classList.remove('opened');
            document.body.classList.remove('modal-open');
        });
    });
});
