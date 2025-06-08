// AMRE - AI Market Research Extension Background Script

class AMREBackground {
    constructor() {
        this.claudeCodeEndpoint = 'http://localhost:8080/amre-api';
        this.syncInterval = 300000; // 5分間隔
        this.init();
    }

    init() {
        // インストール時の初期化
        chrome.runtime.onInstalled.addListener(() => {
            this.onInstall();
        });

        // メッセージハンドリング
        chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
            this.handleMessage(message, sender, sendResponse);
            return true; // 非同期レスポンスを有効化
        });

        // ストレージ変更の監視
        chrome.storage.onChanged.addListener((changes, namespace) => {
            this.onStorageChanged(changes, namespace);
        });

        // 定期同期の開始
        this.startPeriodicSync();

        console.log('🚀 AMRE Background Script initialized');
    }

    async onInstall() {
        console.log('📦 AMRE Extension installed');
        
        // 初期設定
        await chrome.storage.local.set({
            'amre_version': '1.0.0',
            'amre_install_date': new Date().toISOString(),
            'amre_settings': {
                autoSync: true,
                claudeCodeIntegration: true,
                obsidianAutoSave: true,
                collectOnPageLoad: false,
                syncInterval: 300000
            }
        });

        // 統計情報の初期化
        await chrome.storage.local.set({
            'amre_stats': {
                totalCollections: 0,
                lastSync: null,
                sitesSupported: ['fanza', 'dlsite', 'yahoo', 'civitai']
            }
        });

        // Claude Codeに登録通知
        this.notifyClaudeCode('extension_installed', {
            version: '1.0.0',
            timestamp: new Date().toISOString()
        });
    }

    async handleMessage(message, sender, sendResponse) {
        const { action, data } = message;

        try {
            switch (action) {
                case 'collectData':
                    const result = await this.handleDataCollection(data, sender.tab);
                    sendResponse({ success: true, ...result });
                    break;

                case 'saveToObsidian':
                    await this.saveToObsidian(data);
                    sendResponse({ success: true });
                    break;

                case 'syncWithClaudeCode':
                    await this.syncWithClaudeCode(data);
                    sendResponse({ success: true });
                    break;

                case 'getStats':
                    const stats = await this.getStats();
                    sendResponse({ success: true, stats });
                    break;

                case 'updateSettings':
                    await this.updateSettings(data);
                    sendResponse({ success: true });
                    break;

                default:
                    sendResponse({ success: false, error: 'Unknown action' });
            }
        } catch (error) {
            console.error('Message handling error:', error);
            sendResponse({ success: false, error: error.message });
        }
    }

    async handleDataCollection(data, tab) {
        console.log('📊 Handling data collection:', data);

        // データ処理とストレージ保存
        const processedData = await this.processCollectedData(data);
        const storageKey = `amre_data_${data.site}_${Date.now()}`;
        
        await chrome.storage.local.set({
            [storageKey]: {
                ...processedData,
                tabInfo: {
                    id: tab.id,
                    url: tab.url,
                    title: tab.title
                },
                timestamp: new Date().toISOString()
            }
        });

        // 統計情報の更新
        await this.updateStats('collection', data.site);

        // Claude Codeに通知
        if (await this.isClaudeCodeIntegrationEnabled()) {
            this.notifyClaudeCode('data_collected', {
                site: data.site,
                count: processedData.items?.length || 0,
                url: tab.url
            });
        }

        return {
            count: processedData.items?.length || 0,
            storageKey: storageKey
        };
    }

    async processCollectedData(rawData) {
        // データの正規化と品質向上
        const processed = {
            site: rawData.site,
            url: rawData.url,
            collectionTime: new Date().toISOString(),
            items: [],
            metadata: {
                userAgent: navigator.userAgent,
                timestamp: Date.now(),
                dataQuality: 'high'
            }
        };

        // サイト別のデータ処理
        switch (rawData.site) {
            case 'fanza':
                processed.items = await this.processFanzaData(rawData.products || []);
                break;
            case 'yahoo':
                processed.items = await this.processYahooData(rawData.auctions || []);
                break;
            case 'civitai':
                processed.items = await this.processCivitaiData(rawData.models || []);
                break;
            case 'dlsite':
                processed.items = await this.processDLsiteData(rawData.products || []);
                break;
        }

        return processed;
    }

    async processFanzaData(products) {
        return products.map(product => ({
            ...product,
            priceNumeric: this.extractNumericPrice(product.price),
            ratingNumeric: this.extractNumericRating(product.rating),
            tags: this.normalizeTags(product.tags),
            aiGenerated: this.detectAIContent(product.title + ' ' + (product.tags || []).join(' '))
        }));
    }

    async processYahooData(auctions) {
        return auctions.map(auction => ({
            ...auction,
            currentPriceNumeric: this.extractNumericPrice(auction.currentPrice),
            bidCountNumeric: this.extractNumericNumber(auction.bidCount),
            timeLeftMinutes: this.extractTimeInMinutes(auction.timeLeft),
            aiGenerated: this.detectAIContent(auction.title)
        }));
    }

    async processCivitaiData(models) {
        return models.map(model => ({
            ...model,
            downloadsNumeric: this.extractNumericNumber(model.downloads),
            likesNumeric: this.extractNumericNumber(model.likes),
            ratingNumeric: this.extractNumericRating(model.rating),
            tags: this.normalizeTags(model.tags),
            prompts: this.normalizePrompts(model.prompts)
        }));
    }

    async processDLsiteData(products) {
        return products.map(product => ({
            ...product,
            priceNumeric: this.extractNumericPrice(product.price),
            dlCountNumeric: this.extractNumericNumber(product.dlCount),
            ratingNumeric: this.extractNumericRating(product.rating),
            tags: this.normalizeTags(product.tags)
        }));
    }

    // === ユーティリティ関数 ===
    extractNumericPrice(priceText) {
        if (!priceText) return 0;
        const match = priceText.replace(/[^\d]/g, '');
        return parseInt(match) || 0;
    }

    extractNumericRating(ratingText) {
        if (!ratingText) return 0;
        const match = ratingText.match(/[\d.]+/);
        return parseFloat(match?.[0]) || 0;
    }

    extractNumericNumber(numberText) {
        if (!numberText) return 0;
        const match = numberText.replace(/[^\d]/g, '');
        return parseInt(match) || 0;
    }

    extractTimeInMinutes(timeText) {
        if (!timeText) return 0;
        // "2時間30分" -> 150分 など
        const hours = (timeText.match(/(\d+)時間/) || [])[1] || 0;
        const minutes = (timeText.match(/(\d+)分/) || [])[1] || 0;
        return parseInt(hours) * 60 + parseInt(minutes);
    }

    normalizeTags(tags) {
        if (!Array.isArray(tags)) return [];
        return tags
            .map(tag => tag.trim().toLowerCase())
            .filter(tag => tag.length > 0)
            .slice(0, 20); // 最大20個
    }

    normalizePrompts(prompts) {
        if (!Array.isArray(prompts)) return [];
        return prompts
            .map(prompt => prompt.trim())
            .filter(prompt => prompt.length > 0)
            .slice(0, 10); // 最大10個
    }

    detectAIContent(text) {
        if (!text) return false;
        const aiKeywords = [
            'ai', 'artificial intelligence', '人工知能', 'stable diffusion',
            'midjourney', 'dalle', '生成', 'generated', 'neural', 'deep learning'
        ];
        const lowercaseText = text.toLowerCase();
        return aiKeywords.some(keyword => lowercaseText.includes(keyword));
    }

    // === Obsidian連携 ===
    async saveToObsidian(data) {
        console.log('💾 Saving to Obsidian:', data);

        // 最新のデータを取得
        const storage = await chrome.storage.local.get(null);
        const latestDataKey = Object.keys(storage)
            .filter(key => key.startsWith(`amre_data_${data.site}`))
            .sort()
            .pop();

        if (!latestDataKey) {
            throw new Error('保存するデータが見つかりません');
        }

        const collectedData = storage[latestDataKey];
        const obsidianData = this.formatForObsidian(collectedData);

        // Claude Code MCP経由でObsidianに保存
        await this.notifyClaudeCode('save_obsidian', obsidianData);
    }

    formatForObsidian(data) {
        const timestamp = new Date().toISOString().slice(0, 10);
        const siteName = data.site.toUpperCase();
        
        let content = `# ${siteName}市場調査レポート

## 調査概要
- **日時**: ${data.collectionTime}
- **URL**: ${data.url}
- **データ件数**: ${data.items.length}

## 収集データ

`;

        // サイト別のフォーマット
        switch (data.site) {
            case 'fanza':
                content += this.formatFanzaForMarkdown(data.items);
                break;
            case 'yahoo':
                content += this.formatYahooForMarkdown(data.items);
                break;
            case 'civitai':
                content += this.formatCivitaiForMarkdown(data.items);
                break;
            case 'dlsite':
                content += this.formatDLsiteForMarkdown(data.items);
                break;
        }

        content += `

## 分析ポイント
- 売れ筋傾向の把握
- 価格帯分析
- 人気タグ・ジャンルの特定
- 競合状況の確認

#市場調査 #${siteName} #AI生成収益化
`;

        return {
            filename: `市場調査_${siteName}_${timestamp}.md`,
            content: content,
            path: `03_Technical/市場調査/${siteName}/`
        };
    }

    formatFanzaForMarkdown(items) {
        return items.slice(0, 10).map((item, index) => `
### ${index + 1}. ${item.title}
- **価格**: ${item.price} (${item.priceNumeric}円)
- **評価**: ${item.rating}
- **タグ**: ${item.tags.join(', ')}
- **AI生成**: ${item.aiGenerated ? 'はい' : 'いいえ'}
`).join('\n');
    }

    formatYahooForMarkdown(items) {
        return items.slice(0, 10).map((item, index) => `
### ${index + 1}. ${item.title}
- **現在価格**: ${item.currentPrice} (${item.currentPriceNumeric}円)
- **入札数**: ${item.bidCount}
- **残り時間**: ${item.timeLeft}
- **AI関連**: ${item.aiGenerated ? 'はい' : 'いいえ'}
`).join('\n');
    }

    formatCivitaiForMarkdown(items) {
        return items.slice(0, 10).map((item, index) => `
### ${index + 1}. ${item.name}
- **タイプ**: ${item.type}
- **ダウンロード数**: ${item.downloads}
- **いいね数**: ${item.likes}
- **タグ**: ${item.tags.join(', ')}
- **プロンプト例**: ${item.prompts.slice(0, 2).join('; ')}
`).join('\n');
    }

    formatDLsiteForMarkdown(items) {
        return items.slice(0, 10).map((item, index) => `
### ${index + 1}. ${item.title}
- **価格**: ${item.price} (${item.priceNumeric}円)
- **DL数**: ${item.dlCount}
- **サークル**: ${item.circle}
- **タグ**: ${item.tags.join(', ')}
`).join('\n');
    }

    // === Claude Code連携 ===
    async notifyClaudeCode(action, data) {
        if (!(await this.isClaudeCodeIntegrationEnabled())) {
            return;
        }

        try {
            const response = await fetch(this.claudeCodeEndpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    action: action,
                    data: data,
                    timestamp: new Date().toISOString(),
                    source: 'amre_extension'
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            const result = await response.json();
            console.log('🔗 Claude Code response:', result);
            return result;
        } catch (error) {
            console.warn('Claude Code communication failed:', error);
            // 通信エラーは警告として扱い、機能停止しない
        }
    }

    async isClaudeCodeIntegrationEnabled() {
        const settings = await chrome.storage.local.get('amre_settings');
        return settings.amre_settings?.claudeCodeIntegration ?? true;
    }

    // === 統計管理 ===
    async updateStats(action, site = null) {
        const stats = await chrome.storage.local.get('amre_stats');
        const currentStats = stats.amre_stats || {
            totalCollections: 0,
            lastSync: null,
            sitesSupported: ['fanza', 'dlsite', 'yahoo', 'civitai']
        };

        switch (action) {
            case 'collection':
                currentStats.totalCollections++;
                currentStats.lastCollection = new Date().toISOString();
                if (site) {
                    currentStats[`${site}Collections`] = (currentStats[`${site}Collections`] || 0) + 1;
                }
                break;
            case 'sync':
                currentStats.lastSync = new Date().toISOString();
                break;
        }

        await chrome.storage.local.set({ amre_stats: currentStats });
    }

    async getStats() {
        const stats = await chrome.storage.local.get('amre_stats');
        return stats.amre_stats || {};
    }

    // === 設定管理 ===
    async updateSettings(newSettings) {
        const current = await chrome.storage.local.get('amre_settings');
        const updated = {
            ...current.amre_settings,
            ...newSettings
        };
        await chrome.storage.local.set({ amre_settings: updated });
    }

    // === 定期同期 ===
    startPeriodicSync() {
        setInterval(async () => {
            await this.performSync();
        }, this.syncInterval);
    }

    async performSync() {
        console.log('🔄 Performing periodic sync...');
        
        try {
            // Claude Codeとの同期
            if (await this.isClaudeCodeIntegrationEnabled()) {
                await this.syncWithClaudeCode();
            }

            await this.updateStats('sync');
        } catch (error) {
            console.error('Sync error:', error);
        }
    }

    async syncWithClaudeCode() {
        // 同期データの準備
        const storage = await chrome.storage.local.get(null);
        const dataKeys = Object.keys(storage).filter(key => key.startsWith('amre_data_'));
        
        if (dataKeys.length === 0) return;

        // 最新データをClaude Codeに送信
        const syncData = {
            totalItems: dataKeys.length,
            latestCollection: storage[dataKeys.sort().pop()],
            stats: await this.getStats()
        };

        await this.notifyClaudeCode('sync_data', syncData);
    }

    onStorageChanged(changes, namespace) {
        // ストレージ変更時の処理
        if (namespace === 'local') {
            Object.keys(changes).forEach(key => {
                if (key.startsWith('amre_data_')) {
                    console.log('📁 New data stored:', key);
                }
            });
        }
    }
}

// バックグラウンドスクリプト初期化
const amreBackground = new AMREBackground();