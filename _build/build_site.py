import sys, os
OUT = sys.argv[1]
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400;1,6..72,500&display=swap">'
BASE = "https://priflyadvisors.com/"
BOOK = "contact.html?topic=coaching"   # → Cal.com once set up
# Speaking enquiries (Ed, 2026-09-15): a pre-filled email, never a calendar, so Ed answers each date himself
from urllib.parse import quote
SPEAK_TO = "ed@priflyadvisors.com"   # → speaking@priflyadvisors.com once that alias exists
SPEAK = f"mailto:{SPEAK_TO}?subject={quote('Speaking enquiry: [your event]')}&amp;body=" + quote(
    "Hi Ed,\r\n\r\nWe'd like to talk to you about speaking at our event.\r\n\r\nEvent:\r\nDate(s) we have in mind:\r\n"
    "Location:\r\nAudience (who, and roughly how many):\r\nFormat (keynote, fireside, panel, working session):\r\nAnything else:\r\n")
TOMCAT = os.path.exists(os.path.join(OUT, "images", "tomcat.png"))

def nav(active):
    items = [("coaching.html", "Coaching", "coaching"), ("speaking.html", "Speaking", "speaking"),
             ("defence.html", "Defence", "defence"), ("about.html", "About", "about")]
    li = "".join(f'<li><a href="{h}"{" aria-current=\"page\"" if k == active else ""}>{t}</a></li>' for h, t, k in items)
    cur = ' aria-current="page"' if active == "contact" else ""
    return li + f'<li><a href="contact.html" class="btn-nav"{cur}>Contact</a></li>'

# Brand lock-up (Ed, review 1): PriFly Advisors primary on top, double gold rule with the Tomcat, "Ed Chandler, Founder" beneath
jet = '<img src="images/tomcat.png" alt="" width="39" height="24">' if TOMCAT else ""
BRAND = ('<a class="brand" href="index.html" aria-label="PriFly Advisors, Ed Chandler, Founder: home">'
         '<span class="firm-top">PriFly Advisors</span>'
         f'<span class="rulebar"><span class="rule2" aria-hidden="true"></span>{jet}</span>'
         '<span class="founder">Ed Chandler, Founder</span></a>')

def header(active):
    return f'<header><div class="wrap">{BRAND}<nav aria-label="Main"><ul>{nav(active)}</ul></nav></div></header>'

FOOTER = ('<footer><div class="wrap">' + BRAND +
          '<ul><li><a href="coaching.html">Coaching</a></li><li><a href="speaking.html">Speaking</a></li><li><a href="defence.html">Defence</a></li>'
          '<li><a href="about.html">About</a></li><li><a href="contact.html">Contact</a></li><li><a href="https://www.linkedin.com/in/edchandler96/" rel="noopener">LinkedIn</a></li></ul>'
          '<small>© 2026 E. M. Chandler LLC</small></div></footer>')

def page(slug, title, desc, active, body, extra_head=""):
    url = BASE + ("" if slug == "index" else slug)
    head = (f'<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">'
            f'<title>{title}</title><meta name="description" content="{desc}"><link rel="canonical" href="{url}">'
            f'<meta property="og:type" content="website"><meta property="og:url" content="{url}"><meta property="og:title" content="{title}"><meta property="og:description" content="{desc}">'
            f'<meta property="og:image" content="{BASE}images/ed-chandler.jpg"><meta name="twitter:card" content="summary">'
            f'<link rel="icon" type="image/svg+xml" href="favicon.svg">{FONTS}<link rel="stylesheet" href="style.css">{extra_head}')
    return f'<!DOCTYPE html>\n<html lang="en-GB">\n<head>{head}</head>\n<body>\n{header(active)}\n<main>\n{body}\n</main>\n{FOOTER}\n</body>\n</html>\n'

def cta(h, line, btn, href):
    return f'<section class="band cta"><div class="wrap"><div><h2>{h}</h2><p class="muted">{line}</p></div><div class="actions"><a class="btn" href="{href}">{btn} →</a></div></div></section>'

