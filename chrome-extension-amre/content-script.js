// AI Market Research Extension (AMRE) - Content Script
// AI生成収益化事業専用のデータ収集スクリプト

console.log('🚀 AMRE Content Script Loaded for:', window.location.hostname);

class AMRECollector {
    constructor() {
        this.claudeCodeEndpoint = 'http://localhost:8080/amre-data'; // MCPブリッジ経由
        this.currentSite = this.detectSite();
        this.init();
    }

    detectSite() {
        const hostname = window.location.hostname;
        if (hostname.includes('dmm.co.jp')) return 'fanza';
        if (hostname.includes('dlsite.com')) return 'dlsite'; 
        if (hostname.includes('auctions.yahoo.co.jp')) return 'yahoo';
        if (hostname.includes('civitai.com')) return 'civitai';
        return 'unknown';
    }

    init() {
        this.addAMREUI();
        this.setupAutoCollector();
        
        // サイト別の初期化
        switch(this.currentSite) {
            case 'fanza':
                this.initFanzaCollector();
                break;
            case 'yahoo':
                this.initYahooCollector();
                break;
            case 'civitai':
                this.initCivitaiCollector();
                break;
            case 'dlsite':
                this.initDLsiteCollector();
                break;
        }
    }

    addAMREUI() {
        // 固定UI要素を追加
        const amrePanel = document.createElement('div');
        amrePanel.id = 'amre-panel';
        amrePanel.innerHTML = `
            <div class="amre-header">
                <h3>🎯 AMRE</h3>
                <div class="amre-status">準備完了</div>
            </div>
            <div class="amre-controls">
                <button id="amre-collect">📊 データ収集</button>
                <button id="amre-save">💾 Obsidian保存</button>
                <button id="amre-analyze">🔍 AI分析</button>
            </div>
            <div class="amre-results">
                <div id="amre-data-count">データ件数: 0</div>
                <div id="amre-last-update">最終更新: 未実行</div>
            </div>
        `;
        
        document.body.appendChild(amrePanel);

        // イベントリスナー
        document.getElementById('amre-collect').addEventListener('click', () => this.collectData());
        document.getElementById('amre-save').addEventListener('click', () => this.saveToObsidian());
        document.getElementById('amre-analyze').addEventListener('click', () => this.analyzeWithAI());
    }

    // === FANZA同人市場調査 ===
    initFanzaCollector() {
        console.log('🎯 FANZA Collector initialized');
        this.updateStatus('FANZA対応済み');
    }

    collectFanzaData() {
        const data = {
            site: 'fanza',
            url: window.location.href,
            timestamp: new Date().toISOString(),
            products: []
        };

        // 商品一覧ページの場合
        const productItems = document.querySelectorAll('li[data-product-id], .productTile, .tmb');
        productItems.forEach((item, index) => {
            try {
                const productData = {
                    id: item.getAttribute('data-product-id') || index,
                    title: this.extractText(item, 'a[title], .title, .ttl'),
                    price: this.extractText(item, '.price, .prc'),
                    rating: this.extractText(item, '.rating, .star'),
                    thumbnail: this.extractAttribute(item, 'img', 'src'),
                    link: this.extractAttribute(item, 'a', 'href'),
                    tags: this.extractTags(item),
                    salesInfo: this.extractSalesInfo(item)
                };
                
                data.products.push(productData);
            } catch (e) {
                console.warn('FANZA product extraction error:', e);
            }
        });

        // 個別商品ページの場合
        if (data.products.length === 0 && this.isProductDetailPage()) {
            data.productDetail = this.extractProductDetails();
        }

        return data;
    }

    // === ヤフオク調査 ===
    initYahooCollector() {
        console.log('🛒 Yahoo Auction Collector initialized');
        this.updateStatus('ヤフオク対応済み');
    }

    collectYahooData() {
        const data = {
            site: 'yahoo',
            url: window.location.href,
            timestamp: new Date().toISOString(),
            auctions: []
        };

        // オークション一覧
        const auctionItems = document.querySelectorAll('.Product, .Item, .auction-item');
        auctionItems.forEach((item, index) => {
            try {
                const auctionData = {
                    id: index,
                    title: this.extractText(item, '.Product__title, .auction-title, h3'),
                    currentPrice: this.extractText(item, '.Product__price, .price'),
                    bidCount: this.extractText(item, '.Product__bid, .bid-count'),
                    timeLeft: this.extractText(item, '.Product__time, .time-left'),
                    thumbnail: this.extractAttribute(item, 'img', 'src'),
                    link: this.extractAttribute(item, 'a', 'href'),
                    seller: this.extractSellerInfo(item),
                    isAI: this.detectAIContent(item)
                };
                
                data.auctions.push(auctionData);
            } catch (e) {
                console.warn('Yahoo auction extraction error:', e);
            }
        });

        return data;
    }

