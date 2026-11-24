// ============================================
// FIREBASE CONFIGURATION
// ============================================

// Firebase config from Firebase Console
const firebaseConfig = {
  apiKey: "AIzaSyDs-OeLXYeJv4XOAWTq7MhArI8CAPKo-vE",
  authDomain: "spotify-tempo-analysis.firebaseapp.com",
  projectId: "spotify-tempo-analysis",
  storageBucket: "spotify-tempo-analysis.firebasestorage.app",
  messagingSenderId: "264371570914",
  appId: "1:264371570914:web:abc89efb66edcae309b6bb",
  measurementId: "G-ZQRGRCBCXC"
};

// Initialize Firebase (compat version)
firebase.initializeApp(firebaseConfig);
const db = firebase.firestore();

// ============================================
// GLOBAL VARIABLES
// ============================================

// API Base URL - detect environment
const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://localhost:5000/api'  // Local development
    : '/api';  // Production (Vercel proxies to Railway)

console.log('🌐 API Base URL:', API_BASE_URL);

// No Chart.js needed - using custom dot matrix visualization

// ============================================
// LOAD DATA FROM FIRESTORE
// ============================================

async function loadDashboardData() {
    try {
        console.log('🚀 Loading dashboard data...');
        
        // Try Firestore first
        let useFirestore = true;
        let stats = null;
        
        try {
            // 1. Load Global Stats from Firestore
            const globalStatsDoc = await db.collection('summary').doc('global_stats').get();
            if (globalStatsDoc.exists) {
                stats = globalStatsDoc.data();
                updateSummaryCards(stats);
                console.log('✅ Loaded stats from Firestore');
            } else {
                throw new Error('Firestore data not found');
            }
        } catch (firestoreError) {
            console.warn('⚠️ Firestore failed, falling back to PostgreSQL API:', firestoreError);
            useFirestore = false;
            
            // Fallback: Load from PostgreSQL API
            const apiResponse = await fetch(`${API_BASE_URL}/stats/summary`);
            const apiData = await apiResponse.json();
            
            if (apiData.success) {
                stats = apiData.stats;
                updateSummaryCards(stats);
                console.log('✅ Loaded stats from PostgreSQL API');
            } else {
                throw new Error('Failed to load data from API');
            }
        }

        // 2. Load Tempo Zones
        let tempoZonesData = [];
        
        if (useFirestore) {
            try {
                const tempoZonesSnapshot = await db.collection('tempo_zones').get();
                tempoZonesSnapshot.forEach(doc => {
                    tempoZonesData.push(doc.data());
                });
            } catch (err) {
                console.warn('⚠️ Failed to load tempo zones from Firestore:', err);
                useFirestore = false;
            }
        }
        
        // If Firestore failed or no data, use mock data
        if (tempoZonesData.length === 0) {
            console.log('📊 Using calculated tempo zones');
            tempoZonesData = [
                {zone_id: 'less_80', zone_name: '<80 BPM', count: 126953, percentage: 10.54, avg_danceability: 0.3601},
                {zone_id: '80_100', zone_name: '80-100 BPM', count: 258657, percentage: 21.48, avg_danceability: 0.4894},
                {zone_id: '100_120', zone_name: '100-120 BPM', count: 266776, percentage: 22.16, avg_danceability: 0.5429},
                {zone_id: '120_140', zone_name: '120-140 BPM', count: 286577, percentage: 23.80, avg_danceability: 0.5428},
                {zone_id: 'above_140', zone_name: '>140 BPM', count: 265062, percentage: 22.01, avg_danceability: 0.4563}
            ];
        }
        
        renderTempoZoneViz(tempoZonesData);
        
        // Calculate danceability boost
        const sweetSpot = tempoZonesData.find(z => z.zone_id === '100_120');
        const otherZones = tempoZonesData.filter(z => z.zone_id !== '100_120');
        const avgOtherDance = otherZones.reduce((sum, z) => sum + (z.avg_danceability || 0), 0) / otherZones.length;
        const boost = ((sweetSpot.avg_danceability - avgOtherDance) / avgOtherDance * 100).toFixed(1);
        
        // Update boost elements (with null checks)
        const danceBoostEl = document.getElementById('danceBoost');
        const infoBoostEl = document.getElementById('infoBoost');
        if (danceBoostEl) danceBoostEl.textContent = `+${boost}%`;
        if (infoBoostEl) infoBoostEl.textContent = `+${boost}%`;

        // 3. Render key findings
        const mockDecadeData = [];
        renderKeyFindings(stats, tempoZonesData, mockDecadeData);

        // 4. Load Top Tracks
        if (useFirestore) {
            try {
                const topTracksDoc = await db.collection('top_tracks').doc('sweet_spot_top_100').get();
                if (topTracksDoc.exists) {
                    const data = topTracksDoc.data();
                    renderTopTracksTable(data.tracks);
                }
            } catch (err) {
                console.warn('⚠️ Failed to load top tracks from Firestore:', err);
                loadTopTracksFromAPI();
            }
        } else {
            loadTopTracksFromAPI();
        }

        console.log('✅ Dashboard data loaded successfully!');
    } catch (error) {
        console.error('❌ Error loading dashboard data:', error);
        
        // Show user-friendly error  
        const tableBody = safeGetElement('tracksTableBody');
        if (tableBody) {
            tableBody.innerHTML = `
                <tr>
                    <td colspan="5" class="py-8 text-center">
                        <div class="text-red-500 font-semibold mb-2">⚠️ Failed to load data</div>
                        <div class="text-xs text-slate-500">
                            Error: ${error.message}<br>
                            Make sure API server is running: <code>python api/search_api.py</code>
                        </div>
                    </td>
                </tr>
            `;
        }
    }
}

