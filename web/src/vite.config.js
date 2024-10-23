const global = require("@/global.js");
module.exports = {
    devServer: {
        proxy: {
            '/api': {
                target: global.GRADIO_GLOBAL_LINK, // Gradio 后端地址
                changeOrigin: true,
                pathRewrite: { '^/api': '' }, // 将 '/api' 重写为空
            },
        },
    },
};
