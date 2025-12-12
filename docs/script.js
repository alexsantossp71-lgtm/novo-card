document.addEventListener('DOMContentLoaded', () => {
    const gallery = document.getElementById('gallery');
    const modal = document.getElementById('modal');
    const modalBody = document.getElementById('modal-body');
    const closeBtn = document.querySelector('.close-btn');

    // Render Cards
    if (typeof newsData === 'undefined' || newsData.length === 0) {
        gallery.innerHTML = '<p style="grid-column: 1/-1; text-align: center;">No news items generated yet.</p>';
        return;
    }

    newsData.forEach(item => {
        const card = document.createElement('div');
        card.className = 'card';

        // Use general_summary image as cover
        const coverImg = `${item.assets_path}/${item.content.general_summary.image}`;

        card.innerHTML = `
            <img src="${coverImg}" alt="${item.title}" class="card-img" onclick="openModal('${item.id}')">
            <div class="card-body">
                <div class="card-title">${item.title}</div>
                <div class="card-meta"><i class="far fa-clock"></i> ${new Date(item.date).toLocaleDateString('pt-BR')}</div>
                <div class="btn-group">
                    <a href="${item.zip_path}" class="btn btn-download" download>
                        <i class="fas fa-download"></i> Download ZIP
                    </a>
                    <button class="btn" onclick="openModal('${item.id}')">
                        <i class="fas fa-eye"></i> View Details
                    </button>
                    <button class="btn" onclick="copyToClipboard('${escapeText(item.content.tiktok_summary)}', 'TikTok Summary')">
                        <i class="fab fa-tiktok"></i> Copy Caption
                    </button>
                </div>
            </div>
        `;
        gallery.appendChild(card);
    });

    // Modal Logic
    window.openModal = (id) => {
        const item = newsData.find(n => n.id === id);
        if (!item) return;

        let html = `<h2>${item.title}</h2>`;

        // Sections to display
        const sections = [
            { key: 'general_summary', label: 'Capa / General' },
            { key: 'introduction', label: 'Introdução' },
            { key: 'development', label: 'Desenvolvimento' },
            { key: 'conclusion', label: 'Conclusão' }
        ];

        sections.forEach(sec => {
            const content = item.content[sec.key];
            const imgPath = `${item.assets_path}/${content.image}`;

            html += `
                <div class="detail-section">
                    <div>
                        <img src="${imgPath}" class="detail-img">
                        <br>
                        <a href="${imgPath}" download class="btn" style="margin-top:5px; width:100%; justify-content:center;">Download Image</a>
                    </div>
                    <div class="detail-text">
                        <h3>${sec.label}</h3>
                        ${content.text ? `<p><strong>Texto:</strong> ${content.text} <i class="fas fa-copy copy-icon" onclick="copyToClipboard('${escapeText(content.text)}')"></i></p>` : ''}
                        ${content.prompt ? `<div class="prompt-box"><strong>Prompt:</strong> ${content.prompt} <i class="fas fa-copy copy-icon" onclick="copyToClipboard('${escapeText(content.prompt)}')"></i></div>` : ''}
                    </div>
                </div>
            `;
        });

        modalBody.innerHTML = html;
        modal.classList.remove('hidden');
    };

    // Close Modal
    closeBtn.onclick = () => modal.classList.add('hidden');
    window.onclick = (e) => {
        if (e.target == modal) modal.classList.add('hidden');
    };

    // Utils
    window.copyToClipboard = (text, type = "Text") => {
        navigator.clipboard.writeText(text).then(() => {
            alert(`${type} copied to clipboard!`);
        });
    };

    function escapeText(text) {
        if (!text) return '';
        return text.replace(/'/g, "\\'").replace(/"/g, '&quot;').replace(/\n/g, '\\n');
    }
});