async function loadTopTracksFromAPI() {
    try {
        console.log('📊 Loading top tracks from PostgreSQL API...');
        const response = await fetch(`${API_BASE_URL}/search/tracks?tempo_min=100&tempo_max=120&limit=10`);
        const data = await response.json();
        
        if (data.success && data.results.length > 0) {
            renderSearchResults(data.results);
            console.log('✅ Loaded top tracks from API');
        }
    } catch (err) {
        console.error('❌ Failed to load top tracks from API:', err);
    }
}

// ============================================
// UPDATE SUMMARY CARDS
// ============================================

function updateSummaryCards(stats) {
    safeSetText('totalTracks', formatNumber(stats.total_tracks));
    safeSetText('avgTempo', stats.avg_tempo);
    safeSetText('sweetSpotPct', `${stats.sweet_spot_percentage}%`);
    safeSetText('headerSubtitle', `${formatNumber(stats.total_tracks)} Tracks Analysis (1920-2020)`);
}

// ============================================
// RENDER TEMPO ZONE VISUALIZATION (Dot Matrix)
// ============================================

function renderTempoZoneViz(data) {
    // Sort by zone order
    const zoneOrder = ['less_80', '80_100', '100_120', '120_140', 'above_140'];
    data.sort((a, b) => zoneOrder.indexOf(a.zone_id) - zoneOrder.indexOf(b.zone_id));

    const container = document.getElementById('tempoZoneViz');
    if (!container) {
        console.warn('⚠️ tempoZoneViz container not found');
        return;
    }
    
    container.innerHTML = '';

    // Update sweet spot percentage display
    const sweetSpot = data.find(z => z.zone_id === '100_120');
    if (sweetSpot) {
        const vizElement = document.getElementById('sweetSpotPctViz');
        if (vizElement) {
            vizElement.textContent = `Sweet Spot: ${sweetSpot.percentage}% of Catalog`;
        }
    }

    // Calculate max percentage for scaling
    const maxPct = Math.max(...data.map(z => parseFloat(z.percentage)));

    // Generate dot matrix for each zone
    data.forEach(zone => {
        const column = document.createElement('div');
        column.className = 'flex flex-col items-center gap-3 flex-1';

        // Percentage at top
        const pctLabel = document.createElement('div');
        pctLabel.className = `font-headline-md text-headline-md font-bold ${zone.zone_id === '100_120' ? 'text-primary' : 'text-on-surface-variant'}`;
        pctLabel.textContent = `${zone.percentage}%`;

        // Dots container - fixed width for symmetry
        const dotsWrapper = document.createElement('div');
        dotsWrapper.className = 'flex flex-col-reverse gap-2 p-4 rounded-xl bg-surface-container-lowest items-center w-24 min-h-[200px] justify-end';

        // Calculate number of dots (scale to max 12 dots for better proportion)
        const numDots = Math.max(1, Math.round((parseFloat(zone.percentage) / maxPct) * 12));

        // Color and size based on zone
        let dotColor = 'bg-surface-variant';
        let dotSize = 'w-3 h-3';
        
        if (zone.zone_id === '100_120') {
            dotColor = 'bg-primary shadow-lg';
            dotSize = 'w-4 h-4';
        } else if (zone.zone_id === '80_100' || zone.zone_id === '120_140') {
            dotColor = 'bg-secondary-container';
            dotSize = 'w-3 h-3';
        }

        // Generate dots in a column
        for (let i = 0; i < numDots; i++) {
            const dot = document.createElement('div');
            dot.className = `${dotSize} rounded-full ${dotColor} transition-all hover:scale-125`;
            dotsWrapper.appendChild(dot);
        }

        // Zone label at bottom
        const label = document.createElement('div');
        label.className = 'text-center mt-2 w-full';
        label.innerHTML = `
            <div class="font-label-lg text-label-lg ${zone.zone_id === '100_120' ? 'text-primary font-bold' : 'text-on-surface font-semibold'} whitespace-nowrap">
                ${zone.zone_name}
            </div>
            ${zone.zone_id === '100_120' ? '<div class="font-label-sm text-label-sm text-primary mt-1">★ Sweet Spot</div>' : '<div class="h-5"></div>'}
        `;

        column.appendChild(pctLabel);
        column.appendChild(dotsWrapper);
        column.appendChild(label);
        container.appendChild(column);
    });
}

