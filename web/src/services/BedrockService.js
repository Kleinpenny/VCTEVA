import axios from 'axios';

const API_ENDPOINT = 'https://bedrock-api-endpoint'; // 替换为实际的 Amazon Bedrock API 端点
const API_KEY = 'your-api-key'; // 添加 API Key 进行身份验证

export async function fetchPlayerInfo(prompt) {
    try {
        // 构造请求体
        const requestBody = {
            prompt: prompt,  // 用户输入的提问
            maxTokens: 100,  // 定义最大输出长度
        };

        // 发送 POST 请求到 Amazon Bedrock API
        const response = await axios.post(API_ENDPOINT, requestBody, {
            headers: {
                'Authorization': `Bearer ${API_KEY}`,
                'Content-Type': 'application/json',
            },
        });

        // 假设 LLM 返回的数据包含选手信息，我们需要根据实际响应解析
        const playerData = parsePlayerResponse(response.data);
        return playerData;

    } catch (error) {
        console.error('Error fetching player info:', error);
        return null;
    }
}

function parsePlayerResponse(response) {
    // 假设返回的数据结构类似于：
    // { name: 'Jett', position: 'Duelist', team: 'Team A', winRate: 75, skills: ['Mobility', 'Precision'] }
    return {
        name: response.name,
        position: response.position,
        team: response.team,
        winRate: response.winRate,
        skills: response.skills,
    };
}
