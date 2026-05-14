#!/usr/bin/env python3
"""Update build_index.py with RT and Al Jazeera data."""

import re

with open('/home/jian/world-news-brief/build_index.py', 'r') as f:
    content = f.read()

# The WORLD_EN_ITEMS section ends with "]  # closing bracket"
# Need to find it and add RT + AJ items before the closing bracket

# Updated WORLD_EN_ITEMS with fresh BBC/NYT items from RSS + RT + Al Jazeera
# All from 14 May 2026

new_world_en = """WORLD_EN_ITEMS = [
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
        "zh": "古巴能源部长表示，由于美国主导的石油封锁导致大面积停电，该国局势\"极其紧张\"。古巴的柴油和石油储备已经完全耗尽。",
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
        "zh": "中国领导人习近平警告美国总统特朗普，台湾问题处理不当可能将两国推入\"非常危险的境地\"，称这是双边关系中最重要的议题。",
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
        "zh": "美国国务卿卢比奥表示，美国将寻求说服中国在伊朗问题上发挥\"更积极的作用\"，参与正在持续的中东危机谈判。",
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
        "zh": "乌克兰总统泽连斯基表示，自周三以来俄罗斯向乌克兰发射了\"超过1560架无人机\"，造成至少三人死亡和大范围破坏。",
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
        "zh": "被国际刑事法院通缉的参议员罗纳德·\"巴托\"·德拉罗莎逃离了菲律宾参议院大楼，此前他一直藏身其中。现场传出枪声。",
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
]"""

new_tech_en = """TECH_EN_ITEMS = [
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
        "zh": "Wi-Fi连接和基于应用的科技产品正引发越来越多的反弹——消费者开始以\"追求简约\"为名，选择非智能的替代品。",
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
]"""

# Replace WORLD_EN_ITEMS
pattern_world = r'WORLD_EN_ITEMS\s*=\s*\[.*?^\]'
content = re.sub(pattern_world, new_world_en, content, flags=re.DOTALL | re.MULTILINE)

# Replace TECH_EN_ITEMS
pattern_tech = r'TECH_EN_ITEMS\s*=\s*\[.*?^\]'
content = re.sub(pattern_tech, new_tech_en, content, flags=re.DOTALL | re.MULTILINE)

# Update the source badges in the footer to include RT and Al Jazeera
content = content.replace(
    "Sources: BBC · The New York Times &nbsp;|&nbsp; English with Chinese translation",
    "Sources: BBC · New York Times · RT · Al Jazeera &nbsp;|&nbsp; English with Chinese translation"
)

with open('/home/jian/world-news-brief/build_index.py', 'w') as f:
    f.write(content)

print("build_index.py updated successfully")
