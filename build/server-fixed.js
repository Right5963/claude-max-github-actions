#!/usr/bin/env node
/**
 * FANZA同人MCPサーバー - 修正版
 * Note MCPと同じ構造で実装
 */
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { ListToolsRequestSchema, CallToolRequestSchema, } from "@modelcontextprotocol/sdk/types.js";
import { z } from "zod";
import fetch from "node-fetch";
import { JSDOM } from "jsdom";
// FANZAサーバー作成
const server = new Server({
    name: "fanza-doujin-fixed",
    version: "2.0.0",
}, {
    capabilities: {
        tools: {},
    },
});
// 認証情報管理（Note MCPと同じ構造）
let activeSessionCookie = null;
let activeXsrfToken = null;
let isLoggedIn = false;
// APIベースURL
const API_BASE_URL = "https://www.dmm.co.jp";
// デフォルトヘッダー
const DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "ja,en-US;q=0.7,en;q=0.3",
};
// 認証ヘッダー構築（Note MCPと同じパターン）
function buildAuthHeaders() {
    const headers = {};
    if (activeSessionCookie) {
        headers["Cookie"] = activeSessionCookie;
    }
    if (activeXsrfToken) {
        headers["X-XSRF-TOKEN"] = activeXsrfToken;
    }
    return headers;
}
// FANZAへのログイン（Note MCPと同じ構造）
async function loginToFanza(email, password) {
    try {
        console.error("🔐 FANZAログイン処理開始...");
        // 1. ログインページアクセスでCSRFトークン取得
        const loginPageUrl = `${API_BASE_URL}/my/-/login/`;
        console.error(`📡 ログインページアクセス: ${loginPageUrl}`);
        const loginPageResponse = await fetch(loginPageUrl, {
            headers: DEFAULT_HEADERS,
        });
        if (!loginPageResponse.ok) {
            console.error(`❌ ログインページアクセス失敗: ${loginPageResponse.status}`);
            return false;
        }
        // Cookie保存
        const setCookieHeader = loginPageResponse.headers.get("set-cookie");
        if (setCookieHeader) {
            activeSessionCookie = setCookieHeader;
            console.error("🍪 初期Cookie取得");
        }
        // CSRFトークン抽出
        const loginPageHtml = await loginPageResponse.text();
        const dom = new JSDOM(loginPageHtml);
        const document = dom.window.document;
        const tokenInput = document.querySelector('input[name="token"]');
        const csrfToken = tokenInput?.value || "";
        if (!csrfToken) {
            console.error("❌ CSRFトークンが見つかりません");
            return false;
        }
        console.error("🛡️ CSRFトークン取得成功");
        // 2. ログイン実行（正しいエンドポイント使用）
        const loginUrl = `${API_BASE_URL}/service/login/password/authenticate`;
        console.error(`🔑 ログイン送信: ${loginUrl}`);
        // フォームデータ構築（調査で判明した必須フィールド）
        const formData = new URLSearchParams({
            "login_id": email,
            "password": password,
            "use_auto_login": "1",
            "i3_vwtp": "pc",
            "token": csrfToken,
            "recaptchaToken": "",
        });
        const loginResponse = await fetch(loginUrl, {
            method: "POST",
            headers: {
                ...DEFAULT_HEADERS,
                "Content-Type": "application/x-www-form-urlencoded",
                "Cookie": activeSessionCookie || "",
                "Referer": loginPageUrl,
                "Origin": API_BASE_URL,
            },
            body: formData.toString(),
            redirect: "manual", // リダイレクトを手動処理
        });
        console.error(`📊 ログイン応答: ${loginResponse.status}`);
        // 新しいCookie更新
        const newCookies = loginResponse.headers.get("set-cookie");
        if (newCookies) {
            activeSessionCookie = newCookies;
            console.error("🍪 ログイン後Cookie更新");
        }
        // リダイレクト確認（302 = 成功）
        if (loginResponse.status === 302) {
            const location = loginResponse.headers.get("location");
            console.error(`🔄 リダイレクト先: ${location}`);
            // リダイレクト先にアクセスしてセッション確立
            if (location) {
                const redirectUrl = location.startsWith("http") ? location : `${API_BASE_URL}${location}`;
                const redirectResponse = await fetch(redirectUrl, {
                    headers: {
                        ...DEFAULT_HEADERS,
                        "Cookie": activeSessionCookie || "",
                    },
                });
                // 最終Cookie更新
                const finalCookies = redirectResponse.headers.get("set-cookie");
                if (finalCookies) {
                    activeSessionCookie = finalCookies;
                    console.error("🍪 最終Cookie更新");
                }
            }
            isLoggedIn = true;
            console.error("✅ ログイン成功！");
            // 3. 年齢認証処理
            await handleAgeVerification();
            return true;
        }
        else {
            console.error("❌ ログイン失敗");
            return false;
        }
    }
    catch (error) {
        console.error(`❌ ログインエラー: ${error.message}`);
        return false;
    }
}
// 年齢認証処理
async function handleAgeVerification() {
    try {
        console.error("🔞 年齢認証処理開始...");
        // 同人ページアクセスで年齢認証チェック
        const doujinUrl = `${API_BASE_URL}/dc/doujin/`;
        const response = await fetch(doujinUrl, {
            headers: {
                ...DEFAULT_HEADERS,
                ...buildAuthHeaders(),
            },
        });
        const html = await response.text();
        const dom = new JSDOM(html);
        const document = dom.window.document;
        if (document.title.includes("年齢認証")) {
            console.error("⚠️ 年齢認証が必要です");
            // 年齢認証フォーム処理
            const ageForm = document.querySelector('form');
            if (ageForm) {
                const ageAction = ageForm.getAttribute('action') || "/age_check/";
                const ageUrl = `${API_BASE_URL}${ageAction}`;
                // 年齢認証送信
                const ageResponse = await fetch(ageUrl, {
                    method: "POST",
                    headers: {
                        ...DEFAULT_HEADERS,
                        ...buildAuthHeaders(),
                        "Content-Type": "application/x-www-form-urlencoded",
                    },
                    body: "agecheck=1",
                    redirect: "manual",
                });
                console.error(`📊 年齢認証応答: ${ageResponse.status}`);
                // Cookie更新
                const ageCookies = ageResponse.headers.get("set-cookie");
                if (ageCookies) {
                    activeSessionCookie = ageCookies;
                    console.error("🍪 年齢認証後Cookie更新");
                }
                console.error("✅ 年齢認証完了");
                return true;
            }
        }
        else {
            console.error("✅ 年齢認証不要または完了済み");
            return true;
        }
    }
    catch (error) {
        console.error(`❌ 年齢認証エラー: ${error.message}`);
    }
    return false;
}
// APIリクエスト用ヘルパー（Note MCPと同じ構造）
async function makeFANZARequest(path) {
    const url = path.startsWith("http") ? path : `${API_BASE_URL}${path}`;
    const headers = {
        ...DEFAULT_HEADERS,
        ...buildAuthHeaders(),
    };
    try {
        const response = await fetch(url, { headers });
        // Set-Cookieヘッダーからセッション情報を更新
        const setCookieHeader = response.headers.get("set-cookie");
        if (setCookieHeader) {
            activeSessionCookie = setCookieHeader;
        }
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.text();
    }
    catch (error) {
        console.error(`Error making FANZA request: ${error.message}`);
        throw error;
    }
}
// 検索実行（修正版）
async function searchDoujin(query, sort = "popular") {
    try {
        const searchPath = `/dc/doujin/-/search/=/keyword=${encodeURIComponent(query)}/sort=${sort}/`;
        const html = await makeFANZARequest(searchPath);
        const dom = new JSDOM(html);
        const document = dom.window.document;
        // 商品要素取得
        const items = document.querySelectorAll("li.tmb");
        const results = [];
        for (const item of items) {
            const titleElem = item.querySelector("p.ttl a");
            const priceElem = item.querySelector(".price");
            const linkElem = item.querySelector("a");
            if (titleElem && linkElem) {
                results.push({
                    title: titleElem.textContent?.trim(),
                    price: priceElem?.textContent?.trim(),
                    url: `${API_BASE_URL}${linkElem.getAttribute("href")}`,
                });
            }
        }
        return {
            status: "success",
            query: query,
            count: results.length,
            items: results.slice(0, 20),
        };
    }
    catch (error) {
        console.error(`検索エラー: ${error.message}`);
        return {
            status: "error",
            error: error.message,
        };
    }
}
// ランキング取得（修正版）
async function getRanking(period = "daily") {
    try {
        const rankingPath = `/dc/doujin/-/ranking/=/term=${period}/`;
        const html = await makeFANZARequest(rankingPath);
        const dom = new JSDOM(html);
        const document = dom.window.document;
        const items = document.querySelectorAll("li.rank");
        const rankings = [];
        for (const item of items) {
            const rankElem = item.querySelector(".rank-no");
            const titleElem = item.querySelector("p.ttl a");
            const priceElem = item.querySelector(".price");
            if (titleElem) {
                rankings.push({
                    rank: rankElem?.textContent?.trim(),
                    title: titleElem.textContent?.trim(),
                    price: priceElem?.textContent?.trim(),
                });
            }
        }
        return {
            status: "success",
            period: period,
            count: rankings.length,
            rankings: rankings,
        };
    }
    catch (error) {
        console.error(`ランキング取得エラー: ${error.message}`);
        return {
            status: "error",
            error: error.message,
        };
    }
}
// ツール定義
server.setRequestHandler(ListToolsRequestSchema, async () => {
    return {
        tools: [
            {
                name: "fanza_login",
                description: "FANZAにログインしてセッションを確立（年齢認証も自動処理）",
                inputSchema: {
                    type: "object",
                    properties: {
                        email: { type: "string", description: "FANZAログインメールアドレス" },
                        password: { type: "string", description: "FANZAパスワード" },
                    },
                    required: ["email", "password"],
                },
            },
            {
                name: "fanza_search",
                description: "FANZA同人作品を検索",
                inputSchema: {
                    type: "object",
                    properties: {
                        query: { type: "string", description: "検索キーワード" },
                        sort: {
                            type: "string",
                            description: "ソート順（popular/new/price_asc/price_desc）",
                            default: "popular",
                        },
                    },
                    required: ["query"],
                },
            },
            {
                name: "fanza_ranking",
                description: "FANZA同人ランキングを取得",
                inputSchema: {
                    type: "object",
                    properties: {
                        period: {
                            type: "string",
                            description: "期間（daily/weekly/monthly）",
                            default: "daily",
                        },
                    },
                },
            },
        ],
    };
});
// ツール実行
server.setRequestHandler(CallToolRequestSchema, async (request) => {
    const { name, arguments: args } = request.params;
    switch (name) {
        case "fanza_login": {
            const { email, password } = z
                .object({
                email: z.string(),
                password: z.string(),
            })
                .parse(args);
            const success = await loginToFanza(email, password);
            return {
                content: [
                    {
                        type: "text",
                        text: success
                            ? "✅ ログイン成功！セッション確立・年齢認証完了"
                            : "❌ ログイン失敗。認証情報を確認してください",
                    },
                ],
            };
        }
        case "fanza_search": {
            if (!isLoggedIn) {
                return {
                    content: [
                        {
                            type: "text",
                            text: "❌ ログインが必要です。先にfanza_loginを実行してください",
                        },
                    ],
                };
            }
            const { query, sort } = z
                .object({
                query: z.string(),
                sort: z.string().default("popular"),
            })
                .parse(args);
            const results = await searchDoujin(query, sort);
            return {
                content: [
                    {
                        type: "text",
                        text: JSON.stringify(results, null, 2),
                    },
                ],
            };
        }
        case "fanza_ranking": {
            if (!isLoggedIn) {
                return {
                    content: [
                        {
                            type: "text",
                            text: "❌ ログインが必要です。先にfanza_loginを実行してください",
                        },
                    ],
                };
            }
            const { period } = z
                .object({
                period: z.string().default("daily"),
            })
                .parse(args);
            const results = await getRanking(period);
            return {
                content: [
                    {
                        type: "text",
                        text: JSON.stringify(results, null, 2),
                    },
                ],
            };
        }
        default:
            throw new Error(`Unknown tool: ${name}`);
    }
});
// サーバー起動
async function main() {
    console.error("🚀 FANZA同人MCPサーバー v2.0.0 (修正版) を起動中...");
    console.error("📝 Note MCPと同じ構造で実装");
    const transport = new StdioServerTransport();
    await server.connect(transport);
    console.error("✅ サーバー起動完了");
    console.error("🔐 ログイン機能: 正しいエンドポイント使用");
    console.error("🔞 年齢認証: 自動処理対応");
}
main().catch((error) => {
    console.error("Fatal error:", error);
    process.exit(1);
});
