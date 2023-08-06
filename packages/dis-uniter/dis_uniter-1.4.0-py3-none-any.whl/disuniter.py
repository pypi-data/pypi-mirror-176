from http import server
import os, time, logging, glob, threading, asyncio, re, time, datetime
from logging import handlers
from urllib import request

escaper = re.compile(r"([*_\\]|~~|\|\|)").sub
logs = re.compile("(?=^(⚠ |)\d+: )").split
digits = re.compile("\d+").search
errors = re.compile("(?m)^⚠.*$").findall
subbers = [
    (repl, re.compile(pattern).sub)
    for repl, pattern in [
        ("&amp", "&"),
        ("&lt", "<"),
        ("&gt", ">"),
        (r"<a>\1</a>", r"&lt(.+:\/\/[^\w]*)&gt"),
        (r"<b>\1</b>", r"(?<!\\)\*\*(.+?)(?<!\\)\*\*"),
        (r"<i>\2</i>", r"(?<!\\)([*^])(.+?)(?<!\\)\1"),
        (r"<u>\1</u>", r"(?<!\\)__(.+?)(?<!\\)__"),
        (r"<strike>\1</strike>", r"(?<!\\)~~(.+?)(?<!\\)~~"),
        (r"<details>\1</details>", r"(?<!\\)\|\|(.+?)(?<!\\)\|\|"),
        (r"<blockquote><p>\1</blockquote>", r"^&gt&gt&gt (.+)"),
        (r"<blockquote><p>\1</blockquote>", r"^&lt (.+?)"),
        (
            lambda m: "<pre>" + escaper(r"\\\1", m.group(2)) + "</pre>",
            r"(?<!\\)(`(?:``|))(.+?)\1",
        ),
        ("", r"\\"),
    ]
]


class Log24H(logging.Handler):
    def emit(self, record):
        now = round(time.time() * 1000)
        day_ago = now - 864e5
        with open("logs", "a+") as f:
            f.write(
                f"{'⚠' if record.levelno > 10 else ''}{now}: {record.getMessage()}\n"
            )
            f.seek(0)
            data = f.read()
        with open("logs", "w+") as f:
            f.write(
                "".join(
                    x
                    for x in logs(data)
                    if (n := digits(x)) and int(n.group()) > day_ago
                )
            )


class DictClass:
    def __init__(self, data):
        for k, v in data.items():
            if k == "description":
                for repl, subber in subbers:
                    v = subber(repl, v)
            setattr(self, k, DictClass(v) if isinstance(v, dict) else v)