    // === Civitai調査 ===
    initCivitaiCollector() {
        console.log('🎨 Civitai Collector initialized');
        this.updateStatus('Civitai対応済み');
    }

    collectCivitaiData() {
        const data = {
            site: 'civitai',
            url: window.location.href,
            timestamp: new Date().toISOString(),
            models: []
        };

        // モデル一覧
        const modelItems = document.querySelectorAll('[data-testid="model-card"], .model-item');
        modelItems.forEach((item, index) => {
            try {
                const modelData = {
                    id: index,
                    name: this.extractText(item, '.model-name, h3, .title'),
                    type: this.extractText(item, '.model-type, .badge'),
                    downloads: this.extractText(item, '.download-count'),
                    likes: this.extractText(item, '.like-count'),
                    rating: this.extractText(item, '.rating'),
                    thumbnail: this.extractAttribute(item, 'img', 'src'),
                    link: this.extractAttribute(item, 'a', 'href'),
                    tags: this.extractTags(item),
                    prompts: this.extractPrompts(item)
                };
                
                data.models.push(modelData);
            } catch (e) {
                console.warn('Civitai model extraction error:', e);
            }
        });

        return data;
    }

    // === DLsite調査 ===
    initDLsiteCollector() {
        console.log('🎮 DLsite Collector initialized'); 
        this.updateStatus('DLsite対応済み');
    }

    collectDLsiteData() {
        const data = {
            site: 'dlsite',
            url: window.location.href,
            timestamp: new Date().toISOString(),
            products: []
        };

        // 商品一覧
        const productItems = document.querySelectorAll('.search_result_img_box, .product-item');
        productItems.forEach((item, index) => {
            try {
                const productData = {
                    id: index,
                    title: this.extractText(item, '.work_name, .title'),
                    price: this.extractText(item, '.work_price, .price'),
                    dlCount: this.extractText(item, '.dl_count'),
                    rating: this.extractText(item, '.star, .rating'),
                    thumbnail: this.extractAttribute(item, 'img', 'src'),
                    link: this.extractAttribute(item, 'a', 'href'),
                    circle: this.extractText(item, '.maker_name, .circle'),
                    tags: this.extractTags(item)
                };
                
                data.products.push(productData);
            } catch (e) {
                console.warn('DLsite product extraction error:', e);
            }
        });

        return data;
    }

    // === 共通ユーティリティ ===
    extractText(container, selector) {
        const element = container.querySelector(selector);
        return element ? element.textContent.trim() : '';
    }

    extractAttribute(container, selector, attribute) {
        const element = container.querySelector(selector);
        return element ? element.getAttribute(attribute) : '';
    }

    extractTags(container) {
        const tagElements = container.querySelectorAll('.tag, .genre, .category');
        return Array.from(tagElements).map(tag => tag.textContent.trim());
    }

    extractPrompts(container) {
        const promptElements = container.querySelectorAll('[data-prompt], .prompt-text');
        return Array.from(promptElements).map(prompt => prompt.textContent.trim());
    }

    detectAIContent(container) {
        const text = container.textContent.toLowerCase();
        const aiKeywords = ['ai', '人工知能', 'stable diffusion', 'midjourney', 'dalle', '生成', 'generated'];
        return aiKeywords.some(keyword => text.includes(keyword));
    }

    // === データ処理 ===
    async collectData() {
        this.updateStatus('データ収集中...');
        
        let collectedData;
        switch(this.currentSite) {
            case 'fanza':
                collectedData = this.collectFanzaData();
                break;
            case 'yahoo':
                collectedData = this.collectYahooData();
                break;
            case 'civitai':
                collectedData = this.collectCivitaiData();
                break;
            case 'dlsite':
                collectedData = this.collectDLsiteData();
                break;
            default:
                this.updateStatus('非対応サイト');
                return;
        }

        // ローカルストレージに保存
        const storageKey = `amre_data_${this.currentSite}_${Date.now()}`;
        await chrome.storage.local.set({ [storageKey]: collectedData });
        
        this.updateDataCount(collectedData);
        this.updateStatus('収集完了');
        
        console.log('📊 Collected data:', collectedData);
        return collectedData;
    }