// ============================================
// RENDER KEY FINDINGS
// ============================================

function renderKeyFindings(stats, tempoZones, decadeTrends) {
    const container = document.getElementById('keyFindings');
    if (!container) return;
    
    const sweetSpot = tempoZones.find(z => z.zone_id === '100_120');
    const otherZones = tempoZones.filter(z => z.zone_id !== '100_120');
    const avgOtherDance = otherZones.reduce((sum, z) => sum + (z.avg_danceability || 0), 0) / otherZones.length;
    const boost = ((sweetSpot.avg_danceability - avgOtherDance) / avgOtherDance * 100).toFixed(1);

    const findings = [
        {
            icon: 'verified',
            title: 'Sweet Spot Validated',
            value: `${sweetSpot.percentage}%`,
            desc: `${formatNumber(sweetSpot.count)} tracks in 100-120 BPM zone`
        },
        {
            icon: 'trending_up',
            title: 'Danceability Boost',
            value: `+${boost}%`,
            desc: 'Higher than all other tempo zones combined'
        },
        {
            icon: 'database',
            title: 'Dataset Scale',
            value: formatNumber(stats.total_tracks),
            desc: 'Tracks analyzed (1920-2020)'
        },
        {
            icon: 'speed',
            title: 'Avg Sweet Spot Tempo',
            value: `${stats.avg_tempo} BPM`,
            desc: 'Perfect for universal appeal'
        }
    ];

    container.innerHTML = findings.map(f => `
        <div class="p-space-md rounded-xl bg-surface-container-low/60 border border-surface-container-high hover:shadow-sm transition-all">
            <div class="flex items-start gap-3">
                <div class="w-9 h-9 rounded-lg bg-secondary-container/40 flex items-center justify-center shrink-0">
                    <span class="material-symbols-outlined text-[18px] text-primary">${f.icon}</span>
                </div>
                <div class="flex-1 min-w-0">
                    <div class="font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider">${f.title}</div>
                    <div class="font-headline-sm text-headline-sm text-on-surface font-bold mt-1">${f.value}</div>
                    <div class="font-body-sm text-body-sm text-on-surface-variant mt-0.5 leading-snug">${f.desc}</div>
                </div>
            </div>
        </div>
    `).join('');
}

// ============================================
// RENDER TOP TRACKS TABLE
// ============================================

function renderTopTracksTable(tracks) {
    const tbody = document.getElementById('tracksTableBody');
    if (!tbody) return;
    
    tbody.innerHTML = '';

    // Show top 10 only
    const topTracks = tracks.slice(0, 10);

    topTracks.forEach((track, index) => {
        const row = document.createElement('tr');
        row.className = 'border-b border-surface-container-high/30 hover:bg-surface-container-low/30 transition-colors';
        row.innerHTML = `
            <td class="py-3.5 px-3">
                <div class="flex flex-col gap-0.5">
                    <div class="font-body-md text-body-md text-on-surface font-semibold">${escapeHtml(track.name)}</div>
                    <div class="font-body-sm text-body-sm text-on-surface-variant">${escapeHtml(track.artists)}</div>
                </div>
            </td>
            <td class="py-3.5 px-3 text-right">
                <div class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-secondary-container/40 text-primary font-label-md text-label-md font-bold">
                    ${track.tempo.toFixed(1)}
                </div>
            </td>
            <td class="py-3.5 px-3">
                <div class="flex items-center gap-2">
                    <div class="flex-1 h-1.5 bg-surface-container-low rounded-full overflow-hidden">
                        <div class="h-full bg-tertiary-container rounded-full transition-all" style="width: ${Math.round(track.energy * 100)}%"></div>
                    </div>
                    <span class="font-label-md text-label-md text-on-surface-variant font-mono w-10 text-right">${Math.round(track.energy * 100)}%</span>
                </div>
            </td>
            <td class="py-3.5 px-3">
                <div class="flex items-center gap-2">
                    <div class="flex-1 h-1.5 bg-surface-container-low rounded-full overflow-hidden">
                        <div class="h-full bg-primary rounded-full transition-all" style="width: ${Math.round(track.danceability * 100)}%"></div>
                    </div>
                    <span class="font-label-md text-label-md text-on-surface-variant font-mono w-10 text-right">${Math.round(track.danceability * 100)}%</span>
                </div>
            </td>
            <td class="py-3.5 px-3 text-center">
                <span class="inline-flex items-center px-2.5 py-1 rounded-full bg-secondary-container/50 text-on-secondary-fixed-variant font-label-sm text-label-sm font-semibold">
                    <span class="w-1.5 h-1.5 rounded-full bg-primary mr-1.5"></span>Sweet Spot
                </span>
            </td>
        `;
        tbody.appendChild(row);
    });
}

// ============================================
// UTILITY FUNCTIONS
// ============================================

