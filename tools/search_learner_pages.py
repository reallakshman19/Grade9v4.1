"""Enumerate public learner routes from live registries and HTML title metadata.

No solution bodies, scripts, SVGs, hidden answer markup, hints, source keys,
private evidence, or reviewer artifacts are used in the discovery projection.
"""
from __future__ import annotations

import html
import json
import posixpath
import re
from pathlib import Path
from urllib.parse import urlencode, urljoin, urlsplit, urlunsplit

SUBJECTS = ("Physics", "Chemistry", "Biology")
EXCLUDED = {"review", "reviews", "review-artifacts", "evidence", "agent1", "contracts", "fixtures", "assets", "images", "archive", "archives", "legacy", "tests", "qa", "receipts", "source-led-review", "sources"}
INTERNAL_NAME = re.compile(r"(?:^|[-_])(?:answer[-_]?key|solutions?|review|audit|evidence|receipt|validation|manifest|report)(?:[-_.]|$)", re.I)

def read_json(root, path):
    return json.loads((root / path).read_text(encoding="utf-8"))

def is_public_html(path):
    p=Path(path)
    if p.suffix.lower() != ".html" or any(x.lower() in EXCLUDED for x in p.parts) or INTERNAL_NAME.search(p.name):
        return False
    if p.parts[:1] == ("nsejs",):
        if len(p.parts)>2 and p.parts[1] in ("physics","chemistry","biology"):
            if "curriculum" in p.parts and p.parts[2:4] != ("curriculum","topics"):
                return False
        return True
    return p.parts[:3] in (("curriculum","chemistry","preview"),("curriculum","biology","preview"))

def public_pages(root):
    paths=set()
    for directory in ("nsejs","curriculum/chemistry/preview","curriculum/biology/preview"):
        folder=root/directory
        if folder.exists():
            paths.update(p.relative_to(root).as_posix() for p in folder.rglob("*.html") if is_public_html(p.relative_to(root)))
    return sorted(paths)

def absolute_relative(base, href):
    url=urlsplit(urljoin("https://site.invalid/"+base,href))
    if url.netloc!="site.invalid" or url.scheme!="https":
        raise ValueError("Unexpected learner destination "+href)
    return urlunsplit(("", "",url.path.lstrip("/"),url.query,url.fragment))

def change_query(url, params, fragment=None):
    from urllib.parse import parse_qsl
    u=urlsplit(url)
    q=dict(parse_qsl(u.query,keep_blank_values=True))
    q.update(params)
    return urlunsplit(("", "", u.path, urlencode(q), u.fragment if fragment is None else fragment))

def page_title(root,path):
    # Read only the title, not body text or description which can contain answers.
    raw=(root/path).read_text(encoding="utf-8")
    match=re.search(r"<title\b[^>]*>(.*?)</title\s*>",raw,re.I|re.S)
    title=html.unescape(re.sub(r"\s+"," ",match.group(1))).strip() if match else ""
    return title or path.rsplit("/",1)[-1].replace(".html","").replace("-"," ")

def subject_for(path):
    for subject in SUBJECTS:
        s=subject.lower()
        if path.startswith(("nsejs/"+s+"/","curriculum/"+s+"/")):
            return subject
    return "Common"