def phead(crumb, eyebrow, h1, lede, button=None, img=None):
    b = f'<div class="actions"><a class="btn" href="{button[1]}">{button[0]} →</a></div>' if button else ""
    text = f'<span class="eyebrow">{eyebrow}</span><h1>{h1}</h1><p class="lede">{lede}</p>{b}'
    fig = ""
    if img:
        fname, alt = img
        if os.path.exists(os.path.join(OUT, "images", fname)):
            fig = f'<figure class="phead-img"><img src="images/{fname}" alt="{alt}"></figure>'
        elif not LIVE:
            fig = '<figure class="phead-img"><div class="ph" aria-hidden="true">Photo to come</div></figure>'
    if fig:
        return f'<div class="phead"><div class="wrap phead-grid"><div class="phead-text">{text}</div>{fig}</div></div>'
    return f'<div class="phead"><div class="wrap">{text}</div></div>'

def sec(title, inner, band=False, tight=False):
    cls = " ".join(c for c, on in (("band", band), ("tight", tight)) if on)
    return f'<section{f" class=\"{cls}\"" if cls else ""}><div class="wrap"><div class="sec-head"><h2>{title}</h2></div>{inner}</div></section>'

# Photo row (Ed, review 1): mostly wordless images with short captions, replacing the credentials strip.
# Real photos go in images/photo-1.jpg … photo-3.jpg; until then placeholders show in the preview only
# (pass --live to build without placeholders).
LIVE = "--live" in sys.argv
PHOTOS = [("photo-1.jpg", "TOPGUN graduate and instructor"),
          ("photo-2.jpg", "Leading at NATO and U.S. Navy headquarters in Europe"),
          ("photo-3.jpg", "Speaker and moderator")]
def _fig(fname, cap):
    if os.path.exists(os.path.join(OUT, "images", fname)):
        return f'<figure><img src="images/{fname}" alt="{cap}" loading="lazy"><figcaption>{cap}</figcaption></figure>'
    return None if LIVE else f'<figure><div class="ph" aria-hidden="true">Photo to come</div><figcaption>{cap}</figcaption></figure>'
_figs = [f for f in (_fig(n, c) for n, c in PHOTOS) if f]
PHOTO_ROW = f'<section class="photos"><div class="wrap"><div class="photo-row">{"".join(_figs)}</div></div></section>' if _figs else ""

# ---------- HOME ----------
LD = ('<script type="application/ld+json">{"@context":"https://schema.org","@type":"ProfessionalService","name":"PriFly Advisors","url":"https://priflyadvisors.com/",'
      '"founder":{"@type":"Person","name":"Ed Chandler","jobTitle":"Executive coach and leadership advisor","sameAs":["https://www.linkedin.com/in/edchandler96/"]},'
      '"areaServed":["Portugal","Europe"],"address":{"@type":"PostalAddress","addressLocality":"Lisbon","addressCountry":"PT"},"email":"ed@priflyadvisors.com",'
      '"description":"Executive coaching and leadership advisory for founders and executives whose companies are growing faster than their leadership. Also speaking and transatlantic defence advisory."}</script>')

doors = [
    ("coaching.html", "Founders &amp; executives", "When the company is growing faster than its leadership", "Book a 30-minute call"),
    ("speaking.html", "Event organisers", "Planning a conference, summit or leadership offsite and need a speaker who holds the room", "Check availability for your date"),
    ("defence.html", "Defence companies", "Contract support and market entry across the Atlantic", "Start a conversation"),   # Ed, 2026-09-15: minimum essential
]
door_html = "".join(f'<li><a href="{h}"><span class="client">{c}</span><span class="desc">{d}</span><span class="go">{g} →</span></a></li>' for h, c, d, g in doors)

