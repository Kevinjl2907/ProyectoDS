import { fileURLToPath, URL } from "node:url";

import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

// https://vitejs.dev/config/
export default defineConfig(({ command }) => {
    return {
        plugins: [vue()],
        base: command === "serve" ? "/" : "/",
        serve: {
            open: "/",
            fs: {
                strict: false,
            },
        },
        resolve: {
            alias: {
                "@": fileURLToPath(new URL("./src", import.meta.url)),
            },
        },
        build: {
            rollupOptions: {
                // https://rollupjs.org/configuration-options/
            },
        },
    };
});
