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

  head: [
  ['meta', { name: 'naver-site-verification', content: 'dd667c83f23b79886395a0a70e733d9ca8713aae' }]
],

  transformPageData(pageData) {
    const path = pageData.relativePath
      .replace(/index\.md$/, '')
      .replace(/\.md$/, '')
    pageData.frontmatter.head ??= []
    pageData.frontmatter.head.push([
      'link',
      { rel: 'canonical', href: `https://notes.ezilog.dev/${path}` }
    ])
  },

  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    nav: [
      { text: 'Home', link: '/' },
      {
        text: 'Frontend',
        items: [
          { text: 'JavaScript', link: '/javascript/' },
          { text: 'TypeScript', link: '/typescript/' },
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
      '/typescript/': [
        {
          text: 'TypeScript',
          items: [{ text: '소개', link: '/typescript/' }]
        },
        {
          text: '타입스크립트라는 언어',
          collapsed: false,
          items: [
            { text: '타입 에러가 있는데 왜 컴파일은 되는가', link: '/typescript/01-ts-js-relationship' },
            { text: '런타임에 타입은 어떻게 확인하나', link: '/typescript/02-runtime-types' }
          ]
        },
        {
          text: '구조적 타입 시스템',
          collapsed: false,
          items: [
            { text: '선언한 적 없는 타입인데 왜 할당이 되는가', link: '/typescript/03-structural-typing' },
            { text: '객체 리터럴만 더 엄격하게 검사되는 이유', link: '/typescript/04-excess-property-checking' },
            { text: '타입은 값의 집합이다', link: '/typescript/05-types-as-sets' },
            { text: '같은 이름이 타입도 되고 값도 된다', link: '/typescript/06-type-value-space' }
          ]
        },
        {
          text: '타입 추론',
          collapsed: false,
          items: [
            { text: "let은 string인데 const는 왜 'x'인가", link: '/typescript/07-widening' },
            { text: '타입스크립트는 코드 흐름을 읽는다', link: '/typescript/08-narrowing' },
            { text: '인라인은 되는데 변수로 빼면 왜 에러인가', link: '/typescript/09-context-inference' }
          ]
        },
        {
          text: 'any와 타입 안전성',
          collapsed: false,
          items: [
            { text: 'any 대신 unknown을 쓰라는 이유', link: '/typescript/10-any-unknown-never' },
            { text: 'as는 언제 써야 하는가', link: '/typescript/11-type-assertions' },
            { text: '타입 체크를 통과했는데 왜 런타임 에러가 나는가', link: '/typescript/12-unsoundness' }
          ]
        },
        {
          text: '타입 설계',
          collapsed: false,
          items: [
            { text: 'type과 interface, 뭘 써야 하나', link: '/typescript/13-type-vs-interface' },
            { text: '잘못된 상태를 표현할 수 없게 만들기', link: '/typescript/14-discriminated-union' },
            { text: 'null은 타입의 어디에 둬야 하나', link: '/typescript/15-null-handling' }
          ]
        },
        {
          text: '제네릭과 타입 연산',
          collapsed: false,
          items: [
            { text: '제네릭은 타입의 함수다', link: '/typescript/16-generics-as-functions' },
            { text: 'Partial은 어떻게 만들어지는가', link: '/typescript/17-mapped-utility-types' },
            { text: '타입에도 조건문이 있다', link: '/typescript/18-conditional-types' }
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
        },
        {
          text: '통신의 토대',
          collapsed: false,
          items: [
            { text: '네트워크는 왜 계층으로 나눴나', link: '/network/01-layered-model' },
            { text: '연결은 왜 세 번 주고받으며 시작하나', link: '/network/02-tcp-handshake' },
            { text: '빠르게 보내면 왜 안 되나', link: '/network/03-flow-congestion' },
            { text: 'UDP는 결함이 아니라 선택이다', link: '/network/04-tcp-vs-udp' }
          ]
        },
        {
          text: 'HTTP',
          collapsed: false,
          items: [
            { text: 'HTTP 메시지는 어떻게 생겼나', link: '/network/05-http-message' },
            { text: 'GET으로 삭제하면 왜 안 되나', link: '/network/06-method-status' },
            { text: 'HTTP는 왜 세 번 다시 태어났나', link: '/network/07-http-evolution' }
          ]
        },
        {
          text: '상태와 캐싱',
          collapsed: false,
          items: [
            { text: '무상태인데 로그인은 어떻게 유지되나', link: '/network/08-cookie-session' },
            { text: '같은 파일을 두 번 받지 않는 방법', link: '/network/09-http-caching' }
          ]
        },
        {
          text: '보안',
          collapsed: false,
          items: [
            { text: 'HTTPS는 무엇을 어떻게 지키나', link: '/network/10-https-tls' },
            { text: '브라우저는 왜 내 요청을 막나', link: '/network/11-sop-cors' }
          ]
        },
        {
          text: '이름과 성능',
          collapsed: false,
          items: [
            { text: '도메인은 어떻게 IP가 되나', link: '/network/12-dns' }
          ]
        },
        {
          text: '브라우저와 API',
          collapsed: false,
          items: [
            { text: '페이지를 안 바꾸고 데이터만 받으려면', link: '/network/13-ajax-fetch' },
            { text: 'REST API는 무엇을 약속하나', link: '/network/14-rest-api' },
            { text: '서버가 먼저 말을 걸 수 있나', link: '/network/15-realtime' }
          ]
        },
        {
          text: '종합',
          collapsed: false,
          items: [
            { text: 'URL을 입력하면 무슨 일이 일어나나', link: '/network/16-url-to-screen' }
          ]
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
