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
    if (typeof newsData === 'undefined' || !Array.isArray(newsData)) {
        console.error("newsData is missing or invalid");
        gallery.innerHTML = '<p style="grid-column: 1/-1; text-align: center;">No news items loaded.</p>';
        return;
    }

    if (newsData.length === 0) {
        gallery.innerHTML = '<p style="grid-column: 1/-1; text-align: center;">No news items generated yet.</p>';
    }

    // Render Gallery Grid
    newsData.forEach(item => {
        const card = document.createElement('div');
        card.className = 'card';
        // Safety check for image
        let coverImg = 'placeholder.png'; // Fallback?
        if (item.content && item.content.general_summary && item.content.general_summary.image) {
            coverImg = `${item.assets_path}/${item.content.general_summary.image}`;
        }

        card.innerHTML = `
            <img src="${coverImg}" alt="${item.title}" class="card-img">
            <div class="card-body">
                <div class="card-title">${item.title}</div>
                <div class="card-meta"><i class="far fa-clock"></i> ${formatDate(item.date)}</div>
            </div>
        `;

        // Add click listener
        card.addEventListener('click', () => {
            console.log("Card clicked:", item.id);
            showDetail(item.id);
        });

        gallery.appendChild(card);
    });

    // Navigation and Routing
    backBtn.onclick = () => {
        showGallery();
        // Clear hash cleanly
        history.pushState(null, null, window.location.pathname + window.location.search);
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
        console.log("Showing detail for:", id);
        const item = newsData.find(n => n.id === id);
        if (!item) {
            console.error("Item not found:", id);
            return;
        }

        // Populate Data
        if (detailDate) detailDate.innerHTML = `<i class="far fa-calendar"></i> ${formatDate(item.date)}`;
        if (detailTitle) detailTitle.textContent = item.title;
        if (detailTitleText) detailTitleText.textContent = item.title;

        const tiktokSummary = (item.content && item.content.tiktok_summary) ? item.content.tiktok_summary : "No TikTok summary available.";
        if (detailTikTokText) detailTikTokText.textContent = tiktokSummary;

        // Full Description
        const parts = [];
        if (item.content.introduction && item.content.introduction.text) parts.push(item.content.introduction.text);
        if (item.content.development && item.content.development.text) parts.push(item.content.development.text);
        if (item.content.conclusion && item.content.conclusion.text) parts.push(item.content.conclusion.text);

        if (detailDescription) detailDescription.textContent = parts.join('\n\n');

        // Download Link
        if (downloadZipBtn) downloadZipBtn.href = item.zip_path;

        // Populate Images Grid
        if (detailCardsGrid) {
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
                    img.title = "Click to open full size";
                    img.onclick = () => window.open(img.src, '_blank');
                    detailCardsGrid.appendChild(img);
                }
            });
        }

        // Switch View
        galleryView.classList.add('hidden');
        detailView.classList.remove('hidden');
        window.scrollTo(0, 0);

        // Update URL if needed
        if (window.location.hash.slice(1) !== id) {
            history.pushState(null, null, `#${id}`);
        }
    }

    function formatDate(dateString) {
        if (!dateString) return 'Data nd';
        try {
            // Check if it's already formatted or timestamp
            const d = new Date(dateString);
            if (isNaN(d.getTime())) return dateString;
            return d.toLocaleDateString('pt-BR');
        } catch {
            return dateString;
        }
    }

    // Copy Utility
    window.copyContent = (elementId) => {
        const el = document.getElementById(elementId);
        if (!el) return;
        const text = el.textContent;
        navigator.clipboard.writeText(text).then(() => {
            alert('Copiado!');
        }).catch(err => {
            console.error('Failed to copy', err);
        });
    };
});