def build_public_learner_documents(root,normalize):
    docs=[]
    destinations=set()
    def add(identity,title,subject,url,category="tablet",topic="",badge="LEARNING CANDIDATE · HOLD",stem=None,source_id=None):
        target=urlsplit(url)
        if target.scheme or target.netloc or not (root/target.path).is_file():
            raise ValueError("Missing learner destination: "+url)
        if url in destinations:
            return
        destinations.add(url)
        doc={"id":"ROUTE-"+identity,"original_id":identity,"type":{"tablet":"LESSON","curriculum":"TOPIC","question":"QUESTION","page":"PAGE"}[category],"category":category,"badge":badge,"breadcrumb":"NSEJS · "+subject+(" · "+topic if topic else "")+" · HOLD","subject":subject,"exam_family":"NSEJS","is_nsejs":True,"scope":["nsejs",subject.lower()],"title":title,"url":url,"topic":topic}
        if stem is not None:
            doc.update({"stem":stem,"options":[],"hints":[]})
        if source_id:
            doc["source_id"]=source_id
        doc["search_text"]=normalize(" ".join([identity,title,subject,topic,stem or "",source_id or "",url,"nsejs junior science"]))
        docs.append(doc)
    physics=read_json(root,"nsejs/physics/learn/catalog.json")
    for c in physics["chapters"]:
        ch,title=c["id"],c["title"]
        add(ch,title+" · "+("In preparation" if c["state"]=="unavailable" else "Chapter"),"Physics","nsejs/physics/learn/chapter.html?ph="+ch,"curriculum",title,"CHAPTER IN PREPARATION · HOLD" if c["state"]=="unavailable" else "CHAPTER · HOLD")
        for unit in c["units"]:
            uid=unit["id"]
            title2=re.sub(r"^Continue:\s*","",unit["title"])
            for role,label in (("learn","Learn"),("practice","Try it")):
                url=absolute_relative("nsejs/physics/index.html",unit[role])
                add(ch+"-"+uid+"-"+role,title2+" · "+label,"Physics",url,"tablet",title)
    chemistry=read_json(root,"nsejs/chemistry/learner-navigation.v1.json")
    for unit in chemistry["units"]:
        uid=unit["id"]
        base=absolute_relative("nsejs/chemistry/index.html",unit["chapter_href"])
        add("CHEM-"+uid,unit["title"]+" · Chapter","Chemistry",base,"curriculum",unit["title"])
        for sub in unit["subtopics"]:
            for mode,label in (("study","Learn"),("practice","Try it")):
                params={"subtopic":sub["id"]}
                if unit["reader"]=="native":
                    params.update(unit=uid,mode=mode)
                    fragment=None
                else:
                    if mode=="practice":params["mode"]="practice"
                    fragment=("practice-" if mode=="practice" else "")+re.sub(r"[^a-z0-9-]","-",sub["id"],flags=re.I).lower()
                url=change_query(base,params,fragment)
                add(sub["id"]+"-"+mode,sub["title"]+" · "+label,"Chemistry",url,"tablet",unit["title"])
    grav=read_json(root,"nsejs/physics/ph05/source-led-r2/packages.v1.json")
    base="nsejs/physics/ph05/source-led-r2/index.html"
    source_by_id={x["id"]:x for x in grav["census"]["source_records"]}
    for p in grav["packages"]:
        pid=p["id"]
        add("PH05-"+pid,p["title"]+" · Learn","Physics",change_query(base,{"package":pid,"stage":"learn"}),"tablet","Gravitation")
        for t in p["tasks"]:
            # Task title/prompt only; no model JSON, prediction, hint or solution.
            add(t["uid"],p["title"]+" · Protected challenge "+t["uid"].rsplit("-",1)[-1],"Physics",change_query(base,{"package":pid,"task":t["uid"]}),"question","Gravitation","AUTHORED TRANSFER · HOLD",t["prompt"])
        for sid in p["source_locators"]:
            if sid not in source_by_id:
                raise ValueError("Unknown PH05 source "+sid)
            # prompt_tag may contain the answer; use locator and neutral topic only.
            add(sid,"Gravitation historical source · "+sid,"Physics",change_query(base,{"package":pid,"source":sid}),"question","Gravitation","HISTORICAL SOURCE LEAD · HOLD",source_id=sid)
    # Include identity-only map navigation, never derive source-question body from the map.
    qmap=read_json(root,"nsejs/core2/question-map.v1.json")
    for module in qmap["modules"]:
        sub=module["subject"].title()
        if sub not in SUBJECTS:
            continue
        slug=module["slug"]
        add("MAP-"+slug,slug.replace("-"," ").title()+" · Source identity map",sub,"nsejs/core2/question-map.html#module-"+slug,"curriculum","Source identity map","SOURCE IDENTITY ONLY · HOLD")
    pages=public_pages(root)
    # Public static titles only. Dynamic reader shells without a selected entity
    # have their exact query-specific routes above.
    dynamic_shells={"nsejs/physics/learn/chapter.html","nsejs/physics/ph05/source-led-r2/index.html","nsejs/physics/ph05/source-checkpoint.html","nsejs/chemistry/textbook/index.html"}
    for path in pages:
        if path in dynamic_shells:
            continue
        # Every public file is accounted for; redirects are valid but not promoted.
        title=page_title(root,path)
        sub=subject_for(path)
        if "core1b" in path.lower() or "/core1/" in path.lower() or "/practice" in path.lower():
            category="tablet"
        elif "/textbook/" in path or "/curriculum/" in path or "/preview/" in path:
            category="tablet"
        else:
            category="page"
        add("PAGE-"+path,title,sub,path,category)
    return docs,pages

def install_public_search(root,pages):
    """Add a single shared search loader to published public pages at deploy time.
    No protected content is changed; source checkout HTML is not committed by this step.
    """
    for path in pages:
        p=root/path
        raw=p.read_text(encoding="utf-8")
        if not re.search(r"</body\s*>",raw,re.I):
            continue
        prefix=posixpath.relpath(".",posixpath.dirname(path) or ".")
        prefix="" if prefix=="." else prefix+"/"
        # Existing pages already use the same shared runtime. Add only missing assets.
        if not re.search(r"<link\b[^>]*href=[\"'][^\"']*css/site-search\.css",raw,re.I):
            raw=re.sub(r"</head\s*>",lambda m:'<link rel="stylesheet" href="'+prefix+'css/site-search.css">\n'+m.group(0),raw,count=1,flags=re.I)
        if not re.search(r"<script\b[^>]*src=[\"'][^\"']*js/site-search\.js",raw,re.I):
            raw=re.sub(r"</body\s*>",lambda m:'<script src="'+prefix+'js/site-search.js" data-site-root="'+prefix+'"></script>\n'+m.group(0),raw,count=1,flags=re.I)
        p.write_text(raw,encoding="utf-8")