def keepAlive(bot):
    @bot.event
    async def on_ready():
        bot.info = DictClass(await bot.http.application_info())

        class Server(server.BaseHTTPRequestHandler):
            start = time.time()

            def log_request(self, code="", size=""):
                pass

            def do_HEAD(self):
                self.send_response(200)
                self.send_header(
                    "Content-Type",
                    "text/html;charset=utf-8",
                )
                self.send_header("Cache-Control", "no-cache")
                self.send_header("X-Content-Type-Options", "nosniff")
                self.end_headers()

            def do_OPTIONS(self):
                self.send_response(204)
                self.end_headers()

            def do_GET(self):
                self.do_HEAD()
                self.send_response(200)
                info = bot.info
                owner = info.owner
                team = info.team
                user = bot.user
                try:
                    install = f"<a href={info.custom_install_url}>Install</a>"
                except AttributeError:
                    try:
                        install = f"<a href=https://discord.com/api/oauth2/authorize?client_id={bot.info.id}&scope={'+'.join(bot.info.install_params.scopes)}&permissions={int(bot.info.install_params.permissions)}>Install</a>"
                    except AttributeError:
                        install = ""
                description = info.description
                with open("/proc/meminfo") as f:
                    next(f)
                    next(f)
                    mem = digits(next(f)).group()
                self.wfile.write(
                    f"{mem}kB{open('logs').read()}".encode()
                    if self.path == "/dbg"
                    else f"{mem}kB{chr(10).join(errors(open('logs').read()))}".encode()
                    if self.path == "/err"
                    else (
                        f"<!DOCTYPE html><meta charset=utf-8><meta name=viewport content='width=device-width'><meta name=description content='{description}'><link rel='shortcut icon'href={user.avatar}><html lang=en><script>let n,t;function l(){{let x=new XMLHttpRequest();x.open('GET',document.getElementById('s').innerText[0]=='S'?'err':'dbg');x.onload=r=>{{document.getElementById('l').innerText=r.srcElement.responseText.replace(/.+?kB/,r=>{{document.querySelector('tr:last-of-type td').innerText=r;return''}}).replace(/([0-9]+): /g,(_, d)=>`${{new Date(d/1).toLocaleString()}}: `)}};x.send()}};document.onvisibilitychange=()=>{{if(document.visibilityState=='hidden')clearInterval(n);else n=setInterval(l,5e3);}};onload=()=>{{setInterval(()=>{{let u=BigInt(Math.ceil(Date.now()/1000-{self.start}))\ndocument.getElementById('u').innerText=`${{u>86400n?`${{u/86400n}}d`:''}}${{u>3600n?`${{u/3600n%60n}}h`:''}}${{u>60n?`${{u/60n%24n}}m`:''}}${{`${{u%60n}}`}}s`}},1000)\ndocument.getElementById('r').innerText=new Date({self.start*1000}).toLocaleString();let d=document.getElementById('d'),f=new Intl.RelativeTimeFormat();d.innerHTML=`{description.replace('`', '')}`.replace(/&ltt:(\\d+):R&gt/g,(_,t)=>{{const r=t-Date.now(),a=Math.abs(r);return`<abbr title='${{new Date(t/1).toLocaleString(0,{{timeStyle:'short',dateStyle:'full'}})}}'>${{a>31536e6?f.format(r/31536e6,'year'):a>7884e6?f.format(r/7884e6,'quarter'):a>2628e6?f.format(r/2628e6,'month'):a>6048e5?f.format(r/6048e5,'week'):a>864e5?f.format(r/864e5,'day'):a>36e5?f.format(r/36e5,'hour'):a>6e4?f.format(r/6e4,'minute'):f.format(r/1e3,'second')}}</abbr>`}}).replace(/&ltt:(\\d+)(:[tdf])?&gt/gi,(_,t,m)=>{{const d=Date.prototype.toLocaleString.bind(new Date(t/1),0);m=m?.[1];return `<abbr title='${{d({{timeStyle:'short',dateStyle:'full'}})}}'>${{d({{timeStyle:{{t:'short',T:'long'}}[m],dateStyle:{{d:'short',D:'long'}}[m]}})}}</abbr>`}})}}</script><style>*:not(pre){{background-color:#FDF6E3;color:#657B83;font-family:sans-serif;text-align:center;margin:0 auto}}@media(prefers-color-scheme:dark){{*:not(pre){{background-color:#002B36;color:#839496}}}}blockquote>*{{border-color:#073642}}img{{height:1em}}td{{border:1px}}pre{{display:inline}}p{{white-space:pre-wrap}}body{{display:flex;flex-flow:row wrap;width:100vw}}#o,#v,#l{{overflow:auto}}#o{{min-width:min-content;flex:1}}#v{{height:100vh}}button{{display:inline-block}}a{{color:#268BD2}}</style><title>{user}</title><div id=o><h1>{user}<img src={user.avatar} alt></h1><p id=d><table><tr><th>Servers<td>{len(bot.guilds)}<tr><th>Latency<td>{round(bot.latency*1000)if bot.latency!=float('inf')else'Offline?'}ms<tr><th>Uptime<td id=u><tr><th>Up since<td id=r>{datetime.datetime.utcfromtimestamp(self.start).isoformat()}{f'<tr><th>Team<a href={team.icon}>{team.name}'+''.join(f'<tr><td><a href=https://discord.com/users/{m.id}>{m.username}</a><img src={m.avatar} alt>'for m in team.members)if team else f'<tr><th>Owner<td><a href=https://discord.com/users/{owner.id}><img src=https://cdn.discordapp.com/avatars/{owner.id}/{owner.avatar} alt>{owner.username}#{owner.discriminator}</a>'}<tr><th>Tags<td>{'<td>'.join(info.tags)}<tr><th>RAM available<td>{mem}kB</table>{install}<br></div>"
                        + "<div id=v><button id=s type=button onclick=\"document.getElementById('s').innerText=`${document.getElementById('s').innerText[0]=='S'?'Hide':'Show'} debug`\">Show debug</button><p><pre id=l></pre>"
                        if os.path.isfile("logs")
                        else ""
                    ).encode()
                )

        threading.Thread(
            target=server.ThreadingHTTPServer(("", 80), Server).serve_forever
        ).start()
        print(
            "Server is ready! \033[4mHit enter\033[0m to update bot/owner info shown on website"
        )
        while True:
            t = threading.Thread(target=input)
            t.start()
            while t.is_alive():
                await asyncio.sleep(0)
            bot.info = DictClass(await bot.http.application_info())

    intents = bot.intents
    if not (intents.presences or intents.members or intents.message_content):
        logger = logging.getLogger("discord")
        logger.setLevel(logging.DEBUG)
        logger.addHandler(Log24H())
    try:
        request.urlopen(
            f"https://up.repl.link/add?author={os.environ['REPL_OWNER'].lower()}&repl={os.environ['REPL_SLUG'].lower()}"
        )
    except:
        pass

    @bot.listen()
    async def on_disconnect():
        if not bot.ws or bot.is_ws_ratelimited():
            request.urlopen(
                f"https://cd594a2f-0e9f-48f1-b3eb-e7f6e8665adf.id.repl.co/{os.environ['REPL_ID']}"
            )
            os.kill(1, 1)

    try:
        bot.run(os.environ["DISCORD_TOKEN"])
    except Exception as err:
        if getattr(err, "status", 0) == 429:
            request.urlopen(
                f"https://cd594a2f-0e9f-48f1-b3eb-e7f6e8665adf.id.repl.co/{os.environ['REPL_ID']}"
            )
            os.kill(1, 1)
        raise err
