#!/usr/bin/env node
/**
 * DMM アフィリエイトAPI MCPサーバー
 * 公式APIを使用してFANZA同人データを取得
 */
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { ListToolsRequestSchema, CallToolRequestSchema, } from "@modelcontextprotocol/sdk/types.js";
import { z } from "zod";
import fetch from "node-fetch";
// DMMアフィリエイトAPI設定
const API_ID = "uGday1gfBB2SXRLwH454";
const AFFILIATE_ID = "right999-990";
const API_BASE_URL = "https://api.dmm.com/affiliate/v3";
// MCPサーバー作成
const server = new Server({
    name: "dmm-affiliate",
    version: "1.0.0",
}, {
    capabilities: {
        tools: {},
    },
});
// APIリクエストヘルパー
async function callDMMAPI(endpoint, params = {}) {
    // 必須パラメータを追加
    const queryParams = new URLSearchParams({
        api_id: API_ID,
        affiliate_id: AFFILIATE_ID,
        ...params,
    });
    const url = `${API_BASE_URL}${endpoint}?${queryParams.toString()}`;
    try {
        console.error(`📡 DMM API呼び出し: ${endpoint}`);
        const response = await fetch(url, {
            headers: {
                "Accept": "application/json",
            },
        });
        if (!response.ok) {
            throw new Error(`API error: ${response.status} ${response.statusText}`);
        }
        const data = await response.json();
        return data;
    }
    catch (error) {
        console.error(`❌ APIエラー: ${error.message}`);
        throw error;
    }
}
// 同人作品検索
async function searchDoujinItems(keyword = "", sort = "rank", hits = 20, offset = 1) {
    try {
        const params = {
            site: "FANZA",
            service: "doujin", // floorパラメータは不要
            keyword: keyword,
            sort: sort,
            hits: hits.toString(),
            offset: offset.toString(),
            output: "json",
        };
        const response = await callDMMAPI("/ItemList", params);
        if (response.result) {
            const items = response.result.items || [];
            return {
                status: "success",
                request_id: response.request_id,
                total_count: response.result.total_count,
                hit_count: items.length,
                items: items.map((item) => ({
                    content_id: item.content_id,
                    product_id: item.product_id,
                    title: item.title,
                    circle: item.iteminfo?.circle?.[0]?.name || "不明",
                    price: item.prices?.price || "価格不明",
                    review_average: item.review?.average || 0,
                    review_count: item.review?.count || 0,
                    url: item.URL,
                    affiliateURL: item.affiliateURL,
                    imageURL: {
                        small: item.imageURL?.small,
                        large: item.imageURL?.large,
                    },
                    date: item.date,
                    genres: item.iteminfo?.genre?.map((g) => g.name) || [],
                })),
            };
        }
        return {
            status: "error",
            message: "検索結果がありません",
        };
    }
    catch (error) {
        return {
            status: "error",
            message: error.message,
        };
    }
}
// ジャンル一覧取得
async function getGenreList() {
    try {
        const params = {
            floor_id: "27", // 同人フロアID
            output: "json",
        };
        const response = await callDMMAPI("/GenreSearch", params);
        if (response.result) {
            return {
                status: "success",
                genres: response.result.genre || [],
            };
        }
        return {
            status: "error",
            message: "ジャンル情報を取得できません",
        };
    }
    catch (error) {
        return {
            status: "error",
            message: error.message,
        };
    }
}
// サークル検索
async function searchCircles(keyword = "") {
    try {
        const params = {
            floor_id: "27", // 同人フロアID
            keyword: keyword,
            output: "json",
        };
        const response = await callDMMAPI("/MakerSearch", params);
        if (response.result) {
            return {
                status: "success",
                circles: response.result.maker || [],
            };
        }
        return {
            status: "error",
            message: "サークル情報を取得できません",
        };
    }
    catch (error) {
        return {
            status: "error",
            message: error.message,
        };
    }
}
// ランキング取得（同人作品検索を利用）
async function getDoujinRanking(term = "24") {
    // DMMアフィリエイトAPIはランキング専用エンドポイントがないため
    // 売上順ソートで代替
    return await searchDoujinItems("", "rank", 100, 1);
}
// フロア情報取得
async function getFloorList() {
    try {
        const params = {
            output: "json",
        };
        const response = await callDMMAPI("/FloorList", params);
        if (response.result) {
            // FANZAサイトのフロア情報のみ抽出
            const fanzaFloors = response.result.site?.find((site) => site.name === "FANZA");
            return {
                status: "success",
                floors: fanzaFloors?.service || [],
            };
        }
        return {
            status: "error",
            message: "フロア情報を取得できません",
        };
    }
    catch (error) {
        return {
            status: "error",
            message: error.message,
        };
    }
}
// ツール定義
server.setRequestHandler(ListToolsRequestSchema, async () => {
    return {
        tools: [
            {
                name: "dmm_search_doujin",
                description: "FANZA同人作品を検索（公式API使用）",
                inputSchema: {
                    type: "object",
                    properties: {
                        keyword: {
                            type: "string",
                            description: "検索キーワード（空欄で全件）",
                            default: "",
                        },
                        sort: {
                            type: "string",
                            description: "ソート順（rank:人気順, date:新着順, price:価格順, review:レビュー順）",
                            default: "rank",
                            enum: ["rank", "date", "price", "review"],
                        },
                        hits: {
                            type: "number",
                            description: "取得件数（1-100）",
                            default: 20,
                            minimum: 1,
                            maximum: 100,
                        },
                        offset: {
                            type: "number",
                            description: "開始位置（ページング用）",
                            default: 1,
                            minimum: 1,
                        },
                    },
                },
            },
            {
                name: "dmm_get_ranking",
                description: "FANZA同人ランキングを取得",
                inputSchema: {
                    type: "object",
                    properties: {
                        term: {
                            type: "string",
                            description: "期間（24:24時間, week:週間, month:月間）",
                            default: "24",
                            enum: ["24", "week", "month"],
                        },
                    },
                },
            },
            {
                name: "dmm_get_genres",
                description: "FANZA同人のジャンル一覧を取得",
                inputSchema: {
                    type: "object",
                    properties: {},
                },
            },
            {
                name: "dmm_search_circles",
                description: "FANZA同人のサークルを検索",
                inputSchema: {
                    type: "object",
                    properties: {
                        keyword: {
                            type: "string",
                            description: "サークル名検索キーワード",
                            default: "",
                        },
                    },
                },
            },
            {
                name: "dmm_get_floors",
                description: "FANZAのフロア（カテゴリ）一覧を取得",
                inputSchema: {
                    type: "object",
                    properties: {},
                },
            },
            {
                name: "dmm_market_analysis",
                description: "FANZA同人市場の詳細分析（価格帯・サークル・ジャンル・トレンド）",
                inputSchema: {
                    type: "object",
                    properties: {
                        analysis_type: {
                            type: "string",
                            description: "分析タイプ（price:価格帯分析, circle:サークル分析, genre:ジャンル分析, trend:トレンド分析）",
                            default: "price",
                            enum: ["price", "circle", "genre", "trend"],
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
        case "dmm_search_doujin": {
            const { keyword, sort, hits, offset } = z
                .object({
                keyword: z.string().default(""),
                sort: z.string().default("rank"),
                hits: z.number().default(20),
                offset: z.number().default(1),
            })
                .parse(args);
            const results = await searchDoujinItems(keyword, sort, hits, offset);
            return {
                content: [
                    {
                        type: "text",
                        text: JSON.stringify(results, null, 2),
                    },
                ],
            };
        }
        case "dmm_get_ranking": {
            const { term } = z
                .object({
                term: z.string().default("24"),
            })
                .parse(args);
            const results = await getDoujinRanking(term);
            return {
                content: [
                    {
                        type: "text",
                        text: JSON.stringify(results, null, 2),
                    },
                ],
            };
        }
        case "dmm_get_genres": {
            const results = await getGenreList();
            return {
                content: [
                    {
                        type: "text",
                        text: JSON.stringify(results, null, 2),
                    },
                ],
            };
        }
        case "dmm_search_circles": {
            const { keyword } = z
                .object({
                keyword: z.string().default(""),
            })
                .parse(args);
            const results = await searchCircles(keyword);
            return {
                content: [
                    {
                        type: "text",
                        text: JSON.stringify(results, null, 2),
                    },
                ],
            };
        }
        case "dmm_get_floors": {
            const results = await getFloorList();
            return {
                content: [
                    {
                        type: "text",
                        text: JSON.stringify(results, null, 2),
                    },
                ],
            };
        }
        case "dmm_market_analysis": {
            const { analysis_type } = z
                .object({
                analysis_type: z.enum(["price", "circle", "genre", "trend"]).default("price"),
            })
                .parse(args);
            try {
                // 大量データを取得して分析
                const params = {
                    site: "FANZA",
                    service: "doujin",
                    sort: "rank",
                    hits: "100", // 分析用に多めに取得
                    output: "json",
                };
                const response = await callDMMAPI("/ItemList", params);
                if (response.result && response.result.items) {
                    const items = response.result.items;
                    let analysisResult = {};
                    switch (analysis_type) {
                        case "price":
                            // 価格帯分析
                            const priceRanges = {
                                "～500円": 0,
                                "501～1000円": 0,
                                "1001～1500円": 0,
                                "1501～2000円": 0,
                                "2001円～": 0
                            };
                            items.forEach((item) => {
                                const price = parseInt(item.prices?.price || "0");
                                if (price <= 500)
                                    priceRanges["～500円"]++;
                                else if (price <= 1000)
                                    priceRanges["501～1000円"]++;
                                else if (price <= 1500)
                                    priceRanges["1001～1500円"]++;
                                else if (price <= 2000)
                                    priceRanges["1501～2000円"]++;
                                else
                                    priceRanges["2001円～"]++;
                            });
                            analysisResult = {
                                type: "価格帯分析",
                                total_items: items.length,
                                price_distribution: priceRanges,
                                average_price: Math.round(items.reduce((sum, item) => sum + parseInt(item.prices?.price || "0"), 0) / items.length),
                            };
                            break;
                        case "circle":
                            // サークル別分析
                            const circleCount = {};
                            items.forEach((item) => {
                                const circle = item.iteminfo?.circle?.[0]?.name || "不明";
                                circleCount[circle] = (circleCount[circle] || 0) + 1;
                            });
                            const topCircles = Object.entries(circleCount)
                                .sort(([, a], [, b]) => b - a)
                                .slice(0, 10)
                                .map(([name, count]) => ({ name, count }));
                            analysisResult = {
                                type: "サークル別分析",
                                total_circles: Object.keys(circleCount).length,
                                top_circles: topCircles,
                            };
                            break;
                        case "genre":
                            // ジャンル分析
                            const genreCount = {};
                            items.forEach((item) => {
                                const genres = item.iteminfo?.genre || [];
                                genres.forEach((genre) => {
                                    const genreName = genre.name;
                                    genreCount[genreName] = (genreCount[genreName] || 0) + 1;
                                });
                            });
                            const topGenres = Object.entries(genreCount)
                                .sort(([, a], [, b]) => b - a)
                                .slice(0, 15)
                                .map(([name, count]) => ({ name, count }));
                            analysisResult = {
                                type: "ジャンル分析",
                                total_genres: Object.keys(genreCount).length,
                                popular_genres: topGenres,
                            };
                            break;
                        case "trend":
                            // トレンド分析（レビュー評価と価格の相関）
                            const trendData = items
                                .filter((item) => item.review?.average && item.prices?.price)
                                .map((item) => ({
                                title: item.title,
                                price: parseInt(item.prices.price),
                                rating: parseFloat(item.review.average),
                                review_count: item.review.count || 0,
                                circle: item.iteminfo?.circle?.[0]?.name || "不明",
                            }))
                                .sort((a, b) => b.rating - a.rating)
                                .slice(0, 20);
                            analysisResult = {
                                type: "トレンド分析",
                                high_rated_items: trendData,
                                insights: {
                                    average_rating: Math.round((trendData.reduce((sum, item) => sum + item.rating, 0) / trendData.length) * 100) / 100,
                                    average_price_high_rated: Math.round(trendData.reduce((sum, item) => sum + item.price, 0) / trendData.length),
                                }
                            };
                            break;
                    }
                    return {
                        content: [
                            {
                                type: "text",
                                text: JSON.stringify({
                                    status: "success",
                                    analysis: analysisResult,
                                    generated_at: new Date().toISOString(),
                                }, null, 2),
                            },
                        ],
                    };
                }
            }
            catch (error) {
                return {
                    content: [
                        {
                            type: "text",
                            text: `分析エラー: ${error.message}`,
                        },
                    ],
                };
            }
        }
        default:
            throw new Error(`Unknown tool: ${name}`);
    }
});
// サーバー起動
async function main() {
    console.error("🚀 DMM アフィリエイトAPI MCPサーバー v1.0.0 起動中...");
    console.error("📝 公式APIでFANZA同人データ取得");
    console.error(`🔑 API ID: ${API_ID}`);
    console.error(`🏷️ Affiliate ID: ${AFFILIATE_ID}`);
    const transport = new StdioServerTransport();
    await server.connect(transport);
    console.error("✅ サーバー起動完了");
    console.error("🎯 利用可能: 検索、ランキング、ジャンル、サークル");
}
main().catch((error) => {
    console.error("Fatal error:", error);
    process.exit(1);
});
