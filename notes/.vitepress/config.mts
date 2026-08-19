import { defineConfig } from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "Ezilog TIL",
  description: "Frontend Developer Notes",
  lang: 'ko-KR',
  lastUpdated: true,
  cleanUrls: true,

  sitemap: {
    hostname: 'https://notes.ezilog.dev'
  },

  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    nav: [
      { text: 'Home', link: '/' },
      {
        text: 'Frontend',
        items: [
          { text: 'JavaScript', link: '/javascript/' },
          { text: 'Browser', link: '/browser/' }
        ]
      },
      { text: 'Network', link: '/network/' },
      { text: 'OS', link: '/operating-system/' },
      { text: 'Blog', link: 'https://ezilog.dev' }
    ],

    sidebar: {
      '/javascript/': [
        {
          text: 'JavaScript',
          items: [{ text: '소개', link: '/javascript/' }]
        },
        {
          text: '데이터 타입과 메모리',
          collapsed: false,
          items: [
            { text: '원시 타입과 객체는 뭐가 다른가', link: '/javascript/01-primitive-vs-object' },
            { text: '얕은 복사와 깊은 복사는 뭐가 다른가', link: '/javascript/02-shallow-deep-copy' },
            { text: '==와 ===는 뭐가 다른가', link: '/javascript/03-equality' }
          ]
        },
        {
          text: '실행 컨텍스트와 스코프',
          collapsed: false,
          items: [
            { text: '호이스팅은 왜 일어나는가', link: '/javascript/04-hoisting' },
            { text: 'var와 let/const는 뭐가 다른가', link: '/javascript/05-var-let-const' },
            { text: '스코프 체인은 어떻게 만들어지는가', link: '/javascript/06-scope-chain' }
          ]
        },
        {
          text: '클로저',
          collapsed: false,
          items: [
            { text: '클로저는 어떻게 가능한가', link: '/javascript/07-closure' },
            { text: '클로저는 어디에 쓰는가', link: '/javascript/08-closure-in-practice' }
          ]
        },
        {
          text: 'this',
          collapsed: false,
          items: [
            { text: 'this는 언제 결정되는가', link: '/javascript/09-this-binding' },
            { text: '화살표 함수의 this는 왜 다른가', link: '/javascript/10-arrow-function-this' }
          ]
        },
        {
          text: '프로토타입과 클래스',
          collapsed: false,
          items: [
            { text: '자바스크립트의 상속은 어떻게 동작하는가', link: '/javascript/11-prototype-chain' },
            { text: 'new는 무슨 일을 하는가', link: '/javascript/12-new-and-constructor' },
            { text: 'class는 문법 설탕인가', link: '/javascript/13-class-sugar' }
          ]
        },
        {
          text: '함수',
          collapsed: false,
          items: [
            { text: '함수가 일급 객체라는 게 무슨 의미인가', link: '/javascript/14-first-class-function' },
            { text: '화살표 함수와 일반 함수는 뭐가 다른가', link: '/javascript/15-arrow-vs-normal' }
          ]
        },
        {
          text: '비동기',
          collapsed: false,
          items: [
            { text: '싱글 스레드인데 어떻게 동시에 처리하나', link: '/javascript/16-event-loop' },
            { text: 'Promise.then과 setTimeout, 누가 먼저인가', link: '/javascript/17-micro-macro-task' },
            { text: '콜백의 진짜 문제와 프로미스', link: '/javascript/18-promise' },
            { text: 'async/await은 어떻게 동작하나', link: '/javascript/19-async-await' },
            { text: 'Promise.all은 언제 쓰나', link: '/javascript/20-promise-combinators' }
          ]
        },
        {
          text: '이터러블과 모듈',
          collapsed: false,
          items: [
            { text: 'for...of와 for...in은 뭐가 다른가', link: '/javascript/21-iterable' },
            { text: 'ESM과 CJS는 뭐가 다른가', link: '/javascript/22-esm-vs-cjs' },
            { text: '번들러는 왜 여전히 쓰나', link: '/javascript/23-bundler-babel' }
          ]
        }
      ],
      '/browser/': [
        {
          text: 'Browser',
          items: [{ text: '소개', link: '/browser/' }]
        },
        {
          text: '렌더링',
          collapsed: false,
          items: [
            { text: 'HTML이 화면이 되기까지 무슨 일이 일어나나', link: '/browser/01-rendering-pipeline' },
            { text: 'reflow와 repaint는 뭐가 다른가', link: '/browser/02-reflow-repaint' },
            { text: 'script 태그는 어디에 둬야 하나', link: '/browser/03-script-loading' }
          ]
        },
        {
          text: '이벤트와 DOM',
          collapsed: false,
          items: [
            { text: '이벤트 위임은 왜 쓰는가', link: '/browser/04-event-flow-delegation' },
            { text: 'DOM 컬렉션의 함정: live와 non-live', link: '/browser/05-dom-essentials' }
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
