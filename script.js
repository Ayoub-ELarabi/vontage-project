document.addEventListener('DOMContentLoaded', () => {
    // --- State ---
    let state = {
        name: "Welcome User",
        bio: "This is your awesome bio.",
        pfp: "https://ui-avatars.com/api/?name=User&background=random",
        links: [
            { title: "My GitHub", url: "#" },
            { title: "Facebook", url: "https://facebook.com/" },
            { title: "YouTube", url: "https://youtube.com/" }
        ]
    };

    // --- DOM Elements ---
    const elements = {
        profileName: document.getElementById('profileName'),
        profileBio: document.getElementById('profileBio'),
        profileImage: document.getElementById('profileImage'),
        linksContainer: document.getElementById('linksContainer'),

        // Editor
        editorPanel: document.getElementById('editorPanel'),
        editToggleBtn: document.getElementById('editToggleBtn'),
        closeEditorBtn: document.getElementById('closeEditorBtn'),
        nameInput: document.getElementById('nameInput'),
        bioInput: document.getElementById('bioInput'),
        pfpInput: document.getElementById('pfpInput'),
        linksListEditor: document.getElementById('linksListEditor'),
        addLinkBtn: document.getElementById('addLinkBtn'),
        generateBtn: document.getElementById('generateBtn')
    };

    // --- Initialization ---
    function init() {
        // Only run app logic if we are on the main app page
        if (document.getElementById('profileName')) {
            loadStateFromUrl();
            renderProfile();
            setupEventListeners();
        }
    }

    // --- Toast Logic ---
    function showToast(message) {
        const toast = document.getElementById('toast');
        toast.textContent = message;
        toast.classList.add('visible');
        setTimeout(() => {
            toast.classList.remove('visible');
        }, 3000);
    }

    // --- URL Persistence Logic (Compressed) ---
    function loadStateFromUrl() {
        const params = new URLSearchParams(window.location.search);
        const data = params.get('data');
        if (data) {
            try {
                let jsonString;
                // 1. Try Decompressing (New Format)
                const decompressed = LZString.decompressFromEncodedURIComponent(data);

                if (decompressed) {
                    jsonString = decompressed;
                } else {
                    // 2. Fallback to Old Format (Base64)
                    try {
                        jsonString = decodeURIComponent(escape(atob(data)));
                    } catch (err) {
                        // If both fail, it's invalid
                        throw new Error("Invalid data format");
                    }
                }

                if (jsonString) {
                    const parsedState = JSON.parse(jsonString);
                    // Merge with default state
                    state = { ...state, ...parsedState };

                    // Hide Edit Button for Generated Profiles
                    if (elements.editToggleBtn) {
                        elements.editToggleBtn.style.display = 'none';
                    }
                }
            } catch (e) {
                console.error("Failed to load data from URL", e);
                showToast("Error retrieving profile data");
            }
        }
    }

    function saveStateToUrl() {
        try {
            const jsonString = JSON.stringify(state);
            // Compress: JSON String -> LZ-String Compressed URI
            const compressed = LZString.compressToEncodedURIComponent(jsonString);

            // Construct new URL
            const newUrl = `${window.location.protocol}//${window.location.host}${window.location.pathname}?data=${compressed}`;

            // Update browser history
            window.history.pushState({ path: newUrl }, '', newUrl);

            // Copy to clipboard
            navigator.clipboard.writeText(newUrl).then(() => {
                showToast("Link saved & URL copied (Shortened)!");
            }).catch(() => {
                showToast("Profile saved! (Manual copy needed)");
            });

            // Hide Edit Button after generation
            if (elements.editToggleBtn) {
                elements.editToggleBtn.style.display = 'none';
            }

        } catch (e) {
            console.error("Failed to save data to URL", e);
            showToast("Error: Profile data too large");
        }
    }

    // --- Rendering ---
    function renderProfile() {
        elements.profileName.textContent = state.name;
        elements.profileBio.textContent = state.bio;
        elements.profileImage.src = state.pfp;

        // Render Links
        elements.linksContainer.innerHTML = '';
        state.links.forEach(link => {
            if (!link.title || !link.url) return;

            const a = document.createElement('a');
            a.className = 'link-card';
            let finalUrl = link.url;
            if (!finalUrl.startsWith('http') && !finalUrl.startsWith('#')) {
                finalUrl = 'https://' + finalUrl;
            }
            a.href = finalUrl;
            a.textContent = link.title;
            a.target = "_blank";
            a.rel = "noopener noreferrer";
            elements.linksContainer.appendChild(a);
        });
    }

    // ... (Editor functions remain same, called by event listeners) ...

    function populateEditor() {
        elements.nameInput.value = state.name;
        elements.bioInput.value = state.bio;
        elements.pfpInput.value = state.pfp;
        renderEditorLinks();
    }

    function renderEditorLinks() {
        elements.linksListEditor.innerHTML = '';
        state.links.forEach((link, index) => {
            const item = document.createElement('div');
            item.className = 'link-editor-item';
            item.innerHTML = `
                <button class="remove-link-btn" data-index="${index}">
                    <i class="fa-solid fa-trash"></i>
                </button>
                <div class="form-group" style="margin-bottom:0.5rem">
                    <input type="text" value="${link.title}" class="link-title-input" data-index="${index}" placeholder="Link Title">
                </div>
                <div class="form-group" style="margin-bottom:0">
                    <input type="text" value="${link.url}" class="link-url-input" data-index="${index}" placeholder="https://...">
                </div>
            `;
            elements.linksListEditor.appendChild(item);
        });

        // Add listeners to new delete buttons
        document.querySelectorAll('.remove-link-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const index = parseInt(e.currentTarget.dataset.index);
                removeLink(index);
            });
        });
    }

    // --- State Updates ---
    function updateStateFromEditor(strict = true) {
        state.name = elements.nameInput.value;
        state.bio = elements.bioInput.value;
        state.pfp = elements.pfpInput.value || "https://ui-avatars.com/api/?name=" + encodeURIComponent(state.name);

        // Collect links
        const newLinks = [];
        const titleInputs = document.querySelectorAll('.link-title-input');
        const urlInputs = document.querySelectorAll('.link-url-input');

        titleInputs.forEach((input, index) => {
            const url = urlInputs[index].value;
            // Strict mode (for generating): requires both title and url
            // Non-strict mode (for editing): keeps everything so inputs don't vanish
            if (!strict || (input.value && url)) {
                newLinks.push({
                    title: input.value,
                    url: url
                });
            }
        });
        state.links = newLinks;
    }

    function addLink() {
        updateStateFromEditor(false); // Capture current inputs
        state.links.push({ title: "", url: "" });
        renderEditorLinks();
    }

    function removeLink(index) {
        updateStateFromEditor(false); // Capture current inputs
        state.links.splice(index, 1);
        renderEditorLinks();
    }

    // --- Event Listeners ---
    function setupEventListeners() {
        // Toggle Editor
        elements.editToggleBtn.addEventListener('click', () => {
            populateEditor();
            elements.editorPanel.classList.remove('hidden');
        });

        elements.closeEditorBtn.addEventListener('click', () => {
            elements.editorPanel.classList.add('hidden');
        });

        // Add/Remove Links
        elements.addLinkBtn.addEventListener('click', addLink);

        // Generate / Save
        elements.generateBtn.addEventListener('click', () => {
            updateStateFromEditor();
            renderProfile();
            saveStateToUrl();
            elements.editorPanel.classList.add('hidden');
        });
    }

    // Run
    // --- Legal Modal Logic ---
    const legalContent = {
        privacy: `
            <h3>Privacy Policy</h3>
            <p>At Vontage, we prioritize your privacy. This policy outlines how we handle your data.</p>
            <h3>Data Collection</h3>
            <p>Vontage does NOT collect, store, or transmit your personal data to any server. All data you enter (name, bio, links) is encoded directly into the URL you generate.</p>
            <h3>Cookies</h3>
            <p>We use local storage only to enhance your user experience (e.g., remembering your last session). We do not use cookies for tracking purposes.</p>
            <h3>Third-Party Services</h3>
            <p>This site may use Google AdSense to display advertisements. Google may use cookies to serve ads based on your prior visits to this website or other websites.</p>
        `,
        terms: `
            <h3>Terms of Service</h3>
            <p>By using Vontage, you agree to the following terms:</p>
            <h3>Usage License</h3>
            <p>Vontage is free to use for personal and commercial purposes. You may not use this tool for illegal activities or to distribute harmful content.</p>
            <h3>Disclaimer</h3>
            <p>The service is provided "as is". Vontage makes no warranties, expressed or implied, and hereby disclaims all other warranties including without limitation, implied warranties or conditions of merchantability.</p>
        `
    };

    function openLegalModal(type) {
        const modal = document.getElementById('legalModal');
        const title = document.getElementById('legalTitle');
        const content = document.getElementById('legalContent');

        if (type === 'privacy') {
            title.textContent = "Privacy Policy";
            content.innerHTML = legalContent.privacy;
        } else {
            title.textContent = "Terms of Service";
            content.innerHTML = legalContent.terms;
        }

        modal.classList.add('visible');
    }

    // --- Global Search Logic (Redirect to Guides) ---
    const globalSearchInput = document.getElementById('globalSearchInput');
    if (globalSearchInput) {
        globalSearchInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                const query = e.target.value.trim();
                if (query) {
                    window.location.href = `guides.html?q=${encodeURIComponent(query)}`;
                }
            }
        });
    }

    // --- Global Back-to-Top Button ---
    let backToTopBtn = document.getElementById('backToTop');
    if (!backToTopBtn) {
        backToTopBtn = document.createElement('button');
        backToTopBtn.id = 'backToTop';
        backToTopBtn.className = 'back-to-top';
        backToTopBtn.innerHTML = '&uarr;';
        backToTopBtn.title = 'Back to Top';
        document.body.appendChild(backToTopBtn);
    }

    window.addEventListener('scroll', () => {
        if (window.scrollY > 300) {
            backToTopBtn.classList.add('visible');
        } else {
            backToTopBtn.classList.remove('visible');
        }
    });

    backToTopBtn.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });

    // Initialize App
    init();
});