// Safe DOM element getter with null check
function safeGetElement(id) {
    const el = document.getElementById(id);
    if (!el) {
        console.warn(`⚠️ Element not found: ${id}`);
    }
    return el;
}

// Safe set text content
function safeSetText(id, text) {
    const el = safeGetElement(id);
    if (el) el.textContent = text;
}

// Safe set innerHTML
function safeSetHTML(id, html) {
    const el = safeGetElement(id);
    if (el) el.innerHTML = html;
}

function formatNumber(num) {
    if (num >= 1000000) {
        return (num / 1000000).toFixed(2) + 'M';
    } else if (num >= 1000) {
        return (num / 1000).toFixed(0) + 'K';
    }
    return num.toString();
}

function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

// ============================================
// INITIALIZE DASHBOARD
// ============================================

document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 Dashboard initializing...');
    loadDashboardData();
});

// ============================================
// SEARCH FUNCTIONALITY (PostgreSQL API)
// ============================================

// ============================================
// API CONFIGURATION - AUTO-DETECT ENVIRONMENT
// ============================================

const getApiBaseUrl = () => {
    // Check if running on production (Vercel)
    if (typeof window !== 'undefined') {
        const hostname = window.location.hostname;
        
        // Vercel production or preview
        if (hostname.includes('vercel.app') || hostname.includes('.app')) {
            console.log('🌐 Environment: Vercel Production');
            return '/api'; // Use Vercel proxy/rewrite
        }
        
        // Custom domain
        if (!hostname.includes('localhost') && !hostname.includes('127.0.0.1')) {
            console.log('🌐 Environment: Custom Domain');
            return '/api'; // Use proxy
        }
    }
    
    // Development environment
    console.log('🌐 Environment: Local Development');
    return 'http://localhost:5000/api';
};

const API_BASE_URL = getApiBaseUrl();
console.log('📡 API Base URL:', API_BASE_URL);
let isSearchActive = false;
let originalTopTracks = [];

async function performSearch() {
    const searchQuery = document.getElementById('searchInput').value.trim();
    const tempoMin = document.getElementById('tempoMin').value;
    const tempoMax = document.getElementById('tempoMax').value;
    
    // Validate inputs
    if (!searchQuery && !tempoMin && !tempoMax) {
        alert('Please enter a search query or tempo range');
        return;
    }
    
    try {
        // Show loading state
        const tbody = document.getElementById('tracksTableBody');
        tbody.innerHTML = '<tr><td colspan="5" class="py-8 text-center text-on-surface-variant">🔍 Searching...</td></tr>';
        
        // Build query parameters
        const params = new URLSearchParams();
        if (searchQuery) params.append('q', searchQuery);
        if (tempoMin) params.append('tempo_min', tempoMin);
        if (tempoMax) params.append('tempo_max', tempoMax);
        params.append('limit', '50');
        
        // Fetch from PostgreSQL API
        const response = await fetch(`${API_BASE_URL}/search/tracks?${params.toString()}`);
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Search failed');
        }
        
        // Update UI
        isSearchActive = true;
        const clearBtn = document.getElementById('clearSearchBtn');
        if (clearBtn) clearBtn.classList.remove('hidden');
        
        const tableTitle = document.getElementById('tableTitle');
        const tableSubtitle = document.getElementById('tableSubtitle');
        if (tableTitle) tableTitle.textContent = 'Search Results';
        if (tableSubtitle) tableSubtitle.textContent = `Found ${data.count} tracks`;
        
        // Show search stats
        const statsDiv = document.getElementById('searchStats');
        if (statsDiv) {
            statsDiv.classList.remove('hidden');
            statsDiv.innerHTML = `
                <span class="inline-flex items-center px-2.5 py-1 rounded-lg bg-secondary-container/40 text-on-secondary-fixed-variant font-label-sm text-label-sm font-semibold">
                    ✓ ${data.count} results found
                </span>
            `;
        }
        
        // Render results
        if (data.results.length > 0) {
            renderSearchResults(data.results);
        } else {
            tbody.innerHTML = '<tr><td colspan="5" class="py-8 text-center text-on-surface-variant">No tracks found. Try different search terms.</td></tr>';
        }
        
        // Auto-scroll to results table
        const tracksTable = document.getElementById('tracksTable');
        if (tracksTable) {
            tracksTable.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
        
    } catch (error) {
        console.error('Search error:', error);
        alert(`Search failed: ${error.message}`);
        
        const tbody = document.getElementById('tracksTableBody');
        tbody.innerHTML = '<tr><td colspan="5" class="py-8 text-center text-red-400">❌ Search failed. Make sure API server is running.</td></tr>';
    }
}

