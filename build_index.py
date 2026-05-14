#!/usr/bin/env python3
"""Build the complete World News Brief index.html with fresh content."""

HEAD = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>World News Brief · 全球新闻简报</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: { extend: { fontFamily: { sans: ['Inter', 'system-ui', 'sans-serif'] } } }
        }
    </script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        html { scroll-behavior: smooth; }
        body { font-family: 'Inter', system-ui, sans-serif; }
        .gradient-header { background: linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #3730a3 100%); }
        .dark .gradient-header { background: linear-gradient(135deg, #0f0d2e 0%, #1e1b4b 50%, #312e81 100%); }
        .lang-btn { cursor: pointer; transition: all 0.2s; }
        .lang-btn.active { background: rgba(255,255,255,0.2); font-weight: 600; }
        .content-panel { display: none; }
        .content-panel.active { display: block; }
        .zh-text { font-family: 'Inter', 'Noto Sans SC', system-ui, sans-serif; }
        .accordion-btn { cursor: pointer; transition: background-color 0.2s; }
        .accordion-btn:hover { background-color: rgba(99,102,241,0.04); }
        .dark .accordion-btn:hover { background-color: rgba(99,102,241,0.08); }
        .accordion-btn.open { background-color: rgba(99,102,241,0.06); }
        .dark .accordion-btn.open { background-color: rgba(99,102,241,0.1); }
        .accordion-icon { transition: transform 0.3s ease; font-size: 1.25rem; line-height: 1; }
        .accordion-btn.open .accordion-icon { transform: rotate(45deg); }
        .accordion-body {
            max-height: 0; overflow: hidden;
            transition: max-height 0.35s ease, opacity 0.3s ease, padding 0.3s ease;
            opacity: 0; padding: 0 1.25rem;
        }
        .accordion-body.open {
            max-height: 400px; opacity: 1; padding: 0 1.25rem 1.25rem;
        }
        .fade-in { animation: fadeIn 0.5s ease-out both; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }
    </style>
</head>
<body class="bg-slate-50 dark:bg-slate-900 text-slate-800 dark:text-slate-200 transition-colors duration-200">

    <!-- Header -->
    <header class="gradient-header text-white py-10 px-4 shadow-xl mb-10 relative overflow-hidden">
        <div class="absolute inset-0 opacity-10" style="background-image: radial-gradient(circle at 20% 50%, rgba(255,255,255,0.2) 0%, transparent 60%);"></div>
        <div class="max-w-3xl mx-auto text-center relative z-10">
            <h1 class="text-4xl sm:text-5xl font-extrabold tracking-tight mb-2">🌍 World News Brief</h1>
            <p class="text-lg text-indigo-200 font-medium">Click a headline to read the full story</p>
            <div class="mt-4 flex items-center justify-center gap-2 text-sm text-indigo-300">
                <span id="date-display" class="bg-white/10 px-3 py-1 rounded-full">Thursday, 14 May 2026 · Auckland, NZ</span>
                <span class="bg-white/10 px-3 py-1 rounded-full">New Zealand</span>
            </div>
            <div class="mt-5 inline-flex bg-white/10 rounded-full p-1 text-sm">
                <button onclick="switchLang('en')" id="lang-en" class="lang-btn active px-4 py-1.5 rounded-full">🇬🇧 English 中英对照</button>
                <button onclick="switchLang('zh')" id="lang-zh" class="lang-btn px-4 py-1.5 rounded-full">🇨🇳 中文 中文来源</button>
            </div>
        </div>
    </header>

    <main class="max-w-3xl mx-auto px-4 pb-24">

        <!-- ===== ENGLISH PANEL: BBC/NYT with Chinese translation ===== -->
        <div id="panel-en" class="content-panel active">

            <section class="mb-10 fade-in">
                <div class="flex items-center justify-between mb-4">
                    <h2 class="flex items-center text-2xl font-bold text-indigo-900 dark:text-indigo-300">
                        <span class="mr-3 text-3xl">📰</span> World Headlines
                        <span class="ml-3 text-xs font-normal text-slate-400">中英对照</span>
                    </h2>
                    <span class="text-xs text-slate-400 dark:text-slate-500 bg-slate-100 dark:bg-slate-800 px-2 py-1 rounded-full">Click to expand</span>
                </div>
                <div class="bg-white dark:bg-slate-800 rounded-xl shadow-sm divide-y divide-slate-100 dark:divide-slate-700 overflow-hidden">
                    <!-- WORLD_NEWS_EN_START -->
'''

WORLD_EN_ITEMS = [
    {
        "title": "Watch: What happened on day one of Trump's China visit?",
        "source": "BBC",
        "date": "14 May 2026",
        "summary": "China welcomed US President Donald Trump with cheering children and a troop parade on Thursday, before a nearly two-hour long meeting with Xi Jinping covering trade, Taiwan, and global security issues.",
        "zh": "中国以欢呼的儿童和阅兵式欢迎美国总统特朗普，随后习近平与特朗普进行了近两个小时的会谈，涉及贸易、台湾和全球安全问题。",
        "url": "https://www.bbc.com/news/videos/c707xn4ew3po"
    },
    {
        "title": "Rescuers pull dead from rubble of Kyiv flats after massive Russian strikes",
        "source": "BBC",
        "date": "14 May 2026",
        "summary": "A 12-year-old girl is among the dead after Russia launched drones and missiles across Ukraine overnight. Emergency crews continue searching through debris as Kyiv reels from one of the largest aerial attacks in recent weeks.",
        "zh": "乌克兰官员表示，俄罗斯向乌克兰全境发动无人机和导弹袭击，一名12岁女孩在遇难者之列。紧急救援人员继续在废墟中搜寻，基辅正遭受数周来最大规模的空袭之一。",
        "url": "https://www.bbc.com/news/articles/cq5p8yygq94o"
    },
    {
        "title": "Latvian PM resigns after row over stray Ukrainian drones",
        "source": "BBC",
        "date": "14 May 2026",
        "summary": "Drones bound for Russia crashed down in Latvia last week, prompting a political fallout that has led to the resignation of Prime Minister Evika Silina amid the threat of a no-confidence vote.",
        "zh": "飞往俄罗斯的无人机上周在拉脱维亚坠毁，引发政治风波，导致总理埃维卡·西利娜在不信任投票威胁下宣布辞职。",
        "url": "https://www.bbc.com/news/articles/cwy21k5917jo"
    },
    {
        "title": "Cuba has run out of diesel and oil, energy minister says",
        "source": "BBC",
        "date": "14 May 2026",
        "summary": "Cuba's energy minister says the situation is 'extremely tense', as a US-led blockade of oil to the country causes widespread power cuts. The country has completely run out of diesel and oil reserves.",
        "zh": "古巴能源部长表示，由于美国主导的石油封锁导致大面积停电，该国局势\u201c极其紧张\u201d。古巴的柴油和石油储备已经完全耗尽。",
        "url": "https://www.bbc.com/news/articles/cd7pyrj0vx7o"
    },
    {
        "title": "Court overturns Alex Murdaugh's murder convictions and orders new trial",
        "source": "BBC",
        "date": "14 May 2026",
        "summary": "The court has ordered a new trial over the June 2021 killings of Paul and Maggie Murdaugh, overturning the previous murder convictions of disgraced South Carolina attorney Alex Murdaugh.",
        "zh": "法院裁定撤销对亚历克斯·默道的谋杀定罪，并下令重审2021年6月保罗和玛吉·默道被杀案。这位南卡罗来纳州的前律师此前被判有罪。",
        "url": "https://www.bbc.com/news/articles/cedpvnq7wn1o"
    },
    {
        "title": "Israeli strikes in southern Lebanon kill 22 people, health ministry says",
        "source": "BBC",
        "date": "14 May 2026",
        "summary": "Eight children are among those reported dead after a series of air strikes hit the south of Beirut. The strikes mark a significant escalation in cross-border tensions.",
        "zh": "黎巴嫩卫生部称，以色列对黎巴嫩南部的空袭造成22人死亡，其中包括8名儿童。这是跨境紧张局势的显著升级。",
        "url": "https://www.bbc.com/news/articles/c1k2zekj8y9o"
    },
    {
        "title": "Key Moments From the First Day of Trump's China Visit",
        "source": "New York Times",
        "date": "14 May 2026",
        "summary": "During the first round of two days of talks, Xi Jinping issued a stern warning about Taiwan while Trump touted all the top business leaders in his delegation.",
        "zh": "在两日会谈的首轮中，习近平就台湾问题发出严厉警告，而特朗普则大力推介其代表团中的顶级商界领袖。",
        "url": "https://www.nytimes.com/2026/05/14/world/asia/trump-first-day-china-xi.html"
    },
    {
        "title": "Inside the Secret Mission to Fly Taiwan's President to Africa",
        "source": "New York Times",
        "date": "14 May 2026",
        "summary": "From satellite phone check-ins to a borrowed royal plane, new details show how Taiwan's leader's team outwitted China and pulled off an audacious journey to southern Africa.",
        "zh": "从卫星电话签到借用王室飞机，新细节揭示了台湾领导人的团队如何智胜中国，完成了一次前往南部非洲的大胆旅程。",
        "url": "https://www.nytimes.com/2026/05/14/world/asia/taiwan-eswatini-china-flight.html"
    },
    {
        "title": "Duterte Ally Flees to Evade I.C.C. Arrest Warrant After Chaos at Philippine Senate",
        "source": "New York Times",
        "date": "14 May 2026",
        "summary": "Senator Ronald dela Rosa, who is wanted by the International Criminal Court in The Hague, had been holed up in the building when shots rang out. He later fled to evade the arrest warrant.",
        "zh": "被国际刑事法院通缉的菲律宾参议员罗纳德·德拉罗莎此前藏身参议院大楼内，现场传出枪声。他随后逃离以躲避逮捕令。",
        "url": "https://www.nytimes.com/2026/05/14/world/asia/philippines-dela-rosa-senate-icc-warrant-duterte.html"
    },
    {
        "title": "Russia Pummels Kyiv After Putin Hints That War Could End Soon",
        "source": "New York Times",
        "date": "14 May 2026",
        "summary": "At least five people were killed and dozens were wounded in a drone and missile strike, the latest in a series of attacks since a three-day truce expired on Monday.",
        "zh": "在无人机和导弹袭击中，至少五人死亡，数十人受伤。这是自周一三天停火到期以来一系列攻击中的最新一次。",
        "url": "https://www.nytimes.com/2026/05/14/world/europe/ukraine-strike-kyiv-russia-putin.html"
    },
    {
        "title": "Argentina Races To Find Origin of Hantavirus Outbreak",
        "source": "New York Times",
        "date": "14 May 2026",
        "summary": "The scientific investigation into the origin of a cruise ship hantavirus infection has become entangled with international finger pointing as Argentina races to contain the outbreak.",
        "zh": "对邮轮汉坦病毒爆发源头的科学调查已与国际间的相互指责纠缠在一起，阿根廷正争分夺秒控制疫情。",
        "url": "https://www.nytimes.com/2026/05/14/world/americas/hantavirus-cruise-ship-argentina.html"
    },
    {
        "title": "China Restores Beef Trade With U.S. as Goodwill Gesture for Trump Visit",
        "source": "New York Times",
        "date": "14 May 2026",
        "summary": "Beijing approved export licenses for hundreds of American slaughterhouses to resume beef shipments, ending a 15-month ban as a goodwill gesture for Trump's visit.",
        "zh": "北京批准了数百家美国屠宰场的出口许可证，恢复牛肉运输，结束了长达15个月的禁令，作为特朗普访华的善意姿态。",
        "url": "https://www.nytimes.com/2026/05/14/world/asia/trump-china-beef.html"
    },
    {
        "title": "Xi warns Trump over Taiwan",
        "source": "RT",
        "date": "14 May 2026",
        "summary": "Chinese leader Xi Jinping warned US President Donald Trump that a standoff over Taiwan could push the two countries into 'a very dangerous situation,' describing it as the single most important issue in bilateral relations.",
        "zh": "中国领导人习近平警告美国总统特朗普，台湾问题处理不当可能将两国推入\u201c非常危险的境地\u201d，称这是双边关系中最重要的议题。",
        "url": "https://www.rt.com/news/639971-xi-warns-trump-taiwan/"
    },
    {
        "title": "NATO member's government collapses after Ukrainian drone incident",
        "source": "RT",
        "date": "14 May 2026",
        "summary": "Latvian Prime Minister Evika Silina has resigned amid a government crisis caused by an incident involving Ukrainian kamikaze drones hitting an oil depot near the Russian border.",
        "zh": "拉脱维亚总理埃维卡·西利娜因乌克兰自杀式无人机袭击俄边境附近油库事件引发的政府危机而宣布辞职。",
        "url": "https://www.rt.com/news/639977-latvian-prime-minister-resigns/"
    },
    {
        "title": "Gulf states attacked Iraq amid waning faith in US – Reuters",
        "source": "RT",
        "date": "14 May 2026",
        "summary": "Saudi Arabia and Kuwait conducted covert strikes on targets in Iraq linked to Iranian-backed paramilitary groups during the Middle East war, reflecting fading trust in the US security umbrella.",
        "zh": "据路透社报道，沙特阿拉伯和科威特在中东战争期间对伊拉克境内与伊朗支持的准军事组织有关的目标进行了秘密打击，反映出对美国安全保护伞信任的减弱。",
        "url": "https://www.rt.com/news/639970-saudi-arabia-kuwait-strikes-iraq/"
    },
    {
        "title": "US seeking to convince China to pressure Iran – Rubio",
        "source": "RT",
        "date": "14 May 2026",
        "summary": "US Secretary of State Marco Rubio said the US would seek to persuade China to play 'a more active role' in negotiations with Iran amid the ongoing Middle East crisis.",
        "zh": "美国国务卿卢比奥表示，美国将寻求说服中国在伊朗问题上发挥\u201c更积极的作用\u201d，参与正在持续的中东危机谈判。",
        "url": "https://www.rt.com/news/639967-rubio-china-pressure-iran/"
    },
    {
        "title": "Who are the US CEOs in China with Trump, and what's in it for them?",
        "source": "Al Jazeera",
        "date": "14 May 2026",
        "summary": "Top executives hope to expand their businesses in China as Trump aims for a win ahead of the midterm vote. Elon Musk is part of a delegation of business leaders to China.",
        "zh": "顶级高管希望在中国拓展业务，而特朗普则希望在中期选举前取得胜利。埃隆·马斯克是随行的商界领袖代表团成员之一。",
        "url": "https://www.aljazeera.com/news/2026/5/14/who-are-the-us-ceos-in-china-with-trump-and-whats-in-it-for-them"
    },
    {
        "title": "Russia launches hundreds more drones at Ukraine, killing three people",
        "source": "Al Jazeera",
        "date": "14 May 2026",
        "summary": "President Volodymyr Zelenskyy says Russia fired 'more than 1,560 drones' at Ukraine since Wednesday, killing at least three people and causing widespread damage.",
        "zh": "乌克兰总统泽连斯基表示，自周三以来俄罗斯向乌克兰发射了\u201c超过1560架无人机\u201d，造成至少三人死亡和大范围破坏。",
        "url": "https://www.aljazeera.com/news/2026/5/14/russia-launches-hundreds-more-drones-at-ukraine-killing-three-people"
    },
    {
        "title": "Trump praises China as he ignores question about Taiwan",
        "source": "Al Jazeera",
        "date": "14 May 2026",
        "summary": "During his visit to Beijing, Trump praised China while avoiding direct comment on the Taiwan question, as the two leaders held high-stakes talks.",
        "zh": "在访问北京期间，特朗普赞扬了中国，同时避免就台湾问题直接发表评论。两国领导人举行了备受瞩目的会谈。",
        "url": "https://www.aljazeera.com/video/newsfeed/2026/5/14/trump-praises-china-as-he-ignores-question-about-taiwan"
    },
    {
        "title": "Philippine politician wanted by ICC flees Senate",
        "source": "Al Jazeera",
        "date": "14 May 2026",
        "summary": "Senator Ronald 'Bato' dela Rosa, wanted by the International Criminal Court, fled the Philippine Senate building where he had taken refuge as shots rang out.",
        "zh": "被国际刑事法院通缉的参议员罗纳德·\u201c巴托\u201d·德拉罗莎逃离了菲律宾参议院大楼，此前他一直藏身其中。现场传出枪声。",
        "url": "https://www.aljazeera.com/news/2026/5/14/philippine-politician-wanted-by-icc-flees-senate"
    },
    {
        "title": "Iran war day 76: Vance says progress made in talks; Israel pounds Lebanon",
        "source": "Al Jazeera",
        "date": "14 May 2026",
        "summary": "US Vice President Vance says progress is being made in talks with Iran as President Trump begins his trip to China, while Israel continues strikes on Lebanon.",
        "zh": "美国副总统万斯表示与伊朗的谈判取得进展，总统特朗普开始访华行程，同时以色列继续对黎巴嫩进行打击。",
        "url": "https://www.aljazeera.com/news/2026/5/14/iran-war-day-76-vance-says-progress-made-in-talks-israel-pounds-lebanon"
    },
    {
        "title": "Federal judge blocks US sanctions against UN rapporteur Francesca Albanese",
        "source": "Al Jazeera",
        "date": "14 May 2026",
        "summary": "US sanctions imposed on UN expert Francesca Albanese by the Trump administration were temporarily blocked by a federal judge.",
        "zh": "联邦法官暂时阻止了特朗普政府对联合国专家弗兰切斯卡·阿尔巴内塞实施的制裁。",
        "url": "https://www.aljazeera.com/news/2026/5/14/federal-judge-blocks-us-sanctions-against-un-rapporteur-francesca-albanese"
    },
    {
        "title": "Japanese snacks go black-and-white: Why Iran war is driving up ink prices",
        "source": "Al Jazeera",
        "date": "14 May 2026",
        "summary": "Calbee says it would temporarily use only black and white colours on 14 of its products due to a lack of printing ink caused by the Iran war disrupting supply chains.",
        "zh": "日本卡乐比公司表示，由于伊朗战争导致供应链中断，印刷油墨短缺，将暂时在14种产品上仅使用黑白颜色。",
        "url": "https://www.aljazeera.com/news/2026/5/14/japanese-snacks-go-black-and-white-why-iran-war-is-driving-up-ink-prices"
    },
]

TECH_EN_ITEMS = [
    {
        "title": "HMRC to use AI from British tech firm to spot fraud and tax return errors",
        "source": "BBC",
        "date": "14 May 2026",
        "summary": "Quantexa, a financial data platform, won a £175 million contract to help HMRC spot fraud and tax return errors using AI technology.",
        "zh": "金融数据平台Quantexa赢得1.75亿英镑合同，将利用AI技术帮助英国税务海关总署识别欺诈和退税错误。",
        "url": "https://www.bbc.com/news/articles/c7v9ld262n4o"
    },
    {
        "title": "Thousands of Waymos recalled after robotaxi swept into a creek",
        "source": "BBC",
        "date": "14 May 2026",
        "summary": "The voluntary recall follows an incident on 20 April where an empty Waymo car entered a flooded road in San Antonio, Texas.",
        "zh": "此次自愿召回源于4月20日的一起事件——一辆空的Waymo自动驾驶出租车驶入了德克萨斯州圣安东尼奥的一条被水淹没的道路。",
        "url": "https://www.bbc.com/news/articles/cwy2011dl4xo"
    },
    {
        "title": "WhatsApp launches totally private 'incognito' conversations with its AI chatbot",
        "source": "BBC",
        "date": "14 May 2026",
        "summary": "A cyber security expert says deleting chat history could lead to a lack of accountability if things go wrong with the new private AI chatbot feature.",
        "zh": "网络安全专家表示，WhatsApp新推出的AI聊天机器人私密对话功能中删除聊天记录可能导致在出现问题时缺乏问责制。",
        "url": "https://www.bbc.com/news/articles/c99lmyr1dnxo"
    },
    {
        "title": "Why 'Smart' Products Have Started to Look Like the Dumb Choice",
        "source": "New York Times",
        "date": "14 May 2026",
        "summary": "How Wi-Fi-connecting, app-based technology has led to a growing backlash in the name of simplicity, as consumers increasingly choose 'dumb' alternatives.",
        "zh": "Wi-Fi连接和基于应用的科技产品正引发越来越多的反弹——消费者开始以\u201c追求简约\u201d为名，选择非智能的替代品。",
        "url": "https://www.nytimes.com/2026/05/14/magazine/dumb-phones-tvs-retronym-smart-tech.html"
    },
    {
        "title": "Crypto Industry Pushes a Bill to Tilt Regulation in Its Favor",
        "source": "New York Times",
        "date": "14 May 2026",
        "summary": "After a series of political victories under President Trump, crypto firms are lobbying Congress for a sweeping regulatory framework they helped shape.",
        "zh": "在特朗普总统任内取得一系列政治胜利后，加密货币企业正游说国会通过它们参与制定的全面监管框架。",
        "url": "https://www.nytimes.com/2026/05/14/technology/cryptocurrency-clarity-act-senate.html"
    },
    {
        "title": "Dozens of Polymarket Bets Show Signs of Insider Trading, The Times Finds",
        "source": "New York Times",
        "date": "14 May 2026",
        "summary": "Dozens of long-shot bets on Polymarket, from the war with Iran to the cryptocurrency market, have defied the odds, according to a New York Times examination.",
        "zh": "《纽约时报》调查发现，Polymarket上的数十个冷门赌注——从伊朗战争到加密货币市场——都出现了异常赔率，显示出内幕交易的迹象。",
        "url": "https://www.nytimes.com/2026/05/13/technology/polymarket-insider-trading.html"
    },
    {
        "title": "Anduril Raises $5 Billion in Funding and Is Valued at $61 Billion",
        "source": "New York Times",
        "date": "14 May 2026",
        "summary": "The start-up, which makes A.I.-backed weapons, was valued at $61 billion in the financing round, double what it was a year ago.",
        "zh": "这家制造AI驱动武器的初创公司在此轮融资中估值达610亿美元，是一年前的两倍。",
        "url": "https://www.nytimes.com/2026/05/13/technology/anduril-raises-5-billion.html"
    },
    {
        "title": "Silicon Valley's A.I. Lobbying Blitz Reaches a Fever Pitch",
        "source": "New York Times",
        "date": "14 May 2026",
        "summary": "OpenAI and Anthropic are opening offices in Washington, hiring lobbyists and spending more than ever to win over federal lawmakers.",
        "zh": "OpenAI和Anthropic正在华盛顿开设办事处、雇佣说客，并投入前所未有的资金以争取联邦立法者的支持。",
        "url": "https://www.nytimes.com/2026/05/13/technology/ai-lobbying-washington-openai-anthropic.html"
    },
]

WORLD_ZH_ITEMS = [
    {
        "title": "习近平：将构建建设性战略稳定关系作为中美关系新定位",
        "source": "联合早报",
        "date": "2026年5月14日",
        "summary": "中国国家主席习近平在与美国总统特朗普会晤时提出，应将构建建设性战略稳定关系作为中美关系的新定位，推动两国关系健康稳定发展。",
        "url": "https://www.zaobao.com.sg/news/singapore/story20260514-9047294"
    },
    {
        "title": "分析：习近平涉台表述较过去更重 凸显北京急迫感",
        "source": "联合早报",
        "date": "2026年5月14日",
        "summary": "学者分析指出，习近平在习川会上关于台湾问题的表述较以往更为严厉，直指台湾问题是中美关系中最重要的问题，处理不好将导致冲突。",
        "url": "https://www.zaobao.com.sg/news/china/story20260514-9047950"
    },
    {
        "title": "习近平直球对决川普台湾问题！郭正亮惊：有史以来第一次",
        "source": "中天新闻",
        "date": "2026年5月14日",
        "summary": "中国大陆国家主席习近平今日在北京人民大会堂与美国总统川普进行逾2小时会谈。前立委郭正亮直言，习近平当着川普面前强调台湾问题的重要程度，这是有史以来第一次。",
        "url": "https://ctinews.com/news/items/4OaZq9NqW6"
    },
    {
        "title": "習川會雙方可以談出好結果！龔明鑫強調：台美經貿關係不變",
        "source": "中天新闻",
        "date": "2026年5月14日",
        "summary": "經濟部長龔明鑫表示，他樂見「習川會」美中可以談出好結果，讓雙方關係和緩，他認為台美深化經貿關係，這場會面應該對台灣不會有太大影響。",
        "url": "https://ctinews.com/news/items/4Xam4J2JWA"
    },
    {
        "title": "41项空间科学实验项目随天舟十号上行中国空间站",
        "source": "CCTV",
        "date": "2026年5月14日",
        "summary": "天舟十号货运飞船携带41项空间科学实验项目上行中国空间站，涵盖空间生命科学、微重力物理、空间天文等多个领域。",
        "url": "https://tv.cctv.com/2026/05/14/VIDE41jmzeQap4PsLGm3C6gW260514.shtml"
    },
    {
        "title": "外资在华研发中心进入量质齐升加速期",
        "source": "CCTV",
        "date": "2026年5月14日",
        "summary": "跨国公司纷纷加大在华研发投入，外资研发中心正进入数量和质量同步提升的加速期，反映出中国市场吸引力的持续增强。",
        "url": "https://news.cctv.com/2026/05/14/ARTIWi7SYpWlrohb7g5wVfza260514.shtml"
    },
    {
        "title": "专家解读特朗普访华：终结了中美外交冷淡期，开启新的外交阶段",
        "source": "凤凰卫视",
        "date": "2026年5月14日",
        "summary": "凤凰卫视专家分析指出，特朗普此次访华标志着中美外交冷淡期的结束，两国关系进入新的外交阶段。双方在贸易、台湾等核心议题上进行了深入交流。",
        "url": "https://news.ifeng.com/c/8t7irHByBw3"
    },
    {
        "title": "印度再次请求美国延长俄油豁免期限",
        "source": "凤凰卫视",
        "date": "2026年5月14日",
        "summary": "据报道，印度再次向美国提出请求，希望延长其对俄罗斯石油进口的豁免期限，以避免因制裁受到冲击。",
        "url": "https://news.ifeng.com/c/8t7lSVW4NfC"
    },
    {
        "title": "新华社快讯：习近平为美国总统特朗普举行欢迎宴会",
        "source": "观察者网",
        "date": "2026年5月14日",
        "summary": "国家主席习近平为来华进行国事访问的美国总统特朗普举行欢迎宴会，中美两国领导人共同出席宴会并发表讲话。",
        "url": "https://www.guancha.cn/politics/2026_05_14_817046.shtml"
    },
    {
        "title": '中美关系新定位！如何理解\u201c中美建设性战略稳定关系\u201d？',
        "source": "观察者网",
        "date": "2026年5月14日",
        "summary": "观察者网分析指出，习近平提出的\"中美建设性战略稳定关系\"新定位，标志着中美关系进入新的发展阶段，双方在核心利益问题上进行了坦诚交流。",
        "url": "https://www.guancha.cn/internation/2026_05_14_817008.shtml"
    },
    {
        "title": "习近平为特朗普举行欢迎宴会 中美领导人同游天坛",
        "source": "参考消息",
        "date": "2026年5月14日",
        "summary": "美国总统特朗普14日抵达北京，开始对中国进行国事访问。习近平主席为特朗普举行欢迎仪式和宴会，两国领导人还一同参观天坛。双方举行了近两个小时的会谈，就双边关系和共同关心的国际地区问题交换意见。",
        "url": "https://www.cankaoxiaoxi.com/"
    },
    {
        "title": "4月份我国电商物流运行稳中有升",
        "source": "CCTV",
        "date": "2026年5月14日",
        "summary": "数据显示，4月份我国电商物流运行呈现稳中有升态势，网购消费需求持续释放，物流配送效率进一步提升。",
        "url": "https://news.cctv.com/2026/05/14/ARTI1B7biQF6Cm9zztL1wvAW260514.shtml"
    },
]

TECH_ZH_ITEMS = [
    {
        "title": "黄仁勋独家回应凤凰：为何最后一刻才上飞机",
        "source": "凤凰卫视",
        "date": "2026年5月14日",
        "summary": "英伟达CEO黄仁勋接受凤凰卫视独家专访，回应为何在最后一刻才登上前往中国的飞机，透露此行与中美科技合作、AI芯片市场等议题相关。",
        "url": "https://news.ifeng.com/c/8t7kUH1MOP7"
    },
    {
        "title": "\"林龙\"AI大模型上岗 大山的\"数字大脑\"",
        "source": "CCTV",
        "date": "2026年5月14日",
        "summary": "名为林龙的AI大模型正式上岗，成为大山的数字大脑，为林业管理、生态保护等提供智能化解决方案。",
        "url": "https://tv.cctv.com/2026/05/14/VIDEod2DlOod74hDpNB5m2X5260514.shtml"
    },
    {
        "title": "清洁能源基地项目\"进度条\"提速",
        "source": "CCTV",
        "date": "2026年5月14日",
        "summary": "中国多个清洁能源基地项目建设进度加快，包括风电、光伏和水电在内的可再生能源项目正进入集中投产期。",
        "url": "https://news.cctv.com/2026/05/14/ARTIg79kLUllfvIIWfsMQII1260514.shtml"
    },
    {
        "title": "资媒局：AI代理OpenClaw有网安风险 企业和个人须谨慎使用",
        "source": "联合早报",
        "date": "2026年5月14日",
        "summary": "新加坡资讯通信媒体发展局警告，AI代理OpenClaw存在网络安全风险，建议企业和个人谨慎使用该技术工具。",
        "url": "https://www.zaobao.com.sg/news/singapore/story20260514-9047780"
    },
    {
        "title": "联想确认成为英伟达H200中国分销商",
        "source": "观察者网",
        "date": "2026年5月14日",
        "summary": "联想集团正式确认成为英伟达H200人工智能芯片在中国的分销商，此举将进一步推动中国AI产业的发展。",
        "url": "https://www.guancha.cn/economy/2026_05_14_817027.shtml"
    },
    {
        "title": "印度首座晶圆厂将投产，\"产能沧海一粟，中国攻势强劲\"",
        "source": "观察者网",
        "date": "2026年5月14日",
        "summary": "印度首座半导体晶圆厂即将投产，但分析指出其产能相比中国仍然微不足道，中国在半导体领域的攻势依然强劲。",
        "url": "https://www.guancha.cn/internation/2026_05_14_817021.shtml"
    },
    {
        "title": "将矛头指向AI，看似痛快实则错位",
        "source": "观察者网",
        "date": "2026年5月14日",
        "summary": "评论文章指出，将当前社会问题简单归咎于人工智能，虽然看似痛快但实则是一种错位的认知，需要更深入思考技术与社会的互动关系。",
        "url": "https://www.guancha.cn/liuhaoyan/2026_05_14_816937.shtml"
    },
    {
        "title": "顶尖人才加速回流中国，\"这样的美国确实让我更爱国了\"",
        "source": "观察者网",
        "date": "2026年5月14日",
        "summary": "越来越多的中国顶尖科技人才选择从美国回到中国发展，受访者表示美国社会环境和政策变化促使他们做出了回国决定。",
        "url": "https://www.guancha.cn/internation/2026_05_14_817005.shtml"
    },
    {
        "title": "中天新闻AI实验室：人工智能辅助新闻生产新尝试",
        "source": "中天新闻",
        "date": "2026年5月14日",
        "summary": "中天新闻推出AI实验室，探索人工智能在新闻采集、编辑和分发中的应用，旨在提升新闻报道的效率和准确性。",
        "url": "https://ctinews.com/news/items/4Xam4JMXWA"
    },
    {
        "title": "参考消息：全球科技巨头看好中国AI市场前景",
        "source": "参考消息",
        "date": "2026年5月14日",
        "summary": "多家全球科技巨头纷纷表示看好中国人工智能市场的发展前景，计划加大在华投资力度。包括英伟达、微软在内的企业正在扩大在华研发团队。",
        "url": "https://www.cankaoxiaoxi.com/"
    },
]


def make_en_item(item):
    return f'''<div class="fade-in">
                    <button onclick="toggleNews(this)" class="accordion-btn w-full flex items-center justify-between px-5 py-4 text-left">
                        <span class="font-semibold text-base text-slate-900 dark:text-white pr-4">{item['title']}</span>
                        <span class="accordion-icon text-indigo-400 dark:text-indigo-500 shrink-0 text-xl leading-none">+</span>
                    </button>
                    <div class="accordion-body">
                        <div class="flex items-center gap-2 mb-2 flex-wrap">
                            <span class="text-xs font-medium text-indigo-600 dark:text-indigo-400 bg-indigo-50 dark:bg-indigo-900/30 px-2 py-0.5 rounded-full">{item['source']}</span>
                            <span class="text-xs text-slate-400 dark:text-slate-500">| {item['date']}</span>
                        </div>
                        <p class="text-sm text-slate-600 dark:text-slate-400 leading-relaxed mb-2">{item['summary']}</p>
                        <div class="border-t border-slate-100 dark:border-slate-700 pt-2 mt-2">
                            <p class="text-xs text-indigo-400 dark:text-indigo-500 font-medium mb-1">🇨🇳 中文</p>
                            <p class="text-sm text-slate-500 dark:text-slate-400 leading-relaxed">{item['zh']}</p>
                        </div>
                        <a href="{item['url']}" target="_blank" rel="noopener noreferrer" class="inline-flex items-center text-sm font-medium text-indigo-600 dark:text-indigo-400 hover:underline mt-2">Read full article →</a>
                    </div>
                </div>'''


def make_zh_item(item):
    return f'''<div class="fade-in">
                    <button onclick="toggleNews(this)" class="accordion-btn w-full flex items-center justify-between px-5 py-4 text-left">
                        <span class="font-semibold text-base text-slate-900 dark:text-white pr-4">{item['title']}</span>
                        <span class="accordion-icon text-indigo-400 dark:text-indigo-500 shrink-0 text-xl leading-none">+</span>
                    </button>
                    <div class="accordion-body">
                        <div class="flex items-center gap-2 mb-2 flex-wrap">
                            <span class="text-xs font-medium text-indigo-600 dark:text-indigo-400 bg-indigo-50 dark:bg-indigo-900/30 px-2 py-0.5 rounded-full">{item['source']}</span>
                            <span class="text-xs text-slate-400 dark:text-slate-500">| {item['date']}</span>
                        </div>
                        <p class="text-sm text-slate-600 dark:text-slate-400 leading-relaxed mb-3">{item['summary']}</p>
                        <a href="{item['url']}" target="_blank" rel="noopener noreferrer" class="inline-flex items-center text-sm font-medium text-indigo-600 dark:text-indigo-400 hover:underline">阅读全文 →</a>
                    </div>
                </div>'''


def build():
    sections = []

    # HEAD
    sections.append(HEAD)

    # World News EN
    for item in WORLD_EN_ITEMS:
        sections.append(make_en_item(item))

    sections.append('''                    <!-- WORLD_NEWS_EN_END -->
                </div>
            </section>

            <section class="mb-10 fade-in" style="animation-delay: 0.15s">
                <div class="flex items-center justify-between mb-4">
                    <h2 class="flex items-center text-2xl font-bold text-indigo-900 dark:text-indigo-300">
                        <span class="mr-3 text-3xl">🚀</span> Tech Frontiers
                        <span class="ml-3 text-xs font-normal text-slate-400">中英对照</span>
                    </h2>
                    <span class="text-xs text-slate-400 dark:text-slate-500 bg-slate-100 dark:bg-slate-800 px-2 py-1 rounded-full">Click to expand</span>
                </div>
                <div class="bg-white dark:bg-slate-800 rounded-xl shadow-sm divide-y divide-slate-100 dark:divide-slate-700 overflow-hidden">
                    <!-- TECH_NEWS_EN_START -->
''')

    # Tech News EN
    for item in TECH_EN_ITEMS:
        sections.append(make_en_item(item))

    sections.append('''                    <!-- TECH_NEWS_EN_END -->
                </div>
            </section>

            <div class="text-center text-xs text-slate-400 dark:text-slate-600 mt-2 italic">
                Sources: BBC · New York Times · RT · Al Jazeera &nbsp;|&nbsp; English with Chinese translation
            </div>
        </div>

        <!-- ===== CHINESE PANEL: Only Chinese news sources ===== -->
        <div id="panel-zh" class="content-panel zh-text">

            <section class="mb-10 fade-in">
                <div class="flex items-center justify-between mb-4">
                    <h2 class="flex items-center text-2xl font-bold text-indigo-900 dark:text-indigo-300">
                        <span class="mr-3 text-3xl">📰</span> 世界头条
                    </h2>
                    <span class="text-xs text-slate-400 dark:text-slate-500 bg-slate-100 dark:bg-slate-800 px-2 py-1 rounded-full">点击展开</span>
                </div>
                <div class="bg-white dark:bg-slate-800 rounded-xl shadow-sm divide-y divide-slate-100 dark:divide-slate-700 overflow-hidden">
                    <!-- WORLD_NEWS_ZH_START -->
''')

    # World News ZH
    for item in WORLD_ZH_ITEMS:
        sections.append(make_zh_item(item))

    sections.append('''                    <!-- WORLD_NEWS_ZH_END -->
                </div>
            </section>

            <section class="mb-10 fade-in" style="animation-delay: 0.15s">
                <div class="flex items-center justify-between mb-4">
                    <h2 class="flex items-center text-2xl font-bold text-indigo-900 dark:text-indigo-300">
                        <span class="mr-3 text-3xl">🚀</span> 科技前沿
                    </h2>
                    <span class="text-xs text-slate-400 dark:text-slate-500 bg-slate-100 dark:bg-slate-800 px-2 py-1 rounded-full">点击展开</span>
                </div>
                <div class="bg-white dark:bg-slate-800 rounded-xl shadow-sm divide-y divide-slate-100 dark:divide-slate-700 overflow-hidden">
                    <!-- TECH_NEWS_ZH_START -->
''')

    # Tech News ZH
    for item in TECH_ZH_ITEMS:
        sections.append(make_zh_item(item))

    sections.append('''                    <!-- TECH_NEWS_ZH_END -->
                </div>
            </section>

            <div class="text-center text-xs text-slate-400 dark:text-slate-600 mt-2 italic">
                来源：CCTV · 凤凰卫视 · 中天新闻 · 联合早报 · 观察者网 · 参考消息
            </div>
        </div>

    </main>

    <footer class="fixed bottom-0 w-full bg-white/90 dark:bg-slate-800/90 backdrop-blur-sm border-t border-slate-200 dark:border-slate-700 py-3 px-4 text-center">
        <div class="max-w-3xl mx-auto flex items-center justify-center gap-4 text-xs text-slate-400 dark:text-slate-500">
            <span>Powered by Hermes Agent &amp; GitHub Pages</span>
            <span>·</span>
            <span>Updated Daily at 8 AM NZST</span>
        </div>
    </footer>

    <script>
        function toggleNews(btn) {
            const body = btn.nextElementSibling;
            btn.closest('.divide-y').querySelectorAll('.accordion-body.open').forEach(b => {
                if (b !== body) {
                    b.classList.remove('open');
                    b.previousElementSibling.classList.remove('open');
                }
            });
            body.classList.toggle('open');
            btn.classList.toggle('open');
        }

        function switchLang(lang) {
            document.querySelectorAll('.content-panel').forEach(p => p.classList.remove('active'));
            document.querySelectorAll('.lang-btn').forEach(b => b.classList.remove('active'));
            document.getElementById('panel-' + lang).classList.add('active');
            document.getElementById('lang-' + lang).classList.add('active');
        }

        if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
            document.documentElement.classList.add('dark');
        }
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
            document.documentElement.classList.toggle('dark', e.matches);
        });
    </script>
</body>
</html>
''')

    return ''.join(sections)


if __name__ == '__main__':
    html = build()
    with open('/home/jian/world-news-brief/index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'Written {len(html)} bytes to index.html')
