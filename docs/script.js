document.addEventListener('DOMContentLoaded', () => {
    // Elements
    const galleryView = document.getElementById('gallery-view');
    const detailView = document.getElementById('detail-view');
    const gallery = document.getElementById('gallery');
    const backBtn = document.getElementById('back-btn');

    // Detail Elements
    const detailDate = document.getElementById('detail-date');
    const detailTitle = document.getElementById('detail-title');
    const detailTitleText = document.getElementById('detail-title-text');
    const detailTikTokText = document.getElementById('detail-tiktok-text');
    const detailDescription = document.getElementById('detail-description');
    const downloadZipBtn = document.getElementById('download-zip-btn');
    const detailCardsGrid = document.getElementById('detail-cards-grid');

    // State
    const currentPath = window.location.hash.slice(1);

    // Initial Render
    if (typeof newsData === 'undefined' || newsData.length === 0) {
        gallery.innerHTML = '<p style="grid-column: 1/-1; text-align: center;">No news items generated yet.</p>';
        return;
    }

    // Render Gallery Grid
    newsData.forEach(item => {
        const card = document.createElement('div');
        card.className = 'card';
        const coverImg = `${item.assets_path}/${item.content.general_summary.image}`;

        card.innerHTML = `
            <img src="${coverImg}" alt="${item.title}" class="card-img">
            <div class="card-body">
                <div class="card-title">${item.title}</div>
                <div class="card-meta"><i class="far fa-clock"></i> ${formatDate(item.date)}</div>
            </div>
        `;

        card.onclick = () => showDetail(item.id);
        gallery.appendChild(card);
    });

    // Navigation and Routing
    backBtn.onclick = () => {
        showGallery();
        history.pushState(null, null, ' ');
    };

    window.onpopstate = () => {
        const id = window.location.hash.slice(1);
        if (id) {
            showDetail(id);
        } else {
            showGallery();
        }
    };

    // Check initial hash
    if (currentPath) {
        showDetail(currentPath);
    }

    // View Functions
    function showGallery() {
        detailView.classList.add('hidden');
        galleryView.classList.remove('hidden');
        window.scrollTo(0, 0);
    }

    function showDetail(id) {
        const item = newsData.find(n => n.id === id);
        if (!item) return;

        // Populate Data
        detailDate.innerHTML = `<i class="far fa-calendar"></i> ${formatDate(item.date)}`;
        detailTitle.textContent = item.title;
        detailTitleText.textContent = item.title;

        const tiktokSummary = item.content.tiktok_summary || "No TikTok summary available.";
        detailTikTokText.textContent = tiktokSummary;

        // Full Description (Concatenating parts)
        const parts = [
            item.content.introduction.text,
            item.content.development.text,
            item.content.conclusion.text
        ].filter(Boolean).join('\n\n');

        detailDescription.textContent = parts;

        // Download Link
        downloadZipBtn.href = item.zip_path;

        // Populate Images Grid
        detailCardsGrid.innerHTML = '';
        const images = [
            'general_summary',
            'introduction',
            'development',
            'conclusion'
        ];

        images.forEach(key => {
            const imgData = item.content[key];
            if (imgData && imgData.image) {
                const img = document.createElement('img');
                img.src = `${item.assets_path}/${imgData.image}`;
                img.className = 'grid-img';
                img.onclick = () => window.open(img.src, '_blank');
                detailCardsGrid.appendChild(img);
            }
        });

        // Switch View
        galleryView.classList.add('hidden');
        detailView.classList.remove('hidden');
        window.scrollTo(0, 0);

        // Update URL
        if (window.location.hash.slice(1) !== id) {
            history.pushState(null, null, `#${id}`);
        }
    }

    function formatDate(dateString) {
        if (!dateString) return 'Invalid Date';
        // Handle YYYY-MM-DD or assume it's valid check
        try {
            return new Date(dateString).toLocaleDateString('pt-BR');
        } catch {
            return dateString;
        }
    }

    // Copy Utility
    window.copyContent = (elementId) => {
        const text = document.getElementById(elementId).textContent;
        navigator.clipboard.writeText(text).then(() => {
            alert('Copiado para a área de transferência!');
        });
    };
});