home = f'''
<div class="hero"><div class="wrap">
  <div class="hero-text">
    <h1>Leadership that performs <em>as a team</em></h1>
    <p class="lede">When every decision still comes back to you, the company can only move as fast as you can. I help you build a leadership team that makes the right calls without you in the room.</p>
    <div class="actions"><a class="btn" href="{BOOK}">Book a 30-minute call →</a><a class="btn ghost" href="coaching.html">How I work</a></div>
  </div>
  <figure class="portrait"><img src="images/ed-chandler.jpg" alt="Ed Chandler, founder of PriFly Advisors" width="650" height="900"></figure>
</div></div>
<section class="quote-band"><div class="wrap">
  <blockquote>“What got you here won’t get you there.”</blockquote>
  <cite>Marshall Goldsmith, executive coach and author</cite>
</div></section>
{PHOTO_ROW}
{sec("Who I work with", f'<ul class="index">{door_html}</ul>')}
{cta("Let's talk", "Whether it's a leadership challenge, a speaking engagement or a transatlantic defence question, reach out.", "Get in touch", "contact.html")}
'''

# ---------- COACHING ----------
import math as _m

# Growth graphic (Ed, 2026-09-15): the leader in the middle; only the leader's direct lines carry the
# stoplight colour (green = manageable, red = strained); every other relationship is blue.
# A ✓ / ! badge next to the leader is the second cue, so colour is never the only signal.
_PEOPLE, _BLUE, _GREEN, _RED = "#56627A", "#3A6BC8", "#2F8A5E", "#C0392B"

def _leader_svg(n, status, label):
    size, c = 250, 125
    R = 95 if n <= 10 else 105
    s = 1.3 if n <= 10 else 1.0
    col, icon, blue_op = (_GREEN, "✓", .45) if status == "ok" else (_RED, "!", .25)
    ring = n - 1
    pts = [(c + R * _m.cos(2 * _m.pi * i / ring - _m.pi / 2), c + R * _m.sin(2 * _m.pi * i / ring - _m.pi / 2)) for i in range(ring)]
    others = "".join(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}"/>'
                     for i, a in enumerate(pts) for b in pts[i + 1:])
    mine = "".join(f'<line x1="{c}" y1="{c}" x2="{p[0]:.1f}" y2="{p[1]:.1f}"/>' for p in pts)
    def person(x, y, k):
        return (f'<g transform="translate({x:.1f} {y:.1f}) scale({k:.2f})">'
                f'<circle cx="0" cy="1" r="10" fill="#FFFFFF"/>'
                f'<circle cx="0" cy="-4.5" r="3.6" fill="{_PEOPLE}"/>'
                f'<rect x="-6.5" y="0.5" width="13" height="8" rx="4" fill="{_PEOPLE}"/></g>')
    folk = "".join(person(x, y, s) for x, y in pts) + person(c, c, s * 1.45)
    bx, by = c + 16 * s, c - 16 * s
    badge = (f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="9.5" fill="{col}" stroke="#FFFFFF" stroke-width="2"/>'
             f'<text x="{bx:.1f}" y="{by + 4.5:.1f}" text-anchor="middle" font-size="13" font-weight="600" fill="#FFFFFF" font-family="Montserrat, Arial, sans-serif">{icon}</text>')
    return (f'<svg viewBox="0 0 {size} {size}" role="img" aria-label="{label}">'
            f'<g stroke="{_BLUE}" stroke-opacity="{blue_op}" stroke-width=".9">{others}</g>'
            f'<g stroke="{col}" stroke-width="2.2">{mine}</g>{folk}{badge}</svg>')

GROWTH = (
    '<div class="growth">'
    f'<figure class="g-fig">{_leader_svg(10, "ok", "10 people with you in the middle: 45 relationships, 9 of them yours, manageable")}'
    '<figcaption><strong>10 people</strong> · 45 relationships<br>9 are yours · manageable</figcaption></figure>'
    '<div class="g-text"><p class="g-big">Double the headcount = quadruple the leadership burden</p></div>'
    f'<figure class="g-fig">{_leader_svg(20, "strained", "20 people with you in the middle: 190 relationships, 19 of them yours, strained")}'
    '<figcaption><strong>20 people</strong> · 190 relationships<br>19 are yours · strained</figcaption></figure>'
    '</div>'
)

def cta2(h, href):
    return (f'<section class="cta"><div class="wrap"><div><h2>{h}</h2></div><div class="actions">'
            f'<a class="btn" href="{href}">Book a 30-minute call →</a><a class="btn ghost" href="mailto:ed@priflyadvisors.com">Email me</a></div></div></section>')