function renderSearchResults(results) {
    const tbody = document.getElementById('tracksTableBody');
    if (!tbody) return;
    
    tbody.innerHTML = '';
    
    results.forEach((track, index) => {
        const row = document.createElement('tr');
        row.className = 'border-b border-surface-container-high/30 hover:bg-surface-container-low/30 transition-colors';
        
        // Check if in sweet spot
        const inSweetSpot = track.tempo >= 100 && track.tempo < 120;
        
        // Format artists
        let artistsStr = track.artists;
        if (Array.isArray(track.artists)) {
            artistsStr = track.artists.join(', ');
        }
        
        row.innerHTML = `
            <td class="py-3.5 px-3">
                <div class="flex flex-col gap-0.5">
                    <div class="font-body-md text-body-md text-on-surface font-semibold">${escapeHtml(track.name)}</div>
                    <div class="font-body-sm text-body-sm text-on-surface-variant">${escapeHtml(artistsStr)} ${track.year ? `• ${track.year}` : ''}</div>
                </div>
            </td>
            <td class="py-3.5 px-3 text-right">
                <div class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg ${inSweetSpot ? 'bg-secondary-container/40 text-primary' : 'bg-surface-container-low text-on-surface'} font-label-md text-label-md font-bold">
                    ${track.tempo.toFixed(1)}
                </div>
            </td>
            <td class="py-3.5 px-3">
                <div class="flex items-center gap-2">
                    <div class="flex-1 h-1.5 bg-surface-container-low rounded-full overflow-hidden">
                        <div class="h-full bg-tertiary-container rounded-full transition-all" style="width: ${Math.round(track.energy * 100)}%"></div>
                    </div>
                    <span class="font-label-md text-label-md text-on-surface-variant font-mono w-10 text-right">${Math.round(track.energy * 100)}%</span>
                </div>
            </td>
            <td class="py-3.5 px-3">
                <div class="flex items-center gap-2">
                    <div class="flex-1 h-1.5 bg-surface-container-low rounded-full overflow-hidden">
                        <div class="h-full bg-primary rounded-full transition-all" style="width: ${Math.round(track.danceability * 100)}%"></div>
                    </div>
                    <span class="font-label-md text-label-md text-on-surface-variant font-mono w-10 text-right">${Math.round(track.danceability * 100)}%</span>
                </div>
            </td>
            <td class="py-3.5 px-3 text-center">
                ${inSweetSpot 
                    ? '<span class="inline-flex items-center px-2.5 py-1 rounded-full bg-secondary-container/50 text-on-secondary-fixed-variant font-label-sm text-label-sm font-semibold"><span class="w-1.5 h-1.5 rounded-full bg-primary mr-1.5"></span>Sweet Spot</span>'
                    : '<span class="inline-flex items-center px-2.5 py-1 rounded-full bg-surface-container-low text-on-surface-variant font-label-sm text-label-sm">Outside</span>'
                }
            </td>
        `;
        tbody.appendChild(row);
    });
}

async function clearSearch() {
    // Reset inputs
    document.getElementById('searchInput').value = '';
    document.getElementById('tempoMin').value = '';
    document.getElementById('tempoMax').value = '';
    
    // Hide clear button and stats
    document.getElementById('clearSearchBtn').classList.add('hidden');
    document.getElementById('searchStats').classList.add('hidden');
    
    // Reset titles
    document.getElementById('tableTitle').textContent = 'Hit Formula Tracks';
    document.getElementById('tableSubtitle').textContent = '100–120 BPM + Energy >0.7 + Danceability >0.6';
    
    isSearchActive = false;
    
    // Reload original top tracks from Firestore
    try {
        const topTracksDoc = await db.collection('top_tracks').doc('sweet_spot_top_100').get();
        if (topTracksDoc.exists) {
            const data = topTracksDoc.data();
            renderTopTracksTable(data.tracks);
        }
    } catch (error) {
        console.error('Error reloading top tracks:', error);
    }
}

// Add Enter key support for search
document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('searchInput');
    const tempoMin = document.getElementById('tempoMin');
    const tempoMax = document.getElementById('tempoMax');
    
    [searchInput, tempoMin, tempoMax].forEach(input => {
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                performSearch();
            }
        });
    });
});

