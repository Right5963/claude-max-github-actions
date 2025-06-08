// AMRE - AI Market Research Extension Popup Script

class AMREPopup {
    constructor() {
        this.currentTab = null;
        this.currentSite = 'unknown';
        this.isCollecting = false;
        this.init();
    }

    async init() {
        // 現在のタブ情報を取得
        await this.getCurrentTab();
        
        // サイト検出
        this.detectCurrentSite();
        
        // 統計情報の読み込み
        await this.loadStats();
        
        // イベントリスナーの設定
        this.setupEventListeners();
        
        // ステータス更新
        this.updateStatus('準備完了');
    }

    async getCurrentTab() {
        try {
            const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
            this.currentTab = tab;
        } catch (error) {
            console.error('Tab query error:', error);
        }
    }

    detectCurrentSite() {
        if (!this.currentTab?.url) {
            this.updateSiteInfo('不明', 'unsupported');
            return;
        }

        const url = this.currentTab.url;
        const hostname = new URL(url).hostname;

        // サイト検出ロジック
        if (hostname.includes('dmm.co.jp')) {
            this.currentSite = 'fanza';
            this.updateSiteInfo('FANZA', 'supported');
        } else if (hostname.includes('dlsite.com')) {
            this.currentSite = 'dlsite';
            this.updateSiteInfo('DLsite', 'supported');
        } else if (hostname.includes('auctions.yahoo.co.jp')) {
            this.currentSite = 'yahoo';
            this.updateSiteInfo('ヤフオク', 'supported');
        } else if (hostname.includes('civitai.com')) {
            this.currentSite = 'civitai';
            this.updateSiteInfo('Civitai', 'supported');
        } else {
            this.currentSite = 'unknown';
            this.updateSiteInfo('未対応', 'unsupported');
        }
    }

    updateSiteInfo(siteName, status) {
        const siteNameElement = document.getElementById('current-site');
        const siteStatusElement = document.getElementById('site-status');
        
        if (siteNameElement) {
            siteNameElement.textContent = siteName;
        }
        
        if (siteStatusElement) {
            siteStatusElement.textContent = status === 'supported' ? '✅ 対応' : '❌ 未対応';
            siteStatusElement.className = `site-status ${status}`;
        }
    }