areas = [("Decisions", "Who decides what, and where are decisions stuck?", ""),
         ("Rhythms &amp; rituals", "Do your meetings make decisions, share key information, or just waste time?", ""),
         ("Intent", "Do all decision-makers know your intent as well as your inner circle does?", ""),
         ("Feedback", "Does feedback reach the right decision-maker in time to alter course?", ""),
         ("Talent", "Are your managers just managing, or are they leading too?", "")]
arows = '<div class="hd"><span></span><span>What I ask</span><span>What you get</span></div>' + "".join(
    f'<div><h3>{a}</h3><p>{b}</p><p class="get">{c}</p></div>' for a, b, c in areas)

SIGNS = """
  <ul class="signs">
    <li>We're growing fast, but the leadership load is growing faster</li>
    <li>Our managers were promoted from within, with little or no formal leadership training or experience</li>
    <li>My key leaders and I spend more time firefighting than forging the path</li>
  </ul>"""

WHY = """<div class="prose prose-wide">
  <p>For more than 30 years I didn't just hold leadership roles. I was formed inside one of the most deliberate leadership systems in the world, one built to turn newcomers into leaders of thousands, drawing on hard-won lessons about how people behave under pressure, learned long before anyone called it a science. I led and taught at every level of it, in high-stakes environments across the U.S. and Europe. Now I help companies build the same thing for themselves: a system that supports its leaders, adapts as the company changes, and grows new leaders from within.</p>
  <p><a href="about.html">My story →</a></p></div>"""

STEPS = """
  <ol class="steps">
    <li><div><h3>A 30-minute call <span class="price">Free</span></h3><p>Tell me where the pressure is showing, and we'll work out together whether I can help.</p></div></li>
    <li><div><h3>The Leadership Analysis <span class="price">From €4,500 + IVA</span></h3><p>Three weeks: I meet with you, interview up to six of your leaders in confidence and sit in on one or more leadership meetings. You get:</p>
      <ul><li>The area most in need of attention</li><li>The three changes to make first</li><li>A 90-day plan, with two coaching sessions to get it moving</li></ul>
      <p>Yours to keep, whether or not we continue. If you do, €1,000 of the fee counts toward coaching.</p></div></li>
    <li><div><h3>Coaching</h3><p>Two ways to continue, priced after the analysis once we both know the scope:</p><ul><li><strong>A 90-day programme</strong> that puts the plan to work</li><li><strong>Ongoing monthly coaching</strong> for leaders who want a standing, confidential partner</li></ul></div></li>
  </ol>"""

coaching = (phead("Coaching", "Executive Coaching &amp; Leadership Advisory", "Helping leaders lead more, <em>carry less</em>",
                  "Grow your team, extend your reach, reduce the decisions that land on your desk. I help you build the systems to get there, and coach you through the dip, when old habits pull everyone back.",
                  ("Book a 30-minute call", BOOK), img=("photo-team.jpg", "Ed Chandler working with a leadership team"))
            + sec("Is this you or your organisation?", SIGNS + GROWTH)
            + sec("Why me", WHY, band=True)
            + ('<section class="tight-bottom"><div class="wrap two-col">'
               '<div><div class="sec-head"><h2>What I look at</h2></div><ul class="signs asks">'
               + "".join(f"<li>{q}</li>" for _, q, _ in areas) + '</ul></div>'
               '<div><div class="sec-head"><h2>How we work together</h2></div>' + STEPS + '</div>'
               '</div></section>')
            + cta2("Start with a conversation", BOOK))