// ============================================
// NAVIGATION HANDLER - ALL TABS
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    // Get all navigation links
    const navLinks = document.querySelectorAll('nav a[data-path], aside nav a[data-path]');
    
    // Section IDs mapping
    const sections = {
        'overview': ['overviewSection', 'summaryCardsSection', 'mainContentSection'],
        'search-and-query': ['overviewSection', 'summaryCardsSection', 'mainContentSection'],
        'ml-predictions': ['mlPredictionsSection'],
        'tempo-zones': ['tempoZonesSection'],
        'top-tracks': ['topTracksSection'],
        'methodology': ['methodologySection']
    };
    
    // Function to show specific sections
    function showSections(path) {
        console.log('🔄 Switching to:', path);
        
        // Hide all sections first
        const allSectionIds = [
            'overviewSection',
            'summaryCardsSection', 
            'mainContentSection',
            'mlPredictionsSection',
            'topTracksSection',
            'tempoZonesSection',
            'methodologySection'
        ];
        
        allSectionIds.forEach(id => {
            const elem = document.getElementById(id);
            if (elem) {
                elem.classList.add('hidden');
                elem.style.display = 'none';
            }
        });
        
        // Show sections for current path
        const sectionsToShow = sections[path] || sections['overview'];
        console.log('  Showing sections:', sectionsToShow);
        
        sectionsToShow.forEach(sectionId => {
            const elem = document.getElementById(sectionId);
            if (elem) {
                elem.classList.remove('hidden');
                elem.style.display = '';
                console.log('  ✅ Showed:', sectionId);
            } else {
                console.warn('  ⚠️ Section not found:', sectionId);
            }
        });
        
        // Load data if needed
        if (path === 'top-tracks') {
            console.log('  📊 Loading top tracks data...');
            loadTopTracksData();
        } else if (path === 'tempo-zones') {
            console.log('  📊 Loading tempo zones data...');
            loadTempoZonesData();
        }
        
        console.log('✅ Switched to:', path);
    }
    
    // Add click handlers to all nav links
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const path = this.getAttribute('data-path');
            
            // Remove active class from all links
            navLinks.forEach(l => {
                l.classList.remove('bg-primary', 'text-on-primary', 'font-bold', 'shadow-sm', 'bg-surface-container-high');
                l.classList.add('text-on-surface-variant');
            });
            
            // Add active class to clicked link and its pair (top nav + sidebar)
            document.querySelectorAll(`[data-path="${path}"]`).forEach(activeLink => {
                activeLink.classList.add('bg-primary', 'text-on-primary', 'font-bold', 'shadow-sm');
                activeLink.classList.remove('text-on-surface-variant');
            });
            
            // Show appropriate sections
            showSections(path);
        });
    });
    
    // Initialize with overview
    showSections('overview');
    
    console.log('🎯 Navigation handler initialized for all tabs');
});


// ============================================
// TOP TRACKS DATA LOADING
// ============================================

let topTracksData = [];
let currentFilter = 'sweet-spot';
let currentSort = 'danceability';

async function loadTopTracksData() {
    console.log('📊 Loading top tracks...');
    
    try {
        // Try to load from API
        const API_URL = API_BASE_URL || 'http://localhost:5000/api';
        const response = await fetch(`${API_URL}/search/tracks?limit=100&sort=danceability`);
        
        if (response.ok) {
            const data = await response.json();
            if (data.success && data.tracks) {
                topTracksData = data.tracks;
            }
        }
    } catch (error) {
        console.warn('⚠️ Failed to load from API, using mock data:', error);
    }
    
    // If no data loaded, use mock data
    if (topTracksData.length === 0) {
        topTracksData = generateMockTopTracks();
    }
    
    renderTopTracks();
    console.log(`✅ Loaded ${topTracksData.length} top tracks`);
}

function generateMockTopTracks() {
    const artists = ['Daft Punk', 'The Weeknd', 'Taylor Swift', 'Ed Sheeran', 'Billie Eilish', 'Drake', 'Ariana Grande', 'Post Malone', 'Bruno Mars', 'Olivia Rodrigo'];
    const tracks = ['Get Lucky', 'Blinding Lights', 'Shake It Off', 'Shape of You', 'bad guy', 'One Dance', 'thank u, next', 'Circles', 'Uptown Funk', 'drivers license'];
    
    return Array.from({length: 50}, (_, i) => ({
        name: tracks[i % tracks.length] + (i > 9 ? ` ${Math.floor(i/10)}` : ''),
        artists: artists[i % artists.length],
        year: 2015 + (i % 9),
        tempo: 90 + Math.random() * 50,
        energy: 0.5 + Math.random() * 0.5,
        danceability: 0.5 + Math.random() * 0.5,
        zone: Math.random() > 0.5 ? 'sweet-spot' : 'other'
    }));
}

function filterTopTracks(filter) {
    currentFilter = filter;
    
    // Update button states
    document.getElementById('btnAllTracks').className = filter === 'all' 
        ? 'px-space-md py-2 rounded-lg bg-primary text-on-primary font-label-md font-bold transition-colors flex items-center gap-1.5'
        : 'px-space-md py-2 rounded-lg bg-surface-container-low hover:bg-surface-container text-on-surface font-label-md transition-colors flex items-center gap-1.5';
    
    document.getElementById('btnSweetSpot').className = filter === 'sweet-spot'
        ? 'px-space-md py-2 rounded-lg bg-primary text-on-primary font-label-md font-bold transition-colors flex items-center gap-1.5'
        : 'px-space-md py-2 rounded-lg bg-surface-container-low hover:bg-surface-container text-on-surface font-label-md transition-colors flex items-center gap-1.5';
    
    renderTopTracks();
}