    async saveToObsidian() {
        this.updateStatus('Obsidian保存中...');
        
        // 最新のデータを取得
        const storage = await chrome.storage.local.get(null);
        const latestData = Object.entries(storage)
            .filter(([key]) => key.startsWith(`amre_data_${this.currentSite}`))
            .sort(([a], [b]) => b.localeCompare(a))[0];

        if (!latestData) {
            this.updateStatus('保存データなし');
            return;
        }

        const [key, data] = latestData;
        
        // MCPブリッジ経由でObsidianに保存
        try {
            const obsidianData = this.formatForObsidian(data);
            await this.sendToClaudeCode('save_obsidian', obsidianData);
            this.updateStatus('Obsidian保存完了');
        } catch (error) {
            console.error('Obsidian save error:', error);
            this.updateStatus('保存エラー');
        }
    }

    async analyzeWithAI() {
        this.updateStatus('AI分析中...');
        
        try {
            // Claude Code経由でAI分析を実行
            await this.sendToClaudeCode('ai_analyze', { site: this.currentSite });
            this.updateStatus('AI分析完了');
        } catch (error) {
            console.error('AI analysis error:', error);
            this.updateStatus('分析エラー');
        }
    }

    formatForObsidian(data) {
        const timestamp = new Date().toISOString().slice(0, 10);
        const siteName = this.currentSite.toUpperCase();
        
        return {
            filename: `市場調査_${siteName}_${timestamp}.md`,
            content: `# ${siteName}市場調査レポート

## 調査概要
- **日時**: ${data.timestamp}
- **URL**: ${data.url}
- **データ件数**: ${this.getDataCount(data)}

## 収集データ
${this.formatDataForMarkdown(data)}

## 分析ポイント
- 売れ筋傾向
- 価格帯分析  
- 人気タグ・ジャンル
- 競合状況

#市場調査 #${siteName} #AI生成収益化
`,
            path: `03_Technical/市場調査/${siteName}/`
        };
    }

    formatDataForMarkdown(data) {
        // サイト別のマークダウン整形
        switch(data.site) {
            case 'fanza':
                return this.formatFanzaMarkdown(data);
            case 'yahoo':
                return this.formatYahooMarkdown(data);
            case 'civitai':
                return this.formatCivitaiMarkdown(data);
            case 'dlsite':
                return this.formatDLsiteMarkdown(data);
            default:
                return JSON.stringify(data, null, 2);
        }
    }

    async sendToClaudeCode(action, data) {
        // MCPブリッジ経由でClaude Codeと通信
        const message = {
            action: action,
            data: data,
            timestamp: new Date().toISOString()
        };
        
        // WebSocket or HTTP経由でClaude Codeに送信
        // 実装は後で詳細化
        console.log('🔄 Sending to Claude Code:', message);
    }

    // === UI更新 ===
    updateStatus(status) {
        const statusElement = document.querySelector('.amre-status');
        if (statusElement) {
            statusElement.textContent = status;
        }
    }

    updateDataCount(data) {
        const count = this.getDataCount(data);
        const countElement = document.getElementById('amre-data-count');
        const updateElement = document.getElementById('amre-last-update');
        
        if (countElement) countElement.textContent = `データ件数: ${count}`;
        if (updateElement) updateElement.textContent = `最終更新: ${new Date().toLocaleTimeString()}`;
    }

    getDataCount(data) {
        if (data.products) return data.products.length;
        if (data.auctions) return data.auctions.length;
        if (data.models) return data.models.length;
        return 0;
    }

    setupAutoCollector() {
        // ページ変更の監視
        let lastUrl = location.href;
        new MutationObserver(() => {
            const url = location.href;
            if (url !== lastUrl) {
                lastUrl = url;
                console.log('🔄 Page changed, reinitializing AMRE...');
                setTimeout(() => this.init(), 1000);
            }
        }).observe(document, { subtree: true, childList: true });
    }
}

// AMRE初期化
const amre = new AMRECollector();