# ---------- SPEAKING ----------
# Speaking (Ed's review, 2026-09-15): leads with the scaling talk and the TOPGUN hook; stage photo at the top
speaking = phead("Speaking", "Keynotes, firesides and panels", "Breaking the barrier: <em>TOPGUN, speed and leadership</em>",
                 "Talks for founders, executives and operators on breaking the invisible leadership barriers that fast growth and high-risk environments create. From main stages to leadership offsites.",
                 ("Check availability for your date", SPEAK),
                 img=("photo-3.jpg", "Ed Chandler speaking on stage")) + sec("Signature talks", '''<div class="talks">
  <div class="talk"><span class="eyebrow">Keynote · 20 to 25 minutes</span>
    <h3>Breaking the Demon</h3>
    <p class="subt">Overcoming hidden leadership barriers</p>
    <p>In the 1940s, test pilots believed a demon waited at the speed of sound: a wall in the air that shook aircraft apart. In 1961, the Soviet Union put the first human into space, and America was losing the space race. And by 1969, U.S. Navy fighter pilots had lost a 10X advantage over less technologically advanced adversaries.</p>
    <p>None of these were solved by technology or the force of one leader alone. Each solution required leadership systems that removed barriers, aligned effort and delivered usable feedback at the speed these challenges demanded.</p>
    <p>Organisations that grow fast, work under high risk, or face fast-changing markets can learn to identify the hidden barriers challenging their leadership teams — and this talk shows how to break through them.</p></div>
  <div class="talk"><span class="eyebrow">Motivational talk · 45 minutes</span>
    <h3>Danger Close</h3>
    <p class="subt">Leadership at the Edge</p>
    <p>How does a farm boy from a small town in Oklahoma end up at the U.S. Naval Academy, flying fighters into combat from nuclear-powered aircraft carriers, graduating from TOPGUN and teaching at the world's premier air warfare centre of excellence?</p>
    <p>A story-led talk about becoming a naval aviator: surviving combat and night landings at sea, flying into danger to save others, and what <em>the real</em> TOPGUN is like. It's a motivational look at overcoming perceived barriers and fear, and why life often begins after the flying stops.</p>
    <p>Fun, fast and personal, with lessons that land for any audience.</p></div>
</div>''') + sec("Formats", '''<div class="cols2">
    <div><h3>Keynote</h3><p>Built for a main stage, from 20 to 45 minutes</p></div>
    <div><h3>Fireside chat</h3><p>A conversation for founders and operators, with room for the audience's own questions</p></div>
    <div><h3>Working session</h3><p>Hands-on with a leadership team, building the leadership system your organisation is missing</p></div>
    <div><h3>Panel moderation</h3><p>Getting quickly to what actually happened, drawing out every perspective and keeping the panel moving</p></div>
  </div>''', band=True, tight=True) + sec("Recent appearances", '''<div class="table-scroll"><table class="dates">
  <tr><td>18 Sep 2026</td><td><strong>Startup Summit Lisbon</strong><br><span class="muted">Moderator, "The Operator's Playbook" · Unicorn Stage</span></td><td>Lisbon</td></tr>
  <tr><td>18 Sep 2026</td><td><strong>Startup Summit Lisbon</strong><br><span class="muted">Fireside, "What Comes After Product-Market Fit" · Impact Stage</span></td><td>Lisbon</td></tr>
  <tr><td>21 Apr 2026</td><td><strong>American Club of Lisbon</strong><br><span class="muted">"Danger Close: Leadership at the Edge"</span></td><td>Lisbon</td></tr>
  <tr><td>Earlier</td><td><strong>International Men of Purpose</strong><br><span class="muted">Talk on personal growth and mentorship</span></td><td>Portugal</td></tr>
  <tr><td></td><td><strong>Boys &amp; Girls Clubs of America</strong><br><span class="muted">Keynote · European District Public Speaking Finals</span></td><td>Europe</td></tr>
  <tr><td></td><td><strong>University of Maryland Global Campus</strong><br><span class="muted">Graduation keynote · Southern Europe</span></td><td>Europe</td></tr>
</table></div>''', tight=True) + sec("For event organisers", '''<div class="kit solo"><div>
    <p class="bio">Ed Chandler is a former U.S. naval aviator and TOPGUN graduate who went on to teach tactics and leadership at the world's premier air warfare centre of excellence. With a 30-year leadership career spanning roles across the Asia-Pacific, NATO and U.S. Navy headquarters in Europe, today he helps leaders build the systems that keep up with their company's growth. Founder of PriFly Advisors, based in Lisbon and available worldwide.</p>
    <p class="meta">Longer bio and high-resolution headshot on request</p>
    <div class="actions" style="margin-top:28px"><a class="btn" href="''' + SPEAK + '''">Check availability for your date →</a></div>
    <p class="meta">Or write to <a href="mailto:''' + SPEAK_TO + '''">''' + SPEAK_TO + '''</a></p>
    <p class="meta">TOPGUN is a trademark of the U.S. Navy. No endorsement is implied.</p>
  </div></div>''', band=True)