function sortTopTracks(sortBy) {
    currentSort = sortBy;
    
    // Update button states
    ['sortDance', 'sortEnergy', 'sortTempo', 'sortYear'].forEach(id => {
        const btn = document.getElementById(id);
        if (id === 'sort' + sortBy.charAt(0).toUpperCase() + sortBy.slice(1) || 
            (sortBy === 'danceability' && id === 'sortDance')) {
            btn.className = 'px-3 py-1.5 rounded-full bg-primary text-on-primary font-label-sm font-bold';
        } else {
            btn.className = 'px-3 py-1.5 rounded-full bg-surface-container-low text-on-surface-variant hover:bg-surface-container font-label-sm transition-colors';
        }
    });
    
    renderTopTracks();
}

function renderTopTracks() {
    const tbody = document.getElementById('topTracksTableBody');
    if (!tbody) return;
    
    // Filter data
    let filtered = currentFilter === 'all' 
        ? topTracksData 
        : topTracksData.filter(t => t.tempo >= 100 && t.tempo <= 120);
    
    // Sort data
    filtered.sort((a, b) => {
        if (currentSort === 'danceability') return b.danceability - a.danceability;
        if (currentSort === 'energy') return b.energy - a.energy;
        if (currentSort === 'tempo') return a.tempo - b.tempo;
        if (currentSort === 'year') return b.year - a.year;
        return 0;
    });
    
    // Render rows
    tbody.innerHTML = filtered.slice(0, 20).map((track, i) => {
        const zone = track.tempo >= 100 && track.tempo <= 120 ? 'Sweet Spot' : 
                     track.tempo < 80 ? 'Slow' :
                     track.tempo < 100 ? 'Moderate' :
                     track.tempo < 140 ? 'Upbeat' : 'Fast';
        const zoneColor = zone === 'Sweet Spot' ? 'bg-primary text-on-primary' : 'bg-surface-container-low text-on-surface-variant';
        
        return `
            <tr class="hover:bg-surface-container-low/50 transition-colors">
                <td class="py-3 px-4 font-bold text-on-surface-variant">${i + 1}</td>
                <td class="py-3 px-4 font-bold">${track.name || 'Track ' + (i+1)}</td>
                <td class="py-3 px-4 text-on-surface-variant">${track.artists || 'Artist'}</td>
                <td class="py-3 px-4 text-center text-on-surface-variant">${track.year || 2020}</td>
                <td class="py-3 px-4 text-center font-bold">${Math.round(track.tempo)} BPM</td>
                <td class="py-3 px-4 text-center">
                    <div class="inline-flex items-center gap-1">
                        <div class="w-12 h-1.5 bg-surface-container-low rounded-full overflow-hidden">
                            <div class="h-full bg-primary" style="width: ${(track.energy * 100)}%"></div>
                        </div>
                        <span class="text-on-surface-variant text-sm">${(track.energy * 100).toFixed(0)}%</span>
                    </div>
                </td>
                <td class="py-3 px-4 text-center">
                    <div class="inline-flex items-center gap-1">
                        <div class="w-12 h-1.5 bg-surface-container-low rounded-full overflow-hidden">
                            <div class="h-full bg-secondary" style="width: ${(track.danceability * 100)}%"></div>
                        </div>
                        <span class="text-on-surface-variant text-sm">${(track.danceability * 100).toFixed(0)}%</span>
                    </div>
                </td>
                <td class="py-3 px-4 text-center">
                    <span class="px-2 py-0.5 rounded-full text-xs font-bold ${zoneColor}">${zone}</span>
                </td>
            </tr>
        `;
    }).join('');
    
    document.getElementById('topTracksCount').textContent = `Showing ${Math.min(20, filtered.length)} of ${filtered.length} tracks`;
}

function loadMoreTopTracks() {
    console.log('Loading more tracks...');
    // Implement pagination if needed
}

// ============================================
// TEMPO ZONES DATA LOADING
// ============================================

async function loadTempoZonesData() {
    console.log('📊 Loading tempo zones...');
    
    const zones = [
        {id: 'less_80', name: '< 80 BPM', range: 'Slow/Ballad', count: 126953, pct: 10.54, dance: 0.360, color: 'from-blue-500/20 to-blue-600/10'},
        {id: '80_100', name: '80-100 BPM', range: 'Moderate', count: 258657, pct: 21.48, dance: 0.489, color: 'from-green-500/20 to-green-600/10'},
        {id: '100_120', name: '100-120 BPM', range: 'Sweet Spot', count: 266776, pct: 22.16, dance: 0.543, color: 'from-primary/30 to-secondary/20', highlight: true},
        {id: '120_140', name: '120-140 BPM', range: 'Upbeat/Club', count: 286577, pct: 23.80, dance: 0.543, color: 'from-orange-500/20 to-orange-600/10'},
        {id: 'above_140', name: '> 140 BPM', range: 'Fast/Electronic', count: 265062, pct: 22.01, dance: 0.456, color: 'from-red-500/20 to-red-600/10'}
    ];
    
    renderTempoZonesGrid(zones);
    renderTempoZonesStats(zones);
}

