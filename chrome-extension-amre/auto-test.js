// AMRE自動テストシステム
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
            const browser = await puppeteer.launch({
                headless: false,
                args: [
                    `--disable-extensions-except=${this.extensionPath}`,
                    `--load-extension=${this.extensionPath}`,
                    '--no-sandbox',
                    '--disable-setuid-sandbox'
                ]
            });

            const page = await browser.newPage();
            
            // コンソールメッセージをキャプチャ
            page.on('console', msg => {
                if (msg.text().includes('AMRE')) {
                    console.log('📊 Extension Log:', msg.text());
                }
            });

            // テスト実行
            await this.testCivitai(page);
            await this.testFANZA(page);
            await this.testGeneric(page);
            
            await browser.close();
            
            // 結果出力
            this.generateReport();
            
        } catch (error) {
            console.error('❌ テストエラー:', error);
        }
    }

    async testCivitai(page) {
        console.log('🎨 Civitaiテスト開始...');
        
        try {
            await page.goto('https://civitai.com/models', { waitUntil: 'networkidle0' });
            
            // 拡張機能のボタンが表示されるまで待機
            await page.waitForSelector('button:has-text("📊 データ抽出")', { timeout: 5000 });
            
            // データ抽出ボタンをクリック
            await page.click('button:has-text("📊 データ抽出")');
            
            // 少し待機
            await page.waitForTimeout(2000);
            
            // アラートをキャプチャ
            page.on('dialog', async dialog => {
                console.log('✅ Civitai抽出完了:', dialog.message());
                await dialog.accept();
            });
            
            // コンソールからデータを取得
            const extractedData = await page.evaluate(() => {
                return window.lastExtractedData || 'データなし';
            });
            
            this.testResults.push({
                site: 'Civitai',
                status: 'success',
                data: extractedData,
                timestamp: new Date().toISOString()
            });
            
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

    async testFANZA(page) {
        console.log('🔞 FANZAテスト開始...');
        
        try {
            // 年齢認証ページ対応
            await page.goto('https://www.dmm.co.jp/age_check/=/declared=yes/?rurl=%2Fdc%2Fdoujin%2F-list%2F%3D%2Fsort%3Ddate%2F', 
                { waitUntil: 'networkidle0' });
            
            // ページが読み込まれるまで待機
            await page.waitForTimeout(3000);
            
            // 拡張機能テスト
            const buttonExists = await page.$('button:has-text("📊 データ抽出")');
            
            if (buttonExists) {
                await page.click('button:has-text("📊 データ抽出")');
                await page.waitForTimeout(2000);
                
                this.testResults.push({
                    site: 'FANZA',
                    status: 'success',
                    note: '年齢認証後に動作確認',
                    timestamp: new Date().toISOString()
                });
            } else {
                throw new Error('抽出ボタンが見つかりません');
            }
            
        } catch (error) {
            console.error('❌ FANZAテスト失敗:', error.message);
            this.testResults.push({
                site: 'FANZA',
                status: 'failed',
                error: error.message,
                timestamp: new Date().toISOString()
            });
        }
    }

    async testGeneric(page) {
        console.log('🌐 汎用テスト開始...');
        
        try {
            await page.goto('https://example.com', { waitUntil: 'networkidle0' });
            
            // 拡張機能の基本動作確認
            const buttonExists = await page.$('button:has-text("📊 データ抽出")');
            
            if (buttonExists) {
                await page.click('button:has-text("📊 データ抽出")');
                await page.waitForTimeout(1000);
                
                this.testResults.push({
                    site: 'Generic',
                    status: 'success',
                    timestamp: new Date().toISOString()
                });
            } else {
                throw new Error('汎用サイトで拡張機能が動作しません');
            }
            
        } catch (error) {
            console.error('❌ 汎用テスト失敗:', error.message);
            this.testResults.push({
                site: 'Generic',
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
            
            if (result.data) {
                console.log(`   データ: ${typeof result.data === 'object' ? JSON.stringify(result.data).slice(0, 100) + '...' : result.data}`);
            }
            
            result.status === 'success' ? successCount++ : failCount++;
        });
        
        console.log('='.repeat(50));
        console.log(`✅ 成功: ${successCount}件`);
        console.log(`❌ 失敗: ${failCount}件`);
        console.log(`📊 成功率: ${Math.round(successCount / (successCount + failCount) * 100)}%`);
        
        // 結果をファイルに保存
        const reportData = {
            timestamp: new Date().toISOString(),
            summary: {
                total: this.testResults.length,
                success: successCount,
                failed: failCount,
                successRate: Math.round(successCount / (successCount + failCount) * 100)
            },
            results: this.testResults
        };
        
        fs.writeFileSync(
            path.join(__dirname, 'test-report.json'),
            JSON.stringify(reportData, null, 2)
        );
        
        console.log('📄 詳細レポート: test-report.json に保存しました');
        
        // 問題がある場合の修正提案
        if (failCount > 0) {
            console.log('\n🔧 修正提案:');
            this.testResults.forEach(result => {
                if (result.status === 'failed') {
                    this.suggestFix(result);
                }
            });
        }
    }

    suggestFix(failedResult) {
        const site = failedResult.site;
        const error = failedResult.error;
        
        console.log(`\n🔧 ${site}の修正提案:`);
        
        if (error.includes('ボタンが見つかりません')) {
            console.log('  - CSSセレクターの修正が必要');
            console.log('  - content-script-minimal.jsのaddButton()を確認');
        }
        
        if (error.includes('timeout')) {
            console.log('  - ページ読み込み時間の延長');
            console.log('  - waitForTimeout値を増加');
        }
        
        if (site === 'FANZA' && error.includes('年齢認証')) {
            console.log('  - 年齢認証の自動化');
            console.log('  - または手動認証後のテスト実行');
        }
        
        if (site === 'Civitai') {
            console.log('  - サイト構造の変更確認');
            console.log('  - セレクターの更新');
        }
    }
}

// 実行部分
async function main() {
    const tester = new AMREAutoTester();
    await tester.runAllTests();
}

// コマンドライン引数チェック
if (require.main === module) {
    main().catch(console.error);
}

module.exports = AMREAutoTester;