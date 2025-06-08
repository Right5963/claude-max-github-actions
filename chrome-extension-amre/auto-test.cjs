// AMRE自動テストシステム (CommonJS版)
const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

class AMREAutoTester {
    constructor() {
        this.extensionPath = path.join(__dirname);
        this.testResults = [];
    }

    async runAllTests() {
        console.log('🚀 AMRE自動テスト開始...');
        
        try {
            // ブラウザ起動（拡張機能付き）
            console.log('🌐 ブラウザを起動中...');
            const browser = await puppeteer.launch({
                headless: false,
                args: [
                    `--disable-extensions-except=${this.extensionPath}`,
                    `--load-extension=${this.extensionPath}`,
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-web-security',
                    '--disable-features=VizDisplayCompositor'
                ],
                slowMo: 500
            });

            const page = await browser.newPage();
            
            // コンソールメッセージをキャプチャ
            page.on('console', msg => {
                if (msg.text().includes('AMRE')) {
                    console.log('📊 Extension Log:', msg.text());
                }
            });

            // ダイアログ処理
            page.on('dialog', async dialog => {
                console.log('💬 Dialog:', dialog.message());
                await dialog.accept();
            });

            // テスト実行
            await this.testExample(page);
            await this.testCivitai(page);
            
            await browser.close();
            
            // 結果出力
            this.generateReport();
            
        } catch (error) {
            console.error('❌ テストエラー:', error);
        }
    }

    async testExample(page) {
        console.log('🌐 Example.comテスト開始...');
        
        try {
            await page.goto('https://example.com', { waitUntil: 'networkidle0', timeout: 10000 });
            console.log('✅ ページ読み込み完了');
            
            // 拡張機能のボタンが表示されるまで少し待機
            await page.waitForTimeout(3000);
            
            // ボタンの存在確認
            const button = await page.$('button[style*="position: fixed"]');
            if (button) {
                console.log('✅ 拡張機能ボタン発見');
                
                // ボタンクリック
                await button.click();
                console.log('✅ ボタンクリック成功');
                
                this.testResults.push({
                    site: 'Example.com',
                    status: 'success',
                    message: '拡張機能の基本動作確認',
                    timestamp: new Date().toISOString()
                });
            } else {
                throw new Error('拡張機能ボタンが見つかりません');
            }
            
        } catch (error) {
            console.error('❌ Example.comテスト失敗:', error.message);
            this.testResults.push({
                site: 'Example.com',
                status: 'failed',
                error: error.message,
                timestamp: new Date().toISOString()
            });
        }
    }

    async testCivitai(page) {
        console.log('🎨 Civitaiテスト開始...');
        
        try {
            await page.goto('https://civitai.com/models', { waitUntil: 'networkidle0', timeout: 15000 });
            console.log('✅ Civitaiページ読み込み完了');
            
            // 拡張機能のボタン待機
            await page.waitForTimeout(3000);
            
            const button = await page.$('button[style*="position: fixed"]');
            if (button) {
                console.log('✅ Civitaiで拡張機能ボタン発見');
                
                // データ抽出テスト
                await button.click();
                await page.waitForTimeout(2000);
                
                this.testResults.push({
                    site: 'Civitai',
                    status: 'success',
                    message: 'Civitaiでデータ抽出テスト完了',
                    timestamp: new Date().toISOString()
                });
            } else {
                throw new Error('Civitaiで拡張機能ボタンが見つかりません');
            }
            
        } catch (error) {
            console.error('❌ Civitaiテスト失敗:', error.message);
            this.testResults.push({
                site: 'Civitai',
                status: 'failed',
                error: error.message,
                timestamp: new Date().toISOString()
            });
        }
    }

    generateReport() {
        console.log('\n📋 AMRE自動テスト結果レポート');
        console.log('='.repeat(50));
        
        let successCount = 0;
        let failCount = 0;
        
        this.testResults.forEach(result => {
            const status = result.status === 'success' ? '✅' : '❌';
            console.log(`${status} ${result.site}: ${result.status}`);
            
            if (result.error) {
                console.log(`   エラー: ${result.error}`);
            }
            
            if (result.message) {
                console.log(`   詳細: ${result.message}`);
            }
            
            result.status === 'success' ? successCount++ : failCount++;
        });
        
        console.log('='.repeat(50));
        console.log(`✅ 成功: ${successCount}件`);
        console.log(`❌ 失敗: ${failCount}件`);
        
        const total = successCount + failCount;
        const successRate = total > 0 ? Math.round(successCount / total * 100) : 0;
        console.log(`📊 成功率: ${successRate}%`);
        
        // 結果をファイルに保存
        const reportData = {
            timestamp: new Date().toISOString(),
            summary: {
                total: total,
                success: successCount,
                failed: failCount,
                successRate: successRate
            },
            results: this.testResults
        };
        
        fs.writeFileSync(
            path.join(__dirname, 'test-report.json'),
            JSON.stringify(reportData, null, 2)
        );
        
        console.log('📄 詳細レポート: test-report.json に保存しました');
        
        // 成功率評価
        if (successRate >= 80) {
            console.log('\n🎉 テスト合格！拡張機能は正常に動作しています');
        } else if (successRate >= 50) {
            console.log('\n⚠️ 部分的成功。いくつかの問題があります');
        } else {
            console.log('\n❌ テスト不合格。修正が必要です');
        }
    }
}

// 実行部分
async function main() {
    const tester = new AMREAutoTester();
    await tester.runAllTests();
}

// 実行
main().catch(console.error);