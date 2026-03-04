/** @type {import('next').NextConfig} */
const nextConfig = {
  // output: 'export', // Disabled for client-side components
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