# ---------- DEFENCE ----------
# Defence (Ed's review, 2026-09-15): a minor role, two specific offers plus board roles; no background
# section (About and LinkedIn cover it), no company names, one plain contact button
defence = phead("Defence", "Defence advisory", "Defence support <em>on both sides of the Atlantic</em>",
                "I take on selected defence work and serve on boards, helping defence businesses expand and refine their strategy.") + '''
<section class="tight snug"><div class="wrap"><div class="cols2 plain">
  <div><h3>Contract support</h3><p>For firms that need a Europe-based American on contract, with aviation, overseas basing, NATO and U.S. Navy experience</p></div>
  <div><h3>Market-entry scoping</h3><p>A first look for U.S. companies entering Europe, or European companies entering the U.S.</p></div>
</div>
<p class="muted" style="margin-top:20px">My background: <a href="about.html">About</a> · <a href="https://www.linkedin.com/in/edchandler96/" rel="noopener">LinkedIn</a></p>
<div class="actions" style="margin-top:20px"><a class="btn" href="contact.html?topic=defence">Contact me →</a></div>
</div></section>'''

# ---------- ABOUT ----------
about = phead("About", "About", "Ed Chandler", "Executive coach, leadership advisor and speaker · Founder of PriFly Advisors · Lisbon") + '''
<section><div class="wrap about-grid">
  <div>
    <figure class="portrait" style="margin-bottom:32px"><img src="images/ed-chandler.jpg" alt="Ed Chandler" width="650" height="900"></figure>
    <ul class="facts">
      <li><span>Service</span><span>U.S. Navy, 28 years · Commander (Ret.)</span></li>
      <li><span>Flying</span><span>TOPGUN graduate and instructor · ~3,000 hours · 500+ carrier landings</span></li>
      <li><span>Education</span><span>U.S. Naval Academy · University of Florida MBA</span></li>
      <li><span>Credentials</span><span>Lean Six Sigma Black Belt · PMP · AgilePM Practitioner</span></li>
      <li><span>Boards</span><span>Founding Chairman, EU defence startup · Board advisor</span></li>
      <li><span>Based</span><span>Lisbon, Portugal</span></li>
    </ul>
  </div>
  <div class="prose">
    <p>I spent 28 years in the U.S. Navy flying fighters, learning from the best as a TOPGUN graduate and training the best as an instructor at the Navy's Strike and Air Warfare Center of Excellence. I helped oversee entire carrier strike groups in the Pacific, helped NATO develop its first Joint Air Power Doctrine in Europe, and led in some of the U.S. military's most complex organisations along the way.</p>
    <p>My final tours included NATO staff duty at STRIKFORNATO and Executive Officer of Naval Support Activity Naples: two assignments that immersed me in allied operations, transatlantic defence relationships and the institutional machinery that connects American and European security.</p>
    <p>Now based in Portugal for six years, I help founders and executives build the leadership systems that let organisations perform under pressure, as an executive coach, leadership advisor and speaker. I founded PriFly Advisors to provide strategic and practical advisory across leadership and defence, grounded in the credibility that only comes from decades of operating in high-stakes environments.</p>
    <div class="actions" style="margin-top:12px"><a class="btn" href="contact.html">Get in touch →</a><a class="btn ghost" href="https://www.linkedin.com/in/edchandler96/" rel="noopener">LinkedIn</a></div>
  </div>
</div></section>
<section class="band tight"><div class="wrap define">
  <div><div class="word">PriFly</div><div class="phon">/ˈpraɪ.flaɪ/</div><div class="src">Naval aviation slang</div>
    <button class="listen" type="button" onclick="document.getElementById('prifly-audio').play()">▶ Listen</button>
    <audio id="prifly-audio" src="https://priflyadvisors.github.io/audio/prifly.mp3" preload="none"></audio></div>
  <p class="mean">Short for "Primary Flight Control", the tower overseeing carrier flight operations. A place of calm leadership, clarity and control in high-stakes environments.</p>
</div></section>
'''

