/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  output: 'standalone',
  images: {
    domains: ['instagram.com', 'cdninstagram.com', 'scontent.cdninstagram.com'],
    remotePatterns: [
      {
        protocol: 'https',
        hostname: '*.fbcdn.net',
      },
      {
        protocol: 'https',
        hostname: '*.cdninstagram.com',
      },
    ],
  },
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'https://www.coriumai-local.com',
  },
};

module.exports = nextConfig;
