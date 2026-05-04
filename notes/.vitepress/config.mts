import { defineConfig } from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "Ezilog TIL",
  description: "Frontend Developer Notes",
  lang: 'ko-KR',
  lastUpdated: true,
  cleanUrls: true,

  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    nav: [
      { text: 'Home', link: '/' },
      { text: 'Frontend', link: '/frontend/' },
      { text: 'Network', link: '/network/' },
      { text: 'OS', link: '/operating-system/' }
    ],

    sidebar: {
      '/frontend/': [
        {
          text: 'Frontend',
          items: [{ text: '소개', link: '/frontend/' }]
        },
        {
          text: 'JavaScript',
          collapsed: false,
          items: [
            { text: '목록', link: '/frontend/javascript/' }
          ]
        }
      ],
      '/network/': [
        {
          text: 'Network',
          items: [{ text: '소개', link: '/network/' }]
        }
      ],
      '/operating-system/': [
        {
          text: 'Operating System',
          items: [{ text: '소개', link: '/operating-system/' }]
        }
      ]
    },

    outline: {
      label: '페이지 내용',
      level: [2, 3]
    },

    docFooter: {
      prev: '이전 페이지',
      next: '다음 페이지'
    },

    lastUpdated: {
      text: '마지막 업데이트'
    },

    search: {
      provider: 'local'
    },

    socialLinks: [
      { icon: 'github', link: 'https://github.com/Jaeho-Site/TIL' }
    ]
  }
})