    setupEventListeners() {
        // データ収集ボタン
        document.getElementById('collect-current')?.addEventListener('click', () => {
            this.collectCurrentPage();
        });

        document.getElementById('collect-bulk')?.addEventListener('click', () => {
            this.collectBulk();
        });

        // データ管理ボタン
        document.getElementById('save-obsidian')?.addEventListener('click', () => {
            this.saveToObsidian();
        });

        document.getElementById('export-json')?.addEventListener('click', () => {
            this.exportJSON();
        });

        // AI分析ボタン
        document.getElementById('analyze-trends')?.addEventListener('click', () => {
            this.analyzeTrends();
        });

        document.getElementById('analyze-competitors')?.addEventListener('click', () => {
            this.analyzeCompetitors();
        });

        // 設定・ヘルプボタン
        document.getElementById('open-options')?.addEventListener('click', () => {
            chrome.runtime.openOptionsPage();
        });

        document.getElementById('open-help')?.addEventListener('click', () => {
            this.openHelp();
        });

        document.getElementById('open-logs')?.addEventListener('click', () => {
            this.openLogs();
        });

        // クイックアクセスボタン
        document.querySelectorAll('.quick-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const site = e.target.getAttribute('data-site');
                this.quickAccess(site, e.target.id);
            });
        });
    }

    async collectCurrentPage() {
        if (this.isCollecting) return;
        if (this.currentSite === 'unknown') {
            this.updateStatus('未対応のサイトです', 'error');
            return;
        }

        this.isCollecting = true;
        this.updateStatus('データ収集中...', 'loading');
        this.showProgress();

        try {
            // Content scriptにメッセージを送信
            const response = await chrome.tabs.sendMessage(this.currentTab.id, {
                action: 'collectData',
                site: this.currentSite
            });

            if (response && response.success) {
                await this.updateStats();
                this.updateStatus(`${response.count}件のデータを収集しました`, 'success');
            } else {
                this.updateStatus('データ収集に失敗しました', 'error');
            }
        } catch (error) {
            console.error('Collection error:', error);
            this.updateStatus('エラーが発生しました', 'error');
        } finally {
            this.isCollecting = false;
            this.hideProgress();
        }
    }

    async collectBulk() {
        this.updateStatus('一括収集機能は開発中です', 'loading');
        // TODO: 複数ページの一括収集機能
    }

    async saveToObsidian() {
        this.updateStatus('Obsidianに保存中...', 'loading');
        this.showProgress();

        try {
            // Content scriptにメッセージを送信
            const response = await chrome.tabs.sendMessage(this.currentTab.id, {
                action: 'saveToObsidian',
                site: this.currentSite
            });

            if (response && response.success) {
                this.updateStatus('Obsidianに保存しました', 'success');
            } else {
                this.updateStatus('保存に失敗しました', 'error');
            }
        } catch (error) {
            console.error('Save error:', error);
            this.updateStatus('保存エラーが発生しました', 'error');
        } finally {
            this.hideProgress();
        }
    }

    async exportJSON() {
        this.updateStatus('JSON出力中...', 'loading');

        try {
            // ストレージからデータを取得
            const storage = await chrome.storage.local.get(null);
            const siteData = Object.entries(storage)
                .filter(([key]) => key.startsWith(`amre_data_${this.currentSite}`))
                .reduce((acc, [key, value]) => {
                    acc[key] = value;
                    return acc;
                }, {});

            // JSONファイルとしてダウンロード
            const blob = new Blob([JSON.stringify(siteData, null, 2)], {
                type: 'application/json'
            });
            const url = URL.createObjectURL(blob);
            
            await chrome.downloads.download({
                url: url,
                filename: `amre_${this.currentSite}_${new Date().toISOString().slice(0, 10)}.json`
            });

            this.updateStatus('JSONファイルをダウンロードしました', 'success');
        } catch (error) {
            console.error('Export error:', error);
            this.updateStatus('エクスポートに失敗しました', 'error');
        }
    }

    async analyzeTrends() {
        this.updateStatus('トレンド分析中...', 'loading');
        this.showProgress();

        try {
            // Claude Code APIに分析リクエストを送信
            const response = await this.sendToClaudeCode('analyze_trends', {
                site: this.currentSite,
                timeframe: '7d'
            });

            if (response && response.success) {
                this.updateStatus('トレンド分析が完了しました', 'success');
                // 分析結果を新しいタブで開く
                this.openAnalysisResults(response.analysisUrl);
            } else {
                this.updateStatus('分析に失敗しました', 'error');
            }
        } catch (error) {
            console.error('Analysis error:', error);
            this.updateStatus('分析エラーが発生しました', 'error');
        } finally {
            this.hideProgress();
        }
    }

    async analyzeCompetitors() {
        this.updateStatus('競合分析中...', 'loading');
        // TODO: 競合分析機能の実装
    }

    async quickAccess(site, buttonId) {
        const urls = {
            'fanza-ranking': 'https://www.dmm.co.jp/dc/doujin/-/list/=/sort=ranking/',
            'yahoo-ai-auctions': 'https://auctions.yahoo.co.jp/search/search?p=AI%20%E3%82%A4%E3%83%A9%E3%82%B9%E3%83%88&tab_ex=commerce',
            'civitai-trending': 'https://civitai.com/models?sort=Most%20Reactions&period=Week',
            'dlsite-new': 'https://www.dlsite.com/maniax/new'
        };

        const url = urls[buttonId];
        if (url) {
            await chrome.tabs.create({ url: url });
            window.close();
        }
    }

    async loadStats() {
        try {
            const storage = await chrome.storage.local.get(null);
            
            // 今日の収集数を計算
            const today = new Date().toISOString().slice(0, 10);
            const todayCount = Object.keys(storage)
                .filter(key => key.startsWith('amre_data_') && key.includes(today))
                .length;

            // 総収集数を計算
            const totalCount = Object.keys(storage)
                .filter(key => key.startsWith('amre_data_'))
                .length;

            // 最終更新時刻を取得
            const lastUpdate = await chrome.storage.local.get('amre_last_update');
            const lastUpdateTime = lastUpdate.amre_last_update || '未実行';

            // UIを更新
            this.updateStatsUI(todayCount, totalCount, lastUpdateTime);
        } catch (error) {
            console.error('Stats loading error:', error);
        }
    }

    async updateStats() {
        // 統計情報を更新してUIに反映
        await chrome.storage.local.set({
            'amre_last_update': new Date().toLocaleTimeString()
        });
        await this.loadStats();
    }

    updateStatsUI(todayCount, totalCount, lastUpdate) {
        const todayElement = document.getElementById('today-count');
        const totalElement = document.getElementById('total-count');
        const updateElement = document.getElementById('last-update');

        if (todayElement) todayElement.textContent = todayCount;
        if (totalElement) totalElement.textContent = totalCount;
        if (updateElement) updateElement.textContent = lastUpdate;
    }

    updateStatus(message, type = '') {
        const statusElement = document.getElementById('status-message');
        if (statusElement) {
            statusElement.textContent = message;
            statusElement.className = `status-message ${type}`;
        }
    }

    showProgress() {
        const progressBar = document.getElementById('progress-bar');
        if (progressBar) {
            progressBar.style.display = 'block';
        }
    }

    hideProgress() {
        const progressBar = document.getElementById('progress-bar');
        if (progressBar) {
            progressBar.style.display = 'none';
        }
    }

    async sendToClaudeCode(action, data) {
        // Claude Code MCPブリッジとの通信
        try {
            const response = await fetch('http://localhost:8080/amre-api', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    action: action,
                    data: data,
                    timestamp: new Date().toISOString()
                })
            });

            return await response.json();
        } catch (error) {
            console.error('Claude Code communication error:', error);
            return { success: false, error: error.message };
        }
    }

    openAnalysisResults(url) {
        if (url) {
            chrome.tabs.create({ url: url });
        }
    }

    openHelp() {
        chrome.tabs.create({ 
            url: 'https://github.com/your-username/amre-extension/wiki'
        });
    }

    openLogs() {
        chrome.tabs.create({ 
            url: chrome.runtime.getURL('logs.html')
        });
    }
}

// ポップアップ初期化
document.addEventListener('DOMContentLoaded', () => {
    new AMREPopup();
});

// メッセージリスナー（バックグラウンドスクリプトからの通信）
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === 'updateStats') {
        // 統計情報の更新
        const popup = new AMREPopup();
        popup.loadStats();
    }
});