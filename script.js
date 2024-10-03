const gallery = document.getElementById('gallery');
const loadingIndicator = document.getElementById('loading');

let page = 1;
const perPage = 20;
let allItems = [];

// Function to load all image files from the directories
async function loadAllImages() {
    try {
        const response = await fetch('image_list.json');
        const data = await response.json();
        
        allItems = [
            ...data.swatches.map(file => ({ type: 'swatch', filename: file })),
            ...data.palettes.map(file => ({ type: 'palette', filename: file }))
        ];
        
        // Shuffle the array to mix swatches and palettes
        allItems.sort(() => Math.random() - 0.5);
    } catch (error) {
        console.error('Error loading image data:', error);
    }
}

function createCard(item) {
    const card = document.createElement('div');
    card.className = 'color-card';
    
    const folder = item.type === 'swatch' ? 'color_swatches' : 'color_palettes';
    
    card.innerHTML = `
        <div class="color-swatch" style="background-image: url('${folder}/${item.filename}');"></div>
        <div class="color-info">
            <h3 class="color-name">Color ${item.type === 'swatch' ? 'Swatch' : 'Palette'}</h3>
            <a href="#" class="download-btn" data-filename="${item.filename}" data-type="${item.type}">Download</a>
        </div>
    `;
    
    return card;
}

async function loadColors() {
    loadingIndicator.style.display = 'block';
    
    if (allItems.length === 0) {
        await loadAllImages();
    }
    
    const fragment = document.createDocumentFragment();
    const start = (page - 1) * perPage;
    const end = start + perPage;
    
    for (let i = start; i < end && i < allItems.length; i++) {
        const card = createCard(allItems[i]);
        fragment.appendChild(card);
    }
    
    gallery.appendChild(fragment);
    
    // Initialize or reload Masonry layout
    if (page === 1) {
        new Masonry(gallery, {
            itemSelector: '.color-card',
            columnWidth: 250,
            gutter: 20,
            fitWidth: true
        });
    } else {
        msnry.appended(fragment);
    }
    
    page++;
    loadingIndicator.style.display = 'none';
}

// Initial load
loadColors();

// Infinite scroll
window.addEventListener('scroll', () => {
    if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 500) {
        loadColors();
    }
});

// Download functionality
gallery.addEventListener('click', (e) => {
    if (e.target.classList.contains('download-btn')) {
        e.preventDefault();
        const filename = e.target.getAttribute('data-filename');
        const type = e.target.getAttribute('data-type');
        const folder = type === 'palette' ? 'color_palettes' : 'color_swatches';
        const url = `${folder}/${filename}`;
        
        fetch(url)
            .then(response => response.blob())
            .then(blob => {
                const link = document.createElement('a');
                link.href = URL.createObjectURL(blob);
                link.download = filename;
                link.click();
                URL.revokeObjectURL(link.href);
            })
            .catch(console.error);
    }
});