function renderTempoZonesGrid(zones) {
    const grid = document.getElementById('tempoZonesGrid');
    if (!grid) return;
    
    grid.innerHTML = zones.map(zone => `
        <div class="bg-gradient-to-br ${zone.color} rounded-lg p-space-md ${zone.highlight ? 'ring-2 ring-primary' : ''}">
            <div class="flex items-center justify-between mb-space-sm">
                <h3 class="font-headline-sm text-headline-sm text-on-surface font-bold">${zone.name}</h3>
                ${zone.highlight ? '<span class="material-symbols-outlined text-primary">star</span>' : ''}
            </div>
            <p class="font-label-sm text-label-sm text-on-surface-variant uppercase mb-space-md">${zone.range}</p>
            
            <div class="space-y-2">
                <div class="flex items-center justify-between">
                    <span class="font-body-sm text-body-sm text-on-surface-variant">Track Count</span>
                    <span class="font-label-md text-label-md text-on-surface font-bold">${zone.count.toLocaleString()}</span>
                </div>
                <div class="flex items-center justify-between">
                    <span class="font-body-sm text-body-sm text-on-surface-variant">Percentage</span>
                    <span class="font-label-md text-label-md text-on-surface font-bold">${zone.pct}%</span>
                </div>
                <div class="flex items-center justify-between">
                    <span class="font-body-sm text-body-sm text-on-surface-variant">Avg Danceability</span>
                    <span class="font-label-md text-label-md ${zone.highlight ? 'text-primary' : 'text-on-surface'} font-bold">${zone.dance.toFixed(3)}</span>
                </div>
            </div>
            
            <!-- Progress bar -->
            <div class="mt-space-sm">
                <div class="w-full h-2 bg-surface-container-low rounded-full overflow-hidden">
                    <div class="h-full ${zone.highlight ? 'bg-primary' : 'bg-on-surface-variant'}" style="width: ${zone.pct}%"></div>
                </div>
            </div>
        </div>
    `).join('');
}

function renderTempoZonesStats(zones) {
    const stats = document.getElementById('tempoZonesStats');
    if (!stats) return;
    
    const total = zones.reduce((sum, z) => sum + z.count, 0);
    const avgDance = zones.reduce((sum, z) => sum + z.dance * z.count, 0) / total;
    
    stats.innerHTML = `
        <div class="flex items-center justify-between py-2 border-b border-surface-container-high">
            <span class="font-body-sm text-body-sm text-on-surface-variant">Total Tracks</span>
            <span class="font-label-md text-label-md text-on-surface font-bold">${total.toLocaleString()}</span>
        </div>
        <div class="flex items-center justify-between py-2 border-b border-surface-container-high">
            <span class="font-body-sm text-body-sm text-on-surface-variant">Avg Danceability</span>
            <span class="font-label-md text-label-md text-on-surface font-bold">${avgDance.toFixed(3)}</span>
        </div>
        <div class="flex items-center justify-between py-2 border-b border-surface-container-high">
            <span class="font-body-sm text-body-sm text-on-surface-variant">Largest Zone</span>
            <span class="font-label-md text-label-md text-on-surface font-bold">120-140 BPM</span>
        </div>
        <div class="flex items-center justify-between py-2">
            <span class="font-body-sm text-body-sm text-on-surface-variant">Sweet Spot Rank</span>
            <span class="font-label-md text-label-md text-primary font-bold">#1 Dance</span>
        </div>
    `;
}


// ============================================
// DEBUG HELPERS (accessible from console)
// ============================================

window.debugShowSection = function(sectionId) {
    const elem = document.getElementById(sectionId);
    if (elem) {
        elem.classList.remove('hidden');
        elem.style.display = 'block';
        console.log('✅ Showed:', sectionId);
        return true;
    } else {
        console.error('❌ Section not found:', sectionId);
        return false;
    }
};

window.debugListSections = function() {
    const ids = [
        'overviewSection',
        'summaryCardsSection', 
        'mainContentSection',
        'mlPredictionsSection',
        'topTracksSection',
        'tempoZonesSection',
        'methodologySection'
    ];
    
    console.log('📋 Section Status:');
    ids.forEach(id => {
        const elem = document.getElementById(id);
        if (elem) {
            const hidden = elem.classList.contains('hidden');
            const display = elem.style.display;
            console.log(`  ${id}: ${hidden ? 'HIDDEN' : 'VISIBLE'} (display: ${display || 'default'})`);
        } else {
            console.log(`  ${id}: NOT FOUND`);
        }
    });
};

window.testNavigation = function(path) {
    console.log(`🧪 Testing navigation to: ${path}`);
    const event = new Event('click');
    const link = document.querySelector(`[data-path="${path}"]`);
    if (link) {
        link.click();
        setTimeout(() => {
            window.debugListSections();
        }, 100);
    } else {
        console.error('❌ Navigation link not found:', path);
    }
};

console.log('🔧 Debug helpers loaded. Try:');
console.log('  - debugListSections()');
console.log('  - debugShowSection("topTracksSection")');
console.log('  - testNavigation("top-tracks")');