# ---------- CONTACT ----------
contact = phead("Contact", "Contact", "Let's talk", "Whether it's a leadership challenge, a speaking engagement or a transatlantic defence question, reach out.") + '''
<section><div class="wrap split">
  <div class="prose" style="font-size:15px">
    <p><span class="eyebrow">Email</span><br><a href="mailto:ed@priflyadvisors.com">ed@priflyadvisors.com</a></p>
    <p><span class="eyebrow">LinkedIn</span><br><a href="https://www.linkedin.com/in/edchandler96/" rel="noopener">Ed Chandler</a></p>
  </div>
  <form class="form" action="https://formspree.io/f/xeedzodn" method="POST">
    <input type="hidden" name="_subject" value="New enquiry from PriFlyAdvisors.com">
    <div class="row">
      <label>Your name<input type="text" name="name" autocomplete="name" required></label>
      <label>Email<input type="email" name="email" autocomplete="email" required></label>
    </div>
    <div class="row">
      <label>Organisation<input type="text" name="organisation" autocomplete="organization"></label>
      <label>Interested in<select name="topic" id="topic" required><option value="coaching">Coaching &amp; leadership (a 30-minute call)</option><option value="speaking">Speaking</option><option value="defence">Defence advisory</option><option value="other">Something else</option></select></label>
    </div>
    <label>Event date <span class="hint">(speaking only)</span><input type="text" name="event_date" placeholder="e.g. 12 November 2026, Lisbon"></label>
    <label>How can I help?<textarea name="message" required></textarea></label>
    <div class="actions"><button class="btn" type="submit">Send message</button></div>
  </form>
</div></section>
<script>(function(){var t=new URLSearchParams(location.search).get("topic");var s=document.getElementById("topic");if(t&&s&&s.querySelector('option[value="'+t+'"]'))s.value=t;})();</script>
'''

pages = [
    ("index", "PriFly Advisors · Ed Chandler | Executive Coaching &amp; Leadership Advisory, Lisbon",
     "Executive coaching and leadership advisory for founders and executives whose companies are growing faster than their leadership. Ed Chandler, former TOPGUN instructor, based in Lisbon.", "home", home, LD),
    ("coaching", "Executive Coaching &amp; Leadership Advisory | PriFly Advisors",
     "Helping leaders lead more, carry less: a leadership system that changes with your company, and coaching for the leaders who run it. Executive coaching and leadership advisory in Lisbon, Portugal and Europe: a 30-minute call, the Leadership Analysis, then coaching.", "coaching", coaching, ""),
    ("speaking", "Speaking | Ed Chandler, PriFly Advisors",
     "TOPGUN-inspired keynotes, firesides, working sessions and panel moderation on crisis judgement and leadership under pressure.", "speaking", speaking, ""),
    ("defence", "Defence Advisory | PriFly Advisors",
     "Selected defence work from Lisbon: contract support for firms that need a Europe-based American, market-entry scoping across the Atlantic, and board roles.", "defence", defence, ""),
    ("about", "About Ed Chandler | PriFly Advisors",
     "28 years in the U.S. Navy, TOPGUN graduate and instructor, NATO and U.S. Navy leadership in Europe. Now an executive coach and leadership advisor in Lisbon.", "about", about, ""),
    ("contact", "Contact | PriFly Advisors", "Get in touch about coaching, speaking or transatlantic defence advisory.", "contact", contact, ""),
]
for slug, title, desc, active, body, extra in pages:
    with open(os.path.join(OUT, f"{slug}.html"), "w") as f:
        f.write(page(slug, title, desc, active, body, extra))
print("built", [p[0] for p in pages], "| tomcat:", TOMCAT)
