// AMRE - 最小動作版
console.log('🎯 AMRE Minimal Version Loaded');

class AMREMinimal {
    constructor() {
        this.init();
    }

    init() {
        // 右上にシンプルなボタンを追加
        this.addButton();
    }

    addButton() {
        const button = document.createElement('button');
        button.innerHTML = '📊 データ抽出';
        button.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 999999;
            background: #3498db;
            color: white;
            border: none;
            padding: 10px 15px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
        `;
        
        button.addEventListener('click', () => this.extractData());
        document.body.appendChild(button);
    }

    extractData() {
        const hostname = window.location.hostname;
        let data = {};

        if (hostname.includes('dmm.co.jp')) {
            data = this.extractFANZA();
        } else if (hostname.includes('civitai.com')) {
            data = this.extractCivitai();
        } else {
            data = this.extractGeneric();
        }

        // 結果をコンソールに表示
        console.log('📊 抽出データ:', data);
        
        // クリップボードにコピー
        this.copyToClipboard(JSON.stringify(data, null, 2));
        alert('データを抽出してクリップボードにコピーしました！');
    }

    extractFANZA() {
        // 実際のページ構造に基づいて調整
        const products = [];
        
        // 色々なセレクターを試す
        const selectors = [
            '.productTile',
            '.tmb',
            '[data-product-id]',
            '.item',
            '.product-item',
            '.work-item'
        ];

        selectors.forEach(selector => {
            document.querySelectorAll(selector).forEach((item, index) => {
                if (index < 10) { // 最大10件
                    products.push({
                        title: this.getTextContent(item, ['h3', '.title', '.ttl', 'a[title]']),
                        price: this.getTextContent(item, ['.price', '.prc']),
                        link: this.getAttribute(item, 'a', 'href'),
                        selector: selector
                    });
                }
            });
        });

        return {
            site: 'FANZA',
            url: window.location.href,
            timestamp: new Date().toISOString(),
            products: products.filter(p => p.title) // タイトルがあるもののみ
        };
    }

    extractCivitai() {
        const models = [];
        
        // Civitaiの一般的なセレクター
        document.querySelectorAll('[data-testid*="model"], .model-card, .card').forEach((item, index) => {
            if (index < 10) {
                models.push({
                    title: this.getTextContent(item, ['h2', 'h3', '.title']),
                    type: this.getTextContent(item, ['.badge', '.tag']),
                    downloads: this.getTextContent(item, ['[title*="download"]', '.download']),
                    likes: this.getTextContent(item, ['[title*="like"]', '.like']),
                    link: this.getAttribute(item, 'a', 'href')
                });
            }
        });

        return {
            site: 'Civitai',
            url: window.location.href,
            timestamp: new Date().toISOString(),
            models: models.filter(m => m.title)
        };
    }

    extractGeneric() {
        // 汎用的な抽出
        const links = Array.from(document.querySelectorAll('a')).slice(0, 20).map(a => ({
            text: a.textContent.trim(),
            href: a.href
        })).filter(link => link.text);

        return {
            site: window.location.hostname,
            url: window.location.href,
            timestamp: new Date().toISOString(),
            title: document.title,
            links: links
        };
    }

    getTextContent(container, selectors) {
        for (const selector of selectors) {
            const element = container.querySelector(selector);
            if (element && element.textContent.trim()) {
                return element.textContent.trim();
            }
        }
        return '';
    }

    getAttribute(container, selector, attribute) {
        const element = container.querySelector(selector);
        return element ? element.getAttribute(attribute) : '';
    }

    copyToClipboard(text) {
        if (navigator.clipboard) {
            navigator.clipboard.writeText(text);
        } else {
            // フォールバック
            const textArea = document.createElement('textarea');
            textArea.value = text;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
        }
    }
}

// 初期化
new AMREMinimal();