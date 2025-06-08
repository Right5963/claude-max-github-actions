// シンプルテスト版（ブラウザなし）
const fs = require('fs');
const path = require('path');

class SimpleExtensionTester {
    constructor() {
        this.extensionPath = path.join(__dirname);
        this.testResults = [];
    }

    runTests() {
        console.log('🧪 AMRE拡張機能ファイル検証開始...');
        
        this.testManifest();
        this.testContentScript();
        this.testFileStructure();
        
        this.generateReport();
    }

    testManifest() {
        console.log('📄 manifest.json テスト...');
        
        try {
            const manifestPath = path.join(this.extensionPath, 'manifest.json');
            const manifestContent = fs.readFileSync(manifestPath, 'utf8');
            const manifest = JSON.parse(manifestContent);
            
            // 必須フィールドの確認
            const requiredFields = ['manifest_version', 'name', 'version'];
            const missingFields = requiredFields.filter(field => !manifest[field]);
            
            if (missingFields.length === 0) {
                console.log('✅ manifest.json: 基本構造OK');
                
                // マニフェストv3チェック
                if (manifest.manifest_version === 3) {
                    console.log('✅ Manifest V3準拠');
                } else {
                    console.log('⚠️ Manifest V2（非推奨）');
                }
                
                // content_scriptsチェック
                if (manifest.content_scripts && manifest.content_scripts.length > 0) {
                    console.log('✅ Content Scriptsが設定されています');
                } else {
                    console.log('❌ Content Scriptsが設定されていません');
                }
                
                this.testResults.push({
                    test: 'manifest.json',
                    status: 'success',
                    details: `Name: ${manifest.name}, Version: ${manifest.version}`
                });
                
            } else {
                throw new Error(`必須フィールドが不足: ${missingFields.join(', ')}`);
            }
            
        } catch (error) {
            console.error('❌ manifest.json エラー:', error.message);
            this.testResults.push({
                test: 'manifest.json',
                status: 'failed',
                error: error.message
            });
        }
    }

    testContentScript() {
        console.log('📝 content-script-minimal.js テスト...');
        
        try {
            const scriptPath = path.join(this.extensionPath, 'content-script-minimal.js');
            const scriptContent = fs.readFileSync(scriptPath, 'utf8');
            
            // 重要な関数の存在確認
            const requiredElements = [
                'class AMREMinimal',
                'extractData',
                'extractFANZA',
                'extractCivitai',
                'copyToClipboard'
            ];
            
            const missingElements = requiredElements.filter(element => 
                !scriptContent.includes(element)
            );
            
            if (missingElements.length === 0) {
                console.log('✅ Content Script: 必要な関数がすべて存在');
                
                // ファイルサイズチェック
                const sizeKB = Math.round(scriptContent.length / 1024);
                console.log(`📊 ファイルサイズ: ${sizeKB}KB`);
                
                if (sizeKB < 50) {
                    console.log('✅ 適切なファイルサイズ');
                } else {
                    console.log('⚠️ ファイルサイズが大きすぎる可能性');
                }
                
                this.testResults.push({
                    test: 'content-script',
                    status: 'success',
                    details: `Size: ${sizeKB}KB, Functions: ${requiredElements.length}`
                });
                
            } else {
                throw new Error(`必要な要素が不足: ${missingElements.join(', ')}`);
            }
            
        } catch (error) {
            console.error('❌ Content Script エラー:', error.message);
            this.testResults.push({
                test: 'content-script',
                status: 'failed',
                error: error.message
            });
        }
    }

    testFileStructure() {
        console.log('📁 ファイル構造テスト...');
        
        try {
            const requiredFiles = [
                'manifest.json',
                'content-script-minimal.js'
            ];
            
            const missingFiles = requiredFiles.filter(file => {
                const filePath = path.join(this.extensionPath, file);
                return !fs.existsSync(filePath);
            });
            
            if (missingFiles.length === 0) {
                console.log('✅ 必要なファイルがすべて存在');
                
                // 追加ファイルの確認
                const allFiles = fs.readdirSync(this.extensionPath);
                const jsFiles = allFiles.filter(file => file.endsWith('.js') || file.endsWith('.cjs'));
                const jsonFiles = allFiles.filter(file => file.endsWith('.json'));
                
                console.log(`📊 JSファイル: ${jsFiles.length}個`);
                console.log(`📊 JSONファイル: ${jsonFiles.length}個`);
                
                this.testResults.push({
                    test: 'file-structure',
                    status: 'success',
                    details: `JS: ${jsFiles.length}, JSON: ${jsonFiles.length}`
                });
                
            } else {
                throw new Error(`必要なファイルが不足: ${missingFiles.join(', ')}`);
            }
            
        } catch (error) {
            console.error('❌ ファイル構造 エラー:', error.message);
            this.testResults.push({
                test: 'file-structure',
                status: 'failed',
                error: error.message
            });
        }
    }

    generateReport() {
        console.log('\n📋 AMRE拡張機能検証レポート');
        console.log('='.repeat(50));
        
        let successCount = 0;
        let failCount = 0;
        
        this.testResults.forEach(result => {
            const status = result.status === 'success' ? '✅' : '❌';
            console.log(`${status} ${result.test}: ${result.status}`);
            
            if (result.error) {
                console.log(`   エラー: ${result.error}`);
            }
            
            if (result.details) {
                console.log(`   詳細: ${result.details}`);
            }
            
            result.status === 'success' ? successCount++ : failCount++;
        });
        
        console.log('='.repeat(50));
        console.log(`✅ 成功: ${successCount}件`);
        console.log(`❌ 失敗: ${failCount}件`);
        
        const total = successCount + failCount;
        const successRate = total > 0 ? Math.round(successCount / total * 100) : 0;
        console.log(`📊 成功率: ${successRate}%`);
        
        // Chrome拡張機能インストール手順
        console.log('\n🚀 インストール手順:');
        console.log('1. Chrome → chrome://extensions/');
        console.log('2. 右上「デベロッパーモード」をON');
        console.log('3. 「パッケージ化されていない拡張機能を読み込む」');
        console.log(`4. フォルダ選択: ${this.extensionPath}`);
        
        if (successRate >= 80) {
            console.log('\n🎉 検証合格！拡張機能のインストール準備完了');
        } else {
            console.log('\n❌ 検証不合格。修正が必要です');
        }
        
        // 結果をファイルに保存
        const reportData = {
            timestamp: new Date().toISOString(),
            summary: {
                total: total,
                success: successCount,
                failed: failCount,
                successRate: successRate
            },
            results: this.testResults,
            installPath: this.extensionPath
        };
        
        fs.writeFileSync(
            path.join(this.extensionPath, 'test-report.json'),
            JSON.stringify(reportData, null, 2)
        );
        
        console.log('📄 詳細レポート: test-report.json に保存');
    }
}

// 実行
const tester = new SimpleExtensionTester();
tester.runTests();