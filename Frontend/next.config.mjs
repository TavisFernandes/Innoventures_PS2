/** @type {import('next').NextConfig} */

const nextConfig = {

  // No output: 'export' for Vercel - it handles SSR properly

  trailingSlash: true,

  images: {

    unoptimized: true

  },

  webpack: (config) => {

    config.resolve.alias = {

      ...config.resolve.alias,

      '@': './src'

    };

    return config;

  }

};



export default nextConfig;

